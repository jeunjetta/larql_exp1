#!/usr/bin/env python3
"""
Batch Script-Mode Tester for LARQL Marimo Notebooks

Runs all notebooks in script mode and reports pass/fail.
Tests that notebooks can execute without interactive browser.

Usage:
    python scripts/batch-script-mode.py
    python scripts/batch-script-mode.py --notebooks 00_what_is_larql.py
"""

import subprocess
import sys
import time
from pathlib import Path

NOTEBOOKS_DIR = Path(__file__).resolve().parent.parent / "notebooks"
TIMEOUT = 60  # seconds per notebook


def run_script_mode(filepath: Path) -> dict:
    """Run a single notebook in script mode. Returns result dict."""
    result = {
        "file": filepath.name,
        "passed": False,
        "exit_code": None,
        "stdout": "",
        "stderr": "",
        "duration": 0.0,
    }

    # Use `uv run` to handle PEP 723 notebooks correctly
    # For non-PEP 723, it uses the project environment
    cmd = ["uv", "run", str(filepath)]

    start = time.time()
    try:
        proc = subprocess.run(
            cmd,
            cwd=filepath.parent,
            capture_output=True,
            text=True,
            timeout=TIMEOUT,
        )
        result["exit_code"] = proc.returncode
        result["stdout"] = proc.stdout[-500:] if proc.stdout else ""  # Last 500 chars
        result["stderr"] = proc.stderr[-500:] if proc.stderr else ""
        result["passed"] = proc.returncode == 0
    except subprocess.TimeoutExpired:
        result["stderr"] = f"TIMEOUT after {TIMEOUT}s"
    except Exception as e:
        result["stderr"] = str(e)
    finally:
        result["duration"] = round(time.time() - start, 2)

    return result


def main():
    """Run all notebooks in script mode."""
    print(f"🧪 Batch Script-Mode Testing")
    print(f"   Directory: {NOTEBOOKS_DIR}")
    print(f"   Timeout: {TIMEOUT}s per notebook")
    print()

    # Find all notebooks (exclude _vindex_helper.py)
    notebooks = sorted(NOTEBOOKS_DIR.glob("*.py"))
    notebooks = [n for n in notebooks if n.name != "_vindex_helper.py"]

    if not notebooks:
        print("No notebooks found.")
        sys.exit(0)

    print(f"Found {len(notebooks)} notebooks to test:")
    for nb in notebooks:
        print(f"   - {nb.name}")
    print()

    # Run tests
    results = []
    for nb in notebooks:
        print(f"🏃 Running {nb.name}...")
        result = run_script_mode(nb)
        results.append(result)

        status = "✅ PASSED" if result["passed"] else "❌ FAILED"
        print(f"   {status} ({result['duration']}s)")
        if not result["passed"]:
            if result["stderr"]:
                print(f"   Error: {result['stderr'][:200]}")
        print()

    # Summary
    passed = sum(1 for r in results if r["passed"])
    failed = len(results) - passed

    print("=" * 60)
    print(f"📊 Summary: {passed}/{len(results)} passed, {failed} failed")
    print("=" * 60)

    if failed > 0:
        print("\n❌ Failed notebooks:")
        for r in results:
            if not r["passed"]:
                print(f"   - {r['file']}: {r['stderr'][:100]}")
        sys.exit(1)
    else:
        print("\n✅ All notebooks passed script-mode testing!")
        sys.exit(0)


if __name__ == "__main__":
    main()
