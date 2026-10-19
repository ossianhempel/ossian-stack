#!/usr/bin/env python3
"""Read-only GitHub Actions run-cohort evidence; no billing invoice estimate."""
import argparse
import datetime as dt
import json
import math
import pathlib
import re
import subprocess
import sys
import urllib.parse

STANDARD = re.compile(
    r"^(ubuntu-(latest|slim|\d{2}\.\d{2})(-arm)?|"
    r"windows-(latest|\d{4}|11-arm)|macos-(latest|\d{2})(-intel)?)$"
)


def timestamp(value):
    parsed = dt.datetime.fromisoformat(value.replace('Z', '+00:00'))
    if parsed.tzinfo is None:
        raise ValueError('Timestamps must include a UTC offset')
    return parsed.astimezone(dt.timezone.utc)


def iso(value):
    return value.isoformat(timespec='seconds').replace('+00:00', 'Z')


def api(path):
    process = subprocess.run(
        ['gh', 'api', '--method', 'GET', '--paginate', '--slurp', path],
        capture_output=True, text=True,
    )
    if process.returncode:
        raise RuntimeError(process.stderr.strip() or 'GitHub API request failed')
    pages = json.loads(process.stdout)
    if not isinstance(pages, list) or not pages:
        raise RuntimeError('GitHub API returned no response pages')
    return pages


def list_runs(repo, start, end, get=api):
    query = urllib.parse.urlencode({'per_page': 100, 'created': iso(start) + '..' + iso(end)})
    pages = get('repos/' + repo + '/actions/runs?' + query)
    count = pages[0]['total_count']
    if count >= 1000:
        seconds = int((end - start).total_seconds())
        if seconds <= 1:
            raise RuntimeError('Run search remains capped at 1,000 in a one-second window')
        middle = start + dt.timedelta(seconds=seconds // 2)
        runs = list_runs(repo, start, middle, get) + list_runs(repo, middle, end, get)
    else:
        runs = [run for page in pages for run in page['workflow_runs']]
        runs = list({run['id']: run for run in runs}.values())
        if len(runs) != count:
            raise RuntimeError('Incomplete run pagination: expected %s unique records, got %s' % (count, len(runs)))
    return list({run['id']: run for run in runs
                 if start <= timestamp(run['created_at']) < end}.values())


def attempt(value, source):
    if type(value) is not int or value <= 0:
        raise RuntimeError('%s has no valid positive integer attempt identity' % source)
    return value


def classify(repo, run, job, overrides):
    attempt(run.get('run_attempt'), 'Run')
    attempt(job.get('run_attempt'), 'Job')
    labels = [label.lower() for label in job.get('labels', [])]
    setup = any(step.get('name') == 'Set up job' and step.get('conclusion') != 'skipped'
                for step in job.get('steps', []))
    allocated = bool(job.get('runner_id')) or setup
    minutes = None
    if job.get('conclusion') == 'skipped' or (not allocated and job.get('conclusion') == 'cancelled'):
        minutes = 0
    elif allocated and job.get('started_at') and job.get('completed_at'):
        seconds = (timestamp(job['completed_at']) - timestamp(job['started_at'])).total_seconds()
        minutes = seconds / 60 if seconds >= 0 else None
    kind = 'unknown'
    if 'self-hosted' in labels:
        kind = 'self-hosted'
    else:
        mapped = {overrides[label] for label in labels if label in overrides}
        if len(mapped) == 1:
            kind = mapped.pop()
        elif not mapped and any(STANDARD.fullmatch(label) for label in labels):
            kind = 'standard'
    own_dependabot = run.get('path', '').startswith('dynamic/dependabot/')
    private_pages = repo['private'] and run.get('path', '').startswith('dynamic/pages/')
    if minutes == 0:
        billing = 'no-execution'
    elif kind == 'self-hosted':
        billing = 'self-hosted'
    elif kind == 'larger':
        billing = 'chargeable-before-allowance'
    elif kind == 'standard':
        billing = ('free-dependabot' if own_dependabot else
                   'free-public' if not repo['private'] else
                   'unknown' if private_pages else 'chargeable-before-allowance')
    else:
        billing = 'unknown'
    return {
        'repo': repo['full_name'], 'workflow': run.get('name'), 'event': run.get('event'),
        'branch': run.get('head_branch'), 'sha': run.get('head_sha'), 'path': run.get('path'),
        'run_id': run['id'], 'attempt': job.get('run_attempt'), 'job_id': job['id'],
        'job': job.get('name'), 'conclusion': job.get('conclusion'), 'url': job.get('html_url'),
        'labels': job.get('labels', []), 'runner_kind': kind, 'allocated': allocated,
        'raw_minutes': minutes, 'rounded_minutes': math.ceil(minutes) if minutes is not None else None,
        'billing_category': billing,
    }


def collect(repositories, start, end, overrides=None, get=api):
    result = {'start': iso(start), 'end': iso(end), 'captured_at': iso(dt.datetime.now(dt.timezone.utc)),
              'window_basis': 'run creation; all attempts available at capture',
              'repositories': repositories, 'evidence': [], 'rows': [], 'errors': [], 'warnings': []}
    for name in repositories:
        try:
            repo = get('repos/' + name)[0]
            runs = list_runs(name, start, end, get)
        except (RuntimeError, ValueError, KeyError, TypeError, OSError) as error:
            result['errors'].append({'repo': name, 'stage': 'repository/runs', 'error': str(error)})
            continue
        evidence = {'repo': repo, 'runs': []}
        result['evidence'].append(evidence)
        for listed_run in runs:
            run = listed_run
            try:
                run = get('repos/%s/actions/runs/%s' % (name, listed_run['id']))[0]
                if run['id'] != listed_run['id']:
                    raise RuntimeError('Run detail ID does not match listed run')
                run_attempt = attempt(run.get('run_attempt'), 'Run detail')
                if any(run.get(field) != listed_run.get(field)
                       for field in ('run_attempt', 'conclusion', 'status')):
                    result['warnings'].append({'repo': name, 'run_id': run['id'],
                                               'warning': 'List metadata differs from hydrated run detail'})
                pages = get('repos/%s/actions/runs/%s/jobs?per_page=100&filter=all' % (name, run['id']))
                jobs = [job for page in pages for job in page['jobs']]
                # Compare unique records with the declared count: repeated pages
                # can have the expected raw length while omitting real jobs.
                jobs = list({job['id']: job for job in jobs}.values())
                if len(jobs) != pages[0]['total_count']:
                    raise RuntimeError('Incomplete job pagination')
                job_attempts = [attempt(job.get('run_attempt'), 'Job') for job in jobs]
                if any(job_attempt > run_attempt for job_attempt in job_attempts):
                    raise RuntimeError('A newer job attempt appeared during collection; capture again')
                rows = [classify(repo, run, job, overrides or {}) for job in jobs]
                evidence['runs'].append({'listed_run': listed_run, 'run': run, 'jobs': jobs})
                result['rows'].extend(rows)
            except (RuntimeError, ValueError, KeyError, TypeError, OSError) as error:
                result['errors'].append({'repo': name, 'run_id': run['id'], 'stage': 'jobs', 'error': str(error)})
    rows = result['rows']
    unknown = sum(row['raw_minutes'] is None or row['billing_category'] == 'unknown' for row in rows)
    observed = sum(row['rounded_minutes'] or 0 for row in rows
                   if row['billing_category'] == 'chargeable-before-allowance')
    complete = not result['errors'] and not unknown
    result['summary'] = {
        'status': 'complete' if complete else 'partial', 'jobs_observed': len(rows),
        'unknown_jobs': unknown, 'observed_chargeable_rounded_minutes': observed,
        'chargeable_rounded_minutes': observed if complete else None,
        'actual_billed_spend': None,
    }
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('repositories', nargs='+', help='Explicit OWNER/REPO scope')
    parser.add_argument('--days', type=int, default=30)
    parser.add_argument('--start', help='Inclusive ISO-8601 timestamp, offset required')
    parser.add_argument('--end', help='Exclusive ISO-8601 timestamp, offset required')
    parser.add_argument('--runner-kind', action='append', default=[], metavar='LABEL=KIND')
    parser.add_argument('--out', required=True, type=pathlib.Path)
    args = parser.parse_args()
    try:
        if args.days <= 0:
            raise ValueError('--days must be positive')
        end = timestamp(args.end) if args.end else dt.datetime.now(dt.timezone.utc).replace(microsecond=0)
        start = timestamp(args.start) if args.start else end - dt.timedelta(days=args.days)
        if start >= end:
            raise ValueError('--start must precede --end')
        overrides = {}
        for mapping in args.runner_kind:
            label, kind = mapping.rsplit('=', 1)
            if not label or kind not in ('standard', 'larger', 'self-hosted'):
                raise ValueError('Runner mapping requires LABEL=standard|larger|self-hosted')
            overrides[label.lower()] = kind
        if any(not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', name) for name in args.repositories):
            raise ValueError('Repositories must be OWNER/REPO')
    except ValueError as error:
        parser.error(str(error))
    result = collect(list(dict.fromkeys(args.repositories)), start, end, overrides)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result['summary'], indent=2))
    return 0 if result['summary']['status'] == 'complete' else 2


if __name__ == '__main__':
    sys.exit(main())
