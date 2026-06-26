# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "numpy>=2.0.0",
# ]
# ///

# Mirrors logic from docs/specs/vindex-operations-spec.md in chrishayuk/larql
# Notebook: 05_patches.py — Deep dive into LARQL's patch system

import marimo

__generated_with = "0.23.11"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return mo,


@app.cell
def _(mo):
    is_script_mode = mo.app_meta().mode == "script"
    return (is_script_mode,)


@app.cell
def _(mo, is_script_mode):
    mo.md(
        r"""
# 📦 Patch System Deep Dive

*Understand how LARQL safely edits model knowledge with undoable patches.*

---

## 🔑 Key Concept: Base Vindex is Immutable

LARQL's most important invariant: **Base vindex files are never modified.**

Instead, all mutations (INSERT/DELETE/UPDATE) flow through a
`PatchedVindex` overlay — a stack of `.vlp` JSON patch files.

**Analogy:** Think of Git branches vs commits:
- **Base vindex** = main branch (immutable)
- **Patch** = commit (overlay with changes)
- **PatchedVindex** = working directory (base + patches)
- **COMPILE** = merge + create new branch

---
"""
    )
    return


@app.cell
def _(mo):
    # Concept selector
    concept_select = mo.ui.dropdown(
        options=[
            "Patch Structure",
            "Patch Lifecycle",
            "Multi-Patch Stacking",
            "Compile vs Save",
        ],
        value="Patch Structure",
        label="📚 Select Concept",
    )
    concept_select
    return (concept_select,)


@app.cell
def _(mo, concept_select):
    # Build content string based on selected concept (fixes branch-expression error)
    _content = ""

    if concept_select.value == "Patch Structure":
        _content = r"""
## 📄 Patch Structure (.vlp JSON)

A patch file (`.vlp`) is a JSON document describing mutations:

```json
{
  "name": "add-music-bands",
  "created_at": "2026-06-24T10:30:00Z",
  "operations": [
    {
      "type": "insert",
      "entity": "Pink Floyd",
      "relation": "genre",
      "target": "Progressive Rock",
      "layer": 24,
      "confidence": 0.95,
      "feature_idx": 8821
    },
    {
      "type": "delete",
      "entity": "Old Band",
      "relation": "genre",
      "target": "Unknown"
    }
  ]
}
```

**Fields:**
- `name` — Human-readable patch name
- `created_at` — Timestamp (for audit trail)
- `operations` — List of mutations (insert/delete/update)

**Feature allocation:** INSERT auto-allocates a feature index
from the vindex's free feature pool.

---
"""
    elif concept_select.value == "Patch Lifecycle":
        _content = r"""
## 🔄 Patch Lifecycle

Patches have a clear lifecycle: create → modify → save/discard → apply.

### 1. Create (Auto or Manual)

```sql
-- INSERT/DELETE/UPDATE auto-starts a patch
INSERT INTO edges (entity, relation, target)
VALUES ("Test", "relation", "target");
-- Prints: Auto-patch started: patch_123456.vlp

-- Or manually start with a name
BEGIN PATCH "add-music-bands";
```

### 2. Modify (Add More Operations)

```sql
-- Patch is now active — all mutations go into it
INSERT INTO edges (entity, relation, target)
VALUES ("Led Zeppelin", "genre", "Hard Rock");

INSERT INTO edges (entity, relation, target)
VALUES ("The Beatles", "formed", "1960");
```

### 3. Review

```sql
-- Show current patch contents
SHOW PATCH;
-- Output: 3 operations in patch "add-music-bands"
```

### 4. Save or Discard

```sql
-- Save to disk (persists across sessions)
SAVE PATCH;
-- Writes: ~/.larql/patches/add-music-bands.vlp

-- Discard without saving
REMOVE PATCH "add-music-bands";
```

### 5. Apply (Restore Saved Patch)

```sql
-- Apply a previously saved patch
APPLY PATCH "add-music-bands.vlp";
```

### 6. Compile (Bake into New Vindex)

```sql
-- Create new vindex with all patches applied
COMPILE CURRENT INTO VINDEX "gemma3-4b-patched.vindex";
```

**Result:** New vindex directory (~3-10 GB) with patches baked in.

---
"""
    elif concept_select.value == "Multi-Patch Stacking":
        _content = r"""
## 📚 Multi-Patch Stacking

Multiple patches can stack on the same base vindex.

**Example:**

```sql
-- Start first patch
BEGIN PATCH "add-geography";
INSERT INTO edges (entity, "France", relation, "capital")
VALUES ("Paris");

-- Save first patch
SAVE PATCH;

-- Start second patch (stacks on first)
BEGIN PATCH "add-music";
INSERT INTO edges (entity, "Daft Punk", relation, "genre")
VALUES ("Electronic");

-- Save second patch
SAVE PATCH;
```

**Query behavior:**
- `DESCRIBE "France"` → shows `Paris` (from `add-geography` patch)
- `DESCRIBE "Daft Punk"` → shows `Electronic` (from `add-music` patch)

**Patch order matters:**
- Patches apply in stack order (like Git commits)
- Later patches can override earlier ones

**List all patches:**
```sql
SHOW PATCHES;
-- Output:
-- 1. add-geography.vlp (3 ops)
-- 2. add-music.vlp (5 ops)
```

---
"""
    elif concept_select.value == "Compile vs Save":
        _content = r"""
## 🔨 COMPILE vs SAVE

These two operations are often confused — here's the difference:

### SAVE PATCH — Save Patch File

```sql
SAVE PATCH;
```

**What it does:**
- Writes the current patch to a `.vlp` JSON file
- Patch file is small (~KB to MB)
- Can be shared, versioned, applied later
- **Does NOT modify the base vindex**

**Use case:** Save work-in-progress, share patches with others.

### COMPILE CURRENT INTO VINDEX — Bake Patches In

```sql
COMPILE CURRENT INTO VINDEX "gemma3-4b-patched.vindex";
```

**What it does:**
- Creates a new standalone vindex directory
- Hardlinks base weight files (fast, APFS)
- Rewrites `down_weights.bin` column-wise (patches applied)
- No `.vlp` overlay needed — patches are baked in
- Result is a full vindex (~3-10 GB)

**Use case:** Create production vindex with all edits applied.

### Analogy

- **SAVE PATCH** = `git commit` (save changes)
- **COMPILE** = `git merge` + create release branch (bake changes in)

**Workflow:**
1. `SAVE PATCH` while experimenting
2. Share `.vlp` files with team
3. `COMPILE` when ready to deploy

---
"""

    # Display the content (outside the conditional - fixes branch-expression error)
    mo.md(_content)
    return


@app.cell
def _(mo, is_script_mode):
    mo.md(
        r"""
## 🎯 Try It Yourself

**To experiment with patches for real:**

1. **Start the REPL:**
   ```bash
   larql repl
   ```

2. **Create a patch:**
   ```sql
   BEGIN PATCH "test-patch";
   INSERT INTO edges (entity, "Test", relation, "knows")
   VALUES ("LARQL");
   SHOW PATCH;
   ```

3. **Save the patch:**
   ```sql
   SAVE PATCH;
   ```

4. **List patches:**
   ```sql
   SHOW PATCHES;
   ```

5. **Compile when ready:**
   ```sql
   COMPILE CURRENT INTO VINDEX "test-vindex.vindex";
   ```

**Next:** Try `compile_knowledge.py` to see a full mutation + compile workflow.

---

[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/jeunjetta/larql/blob/feature/marimo-notebooks/notebooks/05_patches.py)
"""
    )
    return


if __name__ == "__main__":
    app.run()
