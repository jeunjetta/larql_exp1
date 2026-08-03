# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "numpy>=2.0.0",
#     "plotly>=5.0.0",
# ]
# ///

"""Visualize Gate KNN - Interactive exploration of gate KNN results.

This notebook teaches the gate KNN concept by allowing users to:
1. Select a layer and entity
2. Visualize the top-k activated features
3. Explore feature metadata and relationships

# Mirrors logic from LARQL gate KNN in chrishayuk/larql (to migrate to jeunjetta/larql)
"""

import marimo as mo
__generated_with = "0.23.16"
app = mo.App(width="medium")


@app.cell
def _():
    """Import required libraries."""
    import marimo as mo
    import numpy as np
    import plotly.graph_objects as go
    import plotly.express as px
    from pathlib import Path

    return mo, np, go, px, Path


@app.cell
def _(mo):
    """Script mode detection."""
    is_script_mode = mo.app_meta().mode == "script"
    return (is_script_mode,)


@app.cell
def _(mo):
    """Title and description."""
    mo.md(r"""
    # 🔍 Visualize Gate KNN

    *Interactive exploration of gate KNN results — understand which features activate for different entities.*

    ## What is Gate KNN?

    Gate KNN (K-Nearest Neighbors) finds the top-k most activated features at a given layer for a given residual vector. This helps us understand:

    - Which features are most relevant for an entity
    - How features relate to tokens and concepts
    - The distribution of activations across the feature space

    Use the controls below to explore gate KNN results for different entities and layers.
    """)
    return


@app.cell
def _(mo, is_script_mode):
    """Data source selection."""
    options = ["🎭 Mock Data (Fast)", "🧠 Real Vindex (Slow)"]

    data_source = mo.ui.dropdown(
        options=options,
        value=options[0],
        label="Data Source",
    )
    data_source
    return (data_source,)


@app.cell
def _(mo, data_source, is_script_mode, Path):
    """Load or generate data."""
    use_real = (not is_script_mode) and ("Real" in data_source.value)

    # Mock entities for demo
    mock_entities = ["France", "Python", "Machine Learning", "Paris", "Neural Network"]
    mock_layers = list(range(0, 32, 4))  # Every 4th layer

    if use_real:
        try:
            import larql
            vindex_path = Path("output/gemma3-4b-v2.vindex")
            if vindex_path.is_dir():
                vindex = larql.load(str(vindex_path))
                entities = ["France", "Python", "Machine Learning"]
                layers = list(range(vindex.num_layers()))
                real_mode = True
            else:
                entities = mock_entities
                layers = mock_layers
                real_mode = False
                vindex = None
        except ImportError:
            entities = mock_entities
            layers = mock_layers
            real_mode = False
            vindex = None
    else:
        entities = mock_entities
        layers = mock_layers
        real_mode = False
        vindex = None

    return entities, layers, real_mode, vindex


@app.cell
def _(mo, entities, layers):
    """Entity and layer selection controls."""
    entity_select = mo.ui.dropdown(
        options=entities,
        value=entities[0] if entities else "France",
        label="Entity",
    )

    layer_select = mo.ui.dropdown(
        options=[str(l) for l in layers],
        value=str(layers[0]) if layers else "0",
        label="Layer",
    )

    top_k_slider = mo.ui.slider(
        start=1,
        stop=20,
        value=5,
        label="Top-K Features",
    )

    entity_select, layer_select, top_k_slider
    return entity_select, layer_select, top_k_slider


@app.cell
def _(mo, np, px, go):
    """Generate or load gate KNN results."""

    def generate_mock_knn(entity, layer, top_k):
        """Generate mock gate KNN results for demonstration."""
        np.random.seed(hash((entity, layer)) % (2**32))

        results = []
        for i in range(top_k):
            feature_idx = np.random.randint(0, 348000)
            score = np.random.exponential(scale=10.0)
            top_token = f"token_{np.random.randint(0, 262208)}"
            c_score = np.random.rand()

            results.append({
                "feature_idx": feature_idx,
                "score": score,
                "top_token": top_token,
                "c_score": c_score,
                "layer": layer,
                "entity": entity,
            })

        return results

    def get_real_knn(vindex, entity, layer, top_k):
        """Call real vindex.gate_knn()."""
        try:
            emb = vindex.embed(entity)
            hits = vindex.gate_knn(layer=layer, residual=emb.tolist(), top_k=top_k)

            results = []
            for hit in hits:
                results.append({
                    "feature_idx": hit.feature_idx,
                    "score": hit.score,
                    "top_token": hit.top_token if hasattr(hit, "top_token") else "unknown",
                    "c_score": hit.c_score if hasattr(hit, "c_score") else 0.0,
                    "layer": layer,
                    "entity": entity,
                })
            return results
        except Exception as e:
            print(f"Error calling gate_knn: {e}")
            return generate_mock_knn(entity, layer, top_k)

    return generate_mock_knn, get_real_knn


@app.cell
def _(mo, entity_select, layer_select, top_k_slider, generate_mock_knn, get_real_knn, vindex, real_mode):
    """Compute gate KNN results based on selections."""
    entity = entity_select.value
    layer = int(layer_select.value)
    top_k = top_k_slider.value

    if real_mode and vindex is not None:
        results = get_real_knn(vindex, entity, layer, top_k)
    else:
        results = generate_mock_knn(entity, layer, top_k)

    # Display info
    mo.md(f"### Gate KNN Results for `{entity}` at Layer {layer}")
    mo.md(f"**Top-{top_k} activated features:**")

    return results


@app.cell
def _(mo, go, results):
    """Visualize gate KNN results as a bar chart."""
    mo.md("### Score Bar Chart")

    # Build chart (handles empty results)
    if results:
        _feature_indices = [r["feature_idx"] for r in results]
        _scores = [r["score"] for r in results]

        _fig = go.Figure(data=[
            go.Bar(
                x=[f"F{i}" for i in _feature_indices],
                y=_scores,
                text=[f"{s:.2f}" for s in _scores],
                hovertemplate="<b>Feature %{x}</b><br>Score: %{y:.2f}<extra></extra>",
                marker_color="lightblue",
            )
        ])

        _fig.update_layout(
            title=f"Gate KNN Scores for Top-{len(results)} Features",
            xaxis_title="Feature Index",
            yaxis_title="Score",
            showlegend=False,
            height=500,
        )
    else:
        # Empty figure for no results
        _fig = go.Figure()

    mo.ui.plotly(_fig)


@app.cell
def _(mo, results):
    """Display detailed results table."""
    mo.md("### Detailed Results Table")

    # Build display content
    if results:
        _table_rows = []
        for i, r in enumerate(results):
            _table_rows.append({
                "Rank": i + 1,
                "Feature Index": r["feature_idx"],
                "Score": f"{r['score']:.4f}",
                "Top Token": r["top_token"],
                "C-Score": f"{r['c_score']:.4f}",
            })
        _display = mo.ui.table(_table_rows)
    else:
        _display = mo.md("No results to display.")

    _display


@app.cell
def _(mo, go, results):
    """Visualize feature score distribution."""
    mo.md("### Score Distribution")

    # Build display content
    if results and len(results) >= 3:
        _scores = [r["score"] for r in results]

        _fig = go.Figure(data=[
            go.Histogram(
                x=_scores,
                nbinsx=10,
                marker_color="lightblue",
                opacity=0.75,
            )
        ])

        _fig.update_layout(
            title="Distribution of Gate KNN Scores",
            xaxis_title="Score",
            yaxis_title="Count",
            height=400,
        )
        _display = mo.ui.plotly(_fig)
    else:
        _display = mo.md("Not enough results for distribution visualization (need >= 3).")

    _display


@app.cell
def _(mo):
    """Try It Yourself section."""
    mo.md(r"""
    ## 🎯 Try It Yourself

    ### Basic Exercises:
    1. Change the **Entity** to "Python" or "Machine Learning"
       - Expected: Different features activate for different entities
       - Observe: How do the top tokens change?

    2. Change the **Layer** to a deeper layer (e.g., 20+)
       - Expected: Higher layers capture more abstract concepts
       - Observe: Do the top tokens become more semantic?

    3. Increase **Top-K Features** to 10 or 20
       - Expected: More features reveal the distribution tail
       - Observe: How do scores decay from rank 1 to rank 20?

    ### Challenge Exercises:
    1. **Compare entities**: Run the same layer for two different entities. Which features are shared?

    2. **Layer progression**: Run the same entity at layers 0, 8, 16, 24, 31. How do activations evolve?

    3. **Score patterns**: Look at the score distribution histogram. Is it exponential? Gaussian?

    ### Observation Questions:
    - Which entities have the highest activation scores?
    - Do higher layers have more semantic top tokens?
    - How does the score distribution change with top-k?
    """)
    return


@app.cell
def _(mo):
    """MoLab badge."""
    mo.md(r"""
    [![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/jeunjetta/larql/blob/feature/marimo-notebooks/notebooks/visualize_gate_knn.py)
    """)
    return


if __name__ == "__main__":
    app.run()
