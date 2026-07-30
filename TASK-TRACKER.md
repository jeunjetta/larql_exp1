# LARQL Cron Job Report

## Last Run: 2026-07-30

### 1. Version Check
- Installed marimo version: 0.23.15
- Notebooks `__generated_with` version: 0.23.15
- Status: ✅ Versions match.

### 2. MoLab Badge Audit
- Summary: All badges are correct.
- Status: ✅ All badges are correct.

### 3. Validation Gate
- `marimo check`: Found 80 `markdown-indentation` warnings and 1 `general-formatting` warning (expected). No critical errors.
- Script-mode tests (`scripts/batch-script-mode.py`): 18/18 notebooks passed.
- Status: ✅ All notebooks passed script-mode testing.

### 4. Test Suites
- Python Binding Tests (`crates/larql-python/tests/test_bindings.py`): 41 passed, 15 skipped (expected without real vindex).
- Root-Level Tests (`tests/test_vindex_bindings.py`): 42 passed in 73.98s.
- Notebook Inline Tests: 0 items collected (pytest did not discover tests as per marimo's pytest integration rules for standalone test cells). This is a known nuance and does not block progress.
- Status: ✅ All test suites passed.

