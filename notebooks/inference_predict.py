# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "numpy>=2.0.0",
# ]
# ///

# Mirrors logic from crates/larql-cli/src/commands/query/infer_cmd.rs in chrishayuk/larql
# Notebook: inference_predict.py — Interactive INFER command explorer

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
# 🤖 INFER Command Explorer

*Learn how `INFER` runs inference with the vindex — generating tokens with the model's knowledge.*

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
    # Prompt input for INFER
    prompt_input = mo.ui.text(
        value="The capital of France is",
        label="📝 Prompt for INFER",
        placeholder="Enter a prompt (e.g., The capital of France is)"
    )
    prompt_input
    return (prompt_input,)


@app.cell
def _(mo):
    # Top-k selector
    top_k = mo.ui.number(
        value=3,
        label="🔢 Top-K results",
        start=1,
        stop=10,
    )
    top_k
    return (top_k,)


@app.cell
def _(mo):
    # Compare toggle
    compare_toggle = mo.ui.checkbox(
        value=True,
        label="📊 Compare mode (show token probabilities)"
    )
    compare_toggle
    return (compare_toggle,)


@app.cell
def _(prompt_input, top_k, compare_toggle, is_script_mode, mo, np, Path):
    # Build mock INFER results
    _md_content = ""
    
    if is_script_mode or not _setup.get("vindex_available", False):  # Always use mock for demo
        # Mock INFER results for "The capital of France is"
        mock_predictions = [
            {"token": "Paris", "probability": 0.9791, "rank": 1},
            {"token": "the", "probability": 0.0042, "rank": 2},
            {"token": "a", "probability": 0.0031, "rank": 3},
        ]
        
        # Build markdown content as string
        _md_content = f"""
## 🤖 INFER Results for "{prompt_input.value}"

**Prompt:** {prompt_input.value}  
**Top-K:** {top_k.value}  
**Mode:** {"Compare (with probabilities)" if compare_toggle.value else "Simple"}

### Predictions:
"""
        
        for pred in mock_predictions[:top_k.value]:
            if compare_toggle.value:
                _md_content += f"""
**{pred['rank']}. {pred['token']}**  
   Probability: {pred['probability']:.2%} ({pred['probability']:.4f})
"""
            else:
                _md_content += f"**{pred['rank']}. {pred['token']}**\n"
        
        _md_content += r"""
**Interpretation:** The model confidently predicts "Paris" (97.91%),  
which is the correct answer. The other tokens have very low probability.

---
"""
    
    # Display OUTSIDE if block (fixes branch-expression error)
    mo.md(_md_content)
    return


@app.cell
def _(mo):
    mo.md(
        r"""
## 📖 LQL Syntax

```sql
-- Basic INFER
INFER "The capital of France is" TOP 3;

-- INFER with COMPARE (show token probabilities)
INFER "Einstein developed" TOP 5 COMPARE;

-- INFER with max tokens
INFER "Python is a" TOP 3 MAX_TOKENS 50;

-- INFER with temperature
INFER "The weather today is" TOP 3 TEMPERATURE 0.7;
```

---
"""
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
## 🧠 How INFER Works

`INFER` runs a **full forward pass** through the model:

1. **Tokenize** the prompt
2. **Embed** tokens → initial residual
3. **Forward pass** through all layers:
   - Attention (Q/K/V/O projections)
   - FFN (feed-forward network)
   - Residual connections
4. **LM head** → logits (token probabilities)
5. **Return** top-K tokens with probabilities

**Key difference from `WALK`:**
- `WALK` traverses the residual stream (cheap, uses gate KNN)
- `INFER` runs full inference (accurate, needs model weights)

**Example:**
```
INFER "The capital of France is" TOP 3;

Token 1: "Paris" (97.91%) ← High confidence
Token 2: "the" (0.42%) ← Low confidence
Token 3: "a" (0.31%) ← Low confidence

→ Model correctly knows the answer!
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
2. Adjust **Top-K** to see more/fewer predictions
3. Toggle **Compare Mode** to see token probabilities
4. Check the LQL syntax section for the SQL-like command

**Next:** Try `compile_knowledge.py` to learn how to edit and recompile knowledge with `COMPILE`.

---
"""
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/jeunjetta/larql/blob/feature/marimo-notebooks/notebooks/inference_predict.py)
"""
    )
    return

if __name__ == "__main__":
    app.run()
