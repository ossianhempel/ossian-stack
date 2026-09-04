import copy
import unittest
from client import EvidenceError, Identity, Client, feedback, identity
from watch import BUILD_POLICY, classify, collect

A, B, M = 'a' * 40, 'b' * 40, 'c' * 40


def fixture():
    pr = {'pullRequestId': 12, 'status': 'active', 'isDraft': False, 'supportsIterations': True,
        'mergeStatus': 'succeeded', 'sourceRefName': 'refs/heads/work', 'targetRefName': 'refs/heads/main',
        'lastMergeSourceCommit': {'commitId': A}, 'lastMergeTargetCommit': {'commitId': B},
        'lastMergeCommit': {'commitId': M}, 'reviewers': [{'id': 'reviewer', 'isRequired': True, 'vote': 10}]}
    config = {'id': 1, 'revision': 2, 'isEnabled': True, 'isBlocking': True,
        'type': {'id': BUILD_POLICY}, 'settings': {'buildDefinitionId': 7}}
    refs = {'sourceRefName': A, 'targetRefName': B}
    return {'pr': pr, 'after': copy.deepcopy(pr), 'refs': refs, 'after_refs': dict(refs),
        'identity': {'org': 'org', 'project': 'project-id', 'repository': 'repo-id', 'pr': 12},
        'url': 'https://dev.azure.com/org/project-id/_git/repo-id/pullrequest/12',
        'artifact': 'vstfs:///CodeReview/CodeReviewId/project-id/12',
        'iterations': [{'id': 2, 'sourceRefCommit': {'commitId': A}, 'targetRefCommit': {'commitId': B},
            'createdDate': '2026-09-04T12:00:00Z', 'updatedDate': '2026-09-04T12:00:00Z'}],
        'policies': [config], 'after_policies': [copy.deepcopy(config)], 'evaluations': [
            {'evaluationId': 'eval', 'configuration': copy.deepcopy(config), 'context': {'buildId': 90},
            'artifactId': 'vstfs:///CodeReview/CodeReviewId/project-id/12',
            'status': 'approved', 'completedDate': '2026-09-04T12:05:00Z'}],
        'builds': {'90': {'id': 90, 'project': {'id': 'project-id'}, 'repository': {'id': 'repo-id'},
            'definition': {'id': 7}, 'sourceBranch': 'refs/pull/12/merge', 'sourceVersion': M,
            'reason': 'pullRequest', 'status': 'completed', 'result': 'succeeded',
            'finishTime': '2026-09-04T12:04:00Z'}}, 'threads': []}


class ReadinessTests(unittest.TestCase):
    def test_complete_current_evidence_is_ready(self):
        self.assertEqual(classify(fixture())['kind'], 'READY')

    def test_policy_evidence_fails_closed(self):
        for status in ['queued', 'running', 'rejected', 'broken', 'unknown', None]:
            with self.subTest(status=status):
                s = fixture(); s['evaluations'][0]['status'] = status
                self.assertEqual(classify(s)['kind'], 'BLOCKER')
        for key, value in [('evaluations', []), ('builds', {}), ('iterations', [])]:
            with self.subTest(key=key):
                s = fixture(); s[key] = value
                self.assertEqual(classify(s)['kind'], 'BLOCKER')
        for key, value in [('completedDate', None), ('completedDate', '2026-09-04T11:59:00Z'),
                           ('artifactId', 'another-pr'), ('context', {})]:
            s = fixture(); s['evaluations'][0][key] = value
            self.assertEqual(classify(s)['kind'], 'BLOCKER')

    def test_green_build_is_not_enough(self):
        for key, value in [('status', 'abandoned'), ('status', 'completed'), ('isDraft', True),
                           ('mergeStatus', 'queued'), ('mergeStatus', 'conflicts'), ('mergeStatus', None)]:
            s = fixture(); s['pr'][key] = value; s['after'][key] = value
            self.assertEqual(classify(s)['kind'], 'BLOCKER')
        s = fixture(); s['pr']['reviewers'][0]['vote'] = 0
        s['after'] = copy.deepcopy(s['pr'])
        self.assertEqual(classify(s)['kind'], 'BLOCKER')
        for status in ['active', 'pending', 'unknown']:
            s = fixture(); s['threads'] = [{'id': 2, 'status': status, 'comments': [
                {'id': 1, 'content': 'Please fix', 'commentType': 'text'}]}]
            self.assertEqual(classify(s)['reasons'][0]['kind'], 'review-threads')

    def test_build_identity_and_result(self):
        for key, value in [('sourceVersion', A), ('sourceBranch', 'refs/heads/work'),
                           ('reason', 'manual'), ('result', 'partiallySucceeded'), ('result', 'failed'),
                           ('status', 'inProgress'), ('definition', {'id': 8}),
                           ('repository', {'id': 'wrong'}), ('project', {'id': 'wrong'})]:
            with self.subTest(key=key, value=value):
                s = fixture(); s['builds']['90'][key] = value
                self.assertEqual(classify(s)['kind'], 'BLOCKER')
        s = fixture(); s['builds']['90']['result'] = 'failed'
        reason = next(x for x in classify(s)['reasons'] if x['kind'] == 'failing-checks')
        self.assertEqual(reason['buildId'], 90)
        self.assertIn('/build/builds/90/logs?api-version=7.1', reason['logs'])

    def test_target_only_update_uses_current_merge_build_not_historical_iteration_target(self):
        s = fixture()
        for pr in [s['pr'], s['after']]:
            pr['lastMergeTargetCommit']['commitId'] = 'd' * 40
            pr['lastMergeCommit']['commitId'] = 'e' * 40
        for refs in [s['refs'], s['after_refs']]:
            refs['targetRefName'] = 'd' * 40
        s['builds']['90']['sourceVersion'] = 'e' * 40
        self.assertEqual(classify(s)['kind'], 'READY')
        s['builds']['90']['sourceVersion'] = M
        self.assertEqual(classify(s)['kind'], 'BLOCKER')

    def test_terminal_pr_does_not_need_deleted_source_ref(self):
        class Terminal:
            target = Identity('org', 'p', 'r', 12)
            def get(self, path):
                if not path.endswith('/pullRequests/12'):
                    raise AssertionError('No branch/evidence read is allowed for terminal state')
                return {'pullRequestId': 12, 'status': 'completed',
                    'repository': {'id': 'r', 'name': 'r', 'project': {'id': 'p', 'name': 'p'}}}
        self.assertEqual(classify(collect(Terminal()))['kind'], 'COMPLETE')

    def test_head_target_or_policy_movement_invalidates_observation(self):
        for field in ['lastMergeSourceCommit', 'lastMergeTargetCommit']:
            s = fixture(); s['after'][field] = {'commitId': 'd' * 40}
            self.assertEqual(classify(s)['kind'], 'BLOCKER')
        s = fixture(); s['after_refs']['targetRefName'] = 'd' * 40
        self.assertEqual(classify(s)['kind'], 'BLOCKER')
        s = fixture(); s['after_policies'][0]['revision'] += 1
        self.assertEqual(classify(s)['kind'], 'BLOCKER')
        s = fixture(); s['evaluations'][0]['configuration']['revision'] -= 1
        self.assertEqual(classify(s)['kind'], 'BLOCKER')

    def test_non_build_policy_freshness_and_not_applicable(self):
        s = fixture(); s['evaluations'][0]['status'] = 'notApplicable'; s['builds'] = {}
        self.assertEqual(classify(s)['kind'], 'READY')
        s['evaluations'][0]['completedDate'] = '2026-09-04T11:00:00Z'
        self.assertEqual(classify(s)['kind'], 'BLOCKER')
        s = fixture(); s['policies'][0]['type']['id'] = 'reviewer-policy'
        s['after_policies'] = copy.deepcopy(s['policies']); s['builds'] = {}
        self.assertEqual(classify(s)['kind'], 'READY')


class IdentityAndTransportTests(unittest.TestCase):
    def test_services_urls_remotes_and_encoding(self):
        expected = Identity('org', 'My Project', 'repo & ui', 12)
        for url in ['https://dev.azure.com/org/My%20Project/_git/repo%20%26%20ui/pullrequest/12',
                    'https://org.visualstudio.com/DefaultCollection/My%20Project/_git/repo%20%26%20ui/pullrequest/12']:
            self.assertEqual(identity(url), expected)
        self.assertEqual(identity('git@ssh.dev.azure.com:v3/org/My%20Project/repo%20%26%20ui', 12), expected)
        self.assertIn('repo%20%26%20ui', expected.url)
        for url in ['12', 'https://ado.example/collection/project/_git/repo/pullrequest/12',
                    'https://dev.azure.com/org/proj/_git/r%2Fother/pullrequest/12',
                    'https://dev.azure.com/org/proj/_git/repo',
                    'https://dev.azure.com.evil/org/proj/_git/repo/pullrequest/12']:
            with self.assertRaises((EvidenceError, ValueError)):
                identity(url)
        with self.assertRaises(EvidenceError):
            identity(expected.url, 13)

    def test_deleted_and_system_comments_do_not_hide_live_replies(self):
        row = {'id': 1, 'status': 1, 'comments': [{'id': 1, 'isDeleted': True},
            {'id': 2, 'commentType': 'system', 'content': 'merge event'},
            {'id': 4, 'commentType': 'codeChange', 'content': 'source update'},
            {'id': 3, 'commentType': 1, 'content': 'human reply', 'author': {'id': 'author'}}]}
        self.assertEqual([x['id'] for x in feedback(row)['comments']], [3])
        row['isDeleted'] = True
        self.assertIsNone(feedback(row))

    def test_pagination_and_evaluation_api_version(self):
        class Fake(Client):
            def __init__(self):
                self.calls = []
            def request(self, path, query, version):
                self.calls.append((dict(query), version))
                return ({'value': [1] * 100 if len(self.calls) == 1 else [2]}, None)
        client = Fake()
        self.assertEqual(len(client.collection('policy/evaluations', paging='skip', version='7.1-preview.1')), 101)
        self.assertEqual(client.calls[1], ({'$top': 100, '$skip': 100}, '7.1-preview.1'))
        class Tokens(Fake):
            def request(self, path, query, version):
                self.calls.append(dict(query))
                return ({'value': [1]}, 'next' if len(self.calls) == 1 else None)
        client = Tokens(); self.assertEqual(client.collection('git/policy/configurations', paging='token'), [1, 1])
        self.assertEqual(client.calls[1]['continuationToken'], 'next')


if __name__ == '__main__':
    unittest.main()
