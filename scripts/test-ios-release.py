#!/usr/bin/env python3
"""Exercise the release helper from a project directory with a stubbed Apple lookup."""

import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


HELPER = Path(__file__).resolve().parents[1] / "skills/release-ios-app/scripts/ios-release"
LIVE = {"resultCount": 1, "results": [{"trackId": 123, "version": "1.10.0"}]}
EMPTY = {"resultCount": 0, "results": []}


class VersionGateTest(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory(prefix="ios-release-test-")
        self.addCleanup(directory.cleanup)
        self.project = Path(directory.name)
        (self.project / ".ios-release.env").write_text(
            "IOS_RELEASE_APP_ID=123\n"
            "IOS_RELEASE_VERSION_SOURCE=app.json\n"
            "IOS_RELEASE_APPSTORE_LOOKUP_COUNTRY=se\n"
        )
        (self.project / "app.json").write_text('{"expo": {"version": "1.11.0"}}')
        curl = self.project / "curl"
        curl.write_text(
            '#!/bin/bash\n'
            '[[ " $* " == *" --max-time 15 "* ]] || exit 2\n'
            '[[ " $* " == *" --data-urlencode id=123 "* ]] || exit 2\n'
            '[[ " $* " == *" --data-urlencode country=se "* ]] || exit 2\n'
            '[[ "$LOOKUP_RESPONSE" != "transport-failure" ]] || exit 28\n'
            'printf "%s" "$LOOKUP_RESPONSE"\n'
        )
        curl.chmod(0o700)

    def run_helper(self, command, lookup, *args):
        response = lookup if isinstance(lookup, str) else json.dumps(lookup)
        return subprocess.run(
            ["bash", str(HELPER), command, *args],
            cwd=self.project,
            env={**os.environ, "PATH": f"{self.project}:{os.environ['PATH']}", "LOOKUP_RESPONSE": response},
            capture_output=True,
            text=True,
            check=False,
        )

    def test_compares_numeric_components(self):
        result = self.run_helper("check-version", LIVE)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("1.11.0 > live 1.10.0", result.stdout)
        for version in ("1.9.9", "1.10.0", "1.10"):
            with self.subTest(version=version):
                result = self.run_helper("check-version", LIVE, version)
                self.assertEqual(result.returncode, 1)
                self.assertIn("Version gate failed", result.stderr)

    def test_empty_storefront_requires_confirmation(self):
        result = self.run_helper("check-version", EMPTY)
        self.assertEqual(result.returncode, 3)
        self.assertIn("App Store Connect", result.stdout)
        self.assertIn("NO LIVE VERSION", self.run_helper("status", EMPTY).stdout)

    def test_lookup_failure_never_passes(self):
        for lookup in (
            "transport-failure",
            "not-json",
            {},
            {"resultCount": 1, "results": []},
            {"resultCount": 1, "results": [{"trackId": 321, "version": "1.10.0"}]},
            {"resultCount": 1, "results": [{"trackId": 123, "version": "unknown"}]},
        ):
            with self.subTest(lookup=lookup):
                result = self.run_helper("check-version", lookup)
                self.assertEqual(result.returncode, 1)
                self.assertIn("lookup unavailable", result.stderr)
                self.assertNotEqual(self.run_helper("live-version", lookup).returncode, 0)
                self.assertIn("UNVERIFIED", self.run_helper("status", lookup).stdout)

    def test_missing_current_version_never_passes(self):
        (self.project / "app.json").write_text("{}")
        result = self.run_helper("check-version", LIVE)
        self.assertEqual(result.returncode, 1)
        self.assertIn("numeric current version", result.stderr)
        self.assertIn("UNVERIFIED", self.run_helper("status", LIVE).stdout)


if __name__ == "__main__":
    unittest.main()
