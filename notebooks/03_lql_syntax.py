# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "numpy>=2.0.0",
# ]
# ///

# Mirrors logic from docs/specs/lql-spec.md in chrishayuk/larql (to migrate to jeunjetta/larql)
# Notebook: 03_lql_syntax.py — Comprehensive LQL (Lazarus Query Language) tutorial

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
# 📖 LQL Syntax Tutorial

*Learn the Lazarus Query Language (LQL) — SQL-like syntax for browsing and editing neural network knowledge.*

---

LQL has 20+ statement types across 5 categories:
1. **Lifecycle** — EXTRACT, COMPILE, DIFF, USE
2. **Browse** — WALK, DESCRIBE, SELECT, EXPLAIN WALK
3. **Inference** — INFER, EXPLAIN INFER
4. **Mutation** — INSERT, DELETE, UPDATE, MERGE
5. **Patches** — BEGIN PATCH, SAVE PATCH, APPLY PATCH

Let's explore each category interactively.
"""
    )
    return


@app.cell
def _(mo):
    # Category selector
    category_select = mo.ui.dropdown(
        options=[
            "1. Lifecycle",
            "2. Browse",
            "3. Inference",
            "4. Mutation",
            "5. Patches",
        ],
        value="1. Lifecycle",
        label="📚 Select LQL Category",
    )
    category_select
    return (category_select,)


@app.cell
def _(mo, category_select):
    # Build content string based on selected category (fixes branch-expression error)
    _content = ""

    if "Lifecycle" in category_select.value:
        _content = r"""
## 🔄 Lifecycle Statements

Lifecycle statements manage vindexes and sessions.

### EXTRACT — Build a vindex from model weights

```sql
-- Basic extraction (defaults to inference level, f16)
EXTRACT MODEL "google/gemma-3-4b-it" INTO "gemma3-4b.vindex";

-- Extraction with specific level
EXTRACT MODEL "google/gemma-3-4b-it"
INTO "gemma3-4b.vindex"
WITH INFERENCE;

-- Extraction with all levels (includes COMPILE support)
EXTRACT MODEL "google/gemma-3-4b-it"
INTO "gemma3-4b.vindex"
WITH ALL;

-- Browse-only extraction (~3 GB, DESCRIBE/WALK only)
EXTRACT MODEL "google/gemma-3-4b-it"
INTO "gemma3-4b.vindex"
WITH BROWSE;
```

**Extraction levels:**
- `BROWSE` — Gate KNN + embeddings, no forward pass (~3 GB for 4B)
- `INFERENCE` — Full local forward pass (~6 GB)
- `ALL` — +lm_head + COMPILE extras (~10 GB)

### USE — Select a vindex for queries

```sql
-- Use a local vindex
USE "gemma3-4b.vindex";

-- Use a HuggingFace vindex (auto-downloads)
USE "hf://chrishayuk/gemma-3-4b-it-vindex";
```

### COMPILE — Bake patches into a new vindex

```sql
-- Compile current patches into a new standalone vindex
COMPILE CURRENT INTO VINDEX "gemma3-4b-patched.vindex";
```

### DIFF — Compare two vindexes

```sql
-- Show differences between two vindexes
DIFF "gemma3-4b.vindex" AND "gemma3-4b-patched.vindex";
```
"""
    elif "Browse" in category_select.value:
        _content = r"""
## 🔍 Browse Statements

Browse statements query the vindex without running inference.

### DESCRIBE — Browse what the model knows about an entity

```sql
-- Basic DESCRIBE
DESCRIBE "France";

-- DESCRIBE with layer range
DESCRIBE "France" FROM LAYER 14 TO 27;

-- Brief mode (compact output)
DESCRIBE "France" BRIEF;

-- Verbose mode (default: shows relation labels, also-tokens)
DESCRIBE "France" VERBOSE;

-- DESCRIBE all layers
DESCRIBE "Einstein" ALL LAYERS;
```

**Output:** Edges (relation, target, score, layer) from the entity.

### WALK — Traverse knowledge paths through the residual stream

```sql
-- Basic WALK
WALK "The capital of France is" TOP 5;

-- WALK with specific layers
WALK "The capital of France is"
FROM LAYER 14 TO 27 TOP 10;

-- WALK with inference comparison
WALK "The capital of France is" TOP 5 COMPARE;
```

**Output:** Token predictions with attention weights.

### SELECT — Query edges and features

```sql
-- Select edges by entity
SELECT * FROM edges
WHERE entity = "France";

-- Select edges by relation
SELECT * FROM edges
WHERE relation = "capital";

-- Select top-k features at a layer
SELECT * FROM features
WHERE layer = 24
ORDER BY score DESC
LIMIT 10;
```
"""
    elif "Inference" in category_select.value:
        _content = r"""
## 🚀 Inference Statements

Inference statements run the model forward pass.

### INFER — Run inference with the vindex

```sql
-- Basic INFER
INFER "The capital of France is" TOP 5;

-- INFER with comparison to training
INFER "The capital of France is" TOP 3 COMPARE;

-- INFER with temperature control
INFER "The capital of France is" TOP 5
TEMPERATURE 0.7;

-- INFER with max tokens
INFER "Write a poem about Paris"
MAX_TOKENS 100;
```

**Output:** Token predictions with probabilities.

### EXPLAIN INFER — Show inference decomposition

```sql
-- Explain inference step by step
EXPLAIN INFER "The capital of France is" TOP 5;

-- Show attention weights
EXPLAIN INFER "The capital of France is"
WITH ATTENTION;
```
"""
    elif "Mutation" in category_select.value:
        _content = r"""
## ✏️ Mutation Statements

Mutation statements edit the knowledge graph (auto-create patches).

### INSERT — Add knowledge to the model

```sql
-- Basic INSERT
INSERT INTO edges (entity, relation, target)
VALUES ("John Coyle", "lives-in", "Colchester");

-- INSERT with confidence
INSERT INTO edges (entity, relation, target)
VALUES ("Atlantis", "capital-of", "Poseidon")
AT LAYER 24
CONFIDENCE 0.95;

-- INSERT with multi-layer constellation
INSERT INTO edges (entity, relation, target)
VALUES ("Atlantis", "capital-of", "Poseidon")
AT LAYERS 20-26;
```

**Note:** `INSERT` auto-starts a patch. Base files are never modified.

### DELETE — Remove knowledge from the model

```sql
-- Delete specific edge
DELETE FROM edges
WHERE entity = "John Coyle"
  AND relation = "lives-in"
  AND target = "Colchester";

-- Delete all edges for an entity
DELETE FROM edges
WHERE entity = "Atlantis";
```

### UPDATE — Modify existing knowledge

```sql
-- Update edge target
UPDATE edges
SET target = "London"
WHERE entity = "UK"
  AND relation = "capital";
```
"""
    elif "Patches" in category_select.value:
        _content = r"""
## 📦 Patch Statements

Patches allow undoable edits to the vindex.

### BEGIN PATCH — Start a new patch

```sql
-- Start a new patch
BEGIN PATCH "add-music-bands";

-- Any INSERT/DELETE/UPDATE now goes into this patch
```

### SAVE PATCH — Persist patch to disk

```sql
-- Save current patch as .vlp JSON
SAVE PATCH;

-- Save with custom name
SAVE PATCH AS "my-edits.vlp";
```

### APPLY PATCH — Apply a saved patch

```sql
-- Apply a patch file
APPLY PATCH "my-edits.vlp";

-- List all saved patches
SHOW PATCHES;
```

### REMOVE PATCH — Discard a patch

```sql
-- Remove a patch without applying
REMOVE PATCH "add-music-bands";
```

**Key concept:** Patches are overlays on the readonly base vindex.
Multiple patches can stack. `COMPILE CURRENT INTO VINDEX` bakes
them into a new standalone vindex.
"""

    # Display the content (outside the conditional - fixes branch-expression error)
    mo.md(_content)
    return


@app.cell
def _(mo, is_script_mode):
    mo.md(
        r"""
## 🎯 Interactive Example
[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/jeunjetta/larql/blob/feature/marimo-notebooks/notebooks/03_lql_syntax.py)


Try running these LQL commands in the `larql repl`:

```bash
# Start the REPL
larql repl

# Or run a single command
larql lql 'USE "gemma3-4b.vindex"; DESCRIBE "France";'
```

---
## 📝 Try It Yourself

### Basic Exercises:
1. **DESCRIBE practice**: Write a LQL statement to describe "Paris" with layers 10-20
   - Observe: How does the layer range affect the output?

2. **WALK practice**: Write a LQL statement to walk from "France" with limit 10
   - Observe: What entities appear in the results?

3. **SELECT practice**: Write a LQL statement to select all edges where relation is "capital"
   - Observe: How many results return?

### Challenge Exercises:
1. **Multi-step query**: Combine DESCRIBE and WALK to explore a concept
   ```
   DESCRIBE "machine learning";
   -- Note the top relations, then WALK from one
   WALK "machine learning" TOP 5;
   ```

2. **Patch workflow**: Create a patch, insert a new edge, then save
   ```
   BEGIN PATCH;
   INSERT INTO edges (entity, relation, target, layer)
   VALUES ("AI", "is_a", "Technology", 15);
   SAVE PATCH AS "ai-knowledge.vlp";
   ```

### Observation Questions:
- When does DESCRIBE return more/fewer results? (Try different layer ranges)
- How does WALK path length vary with different TOP values?
- What happens when you INSERT a duplicate edge?

**Next steps:**
1. Try `describe_explorer.py` to interactively explore DESCRIBE
2. Try `walk_knowledge.py` to interactively explore WALK
3. Try `compile_knowledge.py` to see mutation + patch workflow

---
"""
    )
    return


if __name__ == "__main__":
    app.run()
