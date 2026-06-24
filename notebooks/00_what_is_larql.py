# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "numpy>=2.0.0",
# ]
# ///

# Mirrors logic from notebooks/00_what_is_larql.py in chrishayuk/larql (to migrate to jeunjetta/larql)

import marimo

__generated_with = "0.23.9"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    return mo, np


@app.cell
def _(mo):
    is_script_mode = mo.app_meta().mode == "script"
    return (is_script_mode,)


@app.cell
def _(mo, is_script_mode):
    mo.md(
        r"""
# 🕸️ What is LARQL?

*An interactive introduction to LARQL (Lazarus Query Language) — where neural network weights become a queryable graph database.*

---
"""
    )
    return


@app.cell
def _(mo, is_script_mode):
    mo.md(
        r"""
## 🧠 The Core Idea

**LARQL decompiles transformer model weights into a _vindex_ (vector index) — a directory of memory-mapped files that can be queried like a graph database.**

Key insight: **The model IS the database.** Instead of fine-tuning to add knowledge, you:
1. `DESCRIBE` — browse what the model already knows
2. `WALK` — traverse knowledge paths through the residual stream  
3. `INFER` — run inference with the vindex
4. `INSERT`/`COMPILE` — patch knowledge directly into weight matrices

---
"""
    )
    return


@app.cell
def _(mo, is_script_mode):
    mo.md(
        r"""
## 📂 VIndex Format

A vindex is a directory containing model weights reorganised for queryability:

```
gemma3-4b.vindex/
  gate_vectors.bin      # W_gate rows (KNN index, ~3.3 GB)
  embeddings.bin        # W_embed matrix (token lookup, ~2.5 GB)
  down_meta.bin         # Per-feature output metadata (binary)
  index.json           # Config, layer bands, provenance
  tokenizer.json       # Tokenizer
  relation_clusters.json  # Discovered relation types
  feature_labels.json  # Probe-confirmed labels
```

**Three extraction levels:**
- `browse` (~3 GB) — `DESCRIBE`/`WALK`/`SELECT` only
- `inference` (~6 GB) — +`INFER`
- `all` (~10 GB) — +`COMPILE`

---
"""
    )
    return


@app.cell
def _(mo, is_script_mode):
    mo.md(
        r"""
## 🔍 LQL Query Language

LQL (Lazarus Query Language) is SQL-like syntax for browsing and editing model knowledge:

```sql
-- Browse knowledge (no GPU needed)
DESCRIBE "France";
-- Returns: capital → Paris, language → French, ...

WALK "The capital of France is" TOP 5;
-- Traverses the residual stream to find knowledge paths

-- Run inference (needs model weights in vindex)
INFER "The capital of France is" TOP 3;
-- Returns token predictions with confidence

-- Edit knowledge (auto-creates a patch, base files never modified)
INSERT INTO edges (entity, relation, target)
   VALUES ("John Coyle", "lives-in", "Colchester");
-- Creates a .vlp JSON patch overlay

COMPILE CURRENT INTO VINDEX;
-- Bakes patches into a new standalone vindex
```

---
"""
    )
    return


@app.cell
def _(mo, np, is_script_mode):
    mo.md(
        r"""
## 🏗️ Architecture

LARQL uses a strict dependency chain:

```
larql-models      Model config, architecture traits, weight loading
    ↓
larql-compute     CPU substrate: BLAS kernels, attention spine, forward-pass
    ↓
larql-vindex      Vindex lifecycle: extract, load, query, mutate, patch
    ↓
larql-core        Graph algorithms (merge, diff, BFS, pagerank)
    ↓
larql-inference   Engines (Standard, MarkovResidual, Apollo), chat, sessions
    ↓
larql-lql        Lexer/parser/executor/REPL + USE REMOTE client
    ↓
larql-server      HTTP + gRPC server serving vindexes
larql-cli         Top-level `larql` binary (every subcommand lives here)
```

**Key invariant:** Base vindexes are **immutable**. All mutation flows through `PatchedVindex` (overlay) — `INSERT`/`DELETE`/`UPDATE` auto-start a patch; `SAVE PATCH` persists it as `.vlp` JSON.

---
"""
    )
    return


@app.cell
def _(mo, is_script_mode):
    mo.md(
        r"""
## 🚀 Quick Start

```bash
# Build LARQL
cargo build --release

# Pull a pre-built vindex from HuggingFace
larql pull hf://chrishayuk/gemma-3-4b-it-vindex

# List what's cached
larql list

# Run it — one-shot or chat
larql run gemma-3-4b-it-vindex "The capital of France is"
larql run gemma-3-4b-it-vindex          # drops into chat mode

# Query via LQL
larql repl
larql lql 'USE "gemma3-4b.vindex"; DESCRIBE "France";'
```

---
"""
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""## 📚 What's Next?

Explore these interactive notebooks:

1. **`describe_explorer.py`** — Learn `DESCRIBE`: browse what a model knows
2. **`walk_knowledge.py`** — Learn `WALK`: traverse knowledge paths
3. **`inference_predict.py`** — Learn `INFER`: run inference with vindex
4. **`compile_knowledge.py`** — Learn `COMPILE`: edit and recompile knowledge
5. **`verify_vindex.py`** — Validate a vindex structure

---

[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/jeunjetta/larql/blob/feature/marimo-notebooks/notebooks/00_what_is_larql.py)
"""
    )
    return


if __name__ == "__main__":
    app.run()
