# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "huggingface_hub",
#     "numpy",
# ]
# ///

# Mirrors logic from setup.py in chrishayuk/larql (to migrate to jeunjetta/larql)
# Setup notebook for downloading vindex data

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
def _(mo, Path):
    # Auto-discover existing vindexes
    vindex_dirs = []
    candidates = [
        Path.cwd() / "output",
        Path.home() / ".cache" / "larql" / "local",
    ]
    for sp in candidates:
        if sp.is_dir():
            for d in sp.iterdir():
                if d.is_dir() and d.name.endswith(".vindex"):
                    vindex_dirs.append(d)
    
    _found_text = ""
    if vindex_dirs:
        _found_text = f"**Found existing vindexes:** {', '.join(str(d) for d in vindex_dirs)}"
    else:
        _found_text = "**No vindexes found.** Click the button below to download."
    
    mo.md(
        r"""
# ⚙️ LARQL Setup & Data Provisioning

[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/jeunjetta/larql/blob/feature/marimo-notebooks/notebooks/setup.py)

*Download the vindex data needed by other notebooks. Run this FIRST before using
notebooks that work with real model data.*

---

## What This Notebook Does

1. **Auto-discovers** existing vindex files in common locations
2. **Downloads** the Gemma 3 4B vindex from HuggingFace Hub
3. **Verifies** the download completed successfully

**Time estimate:** ~5-10 minutes (vindex is ~3GB)
"""
    )
    
    mo.md(_found_text)
    
    return vindex_dirs


@app.cell
def _(mo):
    download_button = mo.ui.run_button(label="⬇️ Download Vindex (~3GB)")
    download_button
    return (download_button,)


@app.cell
def _(download_button, mo, Path, is_script_mode):
    _status = ""
    
    if download_button.value and not is_script_mode:
        _status = "**Downloading...** This may take 5-10 minutes."
        
        try:
            from huggingface_hub import snapshot_download
            
            # Download to output directory
            output_dir = Path.cwd() / "output"
            output_dir.mkdir(exist_ok=True)
            
            vindex_path = output_dir / "gemma3-4b-v2.vindex"
            
            if not vindex_path.is_dir():
                snapshot_download(
                    repo_id="chrishayuk/gemma-3-4b-it-vindex",
                    local_dir=str(vindex_path),
                    repo_type="model",
                )
            
            _status = f"**Download complete!** Vindex saved to: `{vindex_path}`"
            
        except Exception as e:
            _status = f"**Error downloading:** {e}"
    
    mo.md(_status)
    
    return


@app.cell
def _(mo, Path):
    # Verify setup
    _vindex_path = Path.cwd() / "output" / "gemma3-4b-v2.vindex"
    
    _content = ""
    if _vindex_path.is_dir():
        _content = f"""
## ✅ Setup Complete

**Vindex location:** `{_vindex_path}`

**Next steps:**
1. Run `describe_explorer.py` to explore knowledge with `DESCRIBE`
2. Run `walk_knowledge.py` to traverse knowledge with `WALK`
3. Run `inference_predict.py` to generate text with `INFER`

---
"""
    else:
        _content = """
## ⚠️ Setup Not Complete

Run this notebook and click **Download Vindex** to enable real data in other notebooks.

(Notebooks will use mock data until setup is complete.)
"""
    
    mo.md(_content)
    return


@app.cell
def _(mo):
    mo.md(
        r"""
## 📖 About the Vindex

The **vindex** (vector index) is a directory of memory-mapped files containing:

- **Gate vectors** — knowledge activations for each layer
- **Down weights** — feed-forward network weights  
- **Embeddings** — token/entity embeddings
- **Metadata** — model config, feature labels

**Size:** ~3GB (Gemma 3 4B, extraction level: `inference`)

**Source:** [chrishayuk/gemma-3-4b-it-vindex](https://huggingface.co/chrishayuk/gemma-3-4b-it-vindex)

---
"""
    )
    return


if __name__ == "__main__":
    app.run()
