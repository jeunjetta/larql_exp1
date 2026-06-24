#!/usr/bin/env python3
"""
Badge Audit Script for LARQL Marimo Notebooks

Checks all notebooks in the notebooks/ directory for:
1. Presence of MoLab badge
2. Correct branch in badge URL
3. Correct alias matching (badge cell uses same variable as import cell)

Usage:
    python scripts/badge-audit.py
    python scripts/badge-audit.py --fix  # Auto-fix missing badges
"""

import re
import sys
from pathlib import Path

NOTEBOOKS_DIR = Path(__file__).resolve().parent.parent / "notebooks"
REPO_OWNER = "jeunjetta"
REPO_NAME = "larql"
BRANCH = "feature/marimo-notebooks"
BADGE_PATTERN = r"\[!\[Open in molab\]\(https://marimo\.io/molab-shield\.svg\)\]\(https://molab\.marimo\.io/github/[^)]+\)"


def get_import_alias(content: str) -> str | None:
    """Extract the variable name exported by the import cell."""
    # Find the first @app.cell that contains "import marimo"
    cells = re.split(r"^@app\.cell\s*$", content, flags=re.MULTILINE)

    for cell in cells:
        if "import marimo" in cell:
            # Check if it returns something
            return_match = re.search(r"^\s*return\s+(.+?)\s*$", cell, flags=re.MULTILINE)
            if return_match:
                vars_str = return_match.group(1)
                # Handle "mo," or "marimo," or "mo, np" etc.
                first_var = vars_str.split(",")[0].strip().strip(",")
                return first_var
    return None


def check_badge_in_cell(cell_content: str) -> tuple[bool, str | None]:
    """
    Check if a cell contains a MoLab badge.
    Returns (has_badge, alias_used).
    """
    if "molab-shield" in cell_content or "molab.marimo.io" in cell_content:
        # Extract the alias used in the cell's function definition
        func_match = re.search(r"def\s+_\s*\(([^)]*)\)", cell_content)
        if func_match:
            alias = func_match.group(1).split(",")[0].strip()
            return True, alias
    return False, None


def audit_notebook(filepath: Path) -> dict:
    """Audit a single notebook for badge issues."""
    result = {
        "file": filepath.name,
        "has_badge": False,
        "badge_branch_correct": False,
        "alias_matches": False,
        "issues": [],
    }

    try:
        content = filepath.read_text()
    except Exception as e:
        result["issues"].append(f"Cannot read file: {e}")
        return result

    # Skip _vindex_helper.py (not a user-facing notebook)
    if filepath.name == "_vindex_helper.py":
        return result

    # Check for badge presence
    badge_matches = re.findall(BADGE_PATTERN, content)
    result["has_badge"] = len(badge_matches) > 0

    if not result["has_badge"]:
        result["issues"].append("Missing MoLab badge")
        return result

    # Check for duplicate badges
    if len(badge_matches) > 1:
        result["issues"].append(f"Duplicate badges ({len(badge_matches)})")

    # Check branch is correct
    expected_branch_pattern = f"github/{REPO_OWNER}/{REPO_NAME}/blob/{BRANCH}/"
    result["badge_branch_correct"] = expected_branch_pattern in content

    if not result["badge_branch_correct"]:
        result["issues"].append(f"Badge branch incorrect (expected {BRANCH})")

    # Check alias matches import cell
    import_alias = get_import_alias(content)
    if import_alias:
        # Find badge cells and check their alias
        cells = re.split(r"^@app\.cell\s*$", content, flags=re.MULTILINE)
        for cell in cells:
            has_badge, badge_alias = check_badge_in_cell(cell)
            if has_badge:
                result["alias_matches"] = (badge_alias == import_alias)
                if not result["alias_matches"]:
                    result["issues"].append(
                        f"Badge alias mismatch: import returns '{import_alias}', "
                        f"badge cell uses '{badge_alias}'"
                    )
                break
    else:
        result["issues"].append("Could not determine import alias")

    return result


def main():
    """Run badge audit on all notebooks."""
    print(f"🔍 Auditing MoLab badges in {NOTEBOOKS_DIR}")
    print(f"   Owner: {REPO_OWNER}/{REPO_NAME}")
    print(f"   Branch: {BRANCH}")
    print()

    notebooks = sorted(NOTEBOOKS_DIR.glob("*.py"))
    notebooks = [n for n in notebooks if n.name != "_vindex_helper.py"]

    if not notebooks:
        print("No notebooks found.")
        sys.exit(0)

    results = []
    for nb in notebooks:
        result = audit_notebook(nb)
        results.append(result)

    # Summary
    total = len(results)
    has_badge = sum(1 for r in results if r["has_badge"])
    branch_correct = sum(1 for r in results if r["badge_branch_correct"])
    alias_correct = sum(1 for r in results if r["alias_matches"])

    print(f"📊 Summary: {total} notebooks")
    print(f"   ✅ Has badge: {has_badge}/{total}")
    print(f"   ✅ Branch correct: {branch_correct}/{total}")
    print(f"   ✅ Alias matches: {alias_correct}/{total}")
    print()

    # Detailed issues
    issues_found = False
    for r in results:
        if r["issues"]:
            issues_found = True
            print(f"❌ {r['file']}:")
            for issue in r["issues"]:
                print(f"      - {issue}")
            print()

    if not issues_found:
        print("✅ All badges are correct!")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
