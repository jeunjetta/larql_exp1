# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "numpy>=2.0.0",
#     "plotly>=5.0.0",
# ]
# ///

# Mirrors logic from crates/larql-cli/src/commands/query/walk_cmd.rs in chrishayuk/larql
# Notebook: walk_knowledge.py — Interactive WALK command explorer

import marimo

__generated_with = "0.23.13"
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
# 🚶 WALK Command Explorer

*Learn how `WALK` traverses knowledge paths through the residual stream — finding multi-hop connections that `DESCRIBE` can't reach.*

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
    # Prompt input for WALK
    prompt_input = mo.ui.text(
        value="The capital of France is",
        label="📝 Prompt for WALK",
        placeholder="Enter a prompt (e.g., The capital of France is)"
    )
    prompt_input
    return (prompt_input,)


@app.cell
def _(mo):
    # Top-k selector
    top_k = mo.ui.number(
        value=5,
        label="🔢 Top-K results",
        start=1,
        stop=20,
    )
    top_k
    return (top_k,)


@app.cell
def _(mo):
    # Layer range selector
    walk_layers = mo.ui.text(
        value="14-27",
        label="📊 Layers to walk",
        placeholder="e.g., 14-27 or ALL"
    )
    walk_layers
    return (walk_layers,)


@app.cell
def _(prompt_input, top_k, walk_layers, is_script_mode, mo, np, Path):
    # Build mock WALK results
    _md_content = ""
    
    if is_script_mode or not _setup.get("vindex_available", False):  # Always use mock for demo
        # Mock WALK path: "The capital of France is" → Paris
        mock_walk_path = [
            {"step": 0, "layer": 14, "token": "Paris", "score": 0.97, "source": "gate_knn"},
            {"step": 1, "layer": 18, "token": "Paris", "score": 0.98, "source": "gate_knn"},
            {"step": 2, "layer": 22, "token": "Paris", "score": 0.99, "source": "gate_knn"},
            {"step": 3, "layer": 25, "token": "Paris", "score": 0.995, "source": "gate_knn"},
            {"step": 4, "layer": 27, "token": "Paris", "score": 0.999, "source": "probe"},
        ]
        
        # Build markdown content as string
        _md_content = f"""
## 🚶 WALK Results for "{prompt_input.value}"

**Prompt:** {prompt_input.value} 
**Top-K:** {top_k.value} 
**Layers:** {walk_layers.value}

### Walk Path:
"""
        
        for step in mock_walk_path[:top_k.value]:
            _md_content += f"""
**Step {step['step']}** (Layer {step['layer']}): 
→ Token: `{step['token']}` | Score: {step['score']:.3f} | Source: {step['source']}
"""
        
        _md_content += r"""
**Interpretation:** The walk successfully found "Paris" through multiple layers, 
with increasing confidence (score) as it traversed the residual stream.

---

### 📈 Walk Path Visualization

> 💡 Install `plotly` to see walk path visualization.
"""
    else:
        _md_content = "> 💡 Run in script mode or with mock data to see WALK results."
    
    # Display OUTSIDE if block (fixes branch-expression error)
    mo.md(_md_content)
    return


@app.cell
def _(mo):
    mo.md(
        r"""
## 📖 LQL Syntax

```sql
-- Basic WALK
WALK "The capital of France is" TOP 5;

-- WALK with layer range
WALK "Einstein developed the theory of" TOP 3 FROM LAYER 14 TO 27;

-- WALK with COMPARE (show token probabilities)
WALK "The capital of France is" TOP 3 COMPARE;

-- WALK ALL layers
WALK "Python is a" TOP 10 ALL LAYERS;
```

---

"""
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
## 🧠 How WALK Works

`WALK` traverses the **residual stream** to find knowledge paths:

1. **Embed** the prompt → initial residual vector
2. **Forward pass** through selected layers (or all layers)
3. **At each layer:**
   - Run gate KNN to find activated features
   - Decode features → candidate tokens
   - Follow the strongest path (highest score)
4. **Return** the walk path: sequence of (layer, token, score)

**Key difference from `DESCRIBE`:**
- `DESCRIBE` finds knowledge **about an entity** (one-hop)
- `WALK` traverses **multi-hop paths** through the residual stream

**Example:**
```
WALK "The capital of France is" TOP 5;

Layer 14: "Paris" (0.97) ← Gate KNN found feature F8821
Layer 18: "Paris" (0.98) ← Feature reinforced
Layer 22: "Paris" (0.99) ← Stronger activation
Layer 25: "Paris" (0.995) ← Approaching answer
Layer 27: "Paris" (0.999) ← Probe confirms
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

1. Change the **Prompt** text input above
2. Adjust **Top-K** to see more/fewer steps
3. Modify **Layers** to explore different model depths
4. Check the LQL syntax section for the SQL-like command

**Next:** Try `inference_predict.py` to run full inference with `INFER`.

---

"""
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/jeunjetta/larql/blob/feature/marimo-notebooks/notebooks/walk_knowledge.py)
"""
    )
    return


if __name__ == "__main__":
    app.run()
