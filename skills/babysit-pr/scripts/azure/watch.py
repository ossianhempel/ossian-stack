#!/usr/bin/env python3
"""Read-only Azure Services watcher. READY is a conservative observation, never merge authority."""
import argparse
import json
import sys
import subprocess
import time
from datetime import datetime
from urllib.parse import quote
from client import Client, EvidenceError, canonical, feedback, identity

BUILD_POLICY = '0609b952-1397-4640-95ec-e00a01b2c241'


def stamp(value):
    if not isinstance(value, str):
        raise EvidenceError('Required evidence timestamp is missing')
    return datetime.fromisoformat(value.replace('Z', '+00:00')).timestamp()


def oid(pr, key):
    value = pr.get(key, {}).get('commitId')
    if not isinstance(value, str) or len(value) != 40 or any(c not in '0123456789abcdef' for c in value.lower()):
        raise EvidenceError(f'Missing or invalid {key} commit identity')
    return value.lower()


def fingerprint(pr):
    return {k: pr.get(k) for k in ('pullRequestId', 'status', 'isDraft', 'sourceRefName', 'targetRefName',
        'lastMergeSourceCommit', 'lastMergeTargetCommit', 'lastMergeCommit', 'mergeStatus', 'reviewers')}


def refs(client, pr):
    result = {}
    for field in ('sourceRefName', 'targetRefName'):
        name = pr[field]
        if not name.startswith('refs/heads/'):
            raise EvidenceError('Only branch PRs are supported')
        values = client.collection('git/repositories/' + quote(client.target.repository, safe='') + '/refs',
            {'filter': name.removeprefix('refs/')}, paging='token')
        match = [x['objectId'] for x in values if x.get('name') == name]
        if len(match) != 1:
            raise EvidenceError(f'{field} is missing or ambiguous')
        result[field] = match[0]
    return result


def policies(client, pr):
    return client.collection('git/policy/configurations', {'repositoryId': client.target.repository,
        'refName': pr['targetRefName']}, paging='token')


def evaluations(client):
    return client.collection('policy/evaluations', {'artifactId': client.target.artifact,
        'includeNotApplicable': 'true'}, paging='skip', version='7.1-preview.1')


def collect(client):
    pr = canonical(client)
    if pr.get('status') in ('completed', 'abandoned'):
        return {'identity': vars(client.target), 'url': client.target.url, 'pr': pr,
            'terminalState': pr['status']}
    if pr.get('forkSource'):
        raise EvidenceError('Azure fork PRs are not supported by this watcher; inspect provider evidence explicitly')
    start_refs = refs(client, pr)
    iterations = client.collection(client.target.path + '/iterations')
    configs = policies(client, pr)
    evals = evaluations(client)
    builds = {}
    # context.buildId is only a locator hint. Build identity is independently verified below.
    for e in evals:
        build_id = (e.get('context') or {}).get('buildId')
        if isinstance(build_id, int) and not isinstance(build_id, bool) and build_id > 0:
            builds[str(build_id)] = client.get(f'build/builds/{build_id}')
    threads = client.collection(client.target.path + '/threads')
    after = client.get(client.target.path)
    end_refs = refs(client, after)
    final_configs = policies(client, after)
    return {'identity': vars(client.target), 'url': client.target.url, 'artifact': client.target.artifact,
        'pr': pr, 'after': after, 'refs': start_refs, 'after_refs': end_refs,
        'iterations': iterations, 'policies': configs, 'after_policies': final_configs,
        'evaluations': evals, 'builds': builds, 'threads': threads}


def classify(s):
    if s.get('terminalState') in ('completed', 'abandoned'):
        return {'provider': 'azure-devops-services',
            'kind': 'COMPLETE' if s['terminalState'] == 'completed' else 'CLOSED',
            'url': s['url'], 'identity': s['identity'], 'reasons': [],
            'observedAt': datetime.now().astimezone().isoformat()}
    reasons = []
    def block(kind, detail, **evidence):
        reasons.append({'kind': kind, 'detail': detail, **evidence})
    pr = s['pr']
    try:
        if fingerprint(pr) != fingerprint(s['after']) or s['refs'] != s['after_refs'] or s['policies'] != s['after_policies']:
            block('stale', 'PR, branch, reviewer, or policy evidence changed during this observation')
        if pr.get('status') != 'active':
            block('state', 'PR is not active; completed/abandoned is not READY')
        if pr.get('isDraft') is not False:
            block('draft', 'PR is draft or draft state is unreadable')
        if pr.get('mergeStatus') != 'succeeded':
            block('merge-conflicts' if pr.get('mergeStatus') == 'conflicts' else 'mergeability',
                'Mergeability is not confirmed succeeded', status=pr.get('mergeStatus'))
        source, target, merge = (oid(pr, k) for k in ('lastMergeSourceCommit', 'lastMergeTargetCommit', 'lastMergeCommit'))
        if s['refs'] != {'sourceRefName': source, 'targetRefName': target}:
            block('stale', 'Merge computation does not match the current source and target branches')
        if not s['iterations'] or pr.get('supportsIterations') is not True:
            raise EvidenceError('Current iteration evidence unavailable')
        iteration = max(s['iterations'], key=lambda x: x['id'])
        if oid(iteration, 'sourceRefCommit') != source:
            block('stale', 'Latest iteration is not bound to the current source commit')
        fresh_after = max(stamp(iteration['createdDate']), stamp(iteration['updatedDate']))
        reviewers = pr.get('reviewers')
        if not isinstance(reviewers, list):
            raise EvidenceError('Reviewer requirements/votes unreadable')
        for reviewer in reviewers:
            if 'isRequired' in reviewer and not isinstance(reviewer['isRequired'], bool):
                raise EvidenceError('Reviewer requirement is unreadable')
            vote = reviewer.get('vote')
            if vote not in (-10, -5, 0, 5, 10):
                block('reviewers', 'Unknown reviewer vote', reviewer=reviewer.get('id'))
            elif vote < 0 or (reviewer.get('isRequired') is True and vote <= 0):
                block('reviewers', 'Reviewer requirement or changes request remains', reviewer=reviewer.get('id'), vote=vote)
        for raw in s['threads']:
            thread = feedback(raw)
            if thread and thread['status'] in ('active', 'pending', 'unknown'):
                block('review-threads', 'Unresolved review feedback', thread=thread)
        ids = set()
        for config in s['policies']:
            if not isinstance(config.get('isEnabled'), bool) or not isinstance(config.get('isBlocking'), bool):
                raise EvidenceError('Policy applicability is unreadable')
            if config['id'] in ids:
                raise EvidenceError('Duplicate policy configuration in evidence')
            ids.add(config['id'])
            if not config['isEnabled'] or not config['isBlocking'] or config.get('isDeleted') is True:
                continue
            matches = [e for e in s['evaluations'] if e.get('configuration', {}).get('id') == config['id']]
            label = config.get('type', {}).get('displayName', str(config['id']))
            if len(matches) != 1:
                block('policy', 'Required policy evaluation missing or ambiguous', policy=label)
                continue
            e = matches[0]
            if e.get('artifactId') != s['artifact'] or e['configuration'].get('revision') != config.get('revision') or not isinstance(config.get('revision'), int):
                block('stale', 'Policy evaluation identity/revision does not match', policy=label)
            status = e.get('status')
            if status not in ('approved', 'notApplicable'):
                block('failing-checks' if status in ('rejected', 'broken') else 'policy',
                    'Required policy is not satisfied', policy=label, status=status, evaluation=e.get('evaluationId'))
            if status in ('approved', 'notApplicable') and stamp(e.get('completedDate')) < fresh_after:
                block('stale', 'Policy result predates the latest iteration', policy=label)
            if config.get('type', {}).get('id', '').lower() != BUILD_POLICY or status == 'notApplicable':
                continue
            build_id = (e.get('context') or {}).get('buildId')
            build = s['builds'].get(str(build_id))
            if not build:
                block('build-evidence', 'Policy build locator unavailable; cannot prove current validation', policy=label)
                continue
            evidence = {'policy': label, 'buildId': build.get('id'),
                'logs': s['url'].split('/_git/')[0] + '/_apis/build/builds/' + str(build.get('id')) + '/logs?api-version=7.1'}
            expected_definition = config.get('settings', {}).get('buildDefinitionId')
            if (build.get('id') != build_id or not isinstance(expected_definition, int)
                or build.get('definition', {}).get('id') != expected_definition
                or build.get('project', {}).get('id') != s['identity']['project']
                or build.get('repository', {}).get('id') != s['identity']['repository']
                or build.get('sourceBranch') != f"refs/pull/{s['identity']['pr']}/merge"
                or build.get('sourceVersion') != merge or build.get('reason') != 'pullRequest'):
                block('stale', 'Build identity does not prove validation of the current PR merge commit', **evidence)
            if build.get('status') != 'completed' or build.get('result') != 'succeeded':
                block('failing-checks' if build.get('result') in ('failed', 'canceled', 'partiallySucceeded') else 'build-pending',
                    'Required build has not succeeded', status=build.get('status'), result=build.get('result'), **evidence)
            elif stamp(build.get('finishTime')) < fresh_after:
                block('stale', 'Build completion predates current iteration', **evidence)
        for e in s['evaluations']:
            c = e.get('configuration', {})
            if c.get('isEnabled') is True and c.get('isBlocking') is True and c.get('id') not in ids:
                block('policy', 'Blocking evaluation lacks matching policy inventory', evaluation=e.get('evaluationId'))
    except (EvidenceError, KeyError, TypeError, ValueError, AttributeError) as error:
        block('unreadable', str(error))
    priority = {'merge-conflicts': 0, 'review-threads': 1, 'failing-checks': 2}
    reasons.sort(key=lambda r: priority.get(r['kind'], 3))
    return {'provider': 'azure-devops-services', 'kind': 'BLOCKER' if reasons else 'READY',
        'url': s['url'], 'identity': s['identity'], 'head': pr.get('lastMergeSourceCommit', {}).get('commitId'),
        'reasons': reasons, 'observedAt': datetime.now().astimezone().isoformat()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url', required=True, help='Full Azure Services PR URL, or repository remote with --pr')
    parser.add_argument('--pr', type=int)
    parser.add_argument('--status-only', action='store_true')
    parser.add_argument('--interval', type=float, default=60)
    parser.add_argument('--timeout', type=float, default=3600)
    args = parser.parse_args()
    if args.interval <= 0 or args.timeout <= 0:
        parser.error('interval and timeout must be positive')
    deadline = time.monotonic() + args.timeout
    while True:
        try:
            result = classify(collect(Client(identity(args.url, args.pr))))
        except (EvidenceError, KeyError, TypeError, ValueError, AttributeError, OSError, subprocess.TimeoutExpired) as error:
            result = {'provider': 'azure-devops-services', 'kind': 'BLOCKER',
                'reasons': [{'kind': 'unreadable', 'detail': str(error)}]}
        print(json.dumps(result), flush=True)
        if args.status_only or result['kind'] in ('READY', 'COMPLETE', 'CLOSED'):
            return 0
        # Pending evidence can progress by itself. Mutations and human calls belong to the agent.
        waiting = all(r['kind'] in ('policy', 'build-pending', 'mergeability', 'stale') for r in result['reasons'])
        if not waiting:
            return 2
        if time.monotonic() >= deadline:
            return 5
        time.sleep(min(args.interval, max(0, deadline - time.monotonic())))


if __name__ == '__main__':
    sys.exit(main())
