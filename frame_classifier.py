"""Utility to classify video frames as real or fake."""
from typing import List, Any


def classify_frames(frames: List[Any], model: Any) -> List[int]:
    """Classify each frame as real or fake using ``model``.

    Parameters
    ----------
    frames : list
        Sequence of frames to classify. The exact frame format is model
        dependent.
    model : object or callable
        The model used for classification. It can be a callable or an
        object providing a ``predict`` method.

    Returns
    -------
    list of int
        Predictions for each frame where ``0`` means real and ``1`` means
        fake.
    """

    predictions: List[int] = []
    for frame in frames:
        if hasattr(model, "predict"):
            result = model.predict(frame)
        else:
            result = model(frame)

        if isinstance(result, bool):
            pred = 1 if result else 0
        else:
            try:
                value = float(result)
                pred = 1 if value >= 0.5 else 0
            except (TypeError, ValueError):
                pred = int(result)
        predictions.append(pred)
    return predictions
