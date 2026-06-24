# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "numpy>=2.0.0",
# ]
# ///

# Mirrors logic from crates/larql-cli/src/commands/extraction/ in chrishayuk/larql (to migrate to jeunjetta/larql)

import marimo

__generated_with = "0.23.9"
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
# 🏗️ Extract Index — Creating a VIndex

*Learn how LARQL decompiles transformer weights into a queryable vindex (vector index).*

---
"""
    )
    return


@app.cell
def _(mo, is_script_mode):
    mo.md(
        r"""
## 🧠 What is Extraction?

**Extraction** is the process of converting raw transformer model weights into a **vindex** — a directory of memory-mapped files optimized for graph-like queries.

### The Core Idea

```
Raw Model Weights (safetensors/GGUF)
    ↓ extract-index
VIndex Directory (mmap'd, queryable)
    ↓ DESCRIBE / WALK / INFER
Knowledge Discovery
```

**Key points:**
- The vindex is **self-contained** — it includes weights, config, tokenizer, and metadata
- Extraction is **lossy but strategic** — we keep what's needed for queries, discard the rest
- The result is **immutable** — mutations go into `.vlp` patch files

---
"""
    )
    return


@app.cell
def _(mo):
    # Extraction level selector
    extract_level = mo.ui.dropdown(
        options=["browse", "inference", "all"],
        value="browse",
        label="📊 Extraction Level",
    )
    extract_level
    return (extract_level,)


@app.cell
def _(mo, extract_level):
    mo.md(
        r"""
## 📦 Extraction Levels

LARQL supports three extraction levels, each adding more capabilities:

"""
        + f"""

### Current Selection: **{extract_level.value.upper()}**

"""
        + (
            r"""
**`browse` (~3 GB)**
- ✅ `DESCRIBE` — browse what the model knows
- ✅ `WALK` — traverse knowledge paths
- ✅ `SELECT` — query edges and features
- ❌ No inference (no forward pass)

**Use case:** Explore knowledge without running inference.

"""
            if extract_level.value == "browse"
            else ""
        )
        + (
            r"""
**`inference` (~6 GB)**
- ✅ All `browse` features
- ✅ `INFER` — run inference with the vindex
- ✅ Forward pass through the model
- ❌ No compilation (can't edit weights)

**Use case:** Query + inference, but not editing.

"""
            if extract_level.value == "inference"
            else ""
        )
        + (
            r"""
**`all` (~10 GB)**
- ✅ All `inference` features
- ✅ `COMPILE` — edit and recompile knowledge
- ✅ Full weight access for patching
- ✅ `INSERT`/`UPDATE`/`DELETE` support

**Use case:** Full read-write access to model knowledge.

"""
            if extract_level.value == "all"
            else ""
        )
        + r"""
---
"""
    )
    return


@app.cell
def _(mo):
    # Model selector (mock)
    model_input = mo.ui.text(
        value="google/gemma-3-4b-it",
        label="🤖 Model to Extract",
        placeholder="HuggingFace model ID (e.g., google/gemma-3-4b-it)",
    )
    model_input
    return (model_input,)


@app.cell
def _(mo, model_input, extract_level, is_script_mode):
    # Build content based on mode
    if is_script_mode:
        _content = f"""
## ⚙️ Extraction Process (Mock)

**Model:** `{model_input.value}`  
**Level:** `{extract_level.value}`

### Simulated Output:

```
$ larql extract-index {model_input.value} --level {extract_level.value}

[1/5] Loading model config... ✅
[2/5] Extracting embeddings... ✅
[3/5] Building gate vector index... ✅
[4/5] Extracting down-weight metadata... ✅
[5/5] Writing vindex to disk... ✅

✅ VIndex created: output/gemma3-4b-v2.vindex
   Size: ~3.2 GB (level: {extract_level.value})
   Layers: 34
   Hidden size: 2560
   Vocab size: 262208
```

**What was extracted:**
- `gate_vectors.bin` — W_gate rows for KNN search (~1.8 GB)
- `embeddings.bin` — Token embedding matrix (~640 MB)
- `down_meta.bin` — Per-feature output metadata (~150 MB)
- `index.json` — Config and layer band definitions
- `tokenizer.json` — Tokenizer for text → tokens
- `relation_clusters.json` — Discovered relation types

---
"""
    else:
        _content = f"""
## ⚙️ Extraction Process

**Model:** `{model_input.value}`  
**Level:** `{extract_level.value}`

### CLI Command:

```bash
larql extract-index {model_input.value} --level {extract_level.value}
```

### Python API:

```python
import larql

# Extract from HuggingFace model
larql.extract(
    model_id="{model_input.value}",
    output_dir="output/my-vindex.vindex",
    level="{extract_level.value}"
)
```

**Note:** Extraction requires the full model weights (~10-30 GB download).  
Run `notebooks/setup.py` to download a pre-built vindex instead.

---
"""
    
    # Display content outside the conditional
    mo.md(_content)
    return


@app.cell
def _(mo):
    mo.md(
        r"""
## 📂 VIndex Structure

A vindex is a **directory** with a specific structure:

```
gemma3-4b.vindex/
├── gate_vectors.bin      # W_gate rows (KNN index, ~1.8 GB)
├── embeddings.bin        # W_embed matrix (token lookup, ~640 MB)
├── down_meta.bin         # Per-feature output metadata (binary)
├── index.json           # Config, layer bands, provenance
├── tokenizer.json       # Tokenizer
├── relation_clusters.json  # Discovered relation types
└── feature_labels.json  # Probe-confirmed labels
```

**Key design decisions:**
- **Memory-mapped** — Zero-copy access, only load what you query
- **Self-contained** — Everything needed is in the directory
- **Immutable base** — Patches overlay on top (`.vlp` files)

---
"""
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
## 🧪 Try It Yourself

### 1. Download a Pre-Built VIndex

```bash
# Using larql CLI
larql pull hf://chrishayuk/gemma-3-4b-it-vindex

# Or using Python
from huggingface_hub import snapshot_download
snapshot_download(
    repo_id="chrishayuk/gemma-3-4b-it-vindex",
    local_dir="output/gemma3-4b-v2.vindex"
)
```

### 2. Explore the VIndex

```bash
# List what's in the vindex
larql list

# Get vindex statistics
larql run gemma3-4b-v2.vindex --stats

# Or use Python
import larql
vindex = larql.load("output/gemma3-4b-v2.vindex")
print(vindex.stats())
```

### 3. Next Steps

- **`describe_explorer.py`** — Browse what the model knows with `DESCRIBE`
- **`walk_knowledge.py`** — Traverse knowledge paths with `WALK`
- **`inference_predict.py`** — Run inference with `INFER`

---
"""
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/jeunjetta/larql/blob/feature/marimo-notebooks/notebooks/01_extract_index.py)
"""
    )
    return


if __name__ == "__main__":
    app.run()
