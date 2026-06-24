#!/usr/bin/env python3
"""
Batch script-mode test for LARQL Marimo notebooks.

Runs all notebooks in script mode to verify they work without errors.
Script mode simulates running the notebook as `python notebook.py`.

Usage:
    python scripts/batch-script-mode.py
    python scripts/batch-script-mode.py --notebooks 00_what_is_larql.py 03_lql_syntax.py
"""

import argparse
import subprocess
import sys
import time
from pathlib import Path

NOTEBOOKS_DIR = Path(__file__).resolve().parent.parent / "notebooks"
TIMEOUT = 60  # Seconds per notebook


def run_notebook_script_mode(notebook_path: Path) -> dict:
    """Run a single notebook in script mode and return results."""
    result = {
        'path': notebook_path.name,
        'success': False,
        'exit_code': -1,
        'stdout': '',
        'stderr': '',
        'duration': 0,
    }
    
    cmd = ['uv', 'run', '--no-sync', str(notebook_path)]
    
    start = time.time()
    try:
        proc = subprocess.run(
            cmd,
            cwd=NOTEBOOKS_DIR,
            capture_output=True,
            text=True,
            timeout=TIMEOUT,
        )
        result['exit_code'] = proc.returncode
        result['stdout'] = proc.stdout[-500:] if len(proc.stdout) > 500 else proc.stdout
        result['stderr'] = proc.stderr[-500:] if len(proc.stderr) > 500 else proc.stderr
        result['success'] = proc.returncode == 0
    except subprocess.TimeoutExpired:
        result['stderr'] = f'Timeout after {TIMEOUT}s'
    except Exception as e:
        result['stderr'] = str(e)
    
    result['duration'] = round(time.time() - start, 2)
    return result


def main():
    """Run batch script-mode tests."""
    parser = argparse.ArgumentParser(description='Batch script-mode test for LARQL notebooks')
    parser.add_argument('--notebooks', nargs='+', help='Specific notebooks to test (default: all)')
    args = parser.parse_args()
    
    print(f"🧪 Batch Script-Mode Test")
    print(f"   Notebooks dir: {NOTEBOOKS_DIR}")
    print(f"   Timeout: {TIMEOUT}s per notebook")
    print()
    
    # Find notebooks
    if args.notebooks:
        notebooks = [NOTEBOOKS_DIR / nb for nb in args.notebooks]
        notebooks = [nb for nb in notebooks if nb.exists()]
    else:
        notebooks = sorted(NOTEBOOKS_DIR.glob('*.py'))
        # Exclude helper modules
        notebooks = [nb for nb in notebooks if not nb.name.startswith('_')]
    
    if not notebooks:
        print("❌ No notebooks found!")
        sys.exit(1)
    
    print(f"Found {len(notebooks)} notebooks to test")
    print()
    
    # Run tests
    results = []
    for nb in notebooks:
        print(f"📝 Testing {nb.name}...", end=' ', flush=True)
        result = run_notebook_script_mode(nb)
        results.append(result)
        
        if result['success']:
            print(f"✅ PASS ({result['duration']}s)")
        else:
            print(f"❌ FAIL (exit={result['exit_code']}, {result['duration']}s)")
            if result['stderr']:
                print(f"   Error: {result['stderr'][:200]}")
    
    # Summary
    print()
    print("=" * 70)
    print(f"{'Notebook':<40} {'Status':^10} {'Duration':^10}")
    print("=" * 70)
    
    ok_count = 0
    for r in results:
        status = '✅ PASS' if r['success'] else '❌ FAIL'
        if r['success']:
            ok_count += 1
        print(f"{r['path']:<40} {status:^10} {r['duration']:^10}")
    
    print("=" * 70)
    print(f"\nSummary: {ok_count}/{len(results)} notebooks passed")
    
    # Show failures
    failures = [r for r in results if not r['success']]
    if failures:
        print(f"\n❌ Failures ({len(failures)}):")
        for r in failures:
            print(f"  - {r['path']}: exit={r['exit_code']}")
            if r['stderr']:
                print(f"    {r['stderr'][:300]}")
    
    # Exit with error if any failures
    sys.exit(0 if ok_count == len(results) else 1)


if __name__ == '__main__':
    main()
