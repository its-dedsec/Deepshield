from __future__ import annotations

from datetime import datetime
from math import ceil
from pathlib import Path
from typing import Sequence

try:
    import numpy as np
except Exception:  # pragma: no cover
    np = None

from PIL import Image, ImageDraw


def generate_report(
    faces: Sequence[Image.Image] | Sequence[np.ndarray],
    predictions: Sequence[float],
    filename: str,
    decision: str,
    output_path: str | Path = "report.png",
) -> str:
    """Create an image grid report and save it."""
    imgs = []
    for face in faces:
        if isinstance(face, Image.Image):
            img = face.copy()
        else:
            if np is not None:
                img = Image.fromarray(np.asarray(face))
            else:
                img = Image.fromarray(face)
        imgs.append(img.resize((128, 128)))

    cols = min(4, len(imgs)) or 1
    rows = ceil(len(imgs) / cols)
    report = Image.new("RGB", (cols * 128, rows * 128 + 40), "white")
    draw = ImageDraw.Draw(report)

    for i, (img, pred) in enumerate(zip(imgs, predictions)):
        x = (i % cols) * 128
        y = (i // cols) * 128
        report.paste(img, (x, y))
        draw.text((x + 4, y + 4), f"{pred:.2f}", fill="red")

    text = f"{filename} - {datetime.utcnow().isoformat()} - {decision}"
    draw.text((5, rows * 128 + 10), text, fill="black")
    report.save(str(output_path))
    return str(output_path)

