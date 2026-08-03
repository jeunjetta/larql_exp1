# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "numpy>=2.0.0",
# ]
# ///

# Mirrors logic from docs/specs/vindex-operations-spec.md in chrishayuk/larql
# Notebook: 04_mutation_basics.py — Interactive tutorial on INSERT/DELETE/UPDATE

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
# ✏️ Mutation Basics: INSERT, DELETE, UPDATE

*Learn how to edit model knowledge with LQL mutation statements — safely, with patches.*

---

**Key concept:** LARQL never modifies the base vindex files. All mutations
create a `PatchedVindex` overlay — a stack of `.vlp` JSON patch files.

**Workflow:**
1. `INSERT`/`DELETE`/`UPDATE` → auto-starts a patch
2. `SAVE PATCH` → persists patch to disk
3. `COMPILE CURRENT INTO VINDEX` → bakes patches into new vindex

### Observation Question:
- Why is it important that LARQL uses patches and never directly modifies the base vindex files? What benefits does this approach offer for managing model knowledge?

Let's explore mutations interactively.
"""
    )
    return


@app.cell
def _(mo):
    # Operation selector
    operation_select = mo.ui.dropdown(
        options=["INSERT", "DELETE", "UPDATE", "Patch Workflow"],
        value="INSERT",
        label="🔧 Select Operation",
    )
    operation_select
    return (operation_select,)


@app.cell
def _(mo, operation_select):
    # Build content string based on selected operation (fixes branch-expression error)
    _content = ""

    if operation_select.value == "INSERT":
        _content = r"""
## ➕ INSERT Statement

`INSERT` adds new knowledge edges to the model.

### Basic INSERT

```sql
INSERT INTO edges (entity, relation, target)
VALUES ("John Coyle", "lives-in", "Colchester");
```

**What happens:**
1. Auto-starts a patch (if none active)
2. Allocates a new feature in `down_weights.bin`
3. Updates `gate_vectors.bin` to activate for the entity
4. Updates `down_meta.bin` with the edge metadata

### INSERT with Options

```sql
-- Insert at specific layer
INSERT INTO edges (entity, relation, target)
VALUES ("Atlantis", "capital-of", "Poseidon")
AT LAYER 24;

-- Insert with confidence (affects feature strength)
INSERT INTO edges (entity, relation, target)
VALUES ("Atlantis", "capital-of", "Poseidon")
AT LAYER 24
CONFIDENCE 0.95;

-- Insert with multi-layer constellation (stronger recall)
INSERT INTO edges (entity, relation, target)
VALUES ("Atlantis", "capital-of", "Poseidon")
AT LAYERS 20-26;
```

### Mock Example

**Entity:** `John Coyle`
**Relation:** `lives-in`
**Target:** `Colchester`
**Layer:** 24 (default)
**Confidence:** 0.90 (default)

**Result:** New edge added to patch (not yet saved).
"""
    elif operation_select.value == "DELETE":
        _content = r"""
## ➖ DELETE Statement

`DELETE` removes knowledge edges from the model (adds negation to patch).

### Basic DELETE

```sql
-- Delete specific edge
DELETE FROM edges
WHERE entity = "John Coyle"
  AND relation = "lives-in"
  AND target = "Colchester";

-- Delete all edges for an entity
DELETE FROM edges
WHERE entity = "Atlantis";

-- Delete edges by relation
DELETE FROM edges
WHERE relation = "capital-of";
```

**What happens:**
1. Finds the edge(s) in the vindex
2. Adds a "negation" entry to the patch
3. Future queries won't return deleted edges

**Note:** DELETE doesn't modify base files. The edge still exists
in the base vindex, but the patch overrides it.

### Mock Example

**Delete:** `entity="John Coyle" AND relation="lives-in"`
**Result:** Edge removed from query results (patch negation).
"""
    elif operation_select.value == "UPDATE":
        _content = r"""
## 🔄 UPDATE Statement

`UPDATE` modifies existing knowledge edges.

### Basic UPDATE

```sql
-- Update edge target
UPDATE edges
SET target = "London"
WHERE entity = "UK"
  AND relation = "capital";

-- Update edge confidence
UPDATE edges
SET confidence = 0.99
WHERE entity = "France"
  AND relation = "capital";
```

**What happens:**
1. Finds the edge(s) in the vindex
2. Adds an "update" entry to the patch
3. Future queries return updated values

**Note:** Like INSERT/DELETE, UPDATE creates patch entries.

### Mock Example

**Before:** `("France", "capital", "Paris")`
**UPDATE:** `SET target = "Lyon"`
**After:** `("France", "capital", "Lyon")` (in patch)

**Next query:** `DESCRIBE "France"` → returns `Lyon` (patched).
"""
    elif operation_select.value == "Patch Workflow":
        _content = r"""
## 📦 Patch Workflow

Patches make mutations safe and undoable.

### Step 1: Start a Patch (Auto or Manual)

```sql
-- INSERT/DELETE/UPDATE auto-start a patch
INSERT INTO edges (entity, relation, target)
VALUES ("Test", "relation", "target");
-- Prints: "Auto-patch started: patch_123456.vlp"

-- Or manually start with a name
BEGIN PATCH "add-music-bands";
```

### Step 2: Review Patch Status

```sql
-- Show current patch contents
SHOW PATCH;

-- List all saved patches
SHOW PATCHES;
```

### Step 3: Save or Discard

```sql
-- Save patch to disk (persists across sessions)
SAVE PATCH;

-- Discard without saving
REMOVE PATCH "add-music-bands";
```

### Step 4: Apply Saved Patch

```sql
-- Apply a previously saved patch
APPLY PATCH "add-music-bands.vlp";
```

### Step 5: Compile (Bake Patches into New Vindex)

```sql
-- Create new vindex with all patches applied
COMPILE CURRENT INTO VINDEX "gemma3-4b-patched.vindex";
```

**Key insight:** `COMPILE` creates a new standalone vindex
(hardlinking base weight files + rewriting `down_weights.bin`
column-wise). The original vindex stays unchanged.
"""

    # Display the content (outside the conditional - fixes branch-expression error)
    mo.md(_content)
    return


@app.cell
def _(mo):
    mo.md(r"""
---

## 💡 Knowledge Check: Mutation & Patches

Let's test your understanding of LQL mutation statements and the patching system!

**Question 1:** What is the primary function of an `UPDATE` statement in LARQL?
""")


@app.cell
def _(mo):
    q1_options = {
        "Change attributes of existing knowledge edges": "correct",
        "Add new knowledge edges": "incorrect1",
        "Remove knowledge edges": "incorrect2",
        "Bake patches into a new vindex": "incorrect3",
    }
    q1_radio = mo.ui.radio(q1_options, label="Select your answer:")
    q1_radio
    return q1_radio, mo

@app.cell
def _(q1_radio, mo):
    _content = ""
    if q1_radio.value == "correct":
        _content = "🎉 **Correct!** `UPDATE` is used to change attributes of existing knowledge edges."
    elif q1_radio.value:
        _content = "❌ **Incorrect.** Review the 'UPDATE Statement' section to understand its purpose."
    mo.md(_content)
    return

@app.cell
def _(mo, is_script_mode):
    mo.md(
        r"""
## 🎯 Try It Yourself
[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/jeunjetta/larql/blob/feature/marimo-notebooks/notebooks/04_mutation_basics.py)


### Basic Exercises:

1. **INSERT a new edge**
   ```sql
   INSERT INTO edges (entity, relation, target)
   VALUES ("Ada Lovelace", "field", "Computer Science");
   ```
   - Expected: Auto-starts a patch, allocates feature
   - Observe: What does `SHOW PATCH` return?

2. **DELETE an edge**
   ```sql
   DELETE FROM edges
   WHERE entity = "Ada Lovelace" AND relation = "field";
   ```
   - Expected: Adds negation to patch
   - Observe: Does `DESCRIBE "Ada Lovelace"` still show "Computer Science"?

3. **UPDATE an edge**
   ```sql
   INSERT INTO edges (entity, relation, target)
   VALUES ("Test", "status", "active");
   
   UPDATE edges
   SET target = "inactive"
   WHERE entity = "Test" AND relation = "status";
   
   SHOW PATCH;
   ```
   - Observe: Does the patch have 1 or 2 operations? Why?

### Challenge Exercises:

1. **Multi-layer INSERT**
   ```sql
   INSERT INTO edges (entity, relation, target)
   VALUES ("LARQL", "is", "Graph Database")
   AT LAYERS 20-26;
   ```
   - What happens? Why might multiple layers strengthen recall?
   - Try `DESCRIBE "LARQL"` at different layers

2. **Patch stacking**
   ```sql
   BEGIN PATCH "patch-a";
   INSERT INTO edges (entity, relation, target)
   VALUES ("A", "rel", "B");
   SAVE PATCH;
   
   BEGIN PATCH "patch-b";
   INSERT INTO edges (entity, relation, target)
   VALUES ("B", "rel", "C");
   SAVE PATCH;
   
   SHOW PATCHES;
   ```
   - Observe: Can you apply both patches? What order?

### Observation Questions:

- Why doesn't LARQL modify base files directly?
- When would you use `SAVE PATCH` vs `COMPILE CURRENT INTO VINDEX`?
- What's the difference between a patch and a compiled vindex?
- Why are patches human-readable JSON (`.vlp`) instead of binary?

---

**Next steps:**
1. Run `notebooks/setup.py` to download a real vindex
2. Run `larql repl` to try these commands interactively
3. Try `compile_knowledge.py` to see a full compile workflow

---
"""
    )
    return


if __name__ == "__main__":
    app.run()
