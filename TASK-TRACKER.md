# LARQL Notebook Task Tracker

**Goal**: Create educational Marimo notebooks that teach LARQL concepts
**Target**: 14 notebooks (all core + visualization notebooks created)
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
- [x] All 14 notebooks now have MoLab badges pointing to `jeunjetta/larql/blob/feature/marimo-notebooks/`
- [x] `scripts/badge-audit.py` created for automated auditing (2026-06-25)

### 6. Expand Notebook Suite (Medium Priority) 🚧 IN PROGRESS
- [x] `08_multi_modal.py` - Multi-modal LQL tutorial (image + text alignment) ✅ (created 2026-06-27)

### 5. Create Batch Scripts (Low Priority) ✅ COMPLETE
- [x] `scripts/batch-script-mode.py` - Automated script-mode testing ✅ (created 2026-06-25)
- [x] `scripts/badge-audit.py` - Automated MoLab badge auditing ✅ (created 2026-06-25)

## Current Notebook Status (14/14 COMPLETE)

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
| `describe_explorer.py` | ✅ Yes | ✅ Yes (exercises) | ✅ Yes | ✅ Verified |
| `walk_knowledge.py` | ✅ Yes | ✅ Yes (Plotly chart) | ✅ Yes | ✅ Verified |
| `inference_predict.py` | ✅ Yes | ✅ Yes (Plotly bar chart + exercises) | ✅ Yes | ✅ Verified |
| `compile_knowledge.py` | ✅ Yes | ✅ Yes (demo table) | ✅ Yes | ✅ Verified |
| `visualize_gate_knn.py` | ✅ Yes | ✅ Yes (bar chart + histogram) | ✅ Yes | ✅ Verified |
| `visualize_walk_path.py` | ✅ Yes | ✅ Yes (animated scatter) | ✅ Yes | ✅ Verified |
| `visualize_patch_diff.py` | ✅ Yes | ✅ Yes (table + histogram) | ✅ Yes | ✅ Verified |
| `08_multi_modal.py` | ✅ Yes | ✅ Yes (similarity heatmap) | ✅ Yes | ✅ Verified |
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

## Next Steps

1. **Run batch script-mode tests** - Use `scripts/batch-script-mode.py` to verify all notebooks
2. **Run badge audit** - Use `scripts/badge-audit.py` to verify all badges point to correct branch
3. **Expand notebook suite** - Consider adding more advanced topics (multi-modal, attention visualization, etc.)

## References
- Skill: `larql-build-and-test` (build/test instructions)
- Skill: `marimo-notebook` (notebook authoring patterns)
- AGENTS.md (project architecture)
- README.md (LQL syntax reference)
