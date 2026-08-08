# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "numpy>=2.0.0",
#     "networkx>=3.0",
#     "plotly>=5.0",
#     "larql", # For Python bindings
# ]
# ///

# Mirrors logic from LARQL graph structure concepts (to migrate to jeunjetta/larql)

import marimo

__generated_with = "0.23.15"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    from pathlib import Path
    import larql
    from _vindex_helper import get_vindex_path, setup_hint_md, check_setup
    return mo, np, Path, larql, get_vindex_path, setup_hint_md, check_setup


@app.cell
def _(mo):
    is_script_mode = mo.app_meta().mode == "script"
    return (is_script_mode,)


@app.cell
def _(mo):
    mo.md(
        r"""
# 🕸️ Graph Structure — Knowledge as a Graph

*Learn how LARQL represents model knowledge as a queryable graph database.*

---
"""
    )
    return


@app.cell
def _(mo, is_script_mode):
    mo.md(
        r"""
## 🧠 The Core Abstraction

**LARQL treats a transformer model as a graph database:**

```
Nodes = Entities (France, Einstein, Python)
Edges = Knowledge (entity --[relation]--> target)
Weights = Scores (how strongly the model knows this fact)
Layers = Depth (where in the model this knowledge lives)
```

**Key insight:** The model's **gate vectors** (W_gate rows) encode knowledge as feature activations. When you `DESCRIBE "France"`, LARQL:
1. Converts "France" to a residual vector (embedding)
2. Finds top-k activated features at each layer (KNN search)
3. Decodes features → edges (relation, target, score)

---
"""
    )
    return


@app.cell
def _(mo):
    # Entity selector
    entity_input = mo.ui.text(
        value="France",
        label="🔤 Entity to Explore",
        placeholder="Enter an entity (e.g., France, Einstein, Python)",
    )
    entity_input
    return (entity_input,)


@app.cell
def _(mo, check_setup, get_vindex_path, setup_hint_md):
    setup_status = check_setup()
    vindex_path = get_vindex_path()

    _options = [("🎭 Mock Data", "mock")]
    if vindex_path and setup_status["larql_available"]:
        _options.insert(0, ("🧠 Real Vindex", "real"))
    
    data_source_select = mo.ui.dropdown(
        options=_options,
        value=_options[0], # Default to real if available, else mock
        label="⚙️ Data Source",
    )
    
    if not setup_status["larql_available"]:
        mo.md(setup_hint_md()) # Show hint if larql not available
    
    data_source_select
    return (data_source_select, setup_status, vindex_path)


@app.cell
def _(mo, is_script_mode, data_source_select, vindex_path, larql, entity_input):
    _edges = []
    _source_info = ""

    if is_script_mode or data_source_select.value == "mock":
        _edges = [
            {"relation": "capital", "target": "Paris", "score": 1436.9, "layer": 27},
            {"relation": "language", "target": "French", "score": 35.2, "layer": 24},
            {"relation": "continent", "target": "Europe", "score": 14.4, "layer": 25},
            {"relation": "borders", "target": "Spain", "score": 13.3, "layer": 18},
            {"relation": "currency", "target": "Euro", "score": 8.7, "layer": 22},
            {"relation": "capital", "target": "Paris", "score": 1200.5, "layer": 26},
            {"relation": "language", "target": "French", "score": 42.1, "layer": 23},
            {"relation": "neighbor", "target": "Italy", "score": 11.2, "layer": 20},
        ]
        _source_info = "🎭 Mock Data"
    elif data_source_select.value == "real" and vindex_path:
        try:
            vindex = larql.load(str(vindex_path))
            real_entity = entity_input.value
            real_edges = vindex.describe(real_entity, verbose=True)
            _edges = [
                {
                    "relation": e.relation or "unspecified",
                    "target": e.target,
                    "score": e.score,
                    "layer": e.layer,
                }
                for e in real_edges
            ]
            _source_info = f"🧠 Real Vindex: {vindex_path.name} (described '{real_entity}')"
        except Exception as e:
            mo.md(f"❌ Error loading real vindex: {e}. Falling back to mock data.")
            _edges = [
                {"relation": "capital", "target": "Paris", "score": 1436.9, "layer": 27},
                {"relation": "language", "target": "French", "score": 35.2, "layer": 24},
                {"relation": "continent", "target": "Europe", "score": 14.4, "layer": 25},
                {"relation": "borders", "target": "Spain", "score": 13.3, "layer": 18},
                {"relation": "currency", "target": "Euro", "score": 8.7, "layer": 22},
                {"relation": "capital", "target": "Paris", "score": 1200.5, "layer": 26},
                {"relation": "language", "target": "French", "score": 42.1, "layer": 23},
                {"relation": "neighbor", "target": "Italy", "score": 11.2, "layer": 20},
            ]
            _source_info = "🎭 Mock Data (fallback due to error)"

    mo.md(f"**Data Source:** {_source_info}")

    # Calculate min/max layers and options for filters
    _min_layer = 0
    _max_layer = 33 
    if _edges:
        _min_layer = min(e["layer"] for e in _edges)
        _max_layer = max(e["layer"] for e in _edges)
    
    relation_options = ["All"] + sorted(list(set(e["relation"] for e in _edges if e["relation"] is not None))) # Filter out None relations
    highlight_options = ["None"] + sorted(list(set(e["relation"] for e in _edges if e["relation"] is not None))) # Filter out None relations

    # Define UI elements directly in this cell
    layer_range = mo.ui.range_slider(
        start=_min_layer,
        stop=_max_layer,
        step=1,
        value=(_min_layer, _max_layer),
        label="📊 Layer Range Filter"
    )
    layer_range

    relation_filter = mo.ui.dropdown(
        options=relation_options,
        value="All",
        label="🔗 Relation Type Filter"
    )
    relation_filter

    highlight_relation = mo.ui.dropdown(
        options=highlight_options,
        value="None",
        label="✨ Highlight Relation"
    )
    highlight_relation

    return _edges, layer_range, relation_filter, highlight_relation


@app.cell
def _(mo, entity_input, _edges, layer_range, relation_filter, highlight_relation):
    # Apply filters to _edges
    _filtered = _edges

    # Filter by layer range
    _layer_start, _layer_end = layer_range.value
    _filtered = [e for e in _filtered if _layer_start <= e["layer"] <= _layer_end]

    # Filter by relation type
    if relation_filter.value != "All":
        _filtered = [e for e in _filtered if e["relation"] == relation_filter.value]

    _content_parts = []
    _content_parts.append(f"""
## 📊 Graph View: Edges for "{entity_input.value}"
[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/jeunjetta/larql/blob/feature/marimo-notebooks/notebooks/02_graph_structure.py)

This section displays the knowledge edges (facts) extracted for the entity you entered, applying any filters you've set. The table shows the raw edges, and the interactive graph below visualizes them as nodes and connections.

### Basic Exercises:
1.  **Change Entity:** Type `Einstein` in the input field above and observe how the edges change. What new relations appear?
2.  **Filter by Layer:** Use the `Layer Range Filter` to see edges found only in specific layers (e.g., layers 20-25). How does this affect the graph and table?
3.  **Filter by Relation:** Select `capital` from the `Relation Type Filter`. What entities are connected by this relation for `France`?

### Challenge Exercises:
1.  **Combined Filters:** Find all `language` relations for `France` within layers 20-25. How many edges are left?
2.  **Unknown Entity:** Try entering an entity you expect the model *not* to know (e.g., `Zzzyyxx`). What happens to the graph and table? Why?

### Observation Questions:
- How does changing the `Entity to Explore` affect the `Edges found` count?
- What insights can you gain by filtering edges by `Layer`? Does certain knowledge appear to be concentrated in specific layers?
- In the interactive graph, how do `Score` and `Layer` (shown on hover) contribute to understanding the strength and origin of a knowledge edge?

| Relation | Target | Score | Layer | Source |
|-----------|--------|-------|-------|--------|
"""
)

    for e in _filtered:
        _content_parts.append(f"| **{e['relation']}** | {e['target']} | {e['score']:.1f} | L{e['layer']} | probe |\n")

    _content_parts.append(r"""
---

**Edge attributes:**
- `relation` — The type of knowledge (capital, language, ...)
- `target` — The related entity
- `score` — Activation strength (higher = stronger knowledge)
- `layer` — Model layer where this knowledge was found
- `source` — How this edge was discovered (probe, explicit, ...)


"""
)
    
    _content = "".join(_content_parts)
    mo.md(_content)
    return
@app.cell
def _(mo, entity_input, _edges, layer_range, relation_filter, highlight_relation):
    # Build networkx graph for visualization (computes filtered data independently)
    import networkx as nx
    import plotly.graph_objects as go
    
    # Apply filters to get _filtered
    _filtered = _edges
    _layer_start, _layer_end = layer_range.value
    _filtered = [e for e in _filtered if _layer_start <= e["layer"] <= _layer_end]
    if relation_filter.value != "All":
        _filtered = [e for e in _filtered if e["relation"] == relation_filter.value]
    
    G = nx.DiGraph()
    
    # Add nodes and edges from FILTERED data
    source_entity = entity_input.value
    G.add_node(source_entity, type='source')
    for _e in _filtered:
        target = _e['target']
        G.add_node(target, type='target')
        G.add_edge(source_entity, target,
                   relation=_e['relation'],
                   score=_e['score'],
                   layer=_e['layer'])

    # Use spring layout for positioning
    pos = nx.spring_layout(G, k=2, iterations=50, seed=42)

    data_traces = []

    # Create edge traces (separated for highlighting)
    default_edge_x = []
    default_edge_y = []
    default_edge_text = []

    highlighted_edge_x = []
    highlighted_edge_y = []
    highlighted_edge_text = []

    for u, v, data in G.edges(data=True):
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        
        edge_trace_line = [x0, x1, None]
        edge_trace_text = f"{data['relation']} (L{data['layer']}, score={data['score']:.1f})"

        if highlight_relation.value != "None" and data['relation'] == highlight_relation.value:
            highlighted_edge_x.extend(edge_trace_line)
            highlighted_edge_y.extend(edge_trace_line) # Y coordinates use same structure
            highlighted_edge_text.append(edge_trace_text)
        else:
            default_edge_x.extend(edge_trace_line)
            default_edge_y.extend(edge_trace_line) # Y coordinates use same structure
            default_edge_text.append(edge_trace_text)

    if default_edge_x:
        data_traces.append(go.Scatter(
            x=default_edge_x, y=default_edge_y,
            line=dict(width=2, color='#888'),
            hoverinfo='none',
            mode='lines',
            showlegend=False # Hide from legend if only one type of edge
        ))
    
    if highlighted_edge_x:
        data_traces.append(go.Scatter(
            x=highlighted_edge_x, y=highlighted_edge_y,
            line=dict(width=2, color='#FFC300'), # Highlight color (yellow)
            hoverinfo='none',
            mode='lines',
            showlegend=False # Hide from legend
        ))

    # Create node trace
    node_x = []
    node_y = []
    node_text = []
    node_color = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(node)
        if node == source_entity:
            node_color.append('#FF6B6B')  # Red for source
        else:
            node_color.append('#4ECDC4')  # Teal for targets

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        hoverinfo='text',
        text=node_text,
        textposition='top center',
        marker=dict(
            showscale=False,
            color=node_color,
            size=20,
            line=dict(width=2, color='white')
        )
    )
    data_traces.append(node_trace)

    # Create figure
    fig = go.Figure(
        data=data_traces,
        layout=go.Layout(
            title=dict(
                text=f'Knowledge Graph: "{source_entity}"',
                font=dict(size=16)
            ),
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20, l=5, r=5, t=40),
            annotations=[dict(
                text="Red=Source Entity, Teal=Target Entities<br>Yellow=Highlighted Relation<br>Hover over edges to see relation details",
                showarrow=False,
                xref="paper", yref="paper",
                x=0.005, y=-0.002,
                xanchor='left', yanchor='bottom',
                font=dict(size=10)
            )],
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            height=500
        )
    )

    mo.md(r"""
### Interactive Graph Visualization

*Network representation of knowledge edges. Hover over edges to see relation details.*
"""
    )
    mo.ui.plotly(fig)
    return


@app.cell
def _(mo):
    mo.md(
        r"""
## 🏗️ Vindex as a Graph Database

A **vindex** is a graph database with these tables:

### Nodes (Entities)
```
Table: entities
- id: INTEGER PRIMARY KEY
- name: TEXT (e.g., "France", "Paris")
- embedding: BLOB (residual vector, 2560-dim f16)
```

### Edges (Knowledge)
```
Table: edges
- entity: TEXT (source entity)
- relation: TEXT (relation type)
- target: TEXT (target entity)
- score: REAL (activation strength)
- layer: INTEGER (model layer)
- source: TEXT (discovery method)
```

### Features (Activations)
```
Table: features
- layer: INTEGER
- feature_idx: INTEGER
- top_token: TEXT (what this feature detects)
- c_score: REAL (confidence score)
```

---
"""
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
## 🔍 LQL: SQL for the Knowledge Graph

LQL (Lazarus Query Language) is SQL-like syntax for querying the graph:

### DESCRIBE (Browse Knowledge)
```sql
-- Get all edges for an entity
DESCRIBE "France";

-- With layer filter
DESCRIBE "France" FROM LAYER 14 TO 27;

-- Brief mode (compact output)
DESCRIBE "France" BRIEF;
```

### SELECT (Query Graph)
```sql
-- Get all edges with a specific relation
SELECT * FROM edges WHERE relation = "capital";

-- Join entities and edges
SELECT e.name, r.relation, e2.name
FROM entities e
JOIN edges r ON e.name = r.entity
JOIN entities e2 ON r.target = e2.name;

-- With limits
SELECT * FROM edges LIMIT 10;
```

### WALK (Traverse Graph)
```sql
-- Walk from an entity through relations
WALK "The capital of France is" TOP 5;

-- Returns: [(entity, relation, target, score), ... ]
```

---
"""
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
---

## 💡 Knowledge Check: Graph Structure

Let's test your understanding of LARQL's graph representation!

**Question 1:** In LARQL's graph abstraction, what do **nodes** primarily represent?
"""
    )


@app.cell
def _(mo):
    q1_options = {
        "entities": "correct",
        "relations": "incorrect1",
        "scores": "incorrect2",
        "layers": "incorrect3",
    }
    q1_radio = mo.ui.radio(q1_options, label="Select your answer:")
    q1_radio
    return q1_radio, mo

@app.cell
def _(q1_radio, mo):
    _content = ""
    if q1_radio.value == "correct":
        _content = "🎉 **Correct!** Entities are the nodes in LARQL's knowledge graph."
    elif q1_radio.value:
        _content = "❌ **Incorrect.** Review the 'Core Abstraction' section to recall what nodes represent."
    mo.md(_content)
    return

if __name__ == "__main__":
    app.run()