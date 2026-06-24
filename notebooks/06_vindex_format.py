# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "numpy>=2.0.0",
# ]
# ///

# Mirrors logic from crates/larql-vindex/src/lib.rs in chrishayuk/larql (to migrate to jeunjetta/larql)

import marimo

__generated_with = "0.23.10"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    from pathlib import Path
    return mo, np, Path


@app.cell
def _(mo):
    is_script_mode = mo.app_meta().mode == "script"
    return (is_script_mode,)


@app.cell
def _(mo):
    mo.md(
        r"""
# 📁 Vindex Format Deep Dive

*Learn about the vindex file structure — how LARQL stores model knowledge as memory-mapped files.*
"""
    )
    return


@app.cell
def _(mo, Path):
    # Check if vindex exists for real examples
    vindex_path = None
    for candidate in [Path.cwd() / "output" / "gemma3-4b-v2.vindex",
                     Path.home() / ".cache" / "larql" / "local" / "gemma3-4b-v2.vindex"]:
        if candidate.is_dir():
            vindex_path = candidate
            break

    # Build message string (fixes branch-expression error)
    _msg = ""
    if vindex_path:
        _msg = f"✅ Found vindex at: `{vindex_path}`"
    else:
        _msg = "⚠️ No vindex found. Using mock data for demonstration."

    mo.md(_msg)
    return vindex_path


@app.cell
def _(mo):
    mo.md(
        r"""
## 📂 Vindex Directory Structure

A vindex is a **directory** (not a single file) containing memory-mapped files:

```
gemma3-4b-v2.vindex/
├── config.json              # Model config and metadata
├── gate_vectors.bin        # Gate vectors (KNN index)
├── down_weights.bin        # Down projection weights
├── embeddings.bin         # Token embeddings
├── layer_bands.json       # Layer grouping metadata
├── down_meta.bin          # Feature metadata (top tokens, scores)
└── ...
```

**Key insight:** All large tensors are stored as `.bin` files that are **memory-mapped** (mmap'd) for zero-copy access. This means:
- The files can be larger than RAM
- Access is lazy (only loads what's needed)
- Multiple processes can share the same memory

---
"""
    )
    return


@app.cell
def _(mo):
    # Interactive layer selector for exploration
    layer_selector = mo.ui.dropdown(
        options=["Layer 0-9 (Early)", "Layer 10-19 (Middle)", "Layer 20-33 (Late)"],
        value="Layer 20-33 (Late)",
        label="📊 Select Layer Band"
    )
    layer_selector
    return (layer_selector,)


@app.cell
def _(mo, layer_selector, is_script_mode):
    # Mock vindex file sizes based on layer selection
    if is_script_mode:
        # Use mock data - no file system access needed
        selected_band = layer_selector.value
        if "Early" in selected_band:
            files_info = [
                {"name": "gate_vectors.bin", "size_mb": 800, "description": "Early layer gate vectors"},
                {"name": "down_weights.bin", "size_mb": 1200, "description": "Early layer down weights"},
            ]
        elif "Middle" in selected_band:
            files_info = [
                {"name": "gate_vectors.bin", "size_mb": 850, "description": "Middle layer gate vectors"},
                {"name": "down_weights.bin", "size_mb": 1250, "description": "Middle layer down weights"},
            ]
        else:  # Late
            files_info = [
                {"name": "gate_vectors.bin", "size_mb": 900, "description": "Late layer gate vectors"},
                {"name": "down_weights.bin", "size_mb": 1300, "description": "Late layer down weights"},
            ]
    else:
        # Real vindex - would read actual file sizes
        files_info = [
            {"name": "gate_vectors.bin", "size_mb": 1800, "description": "All layer gate vectors"},
            {"name": "down_weights.bin", "size_mb": 2400, "description": "All layer down weights"},
        ]

    mo.md(
        f"""
## 📊 File Sizes for {layer_selector.value}

Based on the selected layer band:
"""
    )

    for file_info in files_info:
        mo.md(
            f"- **{file_info['name']}**: ~{file_info['size_mb']} MB — {file_info['description']}\n"
        )

    mo.md(
        r"""
**Total vindex size:** ~3-6 GB depending on extraction level (browse/inference/all)

---
"""
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
## 🔬 Binary Format Details

### Key Files Explained

#### `gate_vectors.bin`
- **Format:** f16 (float16) tensor
- **Shape:** `[num_layers, num_features, hidden_size]`
- **Purpose:** KNN index for `DESCRIBE` and `WALK`
- **Access pattern:** mmap'd, queried by layer + feature index

#### `down_weights.bin`
- **Format:** f16 (float16) tensor
- **Shape:** `[num_layers, num_features, hidden_size]`
- **Purpose:** FFN down-projection weights
- **Access pattern:** mmap'd, patched via `COMPILE`

#### `down_meta.bin`
- **Format:** Custom binary (header + records)
- **Structure:**
  ```
  Header (16 bytes):
    - magic: u32 = 0x444D4554 ("DMET")
    - version: u32 = 1
    - num_layers: u32
    - top_k_count: u32
  
  Per layer:
    - num_features: u32
    - Then num_features × records:
        - top_token_id: u32
        - c_score: f32
        - top_k_count × (token_id: u32, logit: f32)
  ```
- **Purpose:** Feature metadata (top tokens, scores for `DESCRIBE`)

---

"""
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
## 🧠 Memory Mapping (mmap)

**What is mmap?**
Memory mapping maps a file directly into virtual memory. The OS loads pages on-demand.

**Why vindex uses mmap:**
1. **Lazy loading:** Only access the parts you need
2. **Zero-copy:** No explicit read into RAM buffer
3. **Shared memory:** Multiple processes can share the same mapping
4. **Large files:** Can mmap files larger than RAM

**LARQL code pattern:**
```rust
// In larql-vindex crate
let file = File::open("gate_vectors.bin")?;
let mmap = unsafe { Mmap::map(&file)? };
let tensor = Tensor::from_mmap(&mmap, shape)?;
```

**Python binding access:**
```python
import larql
vindex = larql.load("model.vindex")
emb = vindex.embed("France")  # Reads from mmap'd embeddings.bin
```

---
"""
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
## 📖 LQL Syntax for Vindex Operations

```sql
-- Load a vindex (Python binding)
vindex = larql.load("path/to/model.vindex")

-- Get vindex metadata
DESCRIBE STATS;

-- Output:
-- Model: google/gemma-3-4b-it
-- Layers: 34
-- Hidden size: 2560
-- Vocab size: 262208

-- Load specific extraction level
EXTRACT BROWSE;  -- ~3 GB, DESCRIBE/WALK/SELECT only
EXTRACT INFERENCE;  -- ~6 GB, adds INFER
EXTRACT ALL;  -- ~10 GB, adds COMPILE
```

---
"""
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
## 🎯 Try It Yourself

1. **Explore the structure:** If you have a vindex, run `ls -lh output/*.vindex/`
2. **Check file sizes:** Compare `gate_vectors.bin` vs `down_weights.bin`
3. **Understand mmap:** Run `python -c "import larql; v = larql.load(...); print(v.stats())"`
4. **Inspect metadata:** Open `config.json` in a text editor

**Next:** Try `07_extraction_levels.py` to learn about extraction levels.

---
"""
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/jeunjetta/larql/blob/feature/marimo-notebooks/notebooks/06_vindex_format.py)
"""
    )
    return

if __name__ == "__main__":
    app.run()
