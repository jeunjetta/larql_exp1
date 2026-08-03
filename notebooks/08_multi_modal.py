# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "numpy>=2.0.0",
#     "plotly>=5.0.0",
# ]
# ///

import marimo

__generated_with = "0.23.16"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo
    import numpy as np
    import plotly.graph_objects as go
    from pathlib import Path
    return marimo, np, go, Path


@app.cell
def _(marimo):
    is_script_mode = marimo.app_meta().mode == "script"
    return (is_script_mode,)


@app.cell
def _(marimo):
    marimo.md(
        r"""
# 🖼️ Multi-Modal LQL

*Teach LARQL to understand images and text together — query visual concepts with LQL.*

In this notebook you'll learn:
1. How LARQL handles multi-modal input (images + text)
2. The `larql run --image` CLI workflow
3. Mock multi-modal DESCRIBE/WALK queries
4. Visualizing image-text embeddings
"""
    )
    return


@app.cell
def _(marimo, is_script_mode):
    marimo.md(
        r"""
## 🔍 How Multi-Modal Works in LARQL

LARQL models with vision support (like Gemma 3) have a **vision tower** (SigLIP) and a **projector** (`multi_modal_projector`) that map image patches to the same embedding space as text tokens.

### Key Components
| Component | Purpose | LQL Relevance |
|------------|---------|----------------|
| `vision_tower` | Encodes image into patch embeddings | Feeds into the same residual stream as text |
| `multi_modal_projector` | Maps vision embeddings to language model space | Aligns image/text in the same vector space |
| `mm_weights` | Directory with SigLIP + projector weights | Loaded via `--mm-weights` flag |

### CLI Workflow
```bash
# Run a multi-modal query
larql run \
  --model gemma-3-4b-it \
  --mm-weights output/gemma-3-4b-v2.mm-weights \
  --image "cat.jpg" \
  "Describe this image in detail"
```

### Observation Question:
- How does the `multi_modal_projector` bridge the gap between image patches and text tokens? Why is this alignment crucial for multi-modal LQL queries?

In LQL, multi-modal support means:
- `DESCRIBE 'image_embedding'` can return visual attributes
- `WALK` can traverse from image concepts to text concepts
- `EMBED` can embed both images and text into the same space
"""
    )
    return


@app.cell
def _(marimo, is_script_mode):
    marimo.md(
        r"""
## 🧪 Mock Multi-Modal Query Demo
[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/jeunjetta/larql/blob/feature/marimo-notebooks/notebooks/08_multi_modal.py)


*This demo uses mock data to show how a multi-modal LQL query would work.*
"""
    )
    return


@app.cell
def _(np, go, marimo, is_script_mode):
    marimo.md("### 1. Generate Mock Image + Text Embeddings")

    # Mock: 10 image patches + 5 text tokens, all in 2560-dim space
    np.random.seed(42)
    num_patches = 10
    num_text_tokens = 5
    hidden_size = 2560

    # Image patch embeddings (from vision tower)
    image_patches = np.random.randn(num_patches, hidden_size).astype(np.float32)
    # Text token embeddings
    text_tokens = np.random.randn(num_text_tokens, hidden_size).astype(np.float32)

    # Projected image embeddings (after projector)
    projected_patches = image_patches @ np.random.randn(hidden_size, hidden_size).astype(np.float32) * 0.1

    # Mock similarity matrix (patches vs text)
    similarity = (projected_patches @ text_tokens.T) / np.sqrt(hidden_size)

    marimo.md(
        f"""
### Observation Question:
- How does the `multi_modal_projector` (simulated by `projected_patches`) transform the raw image patches? Why is this transformation necessary for calculating similarity with text tokens?

- **Image patches**: `{num_patches}` patches from vision tower
- **Text tokens**: `{num_text_tokens}` tokens from prompt
- **Similarity shape**: `{similarity.shape}` (patches × text)
"""
    )
    return similarity, projected_patches, text_tokens


@app.cell
def _(go, marimo, similarity, is_script_mode):
    marimo.md("### 2. Visualize Patch-Text Similarity")

    # Heatmap of patch-text similarity
    fig = go.Figure(
        data=go.Heatmap(
            z=similarity,
            x=[f"token_{i}" for i in range(similarity.shape[1])],
            y=[f"patch_{i}" for i in range(similarity.shape[0])],            colorscale="Viridis",
            hoverongaps=False,
        )
    )
    fig.update_layout(
        title="Mock Patch-Text Similarity (after projection)",
        xaxis_title="Text Tokens",
        yaxis_title="Image Patches",
        width=700,
        height=500,
    )

    marimo.ui.plotly(fig)
    return


@app.cell
def _(np, marimo, projected_patches, text_tokens, is_script_mode):
    marimo.md("### 3. Mock Multi-Modal DESCRIBE")

    # Mock: find top-matching text token for each patch
    top_k = 3
    results = []
    for patch_idx in range(projected_patches.shape[0]):
        patch_emb = projected_patches[patch_idx]
        # Cosine similarity to text tokens
        sims = (patch_emb @ text_tokens.T) / (np.linalg.norm(patch_emb) * np.linalg.norm(text_tokens, axis=1) + 1e-6)
        top_indices = np.argsort(sims)[-top_k:][::-1]
        results.append(
            {
                "patch": f"patch_{patch_idx}",
                "top_tokens": [f"token_{i}" for i in top_indices],
                "scores": [float(sims[i]) for i in top_indices],
            }
        )

    # Display as table
    table_rows = []
    for r in results:
        table_rows.append(
            {
                "Patch": r["patch"],
                "Top Tokens": ", ".join(r["top_tokens"]),
                "Scores": ", ".join([f"{s:.2f}" for s in r["scores"]]),
            }
        )

    marimo.md("**Mock DESCRIBE 'image_patch' returning top-matching text tokens:**")
    marimo.ui.table(table_rows)
    return


@app.cell
def _(marimo):
    marimo.md(r"""
---

## 💡 Knowledge Check: Multi-Modal

Let's test your understanding of LARQL's multi-modal capabilities!

**Question 1:** What is the role of the `multi_modal_projector` in LARQL's multi-modal architecture?
""")
    q1_options = {
        "To extract features from raw image pixels": "incorrect1",
        "To encode text tokens into a shared embedding space": "incorrect2",
        "To align image patch embeddings with the language model's embedding space": "correct",
        "To generate new images based on text prompts": "incorrect3",
    }
    q1_radio = marimo.ui.radio(q1_options, label="Select your answer:")
    q1_radio
    return q1_radio, marimo

@app.cell
def _(q1_radio, marimo):
    if q1_radio.value == "correct":
        marimo.md("🎉 **Correct!** The projector ensures that image and text embeddings are comparable within the same vector space.")
    elif q1_radio.value:
        marimo.md("❌ **Incorrect.** Review the 'How Multi-Modal Works' section to understand the function of each component.")
    return

@app.cell
def _(marimo, is_script_mode):
    marimo.md(
        r"""
## 🎓 Try It Yourself

### Basic Exercises
1. **Change `num_patches` to 20** (in cell 4)
   - Expected: Similarity matrix becomes 20×5
   - Observe: How does patch count affect the heatmap?

2. **Change `hidden_size` to 768** (smaller embedding)
   - Expected: Embeddings are lower-dimensional
   - Observe: Does similarity become more concentrated?

### Challenge Exercises
1. **Add a second image** (mock two images, each with patches)
   - How would you compute cross-image patch similarity?
   - What LQL statement would query "images similar to this one"?

2. **Implement mock `WALK` from image to text**
   - Start at an image patch embedding
   - Walk to the most similar text token
   - Then walk to the next most similar patch
   - Visualize the walk path

### Observation Questions
- Which patches have the highest similarity to text tokens?
- Would real image patches (edges, textures) show different similarity patterns?
- How does the projector alignment affect multi-modal query accuracy?
"""
    )
    return


@app.cell
def _(marimo):
    marimo.md(
        r"""
## 🚀 Next Steps

1. **Try with a real multi-modal model** (if you have `mm_weights` downloaded):
   ```bash
   larql run \
     --model gemma-3-4b-it \
     --mm-weights output/gemma-3-4b-v2.mm-weights \
     --image "your_image.jpg" \
     "Describe this image"
   ```

2. **Explore the vision tower** in `crates/larql-models/src/encoders/vision_tower.rs`

3. Read the design doc: `docs/multi-modal.md`
"""
    )
    return


if __name__ == "__main__":
    app.run()
