# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "numpy>=2.0.0",
# ]
# ///

# Mirrors logic from notebooks/00_what_is_larql.py in chrishayuk/larql (to migrate to jeunjetta/larql)

import marimo

__generated_with = "0.23.15"
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
def _(mo):
    # Interactive DESCRIBE demo
    mo.md(
        r"""
## 🎯 Interactive Demo: Visualize the Knowledge Graph (Mock)

LARQL lets you query a transformer model like a graph database. Use the interactive `DESCRIBE` demo below to explore mock knowledge about entities.

**Imagine this:** Each entity is a node, and the relations (like "capital", "language") are edges connecting them to other nodes (the "targets").

Type an entity name below and click "Describe" to see mock results:

### Basic Exercises:
1.  **Try "France"**: Observe the relations and targets that describe France. Notice how it's connected to `Paris` (capital) and `French` (language).
2.  **Try "Einstein"**: What kind of knowledge does the model store about famous people? Look for connections to fields of study and key achievements.
1.  **Try "Paris"**: How does the knowledge about a city differ from a country? Compare its connections to `France` (country) and `Eiffel Tower` (landmark).

### Challenge Exercises:
1.  **Chaining Queries**: If you wanted to find the `language` spoken in the `capital` of `France`, how would you mentally "chain" the `DESCRIBE` queries? What entities would you search for in what order?

### Observation Questions:
- What patterns do you notice in the "Relation" and "Target" columns?
- What does the "Score" represent in this knowledge graph context?
- How might the "Layer" column be useful in understanding *where* in the model's layers this knowledge is stored?
- What happens if you search for an entity not in the mock database (e.g., "Mars")? How does LARQL handle unknown entities?
"""
    )
    entity_input = mo.ui.text(
        value="France",
        label="Entity to DESCRIBE"
    )
    describe_button = mo.ui.run_button(label="🔍 DESCRIBE")
    mo.md("**Try it:** Type an entity (e.g., `France`, `Einstein`, `Paris`) and click Describe.")
    entity_input, describe_button
    return entity_input, describe_button


@app.cell
def _(mo, entity_input, describe_button):
    # Show mock DESCRIBE results
    _content = ""

    if describe_button.value:
        _entity = entity_input.value or "France"

        # Mock knowledge base for demo
        _mock_knowledge = {
            "France": [
                ("capital", "Paris", 0.98, 18),
                ("language", "French", 0.94, 16),
                ("currency", "Euro", 0.91, 20),
                ("continent", "Europe", 0.89, 14),
            ],
            "Einstein": [
                ("field", "Physics", 0.97, 22),
                ("known-for", "Relativity", 0.95, 24),
                ("nobel-prize", "Physics 1921", 0.92, 20),
                ("born-in", "Germany", 0.88, 18),
            ],
            "Paris": [
                ("is-capital-of", "France", 0.99, 19),
                ("landmark", "Eiffel Tower", 0.96, 21),
                ("language", "French", 0.93, 17),
                ("country", "France", 0.91, 15),
            ],
        }

        _results = _mock_knowledge.get(_entity, [
            ("related-to", f"[mock result for {_entity}]", 0.75, 20),
            ("property", "[not in mock DB]", 0.60, 18),
        ])

        # Build HTML table for results
        _rows = ""
        for rel, tgt, score, layer in _results:
            _rows += f"<tr><td>{rel}</td><td>{tgt}</td><td>{score:.2f}</td><td>{layer}</td></tr>"

        _content = f"""
### DESCRIBE "{_entity}" (Mock Results)

**LQL:** `DESCRIBE "{_entity}";`

| Relation | Target | Score | Layer |
|----------|--------|-------|-------|
{_rows}

*Note: These are mock results for demonstration. Real DESCRIBE queries load a vindex.*
"""
    else:
        _content = '*Click "DESCRIBE" above to see mock results.*'

    mo.md(_content)
    return


@app.cell
def _(mo):
    mo.md(r"""
---

## 💡 Knowledge Check: Core Concepts

Let's test your understanding of LARQL's core ideas!

**Question 1:** What is the primary purpose of a **vindex** in LARQL?
""")
    q1_options = {
        "To fine-tune a model with new data": "incorrect1",
        "To store traditional relational database tables": "incorrect2",
        "To make transformer model weights queryable like a graph database": "correct",
        "To compress large language models for deployment": "incorrect3",
    }
    q1_radio = mo.ui.radio(q1_options, label="Select your answer:")
    q1_radio
    return q1_radio, mo



@app.cell
def _(q1_radio, mo):
    _feedback_content = ""
    if q1_radio.value == "correct":
        _feedback_content = "🎉 **Correct!** A vindex transforms model weights into a queryable knowledge graph."
    elif q1_radio.value:
        _feedback_content = "❌ **Incorrect.** Please review the 'Core Idea' section above and try again."
    mo.md(_feedback_content)
    return

@app.cell
def _(mo, np, is_script_mode):
    mo.md(
        r"""
## 🏗️ Architecture

LARQL uses a strict dependency chain:

```
larql-models      Model config, architecture traits, weight loading
    |
larql-compute     CPU substrate: BLAS kernels, attention spine, forward-pass
    |
larql-vindex      Vindex lifecycle: extract, load, query, mutate, patch
    |
larql-core        Graph algorithms (merge, diff, BFS, pagerank)
    |
larql-inference   Engines (Standard, MarkovResidual, Apollo), chat, sessions
    |
larql-lql        Lexer/parser/executor/REPL + USE REMOTE client
    |
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
5. **`03_lql_syntax.py`** — Complete LQL language tutorial

---

[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/jeunjetta/larql/blob/feature/marimo-notebooks/notebooks/00_what_is_larql.py)
"""
    )
    return


if __name__ == "__main__":
    app.run()
