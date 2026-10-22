#!/usr/bin/env python3
"""Track the iOS simulators a task creates and delete exactly those at the end.

Ownership is explicit, never inferred from age:
  - devices created or cloned through this script (or adopted by UDID) are owned;
  - the one name-based rule: a device that appears in Xcode's test-clone set (`simctl --set testing`)
    after `begin` is this task's leaked clone only when its name says it was
    cloned from an owned device ("Clone N of <name>") and no device the task
    does not own shares that name. Other new clones may belong to Xcode.app or
    another session, so they are reported and left alone. While an xcodebuild
    process runs, `end` skips owned clones too and keeps the ledger for a retry.
Every other simulator, including any the user already had, is left alone.
A failed `simctl` call stops the script without deleting anything.

Usage:
  sim-ledger.py begin  LEDGER                          snapshot the test-clone set
  sim-ledger.py create LEDGER NAME DEVICE_TYPE RUNTIME create a device; prints its UDID
  sim-ledger.py clone  LEDGER SOURCE_UDID NAME          clone a device; prints its UDID
  sim-ledger.py adopt  LEDGER UDID                      record a device made another way
  sim-ledger.py status LEDGER                           list what `end` would delete
  sim-ledger.py end    LEDGER                           shut down and delete owned devices

`end` removes the ledger only when every owned device is gone; otherwise it
prints the leftovers, keeps the ledger for a retry, and exits 1.
"""
import json
import os
import re
import subprocess
import sys


def simctl(*args, testing=False, check=True):
    cmd = ['xcrun', 'simctl'] + (['--set', 'testing'] if testing else []) + list(args)
    return subprocess.run(cmd, capture_output=True, text=True, check=check)


TESTING_SET = os.path.expanduser('~/Library/Developer/XCTestDevices')


def devices(testing):
    """{udid: name} for every device in the default or test-clone set."""
    if testing and not os.path.isdir(TESTING_SET):
        return {}  # xcodebuild has never made a test clone on this machine
    out = simctl('list', 'devices', '-j', testing=testing).stdout  # raises on failure
    return {d['udid']: d['name'] for ds in json.loads(out)['devices'].values() for d in ds}


CLONE_NAME = re.compile(r'Clone \d+ of (.+)')


def xcodebuild_running():
    return subprocess.run(['pgrep', '-x', 'xcodebuild'], capture_output=True).returncode == 0


def load(path):
    with open(path) as f:
        return json.load(f)


def save(path, ledger):
    tmp = path + '.tmp'
    with open(tmp, 'w') as f:
        json.dump(ledger, f, indent=2)
    os.replace(tmp, path)


def scan(ledger):
    """(owned, unclaimed): (udid, testing) pairs this task owns that still exist,
    and new test clones it cannot prove are its own."""
    present = devices(False)
    mine = set(ledger['owned']) | set(ledger.get('clones', []))
    mine_names = {present[u] for u in mine if u in present}
    other_names = {n for u, n in present.items() if u not in mine}
    clones, unclaimed = [], []
    for u, name in sorted(devices(True).items()):
        if u in mine:
            clones.append((u, True))  # adopted, or claimed by an earlier `end`
            continue
        if u in ledger['testing_baseline']:
            continue
        m = CLONE_NAME.fullmatch(name)
        source = m.group(1) if m else None
        if source in mine_names and source not in other_names:
            clones.append((u, True))
        else:
            unclaimed.append(u)
    return [(u, False) for u in sorted(mine) if u in present] + clones, unclaimed


def deletable(pairs):
    """Split owned devices into those safe to delete now and skipped clones."""
    if not xcodebuild_running():
        return pairs, []
    return [p for p in pairs if not p[1]], [p for p in pairs if p[1]]


def record(path, ledger, udid):
    if udid not in ledger['owned']:
        ledger['owned'].append(udid)
        save(path, ledger)
    print(udid)


def main(argv):
    if len(argv) < 2:
        sys.exit(__doc__)
    cmd, path, rest = argv[0], argv[1], argv[2:]

    if cmd == 'begin':
        if os.path.exists(path):
            print(f'ledger exists, resuming: {path}', file=sys.stderr)
            return
        save(path, {'testing_baseline': sorted(devices(True)), 'owned': []})
    elif cmd == 'create' and len(rest) == 3:
        ledger = load(path)  # before simctl, so a missing ledger leaks nothing
        record(path, ledger, simctl('create', *rest).stdout.strip())
    elif cmd == 'clone' and len(rest) == 2:
        ledger = load(path)
        record(path, ledger, simctl('clone', *rest).stdout.strip())
    elif cmd == 'adopt' and len(rest) == 1:
        record(path, load(path), rest[0])
    elif cmd == 'status':
        pairs, unclaimed = scan(load(path))
        now, skipped = deletable(pairs)
        for udid, testing in now:
            print(f"{udid}{' (test clone)' if testing else ''}")
        for udid, _ in skipped:
            print(f'{udid} (test clone, skipped while xcodebuild runs)')
        for udid in unclaimed:
            print(f'{udid} (new test clone, not provably this task\'s; left alone)')
    elif cmd == 'end':
        ledger = load(path)
        pairs, unclaimed = scan(ledger)
        # Record claimed clones before deleting their source devices, which
        # are what ties them to this task; a retry still finds them.
        ledger['clones'] = sorted(set(ledger.get('clones', [])) | {u for u, t in pairs if t})
        save(path, ledger)
        now, skipped = deletable(pairs)
        for udid, testing in now:
            simctl('shutdown', udid, testing=testing, check=False)  # delete refuses a booted device
            simctl('delete', udid, testing=testing, check=False)
        if unclaimed:
            print('left alone, may belong to Xcode.app or another session: '
                  + ', '.join(unclaimed), file=sys.stderr)
        left, _ = scan(ledger)
        if left:
            print('not deleted: ' + ', '.join(u for u, _ in left), file=sys.stderr)
            if skipped:
                print('test clones are skipped while an xcodebuild process runs; '
                      'rerun `end` once it exits', file=sys.stderr)
            sys.exit(1)
        os.remove(path)
        print('all task-owned simulators deleted')
    else:
        sys.exit(__doc__)


if __name__ == '__main__':
    main(sys.argv[1:])
