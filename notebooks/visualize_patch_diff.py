# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "plotly>=5.0.0",
#     "numpy>=2.0.0",
#     "pandas>=2.0.0",
# ]
# ///

import marimo

__generated_with = "0.23.9"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import plotly.graph_objects as go
    import pandas as pd
    import numpy as np
    return go, mo, np, pd


@app.cell
def _(mo):
    mo.md(
        r"""[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/jeunjetta/larql/blob/feature/marimo-notebooks/notebooks/visualize_patch_diff.py)
"""
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
# 🔄 Patch Diff Visualization

*Visualize the difference between a base vindex and a patched vindex — see what changes when you INSERT/DELETE/UPDATE.*

LARQL's patch system lets you make changes without modifying the original vindex.
This notebook shows what those changes look like.
"""
    )
    return


@app.cell
def _(mo):
    is_script_mode = mo.app_meta().mode == "script"
    return (is_script_mode,)


@app.cell
def _(mo):
    mo.md(
        r"""
## 🎯 How Patches Work

1. **Start with base vindex** — read-only, never modified
2. **Begin a patch** — `BEGIN PATCH "my_changes"`
3. **Make changes** — `INSERT`, `DELETE`, `UPDATE` statements
4. **Save patch** — `SAVE PATCH` writes a `.vlp` JSON file
5. **Apply patch** — `COMPILE CURRENT INTO VINDEX` bakes changes into new vindex

Let's visualize what happens at each step!
"""
    )
    return


@app.cell
def _(mo):
    patch_name_input = mo.ui.text(
        value="demo_patch",
        label="📝 Patch Name",
        placeholder="Enter patch name...",
    )
    show_diff_button = mo.ui.run_button(label="🔍 Show Patch Diff")
    patch_name_input, show_diff_button
    return patch_name_input, show_diff_button


@app.cell
def _(is_script_mode, np, patch_name_input, show_diff_button):
    # Generate mock base vs patched data
    np.random.seed(42)

    # Mock base vindex: 100 features across 5 layers
    num_layers = 5
    features_per_layer = 20

    base_data = []
    for layer in range(num_layers):
        for feat_idx in range(features_per_layer):
            base_data.append(
                {
                    "layer": layer,
                    "feature": f"feature_{layer}_{feat_idx}",
                    "target": f"entity_{np.random.randint(0, 10)}",
                    "score": np.random.uniform(0.3, 0.9),
                    "in_patch": False,
                }
            )

    # Mock patch: modify 10% of features (DELETE 5, UPDATE 5)
    patch_data = base_data.copy()
    num_modifications = 10

    if is_script_mode or show_diff_button.value:
        # Select random features to modify
        modify_indices = np.random.choice(
            len(base_data), size=num_modifications, replace=False
        )

        for idx in modify_indices[:5]:  # DELETE first 5
            patch_data[idx]["in_patch"] = True
            patch_data[idx]["operation"] = "DELETE"

        for idx in modify_indices[5:]:  # UPDATE last 5
            patch_data[idx]["in_patch"] = True
            patch_data[idx]["operation"] = "UPDATE"
            patch_data[idx]["score"] = np.random.uniform(0.8, 1.0)  # Boost score
            patch_data[idx]["target"] = f"entity_{np.random.randint(10, 15)}"  # New target

    return base_data, patch_data


@app.cell
def _(mo, base_data, patch_data):
    mo.md(
        r"""
## 📊 Base vs Patched Comparison

Features modified by the patch are highlighted.
"""
    )

    # Build comparison table
    diff_data = []
    for base, patched in zip(base_data, patch_data):
        if patched.get("in_patch", False):
            diff_data.append(
                {
                    "Layer": base["layer"],
                    "Feature": base["feature"],
                    "Operation": patched.get("operation", ""),
                    "Base Target": base["target"],
                    "Patched Target": patched["target"],
                    "Base Score": f"{base['score']:.3f}",
                    "Patched Score": f"{patched['score']:.3f}",
                }
            )

    mo.ui.table(diff_data[:20])  # Show first 20 diffs
    return


@app.cell
def _(go, np, base_data, patch_data):
    mo.md(
        r"""
## 📈 Score Distribution Before/After

Compare the score distributions of base vs patched features.
"""
    )

    # Extract scores
    base_scores = [d["score"] for d in base_data]
    patched_scores = [d["score"] for d in patch_data if d.get("in_patch", False)]

    # Create histogram comparison
    fig = go.Figure()

    fig.add_trace(
        go.Histogram(
            x=base_scores,
            name="Base",
            opacity=0.7,
            nbinsx=20,
            marker_color="blue",
        )
    )

    if patched_scores:
        fig.add_trace(
            go.Histogram(
                x=patched_scores,
                name="Patched",
                opacity=0.7,
                nbinsx=20,
                marker_color="red",
            )
        )

    fig.update_layout(
        title="Score Distribution: Base vs Patched",
        xaxis_title="Score",
        yaxis_title="Count",
        barmode="overlay",
    )

    mo.ui.plotly(fig)
    return


@app.cell
def _(mo, base_data, patch_data):
    mo.md(
        r"""
## 💡 Try It Yourself

### Exercises:
1. **Change patch name** — How does this affect the visualization?
2. **Click "Show Patch Diff"** — What happens when you apply the same patch twice?
3. **Observe**: Which features were modified? Are they clustered in certain layers?

### Observation Questions:
- Do DELETE operations tend to target low-score features?
- Do UPDATE operations boost scores? Why might this be useful?
- How would you visualize an INSERT operation (not shown here)?
"""
    )
    return


if __name__ == "__main__":
    app.run()
