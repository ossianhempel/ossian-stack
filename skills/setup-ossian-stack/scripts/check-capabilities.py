#!/usr/bin/env python3
"""Report command resolution without installing, downloading, or authenticating."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path


COMMANDS = (
    "asc",
    "gh",
    "glab",
    "az",
    "curl",
    "jq",
    "op",
    "xcodebuild",
    "bun",
    "clerk",
    "convex",
    "rc",
    "trash",
    "python3",
)
RUNNERS = ("npx", "bunx", "pnpm", "yarn")
# `rc` is deliberately excluded: the common npm package named `rc` also ships an
# unrelated executable, so filename presence cannot identify RevenueCat's CLI.
PROJECT_NODE_COMMANDS = ("clerk", "convex")


def project_roots(cwd: Path) -> list[Path]:
    """Return cwd and its parents through the Git worktree root, if present."""
    roots: list[Path] = []
    for candidate in (cwd, *cwd.parents):
        roots.append(candidate)
        if (candidate / ".git").exists():
            break
    return roots


def project_commands(cwd: Path) -> dict[str, list[str]]:
    found = {name: [] for name in PROJECT_NODE_COMMANDS}
    for root in project_roots(cwd):
        bin_dir = root / "node_modules" / ".bin"
        for name in PROJECT_NODE_COMMANDS:
            candidate = bin_dir / name
            if candidate.exists() and os.access(candidate, os.X_OK):
                found[name].append(str(candidate))
    return found


def runner_details(name: str) -> dict[str, object]:
    path = shutil.which(name)
    details: dict[str, object] = {"path": path, "supports_on_demand": bool(path)}
    if name != "yarn" or not path:
        return details

    try:
        result = subprocess.run(
            [path, "--version"],
            capture_output=True,
            check=False,
            text=True,
            timeout=5,
        )
        version = result.stdout.strip() or result.stderr.strip() or None
    except (OSError, subprocess.TimeoutExpired):
        version = None

    details["version"] = version
    try:
        major = int(version.split(".", 1)[0]) if version else None
    except ValueError:
        major = None
    details["supports_on_demand"] = major is not None and major >= 2
    if major == 1:
        details["note"] = "Yarn Classic has no dlx subcommand"
    elif major is None:
        details["note"] = "Could not verify a Yarn version with dlx support"
    return details


def identifies_revenuecat_rc(path: str) -> bool:
    try:
        result = subprocess.run(
            [path, "--help"],
            capture_output=True,
            check=False,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.TimeoutExpired):
        return False
    output = f"{result.stdout}\n{result.stderr}".lower()
    return "revenuecat" in output and "rc projects" in output


def main() -> None:
    cwd = Path.cwd().resolve()
    local = project_commands(cwd)
    commands = {}
    for name in COMMANDS:
        direct = shutil.which(name)
        if name == "rc" and direct:
            revenuecat_rc = identifies_revenuecat_rc(direct)
            status = "verified-global" if revenuecat_rc else "ambiguous-global"
        else:
            revenuecat_rc = None
            status = "global" if direct else ("project-local" if local.get(name) else "not-resolved")
        commands[name] = {
            "status": status,
            "global_path": direct,
            "project_paths": local.get(name, []),
        }
        if name == "rc":
            commands[name]["revenuecat_identity_verified"] = revenuecat_rc

    payload = {
        "cwd": str(cwd),
        "path": os.environ.get("PATH", ""),
        "commands": commands,
        "package_runners": {name: runner_details(name) for name in RUNNERS},
        "notes": [
            "not-resolved means absent from this process PATH and the current project, not absent from the computer",
            "package-runner presence means on-demand execution may be possible; it does not prove the package is installed or authenticated",
            "an rc path is verified only when its help output identifies RevenueCat and its project command group",
            "active MCPs and host-provided tools must be checked by the invoking runtime",
        ],
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
