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

__generated_with = "0.23.11"
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
def _(mo, is_script_mode):
    mo.md(
        r"""
## 🧪 Try It Yourself (Mock Demo)

Since we don't have a real vindex in script mode, here's a mock
demonstration of the patch workflow:

**Mock State:**
- Base vindex: `gemma3-4b.vindex` (readonly)
- Active patch: `patch_123456.vlp` (overlay)

**Mock Operations:**
1. `INSERT ... ("John", "lives-in", "Colchester")` → patch updated
2. `DESCRIBE "John"` → shows `Colchester` (patched)
3. `SAVE PATCH` → `patch_123456.vlp` written to disk
4. `COMPILE CURRENT INTO VINDEX "gemma3-4b-patched.vindex"` → new vindex

**To try for real:**
1. Run `notebooks/setup.py` to download a vindex
2. Run `larql repl` to interactively execute LQL
3. Try the commands from this tutorial

---

[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/jeunjetta/larql/blob/feature/marimo-notebooks/notebooks/04_mutation_basics.py)
"""
    )
    return


if __name__ == "__main__":
    app.run()
