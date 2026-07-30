# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "numpy>=2.0.0",
# ]
# ///

# Mirrors logic from docs/README.md in chrishayuk/larql (to migrate to jeunjetta/larql)

import marimo

__generated_with = "0.23.15"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    return mo, np


@app.cell
def _(mo):
    is_script_mode = mo.app_meta().mode == "script"
    return (is_script_mode,)


@app.cell
def _(mo, is_script_mode):
    mo.md(
        r"""
# 🚀 LARQL Deployment Architecture

*Learn how to deploy LARQL vindexes as servers, slice models for client/server architectures, and stream tokens via WebSocket.*

---

## Overview

LARQL supports flexible deployment architectures:
- **Standalone server** — `larql serve` hosts a vindex over HTTP + gRPC
- **Client/server split** — `larql slice` carves a model into attention (client) + FFN (server) slices
- **WebSocket streaming** — real-time token-by-token generation
- **MoE expert sharding** — serve Mixture-of-Experts models across multiple machines

This notebook demonstrates these deployment patterns with mock examples.
"""
    )
    return


@app.cell
def _(mo):
    mo.md(r"""## 🎛️ Deployment Tradeoff Explorer
""")
    return


@app.cell
def _(mo):
    strategy_select = mo.ui.dropdown(
        options=["Standalone", "Sliced (Attention on Client)", "MoE Sharding"],
        value="Standalone",
        label="Deployment Strategy",
    )
    strategy_select
    return (strategy_select,)


@app.cell
def _(mo, strategy_select, np):
    mo.md(r"""### 📊 Performance Estimates (Mock Data)""")
    
    strategy = strategy_select.value
    
    if strategy == "Standalone":
        latency = "120ms"
        cost = "$0.001 / 1K tokens"
        scalability = "Single machine (vertical scaling)"
        _details = "Simple to deploy, but requires full model weights on one machine."
    elif strategy == "Sliced (Attention on Client)":
        latency = "45ms (client) + 80ms (server)"
        cost = "$0.0007 / 1K tokens"
        scalability = "Client + Server (horizontal scaling)"
        _details = "Reduces client RAM by ~60%, but adds network round-trip."
    else:  # MoE Sharding
        latency = "30ms (parallel experts)"
        cost = "$0.0005 / 1K tokens"
        scalability = "Distributed across 8 machines"
        _details = "Best for large MoE models (e.g., GPT-OSS). Requires orchestration."
    
    _table = mo.ui.table([
        {"Metric": "Latency", "Value": latency},
        {"Metric": "Cost (Mock)", "Value": cost},
        {"Metric": "Scalability", "Value": scalability},
        {"Metric": "Notes", "Value": _details},
    ])
    _table
    return


@app.cell
def _(mo):
    mo.md(r"""## 🖥️ Server Deployment with `larql serve`""")
    return


@app.cell
def _(mo, is_script_mode):
    mo.md(
        r"""
### Basic Server Setup

```bash
# Start a server hosting a vindex
larql serve gemma3-4b.vindex --port 8080
```

The server provides:
- **HTTP API** — `POST /v1/chat/completions` (OpenAI-compatible)
- **gRPC API** — high-performance binary protocol
- **WebSocket streaming** — `WS /v1/stream` for token-by-token generation

### Server Configuration Options

```bash
larql serve gemma3-4b.vindex \
  --port 8080 \
  --host 0.0.0.0 \
  --f16-wire        # Use f16 wire format (50% bandwidth)
```
"""
    )
    return


@app.cell
def _(mo):
    mo.md(r"""## ✂️ Model Slicing with `larql slice`""")
    return


@app.cell
def _(mo, is_script_mode):
    mo.md(
        r"""
### Client/Server Architecture

For large models, you can split the workload:
- **Client** — runs attention locally (laptop/edge device)
- **Server** — holds FFN weights (remote machine with more RAM)

```bash
# Extract once
larql extract google/gemma-4-31b-it -o gemma4-31b.vindex --quant q4k

# Create client slice (7.4 GB for 31B Q4_K)
larql slice gemma4-31b.vindex --preset client -o gemma4-31b.client.vindex

# Create server slice (27 GB — gate + FFN)
larql slice gemma4-31b.vindex --preset server -o gemma4-31b.server.vindex

# Start server (holds FFN weights)
larql serve gemma4-31b.server.vindex --port 8080 --ffn-only

# Run client (attention locally, FFN over network)
larql run gemma4-31b.client.vindex \
  --ffn http://server.local:8080 \
  "The capital of France is"
```

### Available Presets

| Preset | Description | Size (31B Q4_K) |
|---------|-------------|-------------------|
| `client` | Attention + embed + norms | 7.4 GB |
| `server` | Gate + interleaved FFN + down_meta | 27 GB |
| `browse` | DESCRIBE/WALK only | ~3 GB |
| `router` | MoE router weights only | Small |
| `expert-server` | MoE expert weights (CPU-only) | Varies |
| `all` | Full clone | 34 GB |

Use `larql slice --help` to see the full list of parts.
"""
    )
    return


@app.cell
def _(mo):
    mo.md(r"""## 📡 WebSocket Streaming""")
    return


@app.cell
def _(mo, is_script_mode):
    mo.md(
        r"""
### Real-Time Token Streaming

LARQL supports WebSocket streaming for real-time token generation:

```javascript
// Connect to WebSocket endpoint
const ws = new WebSocket("ws://localhost:8080/v1/stream");

// Send generation request
ws.send(JSON.stringify({
    type: "generate",
    prompt: "The capital of France is",
    max_tokens: 50
}));

// Receive tokens one-by-one
ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.type === "token") {
        console.log(`Token ${data.index}: ${data.text}`);
    } else if (data.type === "done") {
        console.log(`Done! ${data.tokens} tokens, ${data.latency_ms}ms`);
    }
};

// Abort mid-generation
ws.send(JSON.stringify({type: "cancel"}));
```

### Server-Sent Events (SSE)

Alternatively, use SSE on the HTTP endpoint:

```bash
curl -X POST http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemma3-4b",
    "messages": [{"role": "user", "content": "Hello"}],
    "stream": true
  }'
```

Each token arrives as a separate SSE event.
"""
    )
    return


@app.cell
def _(mo):
    mo.md(r"""## 🧩 MoE Expert Sharding""")
    return


@app.cell
def _(mo, is_script_mode):
    mo.md(
        r"""
### Serving MoE Models Across Multiple Machines

For Mixture-of-Experts models (Gemma 4 26B A4B, Mixtral, etc.), expert weights can be served from **CPU-only machines with no GPU**:

```bash
# Extract MoE model
larql extract google/gemma-4-26b-it -o gemma4-26b.vindex --quant q4k

# Create expert server slices
larql slice gemma4-26b.vindex \
  --preset expert-server \
  --experts 0-31 \
  -o gemma4-26b.experts-0-31.vindex

# Start expert servers (CPU-only machines)
larql serve gemma4-26b.experts-0-31.vindex --port 8081 --expert-only
larql serve gemma4-26b.experts-32-63.vindex --port 8082 --expert-only

# Router coordinates experts
larql serve gemma4-26b.vindex \
  --port 8080 \
  --expert-endpoints http://server1:8081,http://server2:8082
```

### Benefits

- **Cost-effective** — Experts run on CPU-only machines (no expensive GPUs)
- **Scalable** — Add more expert servers as needed
- **Fault-tolerant** — Router can retry failed expert calls
"""
    )
    return


@app.cell
def _(mo):
    mo.md(r"""## 🧪 Try It Yourself""")
    return


@app.cell
def _(mo, is_script_mode):
    mo.md(
        r"""
### Exercises

1. **Server Simulation**
   - Imagine you have a 31B model extracted
   - Calculate the client vs server slice sizes for Q4_K quantization
   - Answer: Client = 7.4 GB, Server = 27 GB

2. **WebSocket Flow**
   - List the 3 message types in the WebSocket protocol
   - Answer: `generate`, `token`, `done` (plus `cancel`)

3. **MoE Architecture**
   - Why can expert weights run on CPU-only machines?
   - Answer: Experts are dense FFN layers that don't need attention computation

### Observation Questions

- When would you use client/server slicing vs a standalone server?
- What are the tradeoffs of WebSocket streaming vs SSE?
- Why is MoE expert sharding particularly cost-effective?
"""
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
---

## 📚 Summary

In this notebook, you learned:
- ✅ How to start a LARQL server with `larql serve`
- ✅ How to split models with `larql slice` for client/server deployment
- ✅ How to stream tokens via WebSocket
- ✅ How to shard MoE experts across multiple machines

### Next Steps

- Deploy a real vindex with `larql serve`
- Try client/server architecture with a large model
- Experiment with WebSocket streaming in your applications

[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/jeunjetta/larql/blob/feature/marimo-notebooks/notebooks/09_deployment.py)
"""
    )
    return


if __name__ == "__main__":
    app.run()
