# LARQL Notebook Task Tracker

**Goal**: Create educational Marimo notebooks that teach LARQL concepts
**Target**: 43 notebooks total (currently 8 exist)
**Branch**: `feature/marimo-notebooks`

## Priority Items

### 1. Enhance Existing Notebooks (High Priority)
Current notebooks exist but need to be more educational:
- [x] `00_what_is_larql.py` - Add interactive examples, LLM syntax demos ✅ (added mock DESCRIBE demo 2026-06-25)
- [ ] `01_extract_index.py` - Add step-by-step extraction visualization
- [ ] `02_graph_structure.py` - Add interactive graph exploration
- [ ] `describe_explorer.py` - Add "Try it yourself" sections
- [ ] `walk_knowledge.py` - Add visualization of walk paths
- [ ] `inference_predict.py` - Add side-by-side comparison (mock vs real)
- [ ] `compile_knowledge.py` - Add before/after compile visualization

### 2. Create Missing Core Concept Notebooks (High Priority)
- [x] `03_lql_syntax.py` - LQL language tutorial (DESCRIBE, WALK, SELECT syntax) ✅ (created + script-mode verified 2026-06-25)
- [x] `04_mutation_basics.py` - INSERT/DELETE/UPDATE tutorial ✅ (created + script-mode verified 2026-06-25)
- [x] `05_patches.py` - Patch system tutorial (BEGIN PATCH, SAVE PATCH) ✅ (created + script-mode verified 2026-06-25)
- [ ] `06_vindex_format.py` - Vindex file format deep dive
- [ ] `07_extraction_levels.py` - Browse vs Inference vs All levels

### 3. Create Interactive Visualization Notebooks (Medium Priority)
- [ ] `visualize_gate_knn.py` - Interactive gate KNN exploration
- [ ] `visualize_walk_path.py` - Animated walk path visualization
- [ ] `visualize_patch_diff.py` - Visual diff of patched vindex

### 4. Add MoLab Badges (Medium Priority)
Only 5 of 43 notebooks have MoLab badges. Need to add to remaining 38.
- [ ] Create `scripts/badge-audit.py` for automated auditing
- [ ] Batch-add badges to all notebooks

### 5. Create Batch Scripts (Low Priority)
- [ ] `scripts/batch-script-mode.py` - Automated script-mode testing
- [ ] `scripts/badge-audit.py` - Automated MoLab badge auditing

## Current Notebook Status

| Notebook | Educational? | Interactive? | MoLab Badge? | Script Mode? |
|----------|-------------|-------------|--------------|--------------|
| `00_what_is_larql.py` | ✅ Enhanced | ✅ Yes (DESCRIBE demo) | ✅ Yes | ✅ Verified |
| `01_extract_index.py` | Partial | No | No | Unknown |
| `02_graph_structure.py` | Partial | No | No | Unknown |
| `03_lql_syntax.py` | ✅ Yes | ✅ Yes (dropdown) | ✅ Yes | ✅ Verified |
| `04_mutation_basics.py` | ✅ Yes | ✅ Yes (dropdown) | ✅ Yes | ✅ Verified |
| `05_patches.py` | ✅ Yes | ✅ Yes (dropdown) | ✅ Yes | ✅ Verified |
| `describe_explorer.py` | Yes | Partial | Yes | Yes |
| `walk_knowledge.py` | Yes | Partial | Yes | Unknown |
| `inference_predict.py` | Yes | Partial | Yes | Unknown |
| `compile_knowledge.py` | Yes | Partial | Yes | Unknown |
| `setup.py` | N/A | N/A | No | Yes |

## Educational Notebook Checklist

Each educational notebook should have:
- [ ] Title with italicized one-liner description
- [ ] Interactive UI elements (sliders, dropdowns, text inputs)
- [ ] Mock data for script mode (fast CI testing)
- [ ] "Try it yourself" guidance sections
- [ ] LLM syntax examples (code blocks showing LQL syntax)
- [ ] Visualizations (plots, graphs, tables)
- [ ] MoLab badge at bottom of README

## References
- Skill: `larql-build-and-test` (build/test instructions)
- Skill: `marimo-notebook` (notebook authoring patterns)
- AGENTS.md (project architecture)
- README.md (LQL syntax reference)
