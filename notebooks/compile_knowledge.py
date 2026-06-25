# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "numpy>=2.0.0",
# ]
# ///

# Mirrors logic from crates/larql-lql/src/executor/mutation.rs in chrishayuk/larql
# Notebook: compile_knowledge.py — Interactive COMPILE and mutation explorer

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
# ✏️ COMPILE & Knowledge Editing

*Learn how to edit model knowledge with `INSERT`, `DELETE`, `UPDATE`, and `COMPILE`.*

---
"""
    )
    return


@app.cell
def _(mo, Path):
    # Try to import from helper, fall back to mock
    try:
        from _vindex_helper import setup_hint_md, check_setup
        _hint = setup_hint_md()
        _setup = check_setup()
    except ImportError:
        _hint = "> 💡 Run `notebooks/setup.py` first to download data."
        _setup = {"vindex_available": False, "larql_available": False}
    
    # Always render md (empty if no hint) - fixes branch-expression error
    mo.md(_hint if _hint else "")
    return _setup


@app.cell
def _(mo):
    mo.md(
        r"""
## 📝 Mutation Commands

LARQL uses three mutation verbs to edit knowledge:

### INSERT
Add new knowledge edges to the model:
```sql
INSERT INTO edges (entity, relation, target)
   VALUES ("John Coyle", "lives-in", "Colchester");
```

### DELETE
Remove knowledge edges:
```sql
DELETE FROM edges WHERE entity="John Coyle" AND relation="lives-in";
```

### UPDATE
Modify existing edges:
```sql
UPDATE edges SET target="London" 
   WHERE entity="John Coyle" AND relation="lives-in";
```

**Key point:** All mutations auto-start a patch. Base files are **never modified**.

---
"""
    )
    return


@app.cell
def _(mo):
    # Mock mutation demo
    mutation_type = mo.ui.dropdown(
        options=["INSERT", "DELETE", "UPDATE"],
        value="INSERT",
        label="🔧 Mutation Type"
    )
    mutation_type
    return (mutation_type,)


@app.cell
def _(mo):
    # Entity and relation inputs
    entity_input = mo.ui.text(
        value="John Coyle",
        label="🏷️ Entity",
        placeholder="Enter entity name"
    )
    relation_input = mo.ui.text(
        value="lives-in",
        label="🔗 Relation",
        placeholder="Enter relation type"
    )
    target_input = mo.ui.text(
        value="Colchester",
        label="🎯 Target",
        placeholder="Enter target value"
    )
    entity_input
    relation_input
    target_input
    return entity_input, relation_input, target_input


@app.cell
def _(mutation_type, entity_input, relation_input, target_input, mo):
    # Generate mock LQL statement
    if mutation_type.value == "INSERT":
        lql_statement = f'''INSERT INTO edges (entity, relation, target)
   VALUES ("{entity_input.value}", "{relation_input.value}", "{target_input.value}");'''
        mock_response = f'''Inserted 1 edge. Feature F8821@L26 allocated.
Auto-patch started (use SAVE PATCH to persist).'''
    
    elif mutation_type.value == "DELETE":
        lql_statement = f'''DELETE FROM edges 
   WHERE entity="{entity_input.value}" AND relation="{relation_input.value}";'''
        mock_response = f'''Deleted 1 edge. Patch updated.'''
    
    else:  # UPDATE
        new_target = mo.ui.text(value="London", label="New Target")
        lql_statement = f'''UPDATE edges SET target="{new_target.value}" 
   WHERE entity="{entity_input.value}" AND relation="{relation_input.value}";'''
        mock_response = f'''Updated 1 edge. Patch updated.'''
    
    mo.md(
        f"""
## 📝 Generated LQL Statement

```sql
{lql_statement}
```

### Mock Response:
```
{mock_response}
```

---
"""
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
## 💾 Patch System

Mutations don't modify base files directly. Instead:

1. **Auto-patch** — First mutation auto-starts a patch
2. **Patch overlay** — Changes stored in `.vlp` JSON (not base files)
3. **SAVE PATCH** — Persist patch to disk
4. **APPLY PATCH** — Apply saved patch to a vindex
5. **COMPILE CURRENT INTO VINDEX** — Bake patch into new standalone vindex

**Benefits:**
- Base vindex stays **immutable** (can always revert)
- Multiple patches can stack
- Patches are **portable** (share knowledge edits)

---
"""
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
## 🔨 COMPILE Command

`COMPILE` bakes patches into a new vindex:

```sql
-- Compile current patches into a new vindex
COMPILE CURRENT INTO VINDEX "edited-gemma3-4b.vindex";

-- Compile with a specific patch
COMPILE PATCH "my-edits.vlp" INTO VINDEX "edited-gemma3-4b.vindex";
```

**What happens:**
1. Hardlink base weight files (fast, APFS optimization)
2. Rewrite only `down_weights.bin` column-wise
3. New vindex is **standalone** (no patch needed at load time)

---
"""
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
## 🧠 How It Works

Knowledge editing modifies **gate/down matrices**:

1. **INSERT** → Allocate a new feature (gate vector + down weight column)
2. **DELETE** → Zero out a feature's down weight column
3. **UPDATE** → Modify down weight column values
4. **COMPILE** → Bake changes into new weight files

**Key insight:**  
The model IS the database. Editing knowledge = editing weights.

**Analogy:**
- `DESCRIBE` = SELECT (read)
- `INSERT`/`DELETE`/`UPDATE` = INSERT/DELETE/UPDATE (write)
- `COMPILE` = COMMIT (persist)

---
"""
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
## 🔍 Before vs After COMPILE (Mock Demo)

This table shows what changes before and after compiling.

| Step | Action | Result |
|------|--------|--------|
| 1 | `INSERT ...` | Edge added to **patch** (overlay) |
| 2 | `DESCRIBE "X"` | Returns base knowledge + patch overlay |
| 3 | `COMPILE ...` | New vindex with **edited weights** |
| 4 | `DESCRIBE "X"` (new vindex) | Returns **edited** knowledge |

**Key benefit:** COMPILE creates a **standalone** vindex — no patch files needed at load time.

*In script mode: imagine the table above represents the workflow. In interactive mode with a real vindex, you'd see actual DESCRIBE results change before/after COMPILE.*

---
"""
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
## 🎯 Try It Yourself

1. Change the **Mutation Type** dropdown above
2. Modify **Entity**, **Relation**, **Target** inputs
3. See the generated LQL statement
4. Imagine the patch workflow

**Next steps:**
- Run `larql repl` to try mutations for real
- Use `SHOW PATCHES` to see active patches
- Use `SAVE PATCH` to persist changes

---
"""
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/jeunjetta/larql/blob/feature/marimo-notebooks/notebooks/compile_knowledge.py)
"""
    )
    return

if __name__ == "__main__":
    app.run()
