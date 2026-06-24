#!/usr/bin/env python3
"""
Badge audit script for LARQL Marimo notebooks.

Checks all notebooks in the notebooks/ directory for:
1. Presence of MoLab badges
2. Correct badge URLs (points to correct branch)
3. Correct badge alias (matches import cell export)

Usage:
    python scripts/badge-audit.py
"""

import re
import sys
from pathlib import Path

NOTEBOOKS_DIR = Path(__file__).resolve().parent.parent / "notebooks"
BRANCH = "feature/marimo-notebooks"
REPO_OWNER = "jeunjetta"
REPO_NAME = "larql"


def get_import_alias(notebook_path: Path) -> str:
    """Extract the variable name exported by the import cell."""
    content = notebook_path.read_text()
    
    # Find the import cell's return statement
    in_import_cell = False
    for line in content.split('\n'):
        if '@app.cell' in line:
            in_import_cell = False
        if in_import_cell and 'import marimo' in line:
            # Found import cell, now look for return
            continue
        if in_import_cell and 'return' in line:
            # Extract variable names from return statement
            return_line = line.split('return', 1)[1].strip()
            # Match mo or marimo
            match = re.search(r'\b(mo|marimo)\b', return_line)
            if match:
                return match.group(1)
        if 'import marimo' in line and '@app.cell' in content.split(line)[0].split('@app.cell')[-1]:
            in_import_cell = True
    
    # Fallback: search more broadly
    for line in content.split('\n'):
        if 'return' in line and ('mo,' in line or 'marimo,' in line or 'mo)' in line or 'marimo)' in line):
            if 'mo' in line and 'marimo' not in line:
                return 'mo'
            return 'marimo'
    
    return 'mo'  # Default assumption


def check_badge(notebook_path: Path) -> dict:
    """Check a single notebook for badge issues."""
    content = notebook_path.read_text()
    
    result = {
        'path': notebook_path.name,
        'has_badge': False,
        'badge_count': 0,
        'correct_url': False,
        'correct_alias': False,
        'issues': [],
    }
    
    # Check for MoLab badge
    badge_pattern = r'\[!\[Open in molab\]\(https://marimo\.io/molab-shield\.svg\)\]\(https://molab\.marimo\.io/github/([^/]+)/([^/]+)/blob/(.+?)/(notebooks/[^)]+)\)'
    matches = list(re.finditer(badge_pattern, content))
    
    result['badge_count'] = len(matches)
    result['has_badge'] = len(matches) > 0
    
    if len(matches) == 0:
        result['issues'].append('Missing MoLab badge')
        return result
    
    if len(matches) > 1:
        result['issues'].append(f'Multiple badges ({len(matches)}) - may cause script mode errors')
    
    # Check badge URL
    match = matches[0]
    owner, repo, branch, path = match.groups()
    
    if branch != BRANCH:
        result['issues'].append(f'Badge points to wrong branch: {branch} (expected: {BRANCH})')
    else:
        result['correct_url'] = True
    
    # Check badge alias matches import
    import_alias = get_import_alias(notebook_path)
    
    # Find the badge cell's parameters - look for the cell containing molab-shield
    lines = content.split('\n')
    badge_cell_start = None
    badge_cell_params = None
    
    for i, line in enumerate(lines):
        if 'molab-shield' in line:
            # Go back to find the def line for this cell
            for j in range(i, max(0, i-20), -1):
                if lines[j].strip().startswith('@app.cell'):
                    # Found the cell boundary, now find the def line
                    for k in range(j+1, i):
                        if lines[k].strip().startswith('def _('):
                            badge_cell_params = lines[k].strip()
                            break
                    break
            break
    
    if badge_cell_params:
        # Extract parameter names from def _(param1, param2):
        params_match = re.search(r'def _\(([^)]*)\)', badge_cell_params)
        if params_match:
            params_str = params_match.group(1)
            # Check if import_alias is in the parameters
            if import_alias in params_str.split(','):
                result['correct_alias'] = True
            else:
                result['issues'].append(f'Badge cell missing "{import_alias}" parameter (has: {params_str})')
        else:
            result['issues'].append('Could not parse badge cell parameters')
    else:
        result['issues'].append('Could not find badge cell')
    
    return result


def main():
    """Run the badge audit."""
    print(f"🔍 Auditing MoLab badges in {NOTEBOOKS_DIR}")
    print(f"   Expected branch: {BRANCH}")
    print()
    
    notebooks = sorted(NOTEBOOKS_DIR.glob('*.py'))
    # Exclude helper modules
    notebooks = [n for n in notebooks if not n.name.startswith('_')]
    
    results = []
    for nb in notebooks:
        result = check_badge(nb)
        results.append(result)
    
    # Report
    print("=" * 70)
    print(f"{'Notebook':<40} {'Badge':^6} {'URL':^6} {'Alias':^6} {'Issues'}")
    print("=" * 70)
    
    ok_count = 0
    for r in results:
        badge_icon = '✅' if r['has_badge'] else '❌'
        url_icon = '✅' if r['correct_url'] else '❌'
        alias_icon = '✅' if r['correct_alias'] else '❌'
        
        if r['has_badge'] and r['correct_url'] and r['correct_alias'] and not r['issues']:
            ok_count += 1
        
        issues_str = '; '.join(r['issues']) if r['issues'] else ''
        print(f"{r['path']:<40} {badge_icon:^6} {url_icon:^6} {alias_icon:^6} {issues_str}")
    
    print("=" * 70)
    print(f"\nSummary: {ok_count}/{len(results)} notebooks have correct badges")
    
    # Exit with error if any issues
    if ok_count < len(results):
        sys.exit(1)
    else:
        print("✅ All badges are correct!")
        sys.exit(0)


if __name__ == '__main__':
    main()
