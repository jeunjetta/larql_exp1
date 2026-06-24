# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "numpy>=2.0.0",
# ]
# ///

# Mirrors logic from LARQL graph structure concepts (to migrate to jeunjetta/larql)

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
# 🕸️ Graph Structure — Knowledge as a Graph

*Learn how LARQL represents model knowledge as a queryable graph database.*

---
"""
    )
    return


@app.cell
def _(mo, is_script_mode):
    mo.md(
        r"""
## 🧠 The Core Abstraction

**LARQL treats a transformer model as a graph database:**

```
Nodes = Entities (France, Einstein, Python)
Edges = Knowledge (entity --[relation]--> target)
Weights = Scores (how strongly the model knows this fact)
Layers = Depth (where in the model this knowledge lives)
```

**Key insight:** The model's **gate vectors** (W_gate rows) encode knowledge as feature activations. When you `DESCRIBE "France"`, LARQL:
1. Converts "France" to a residual vector (embedding)
2. Finds top-k activated features at each layer (KNN search)
3. Decodes features → edges (relation, target, score)

---
"""
    )
    return


@app.cell
def _(mo):
    # Entity selector
    entity_input = mo.ui.text(
        value="France",
        label="🔤 Entity to Explore",
        placeholder="Enter an entity (e.g., France, Einstein, Python)",
    )
    entity_input
    return (entity_input,)


@app.cell
def _(mo, entity_input, is_script_mode):
    # Build mock graph data
    mock_edges = [
        {"relation": "capital", "target": "Paris", "score": 1436.9, "layer": 27},
        {"relation": "language", "target": "French", "score": 35.2, "layer": 24},
        {"relation": "continent", "target": "Europe", "score": 14.4, "layer": 25},
        {"relation": "borders", "target": "Spain", "score": 13.3, "layer": 18},
        {"relation": "currency", "target": "Euro", "score": 8.7, "layer": 22},
    ]
    
    # Build content string
    _content = f"""
## 📊 Graph View: Edges for "{entity_input.value}"

**Entity:** `{entity_input.value}`  
**Edges found:** {len(mock_edges)}

### Edge Structure:

| Relation | Target | Score | Layer | Source |
|-----------|--------|-------|-------|--------|
"""
    for e in mock_edges:
        _content += f"| **{e['relation']}** | {e['target']} | {e['score']:.1f} | L{e['layer']} | probe |\n"

    _content += r"""
---

**Edge attributes:**
- `relation` — The type of knowledge (capital, language, ...)
- `target` — The related entity
- `score` — Activation strength (higher = stronger knowledge)
- `layer` — Model layer where this knowledge was found
- `source` — How this edge was discovered (probe, explicit, ...)

"""
    
    # Display content outside conditional
    mo.md(_content)
    return


@app.cell
def _(mo):
    mo.md(
        r"""
## 🏗️ VIndex as a Graph Database

A **vindex** is a graph database with these tables:

### Nodes (Entities)
```
Table: entities
- id: INTEGER PRIMARY KEY
- name: TEXT (e.g., "France", "Paris")
- embedding: BLOB (residual vector, 2560-dim f16)
```

### Edges (Knowledge)
```
Table: edges
- entity: TEXT (source entity)
- relation: TEXT (relation type)
- target: TEXT (target entity)
- score: REAL (activation strength)
- layer: INTEGER (model layer)
- source: TEXT (discovery method)
```

### Features (Activations)
```
Table: features
- layer: INTEGER
- feature_idx: INTEGER
- top_token: TEXT (what this feature detects)
- c_score: REAL (confidence score)
```

---
"""
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
## 🔍 LQL: SQL for the Knowledge Graph

LQL (Lazarus Query Language) is SQL-like syntax for querying the graph:

### DESCRIBE (Browse Knowledge)
```sql
-- Get all edges for an entity
DESCRIBE "France";

-- With layer filter
DESCRIBE "France" FROM LAYER 14 TO 27;

-- Brief mode (compact output)
DESCRIBE "France" BRIEF;
```

### SELECT (Query Graph)
```sql
-- Get all edges with a specific relation
SELECT * FROM edges WHERE relation = "capital";

-- Join entities and edges
SELECT e.name, r.relation, e2.name
FROM entities e
JOIN edges r ON e.name = r.entity
JOIN entities e2 ON r.target = e2.name;

-- With limits
SELECT * FROM edges LIMIT 10;
```

### WALK (Traverse Graph)
```sql
-- Walk from an entity through relations
WALK "The capital of France is" TOP 5;

-- Returns: [(entity, relation, target, score), ...]
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

### 1. Browse Knowledge
```bash
# Using CLI
larql repl
```

Then in the REPL:
```sql
USE "gemma3-4b.vindex";
DESCRIBE "France" LIMIT 10;
```

### 2. Query with Python
```python
import larql

vindex = larql.load("output/gemma3-4b-v2.vindex")

# Get edges (knowledge)
edges = vindex.describe("France", verbose=True)
for e in edges[:5]:
    print(f"  {e.relation or '?'} → {e.target} score={e.score:.1f} L{e.layer}")

# Get embedding (node representation)
emb = vindex.embed("France")
print(f"Embedding shape: {emb.shape}")  # (2560,)
```

### 3. Explore Graph Structure
```python
# Get all relations in the vindex
relations = vindex.relations()
print(f"Discovered relations: {relations}")

# Get feature metadata (what features detect)
meta = vindex.feature_meta(layer=24, feature_idx=0)
print(f"Feature 0 detects: {meta.top_token}")
```

---
"""
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
## 📚 What's Next?

1. **`describe_explorer.py`** — Deep dive into `DESCRIBE` command
2. **`walk_knowledge.py`** — Learn to traverse knowledge with `WALK`
3. **`compile_knowledge.py`** — Edit the graph with `INSERT`/`COMPILE`

---
"""
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/jeunjetta/larql/blob/feature/marimo-notebooks/notebooks/02_graph_structure.py)
"""
    )
    return


if __name__ == "__main__":
    app.run()
