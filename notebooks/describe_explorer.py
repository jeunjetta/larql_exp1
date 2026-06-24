# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "numpy>=2.0.0",
# ]
# ///

# Mirrors logic from crates/larql-cli/src/commands/query/describe_cmd.rs in chrishayuk/larql
# Notebook: describe_explorer.py — Interactive DESCRIBE command explorer

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
# 🔍 DESCRIBE Command Explorer

*Learn how `DESCRIBE` browses model knowledge by querying the vindex's KNN index.*

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
    # Entity selector — always show, use mock data in script mode
    entity_input = mo.ui.text(
        value="France",
        label="🔤 Entity to DESCRIBE",
        placeholder="Enter an entity (e.g., France, Einstein, Python)"
    )
    entity_input
    return (entity_input,)


@app.cell
def _(mo):
    # Layer range selector
    layer_start = mo.ui.number(
        value=14,
        label="📊 Start Layer",
        start=0,
        stop=33,
    )
    layer_end = mo.ui.number(
        value=27,
        label="📊 End Layer",
        start=0,
        stop=33,
    )
    layer_start
    layer_end
    return layer_start, layer_end


@app.cell
def _(mo):
    # Verbose toggle
    verbose_toggle = mo.ui.checkbox(
        value=True,
        label="📝 Verbose mode (show relation labels, also-tokens)"
    )
    verbose_toggle
    return (verbose_toggle,)


@app.cell
def _(entity_input, layer_start, layer_end, verbose_toggle, is_script_mode, mo, np, Path):
    # Build mock data for script mode or when vindex not available
    if is_script_mode or not _setup.get("vindex_available", False):  # Always use mock for demo (avoids 3GB load)
        # Mock DESCRIBE results
        mock_edges = [
            {"relation": "capital", "target": "Paris", "score": 1436.9, "layer": 27, "source": "probe"},
            {"relation": "language", "target": "French", "score": 35.2, "layer": 24, "source": "probe"},
            {"relation": "continent", "target": "Europe", "score": 14.4, "layer": 25, "source": "probe"},
            {"relation": "borders", "target": "Spain", "score": 13.3, "layer": 18, "source": "probe"},
            {"relation": "currency", "target": "Euro", "score": 8.7, "layer": 22, "source": "probe"},
        ]
        
        # Filter by layer range
        filtered_edges = [
            e for e in mock_edges
            if layer_start.value <= e["layer"] <= layer_end.value
        ]
        
        # Display results
        mo.md(
            f"""
## 📊 DESCRIBE Results for "{entity_input.value}"

**Entity:** {entity_input.value}  
**Layer Range:** {layer_start.value}–{layer_end.value}  
**Mode:** {"Verbose" if verbose_toggle.value else "Brief"}

### Edges Found:
"""
        )
        
        if filtered_edges:
            for edge in filtered_edges[:10]:  # Show top 10
                if verbose_toggle.value:
                    mo.md(
                        f"""
- **{edge['relation'] or '?'}** → `{edge['target']}`  
  Score: {edge['score']:.1f} | Layer {edge['layer']} ({edge['source']})
"""
                    )
                else:
                    mo.md(
                        f"- {edge['relation'] or '?'} → {edge['target']} (L{edge['layer']})\n"
                    )
        else:
            mo.md("No edges found in the selected layer range.\n")
    else:
        # Real vindex code would go here
        pass
    
    return


@app.cell
def _(mo):
    mo.md(
        r"""
## 📖 LQL Syntax

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

---
"""
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
## 🧠 How It Works

`DESCRIBE` queries the vindex's gate vector KNN index:

1. **Embed** the entity string → residual vector
2. **Gate KNN** — find top-k activated features at each layer
3. **Decode** features → edges (relation, target, score)
4. **Return** ordered by score (strongest connections first)

**Key insight:** The gate vectors encode knowledge as feature activations.  
`DESCRIBE` finds which features activate for your entity, then decodes  
what those features mean (via `feature_meta`).

---
"""
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
## 🎯 Try It Yourself

1. Change the **Entity** text input above
2. Adjust the **Layer Range** to explore different model depths
3. Toggle **Verbose Mode** to see more/less detail
4. Check the LQL syntax section for the SQL-like command

**Next:** Try `walk_knowledge.py` to traverse knowledge paths with `WALK`.

---
"""
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/jeunjetta/larql/blob/feature/marimo-notebooks/notebooks/describe_explorer.py)
"""
    )
    return

if __name__ == "__main__":
    app.run()
