"""Resizing helpers for course data.

The important thing here is that intensity images and label images must be
resized differently. Intensity images are interpolated and anti-aliased. Label
images must not be: interpolating between label 3 and label 7 invents label 5
along every object boundary, which produces ground truth that looks plausible
in a viewer and silently invalidates any IoU/Dice score computed against it.
"""

from __future__ import annotations

import numpy as np
from skimage.transform import resize

__all__ = ["target_shape", "downscale_image", "downscale_labels"]


def target_shape(shape, max_size: int = 512):
    """Shape that fits within ``max_size`` on both axes, preserving aspect ratio.

    Returns ``shape`` unchanged if it already fits, so this is safe to call
    unconditionally.
    """
    height, width = shape[:2]
    scale = min(max_size / height, max_size / width, 1.0)
    return (max(1, round(height * scale)), max(1, round(width * scale)))


def downscale_image(image: np.ndarray, max_size: int = 512) -> np.ndarray:
    """Downscale an intensity image, preserving dtype.

    Anti-aliased and interpolated - correct for intensity data, wrong for labels.
    """
    new_shape = target_shape(image.shape, max_size)
    if new_shape == image.shape[:2]:
        return image

    if image.ndim == 3:
        new_shape = (*new_shape, image.shape[2])

    resized = resize(
        image,
        new_shape,
        order=1,
        anti_aliasing=True,
        preserve_range=True,
    )
    return resized.astype(image.dtype)


def downscale_labels(labels: np.ndarray, max_size: int = 512) -> np.ndarray:
    """Downscale a label or mask image without inventing new labels.

    Nearest-neighbour, no anti-aliasing. Small objects can disappear entirely at
    aggressive scale factors, so the caller should check that the label count
    survived - `check_labels_survived` does exactly that.
    """
    new_shape = target_shape(labels.shape, max_size)
    if new_shape == labels.shape[:2]:
        return labels

    resized = resize(
        labels,
        new_shape,
        order=0,
        anti_aliasing=False,
        preserve_range=True,
    )
    return resized.astype(labels.dtype)


def check_labels_survived(original: np.ndarray, resized: np.ndarray) -> list[int]:
    """Return labels present in ``original`` but lost in ``resized``.

    An empty list means the downscale was lossless in the sense that matters for
    the metrics exercise.
    """
    before = set(np.unique(original)) - {0}
    after = set(np.unique(resized)) - {0}
    return sorted(before - after)
