# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "numpy>=2.0.0",
# ]
# ///

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
    mo.md(r"""# 📊 Extraction Levels

*Understand the three extraction levels in LARQL and which LQL operations work at each level.*
""")
    return


@app.cell
def _(mo):
    mo.md(r"""## 🎯 What are Extraction Levels?

LARQL vindexes can be extracted at three different levels, each adding more capabilities:

| Level | Size | Operations | Use Case |
|-------|------|-------------|----------|
| **Browse** | ~3 GB | DESCRIBE, WALK, SELECT | Explore knowledge graph |
| **Inference** | ~6 GB | + INFER | Run inference queries |
| **All** | ~10 GB | + COMPILE | Patch and recompile |

**Key insight**: Not all LQL statements work at all levels. Trying to COMPILE on a "browse" vindex will fail!
""")
    return


@app.cell
def _(mo):
    level_selector = mo.ui.dropdown(
        options=["Browse (~3 GB)", "Inference (~6 GB)", "All (~10 GB)"],
        value="Browse (~3 GB)",
        label="📦 Select Extraction Level",
    )
    level_selector
    return (level_selector,)


@app.cell
def _(level_selector, mo):
    _level = level_selector.value

    _content = ""

    if "Browse" in _level:
        _content = r"""
### 🔍 Browse Level

**Operations available:**
- `DESCRIBE 'entity'` - Find knowledge edges
- `WALK 'prompt' TOP N` - Walk the knowledge graph
- `SELECT ... FROM ...` - Query node/edge tables

**Operations NOT available:**
- `INFER` - Requires inference weights
- `COMPILE` - Requires full weight matrices

**Example:**
```sql
-- This works at browse level
DESCRIBE 'France' LIMIT 10;

-- This fails at browse level
INFER 'The capital of France is [MASK]';
```

**Memory footprint**: ~3 GB (gate vectors + embeddings + metadata)
"""
    elif "Inference" in _level:
        _content = r"""
### 🧠 Inference Level

**Operations available:**
- All Browse operations
- `INFER 'prompt'` - Run inference with residual tracing
- `INFER_TRACE` - Get detailed inference traces

**Operations NOT available:**
- `COMPILE` - Requires down-weight matrices

**Example:**
```sql
-- This works at inference level
DESCRIBE 'France' LIMIT 10;
INFER 'The capital of France is [MASK]';

-- This fails at inference level
COMPILE CURRENT INTO VINDEX 'output/new_index';
```

**Memory footprint**: ~6 GB (+ attention weights + layer norms)
"""
    else:
        _content = r"""
### 🔧 All Level

**Operations available:**
- All Browse + Inference operations
- `COMPILE` - Bake patches into new vindex
- `INSERT/DELETE/UPDATE` - Full mutation support
- `BEGIN PATCH / SAVE PATCH` - Patch management

**Example:**
```sql
-- Everything works at all level
DESCRIBE 'France' LIMIT 10;
INFER 'The capital of France is [MASK]';

-- Now we can compile!
COMPILE CURRENT INTO VINDEX 'output/optimized_index';
```

**Memory footprint**: ~10 GB (full weight matrices including down_weights.bin)

**Use case**: Development, patching, and recompilation workflows.
"""

    mo.md(_content)
    return


@app.cell
def _(mo, is_script_mode):
    _content = r"""
## 🔬 Interactive Exploration

Use the dropdown above to explore what operations work at each level.

**Try it yourself:**
1. Select each extraction level
2. See which LQL statements become available
3. Understand the trade-off between memory and capability
"""

    if not is_script_mode:
        _content += r"""
**Pro tip**: Start with "Browse" level for exploration. Upgrade to "Inference" or "All" only when you need those specific operations.
"""

    mo.md(_content)
    return


@app.cell
def _(mo, np, is_script_mode):
    # Mock data showing extraction level characteristics
    _levels = ["Browse", "Inference", "All"]
    _sizes = [3.0, 6.0, 10.0]  # GB
    _operations = [
        ["DESCRIBE", "WALK", "SELECT"],
        ["DESCRIBE", "WALK", "SELECT", "INFER"],
        ["DESCRIBE", "WALK", "SELECT", "INFER", "COMPILE", "INSERT/DELETE/UPDATE"],
    ]

    _content = r"""
### 📋 Extraction Level Comparison
"""

    if not is_script_mode:
        # Build table
        _table_rows = []
        for i, _ops in enumerate(_operations):
            _table_rows.append(
                f"| {_levels[i]} | {_sizes[i]} | {', '.join(_ops)} |"
            )
        
        _content += (
            r"""
| Level | Size (GB) | Key Operations |
|-------|-----------|----------------|
"""
            + "\n".join(_table_rows)
        )
    else:
        # Script mode - simple output
        _content += r"""
*Table shown in interactive mode*
"""

    mo.md(_content)
    return


@app.cell
def _(mo):
    mo.md(
        r"""
## 💡 Key Takeaways

1. **Start small**: Use "Browse" level for initial exploration (lowest memory)
2. **Scale as needed**: Upgrade only when you need specific operations
3. **Check before using**: Always verify operation support at current level
4. **Memory matters**: Each level doubles memory usage

### 🔍 Quick Check Pattern

```python
import larql

vindex = larql.load("path/to/vindex")

# Check what level this vindex supports
stats = vindex.stats()
print(f"Model: {stats['model']}")
print(f"Layers: {stats['num_layers']}")

# Try an operation
try:
    result = session.query("INFER 'test'")
    print("Inference supported!")
except Exception as e:
    print(f"Inference not supported: {e}")
```

---
"""
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/jeunjetta/larql/blob/feature/marimo-notebooks/notebooks/07_extraction_levels.py)"""
    )
    return


if __name__ == "__main__":
    app.run()
