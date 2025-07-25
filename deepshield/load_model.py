import os
from typing import Iterable

try:
    import numpy as np
except Exception:  # pragma: no cover
    np = None

try:
    from tensorflow.keras.models import load_model as keras_load
except Exception:  # pragma: no cover - tensorflow may not be available
    keras_load = None


def _brightness_score(image) -> float:
    if np is not None:
        arr = np.asarray(image, dtype="float32")
        return float(arr.mean() / 255.0)
    # fallback without numpy
    def flatten(x: Iterable):
        for v in x:
            if isinstance(v, (list, tuple)):
                yield from flatten(v)
            else:
                yield float(v)
    vals = list(flatten(image if isinstance(image, Iterable) else [image]))
    return sum(vals) / len(vals) / 255.0 if vals else 0.0


class DummyModel:
    """Fallback model that predicts based on average brightness."""

    def predict(self, images):
        if not isinstance(images, (list, tuple)):
            images = [images]
        scores = [_brightness_score(img) for img in images]
        return [[s] for s in scores]


def load_model(model_path: str | None = None):
    """Load a TensorFlow model if available, otherwise return :class:`DummyModel`."""
    if keras_load is None or model_path is None or not os.path.exists(model_path):
        return DummyModel()
    try:
        model = keras_load(model_path, compile=False)
        return model
    except Exception:  # pragma: no cover - fallback path
        return DummyModel()

