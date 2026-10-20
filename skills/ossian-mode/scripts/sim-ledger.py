#!/usr/bin/env python3
"""Track the iOS simulators a task creates and delete exactly those at the end.

Ownership is explicit, never inferred from names or age:
  - devices created or cloned through this script (or adopted by UDID) are owned;
  - devices that appear in Xcode's test-clone set (`simctl --set testing`) after
    `begin` are owned, because only xcodebuild creates devices there.
Every other simulator, including any the user already had, is left alone.

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
import subprocess
import sys


def simctl(*args, testing=False, check=True):
    cmd = ['xcrun', 'simctl'] + (['--set', 'testing'] if testing else []) + list(args)
    return subprocess.run(cmd, capture_output=True, text=True, check=check)


def udids(testing):
    try:
        out = simctl('list', 'devices', '-j', testing=testing).stdout
    except subprocess.CalledProcessError:
        return set()  # no test-clone set exists yet
    return {d['udid'] for devices in json.loads(out)['devices'].values() for d in devices}


def load(path):
    with open(path) as f:
        return json.load(f)


def save(path, ledger):
    tmp = path + '.tmp'
    with open(tmp, 'w') as f:
        json.dump(ledger, f, indent=2)
    os.replace(tmp, path)


def owned(ledger):
    """(udid, testing) pairs this task owns that still exist."""
    default = [(u, False) for u in ledger['owned'] if u in udids(False)]
    clones = [(u, True) for u in sorted(udids(True) - set(ledger['testing_baseline']))]
    return default + clones


def record(path, udid):
    ledger = load(path)
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
        save(path, {'testing_baseline': sorted(udids(True)), 'owned': []})
    elif cmd == 'create' and len(rest) == 3:
        record(path, simctl('create', *rest).stdout.strip())
    elif cmd == 'clone' and len(rest) == 2:
        record(path, simctl('clone', *rest).stdout.strip())
    elif cmd == 'adopt' and len(rest) == 1:
        record(path, rest[0])
    elif cmd == 'status':
        for udid, testing in owned(load(path)):
            print(f"{udid}{' (test clone)' if testing else ''}")
    elif cmd == 'end':
        ledger = load(path)
        for udid, testing in owned(ledger):
            simctl('shutdown', udid, testing=testing, check=False)  # delete refuses a booted device
            simctl('delete', udid, testing=testing, check=False)
        left = owned(ledger)
        if left:
            print('not deleted: ' + ', '.join(u for u, _ in left), file=sys.stderr)
            sys.exit(1)
        os.remove(path)
        print('all task-owned simulators deleted')
    else:
        sys.exit(__doc__)


if __name__ == '__main__':
    main(sys.argv[1:])
