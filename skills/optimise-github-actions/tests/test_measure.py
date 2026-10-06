import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('measure', ROOT / 'scripts' / 'measure.py')
measure = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(measure)


def fixture():
    return ({'full_name': 'owner/repo', 'private': True},
            {'id': 1, 'name': 'CI', 'path': '.github/workflows/ci.yml', 'event': 'pull_request',
             'created_at': '2026-01-01T12:00:00Z', 'run_attempt': 1, 'conclusion': 'success'},
            {'id': 2, 'run_attempt': 1, 'labels': ['ubuntu-latest'], 'runner_id': 7,
             'conclusion': 'success', 'started_at': '2026-01-01T12:00:00Z',
             'completed_at': '2026-01-01T12:01:01Z', 'steps': []})


class AccountingTests(unittest.TestCase):
    def row(self, repo=None, run=None, job=None, mappings=None):
        defaults = fixture()
        return measure.classify(repo or defaults[0], run or defaults[1], job or defaults[2], mappings or {})

    def test_rounds_per_job(self):
        row = self.row()
        self.assertEqual(row['rounded_minutes'], 2)
        self.assertEqual(row['billing_category'], 'chargeable-before-allowance')

    def test_public_standard_free_but_larger_chargeable(self):
        repo, run, job = fixture()
        repo['private'] = False
        self.assertEqual(self.row(repo, run, job)['billing_category'], 'free-public')
        job['labels'] = ['custom-large']
        self.assertEqual(self.row(repo, run, job, {'custom-large': 'larger'})['billing_category'],
                         'chargeable-before-allowance')

    def test_attempt_runner_labels_win_over_workflow_name(self):
        repo, run, job = fixture()
        hosted = self.row(repo, run, job)
        job['run_attempt'] = 2
        job['labels'] = ['self-hosted', 'macOS', 'ARM64']
        retry = self.row(repo, run, job)
        self.assertEqual(hosted['billing_category'], 'chargeable-before-allowance')
        self.assertEqual(retry['billing_category'], 'self-hosted')

    def test_queue_cancellation_is_not_runtime(self):
        repo, run, job = fixture()
        job.update(runner_id=0, conclusion='cancelled', completed_at='2026-01-01T15:00:00Z')
        row = self.row(repo, run, job)
        self.assertEqual(row['rounded_minutes'], 0)
        self.assertEqual(row['billing_category'], 'no-execution')

    def test_allocated_cancellation_still_counts(self):
        repo, run, job = fixture()
        job['conclusion'] = 'cancelled'
        self.assertEqual(self.row(repo, run, job)['rounded_minutes'], 2)

    def test_setup_evidence_handles_retired_runner_id(self):
        repo, run, job = fixture()
        job['runner_id'] = 0
        job['steps'] = [{'name': 'Set up job', 'conclusion': 'success'}]
        self.assertEqual(self.row(repo, run, job)['rounded_minutes'], 2)

    def test_dependabot_own_update_differs_from_ci_on_its_pr(self):
        repo, run, job = fixture()
        run.update(event='dynamic', path='dynamic/dependabot/dependabot-updates')
        self.assertEqual(self.row(repo, run, job)['billing_category'], 'free-dependabot')
        run.update(event='pull_request', path='.github/workflows/ci.yml', actor={'login': 'dependabot[bot]'})
        self.assertEqual(self.row(repo, run, job)['billing_category'], 'chargeable-before-allowance')
        run.update(event='dynamic', path='dynamic/copilot/review')
        self.assertEqual(self.row(repo, run, job)['billing_category'], 'chargeable-before-allowance')

    def test_unknown_runner_does_not_default_to_linux(self):
        repo, run, job = fixture()
        job['labels'] = ['my-macos-pool']
        self.assertEqual(self.row(repo, run, job)['billing_category'], 'unknown')

    def test_private_generated_pages_exemption_requires_evidence(self):
        repo, run, job = fixture()
        run['path'] = 'dynamic/pages/pages-build-deployment'
        self.assertEqual(self.row(repo, run, job)['billing_category'], 'unknown')
        repo['private'] = False
        self.assertEqual(self.row(repo, run, job)['billing_category'], 'free-public')
        repo['private'] = True
        job['labels'] = ['self-hosted', 'linux']
        self.assertEqual(self.row(repo, run, job)['billing_category'], 'self-hosted')
        job['labels'] = ['custom-large']
        self.assertEqual(self.row(repo, run, job, {'custom-large': 'larger'})['billing_category'],
                         'chargeable-before-allowance')

    def test_pages_workflow_name_does_not_imply_exemption(self):
        repo, run, job = fixture()
        run['name'] = 'GitHub Pages'
        self.assertEqual(self.row(repo, run, job)['billing_category'], 'chargeable-before-allowance')

    def test_missing_duration_is_unknown(self):
        repo, run, job = fixture()
        job['completed_at'] = None
        self.assertIsNone(self.row(repo, run, job)['rounded_minutes'])


class CollectionTests(unittest.TestCase):
    START = measure.timestamp('2026-01-01T00:00:00Z')
    END = measure.timestamp('2026-01-02T00:00:00Z')

    def get(self, path):
        repo, run, job = fixture()
        if path == 'repos/owner/repo':
            return [repo]
        if '/jobs?' in path:
            return [{'total_count': 1, 'jobs': [job]}]
        if '/runs?' in path:
            return [{'total_count': 1, 'workflow_runs': [run]}]
        if path.endswith('/runs/1'):
            return [run]
        raise RuntimeError('Not found')

    def test_partial_repo_failure_never_reports_zero_definitive_total(self):
        result = measure.collect(['owner/repo', 'owner/missing'], self.START, self.END, get=self.get)
        self.assertEqual(result['summary']['observed_chargeable_rounded_minutes'], 2)
        self.assertIsNone(result['summary']['chargeable_rounded_minutes'])
        self.assertEqual(len(result['errors']), 1)

    def test_job_failure_never_reports_zero_definitive_total(self):
        def failed_jobs(path):
            if '/jobs?' in path:
                raise RuntimeError('403 unavailable')
            return self.get(path)
        result = measure.collect(['owner/repo'], self.START, self.END, get=failed_jobs)
        self.assertIsNone(result['summary']['chargeable_rounded_minutes'])
        self.assertEqual(result['summary']['status'], 'partial')

    def test_incomplete_pagination_is_partial(self):
        def incomplete(path):
            if '/jobs?' in path:
                return [{'total_count': 2, 'jobs': [fixture()[2]]}]
            return self.get(path)
        result = measure.collect(['owner/repo'], self.START, self.END, get=incomplete)
        self.assertEqual(result['summary']['status'], 'partial')
        self.assertIsNone(result['summary']['chargeable_rounded_minutes'])

    def test_duplicate_jobs_cannot_hide_missing_job(self):
        def duplicate_jobs(path):
            if '/jobs?' in path:
                job = fixture()[2]
                return [{'total_count': 2, 'jobs': [job]}, {'total_count': 2, 'jobs': [job]}]
            return self.get(path)
        result = measure.collect(['owner/repo'], self.START, self.END, get=duplicate_jobs)
        self.assertEqual(result['summary']['status'], 'partial')
        self.assertIsNone(result['summary']['chargeable_rounded_minutes'])
        self.assertEqual(result['errors'][0]['stage'], 'jobs')

    def test_duplicate_runs_cannot_hide_missing_run(self):
        def duplicate_runs(path):
            if '/runs?' in path:
                run = fixture()[1]
                return [{'total_count': 2, 'workflow_runs': [run]},
                        {'total_count': 2, 'workflow_runs': [run]}]
            return self.get(path)
        result = measure.collect(['owner/repo'], self.START, self.END, get=duplicate_runs)
        self.assertEqual(result['summary']['status'], 'partial')
        self.assertIsNone(result['summary']['chargeable_rounded_minutes'])
        self.assertEqual(result['errors'][0]['stage'], 'repository/runs')

    def test_stale_list_outcome_hydrates_detail_and_keeps_attempts(self):
        def retry(path):
            if path.endswith('/runs/1'):
                run = fixture()[1]
                run.update(run_attempt=2, conclusion='success')
                return [run]
            if '/runs?' in path:
                run = fixture()[1]
                run['conclusion'] = 'failure'
                return [{'total_count': 1, 'workflow_runs': [run]}]
            if '/jobs?' in path:
                first = fixture()[2]
                first['conclusion'] = 'failure'
                second = dict(first, id=3, run_attempt=2, conclusion='success')
                return [{'total_count': 2, 'jobs': [first, second]}]
            return self.get(path)
        result = measure.collect(['owner/repo'], self.START, self.END, get=retry)
        self.assertEqual(result['summary']['chargeable_rounded_minutes'], 4)
        self.assertEqual(result['evidence'][0]['runs'][0]['run']['run_attempt'], 2)
        self.assertEqual(result['evidence'][0]['runs'][0]['listed_run']['conclusion'], 'failure')
        self.assertEqual([row['attempt'] for row in result['rows']], [1, 2])
        self.assertEqual(len(result['warnings']), 1)

    def test_new_attempt_race_is_partial(self):
        def race(path):
            if '/jobs?' in path:
                job = fixture()[2]
                job['run_attempt'] = 2
                return [{'total_count': 1, 'jobs': [job]}]
            return self.get(path)
        self.assertEqual(measure.collect(['owner/repo'], self.START, self.END, get=race)['summary']['status'],
                         'partial')

    def test_invalid_job_attempt_identity_is_partial(self):
        for invalid in (None, 0, -1, True, '1', 1.0):
            with self.subTest(attempt=invalid):
                def invalid_job(path):
                    if '/jobs?' in path:
                        job = fixture()[2]
                        job['run_attempt'] = invalid
                        return [{'total_count': 1, 'jobs': [job]}]
                    return self.get(path)
                result = measure.collect(['owner/repo'], self.START, self.END, get=invalid_job)
                self.assertEqual(result['summary']['status'], 'partial')
                self.assertIsNone(result['summary']['chargeable_rounded_minutes'])

    def test_invalid_run_attempt_identity_is_partial(self):
        for invalid in (None, 0, -1, True, '1', 1.0):
            with self.subTest(attempt=invalid):
                def invalid_run(path):
                    if path.endswith('/runs/1'):
                        run = fixture()[1]
                        run['run_attempt'] = invalid
                        return [run]
                    return self.get(path)
                result = measure.collect(['owner/repo'], self.START, self.END, get=invalid_run)
                self.assertEqual(result['summary']['status'], 'partial')
                self.assertIsNone(result['summary']['chargeable_rounded_minutes'])

    def test_runs_split_at_cap_and_end_is_exclusive(self):
        calls = []
        def capped(path):
            calls.append(path)
            run = fixture()[1]
            if len(calls) == 1:
                return [{'total_count': 1000, 'workflow_runs': []}]
            return [{'total_count': 1, 'workflow_runs': [run]}]
        runs = measure.list_runs('owner/repo', self.START, self.END, capped)
        self.assertEqual(len(calls), 3)
        self.assertEqual(len(runs), 1)
        self.assertEqual(measure.list_runs('owner/repo', self.START,
                                         measure.timestamp('2026-01-01T12:00:00Z'), self.get), [])

    def test_explicit_only_policy_is_paired(self):
        self.assertIn('disable-model-invocation: true', (ROOT / 'SKILL.md').read_text())
        self.assertIn('allow_implicit_invocation: false', (ROOT / 'agents' / 'openai.yaml').read_text())


if __name__ == '__main__':
    unittest.main()
