# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "plotly>=5.0.0",
#     "numpy>=2.0.0",
# ]
# ///

import marimo

__generated_with = "0.23.13"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import plotly.graph_objects as go
    import numpy as np
    return go, mo, np


@app.cell
def _(mo):
    mo.md(
        r"""[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/jeunjetta/larql/blob/feature/marimo-notebooks/notebooks/visualize_walk_path.py)
"""
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
# 🚶 Walk Path Visualization

*Visualize how LARQL's WALK statement traverses the knowledge graph — from prompt to prediction.*

WALK starts at a prompt's residual vector and follows the highest-activated gates
layer-by-layer, building a path through the knowledge graph.
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
## 🎯 How WALK Works

1. **Start with a prompt** — `"What is the capital of France?"`
2. **Tokenize + embed** — convert to residual vector
3. **Gate KNN at each layer** — find top-k activated features
4. **Follow edges** — trace which entities/concepts are activated
5. **Build path** — sequence of (layer, feature, target) tuples

Let's visualize this step by step!
"""
    )
    return


@app.cell
def _(mo):
    prompt_input = mo.ui.text(
        value="capital of France",
        label="📝 Prompt",
        placeholder="Enter a prompt...",
    )
    top_k_slider = mo.ui.slider(
        start=1,
        stop=10,
        value=5,
        label="Top-K features per layer",
    )
    prompt_input, top_k_slider
    return prompt_input, top_k_slider


@app.cell
def _(is_script_mode, np, prompt_input, top_k_slider):
    # Generate mock walk path
    np.random.seed(42)

    # Simulate a walk path: 5 layers, each with top_k features
    num_layers = 5
    top_k = top_k_slider.value if not is_script_mode else 3

    walk_path = []
    for _layer_mock in range(num_layers):
        for _rank_mock in range(top_k):
            walk_path.append(
                {
                    "layer": _layer_mock,
                    "rank": _rank_mock,
                    "feature": f"feature_{_layer_mock}_{_rank_mock}",
                    "target": f"entity_{np.random.randint(0, 10)}",
                    "score": np.random.uniform(0.5, 1.0),
                }
            )

    # Build edges between consecutive layers
    edges = []
    for i in range(len(walk_path) - top_k):
        if walk_path[i]["layer"] < walk_path[i + top_k]["layer"]:
            edges.append(
                {
                    "source": walk_path[i]["target"],
                    "target": walk_path[i + top_k]["target"],
                    "layer": walk_path[i]["layer"],
                }
            )

    return edges, walk_path


@app.cell
def _(mo, walk_path):
    mo.md(
        r"""
## 📊 Walk Path Table

Each row shows a step in the walk — which feature was activated and what entity it points to.
"""
    )

    # Display as table
    table_data = [
        {
            "Layer": wp["layer"],
            "Rank": wp["rank"],
            "Feature": wp["feature"],
            "Target": wp["target"],
            "Score": f"{wp['score']:.3f}",
        }
        for wp in walk_path[:15]  # Show first 15 steps
    ]

    mo.ui.table(table_data)
    return


@app.cell
def _(edges, go, np, walk_path):
    mo.md(
        r"""
## 🌐 Animated Walk Path

Watch the walk propagate through layers — each frame shows one layer's activations.
"""
    )

    # Build animated scatter plot
    # X-axis: layer, Y-axis: entity index, color: score

    # Get unique entities and map to Y positions
    entities = list(set(wp["target"] for wp in walk_path))
    entity_to_y = {e: i for i, e in enumerate(entities)}

    # Build frames for animation
    frames = []
    for _layer_anim in range(5):
        layer_points = [wp for wp in walk_path if wp["layer"] == _layer_anim]

        if layer_points:
            frames.append(
                go.Frame(
                    data=[
                        go.Scatter(
                            x=[wp["layer"] for wp in layer_points],
                            y=[entity_to_y[wp["target"]] for wp in layer_points],
                            mode="markers+text",
                            marker=dict(
                                size=10,
                                color=[wp["score"] for wp in layer_points],
                                colorscale="Viridis",
                                showscale=True,
                            ),
                            text=[wp["target"] for wp in layer_points],
                            textposition="top center",
                            name=f"Layer {_layer_anim}",
                        )
                    ],
                    name=f"layer_{_layer_anim}",
                )
            )

    # Create figure with animation
    fig = go.Figure(
        data=[go.Scatter(x=[], y=[], mode="markers")],
        layout=go.Layout(
            title="Walk Path Animation (Layer-by-Layer)",
            xaxis=dict(title="Layer", range=[-0.5, 4.5]),
            yaxis=dict(title="Entity", range=[-0.5, len(entities) - 0.5]),
            updatemenus=[
                dict(
                    type="buttons",
                    showactive=False,
                    buttons=[
                        dict(
                            label="Play",
                            method="animate",
                            args=[
                                [f"layer_{i}" for i in range(5)],
                                dict(
                                    mode="immediate",
                                    transition=dict(duration=500),
                                    frame=dict(duration=500, redraw=True),
                                ),
                            ],
                        )
                    ],
                )
            ],
        ),
        frames=frames,
    )

    mo.ui.plotly(fig)
    return


@app.cell
def _(mo, walk_path):
    mo.md(
        r"""
## 💡 Try It Yourself

### Exercises:
1. **Change the prompt** — How does the walk path change for different prompts?
2. **Adjust Top-K** — What happens when you increase/decrease the number of features per layer?
3. **Observe**: Which layers have the most diverse activations?

### Observation Questions:
- Do certain entities appear repeatedly across layers?
- How does the score distribution change across layers?
"""
    )
    return


if __name__ == "__main__":
    app.run()
