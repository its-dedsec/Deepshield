import os
import random

try:
    import torch
    from torch import nn
except ImportError:  # torch not installed
    torch = None
    nn = None

class RandomDeepfakeModel:
    """Fallback model that randomly predicts real (0) or fake (1)."""

    def predict(self, image):
        return random.randint(0, 1)


def load_deepfake_model(model_path=None):
    """Load a pretrained deepfake detection model.

    Attempts to load a model from ``model_path`` using PyTorch. When that
    isn't possible (for example, PyTorch isn't installed or the weights
    are missing), this function returns a :class:`RandomDeepfakeModel` that
    simply returns a random prediction.
    """
    if torch is None:
        return RandomDeepfakeModel()

    if model_path and os.path.exists(model_path):
        try:
            model = torch.load(model_path, map_location="cpu")
            model.eval()
            return model
        except Exception:
            pass
    return RandomDeepfakeModel()
