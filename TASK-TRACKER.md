# LARQL Notebook Task Tracker

**Goal**: Create educational Marimo notebooks that teach LARQL concepts
**Target**: 18 notebooks (17 educational + setup.py + _vindex_helper.py)
**Branch**: `feature/marimo-notebooks`

## Priority Items

### 1. Enhance Existing Notebooks (High Priority) ✅ COMPLETE
- [x] `00_what_is_larql.py` - Add interactive examples, LLM syntax demos ✅ (added mock DESCRIBE demo 2026-06-25)
- [x] `01_extract_index.py` - Add step-by-step extraction visualization ✅ (added interactive step-by-step simulator 2026-06-25)
- [x] `02_graph_structure.py` - Add interactive graph exploration (filters now connected to data, script mode fixed 2026-06-25)
- [x] `describe_explorer.py` - Add "Try it yourself" sections ✅ (enhanced with structured exercises 2026-06-26)
- [x] `walk_knowledge.py` - Add visualization of walk paths (Plotly line chart added 2026-06-25)
- [x] `inference_predict.py` - Add side-by-side comparison (mock vs real) ✅ (added Plotly visualization + exercises 2026-06-25)
- [x] `compile_knowledge.py` - Add before/after compile visualization ✅ (added mock demo table 2026-06-26)

### 2. Create Missing Core Concept Notebooks (High Priority) ✅ COMPLETE
- [x] `03_lql_syntax.py` - LQL language tutorial (DESCRIBE, WALK, SELECT syntax) ✅ (created + script-mode verified 2026-06-25)
- [x] `04_mutation_basics.py` - INSERT/DELETE/UPDATE tutorial ✅ (created + script-mode verified 2026-06-25)
- [x] `05_patches.py` - Patch system tutorial (BEGIN PATCH, SAVE PATCH) ✅ (created + script-mode verified 2026-06-25)
- [x] `06_vindex_format.py` - Vindex file format deep dive ✅ (created 2026-06-25)
- [x] `07_extraction_levels.py` - Browse vs Inference vs All levels ✅ (created 2026-06-25)

### 3. Create Interactive Visualization Notebooks (Medium Priority) ✅ COMPLETE
- [x] `visualize_gate_knn.py` - Interactive gate KNN exploration ✅ (created 2026-06-26)
- [x] `visualize_walk_path.py` - Animated walk path visualization ✅ (created 2026-06-26)
- [x] `visualize_patch_diff.py` - Visual diff of patched vindex ✅ (created 2026-06-26)

### 4. Add MoLab Badges (Medium Priority) ✅ COMPLETE
- [x] All 18 notebooks now have MoLab badges pointing to `jeunjetta/larql/blob/feature/marimo-notebooks/`
- [x] `scripts/badge-audit.py` created for automated auditing (2026-06-25)

### 6. Expand Notebook Suite (Medium Priority) ✅ COMPLETE
- [x] `08_multi_modal.py` - Multi-modal LQL tutorial (image + text alignment) ✅ (created 2026-06-27)
- [x] `09_deployment.py` - Deployment architecture (serve, slice, WebSocket, MoE sharding) ✅ (created 2026-06-28)

### 5. Create Batch Scripts (Low Priority) ✅ COMPLETE
- [x] `scripts/batch-script-mode.py` - Automated script-mode testing ✅ (created 2026-06-25)
- [x] `scripts/badge-audit.py` - Automated MoLab badge auditing ✅ (created 2026-06-25)

## Current Notebook Status (18/18 COMPLETE)

| Notebook | Educational? | Interactive? | MoLab Badge? | Script Mode? |
|----------|-------------|-------------|--------------|--------------|
| `00_what_is_larql.py` | ✅ Enhanced | ✅ Yes (DESCRIBE demo) | ✅ Yes | ✅ Verified |
| `01_extract_index.py` | ✅ Enhanced | ✅ Yes (step-by-step simulator) | ✅ Yes | ✅ Verified |
| `02_graph_structure.py` | ✅ Enhanced | ✅ Yes (filters connected) | ✅ Yes | ✅ Verified |
| `03_lql_syntax.py` | ✅ Yes | ✅ Yes (dropdown) | ✅ Yes | ✅ Verified |
| `04_mutation_basics.py` | ✅ Yes | ✅ Yes (dropdown) | ✅ Yes | ✅ Verified |
| `05_patches.py` | ✅ Yes | ✅ Yes (dropdown) | ✅ Yes | ✅ Verified |
| `06_vindex_format.py` | ✅ Yes | ✅ Yes (layer selector) | ✅ Yes | ✅ Verified |
| `07_extraction_levels.py` | ✅ Yes | ✅ Yes (dropdown) | ✅ Yes | ✅ Verified |
| `08_multi_modal.py` | ✅ Yes | ✅ Yes (similarity heatmap) | ✅ Yes | ✅ Verified |
| `09_deployment.py` | ✅ Yes | ✅ Yes (code examples) | ✅ Yes | ✅ Verified |
| `describe_explorer.py` | ✅ Yes | ✅ Yes (exercises) | ✅ Yes | ✅ Verified |
| `walk_knowledge.py` | ✅ Yes | ✅ Yes (Plotly chart) | ✅ Yes | ✅ Verified |
| `inference_predict.py` | ✅ Yes | ✅ Yes (Plotly bar chart + exercises) | ✅ Yes | ✅ Verified |
| `compile_knowledge.py` | ✅ Yes | ✅ Yes (demo table) | ✅ Yes | ✅ Verified |
| `visualize_gate_knn.py` | ✅ Yes | ✅ Yes (bar chart + histogram) | ✅ Yes | ✅ Verified |
| `visualize_walk_path.py` | ✅ Yes | ✅ Yes (animated scatter) | ✅ Yes | ✅ Verified |
| `visualize_patch_diff.py` | ✅ Yes | ✅ Yes (table + histogram) | ✅ Yes | ✅ Verified |
| `setup.py` | N/A | N/A | No | ✅ Yes |
| `_vindex_helper.py` | N/A | N/A | No | N/A (helper module) |

## Educational Notebook Checklist

Each educational notebook should have:
- [x] Title with italicized one-liner description
- [x] Interactive UI elements (sliders, dropdowns, text inputs)
- [x] Mock data for script mode (fast CI testing)
- [x] "Try it yourself" guidance sections
- [x] LLM syntax examples (code blocks showing LQL syntax)
- [x] Visualizations (plots, graphs, tables)
- [x] MoLab badge at bottom of README

## Cron Job Verification (Last Run: 2026-06-29)

- [x] **Version check**: marimo 0.23.9 matches `__generated_with` in all 18 notebooks
- [x] **MoLab badge audit**: 18/18 notebooks have badges, all point to correct branch, all alias matches
- [x] **Validation gate**: `marimo check` passed (0 critical/error, 81 non-critical warnings)
- [x] **Script-mode tests**: 18/18 notebooks passed (0 failures)
- [x] **Python binding tests**: 46 passed, 5 failed (asserting specific values - should check types/structure per skill), 5 skipped
- [x] **Root-level tests**: 42 passed (vindex now available via symlink)
- [x] **Git status**: clean, 0 ahead/0 behind `origin/feature/marimo-notebooks`

## Next Steps

1. **Fix Python binding tests** - 5 tests fail due to asserting specific values (e.g., `result[0][0] == "Paris"`). Per `larql-build-and-test` skill: "Do NOT assert specific values — probe data varies across vindex versions and rebuilds. DO check types and structure."
2. **Keep documentation updated** - TASK-TRACKER.md now reflects 18 notebooks + vindex availability (updated 2026-06-29)
3. **Monitor cron job execution** - All gates passing, test coverage improved (42/42 root-level tests now pass)

## References
- Skill: `larql-build-and-test` (build/test instructions)
- Skill: `marimo-notebook` (notebook authoring patterns)
- AGENTS.md (project architecture)
- README.md (LQL syntax reference)
