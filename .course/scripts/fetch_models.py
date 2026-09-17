"""Download the cellpose model weights the day 2 notebooks use.

    pixi run fetch-models

Cellpose fetches a model (~25 MB, plus its size model) the first time it is
instantiated, into ~/.cellpose/models. Left to happen on day 2, that is every
student downloading at once on the lecture-room network, so the setup page
asks students to run this once beforehand. Idempotent: cellpose skips models
that are already cached.
"""

from cellpose import models

# Keep in sync with the model_type= arguments in notebooks/03_ml_segmentation.ipynb.
MODELS = ["cyto", "nuclei"]

for name in MODELS:
    print(f"cellpose model '{name}': ", end="", flush=True)
    models.Cellpose(model_type=name, gpu=False)
    print("ok")

print(f"Models are cached in {models.MODEL_DIR}")
