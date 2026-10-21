#!/usr/bin/env python3
"""Validate trace JSON against local sources; 0 PASS, 1 FAIL, 2 BLOCKED.
No dependencies beyond Python 3. Does not parse Mermaid or prove semantics.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys


def validate(data, root):
    errors = []
    def require(ok, message):
        if not ok:
            errors.append(message)
        return ok
    def local(name):
        if not isinstance(name, str) or not name or Path(name).is_absolute():
            raise ValueError('expected nonempty repository-relative path')
        path = (root / name).resolve()
        if not path.is_relative_to(root):
            raise ValueError('path escapes repository')
        return path
    if not isinstance(data, dict):
        return ['manifest must be an object']
    require(data.get('analysis') in ('static', 'runtime', 'mixed'), 'invalid analysis mode')
    require(type(data.get('dirty')) is bool, 'dirty must be boolean')
    require('commit' in data, 'commit is required (null for non-Git input)')
    sha = data.get('commit')
    if sha is not None:
        if require(isinstance(sha, str) and re.fullmatch(r'[0-9a-f]{40}|[0-9a-f]{64}', sha), 'invalid full commit SHA'):
            try:
                head = subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD'], stderr=subprocess.DEVNULL, text=True).strip()
                require(head == sha, 'commit does not match current HEAD')
                status = subprocess.check_output(['git', '-C', str(root), 'status', '--porcelain'], text=True)
                require(bool(status.strip()) == data.get('dirty'), 'dirty flag does not match worktree')
            except (FileNotFoundError, subprocess.CalledProcessError) as exc:
                raise RuntimeError('Git provenance unavailable') from exc
    algorithms = data.get('algorithms')
    if not require(isinstance(algorithms, list) and bool(algorithms), 'algorithms must be a nonempty list'):
        return errors
    seen = set()
    for a in algorithms:
        if not require(isinstance(a, dict), 'algorithm must be object'):
            continue
        aid = a.get('id')
        if not require(isinstance(aid, str) and bool(aid), 'algorithm id required'):
            continue
        require(aid not in seen, f'duplicate algorithm {aid}')
        seen.add(aid)
        require(isinstance(a.get('entry'), str) and bool(a.get('entry')), f'{aid}: entry required')
        for key in ('calls', 'uncertainties'):
            require(isinstance(a.get(key), list) and all(isinstance(x, str) for x in a.get(key, [])), f'{aid}: {key} must be string list')
        try:
            require(local(a.get('diagram')).is_file(), f'{aid}: diagram missing')
        except ValueError as exc:
            errors.append(f'{aid}: {exc}')
        expected = set()
        for kind, key in [('node', 'nodes'), ('edge', 'edges')]:
            ids = a.get(key)
            if require(isinstance(ids, list) and all(isinstance(x, str) and x for x in ids), f'{aid}: invalid {key}'):
                require(len(ids) == len(set(ids)), f'{aid}: duplicate {key}')
                if kind == 'node':
                    require(bool(ids), f'{aid}: nodes cannot be empty')
                expected.update((kind, x) for x in ids)
        covered = set()
        evidence = a.get('evidence')
        if not require(isinstance(evidence, list), f'{aid}: evidence must be list'):
            continue
        for e in evidence:
            if not require(isinstance(e, dict), f'{aid}: evidence must be object'):
                continue
            kind, eid = e.get('kind'), e.get('id')
            if not require(isinstance(kind, str) and isinstance(eid, str), f'{aid}: invalid evidence identity'):
                continue
            identity = (kind, eid)
            require(identity in expected, f'{aid}: unlisted evidence {identity}')
            covered.add(identity)
            for key in ('symbol', 'condition'):
                require(isinstance(e.get(key), str) and bool(e.get(key)), f'{aid}/{eid}: {key} required')
            try:
                path = local(e.get('file'))
                content = path.read_bytes()
                lines = len(content.decode('utf-8').splitlines())
                start, end = e.get('start'), e.get('end')
                require(type(start) is int and type(end) is int and 1 <= start <= end <= lines, f'{aid}/{eid}: invalid line range')
                require(e.get('sha256') == hashlib.sha256(content).hexdigest(), f'{aid}/{eid}: source hash mismatch')
            except (ValueError, OSError) as exc:
                errors.append(f'{aid}/{eid}: {exc}')
        require(expected <= covered, f'{aid}: missing evidence {sorted(expected - covered)}')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path)
    parser.add_argument('--root', type=Path, required=True)
    args = parser.parse_args()
    if not args.root.is_dir() or not args.manifest.is_file():
        print('BLOCKED: repository root or manifest unavailable', file=sys.stderr)
        return 2
    try:
        data = json.loads(args.manifest.read_text())
        errors = validate(data, args.root.resolve())
    except RuntimeError as exc:
        print(f'BLOCKED: {exc}', file=sys.stderr)
        return 2
    except (ValueError, OSError) as exc:
        print(f'FAIL: {exc}', file=sys.stderr)
        return 1
    if errors:
        print('\n'.join('FAIL: ' + e for e in errors), file=sys.stderr)
        return 1
    print('PASS: provenance structure and local source references; semantics/rendering not tested')
    return 0


if __name__ == '__main__':
    sys.exit(main())
