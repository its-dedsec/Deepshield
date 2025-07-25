from typing import Iterable

try:
    import numpy as np
except Exception:  # pragma: no cover
    np = None


def _to_float_list(obj):
    if np is not None:
        arr = np.asarray(obj, dtype="float32")
        return arr.reshape(-1).tolist()
    if isinstance(obj, (list, tuple)):
        vals = []
        for v in obj:
            vals.extend(_to_float_list(v))
        return vals
    return [float(obj)]


def classify_faces(faces, model):
    """Classify each cropped face using ``model`` and return prediction scores."""
    preds = []
    for face in faces:
        if hasattr(model, "predict"):
            out = model.predict([face])[0]
        else:
            out = model([face])[0]
        if isinstance(out, (list, tuple)):
            score = float(out[0])
        else:
            score = float(out)
        preds.append(score)
    return preds

