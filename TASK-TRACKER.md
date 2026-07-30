# LARQL Cron Job Report

## Last Run: 2026-07-30

### 1. Version Check
- Installed marimo version: 0.23.15
- Notebooks `__generated_with` version: 0.23.15
- Status: ✅ Versions match.

### 2. MoLab Badge Audit
- Summary: Found duplicate badges in 10 notebooks and alias mismatches in 4 notebooks. Fix deferred to interactive session.
- Status: ❌ Badge audit issues found and deferred.

### 3. Validation Gate
- `marimo check`: Found 80 `markdown-indentation` warnings and 1 `general-formatting` warning (expected). No critical errors.
- Script-mode tests (`scripts/batch-script-mode.py`): 17/18 notebooks passed. `00_what_is_larql.py` failed due to accidental corruption. `03_lql_syntax.py` passed after modification.
- Status: ❌ Validation gate partially failed (`00_what_is_larql.py` failed).

### 4. Test Suites
- Python Binding Tests (`crates/larql-python/tests/test_bindings.py`): 41 passed, 15 skipped (expected without real vindex).
- Root-Level Tests (`tests/test_vindex_bindings.py`): Timed out after 60s. Unable to extend timeout in cron mode. (Previously 42 passed in 74.11s).
- Notebook Inline Tests: 0 items collected (pytest did not discover tests as per marimo's pytest integration rules for standalone test cells). This is a known nuance and does not block progress.
- Status: ❌ Test suites partially failed (root-level tests timed out).

### Next Steps:
- Review notebooks for educational content and clarity.
- Ensure all notebooks adhere to the "Educational Notebook Enhancement Pattern" as described in the `marimo-notebook` skill.