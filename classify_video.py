import sys

def classify_frame_results(frame_results):
    """Return 'DEEPFAKE' if more than half of frames are fake."""
    fake_frames = sum(1 for is_fake in frame_results if is_fake)
    return "DEEPFAKE" if fake_frames > len(frame_results) / 2 else "REAL"


def parse_frame_file(path):
    """Parse file with one result per line (1/0 or True/False)."""
    results = []
    with open(path, 'r') as f:
        for line in f:
            token = line.strip().lower()
            if token in {"1", "true", "yes", "fake"}:
                results.append(True)
            elif token in {"0", "false", "no", "real"}:
                results.append(False)
            else:
                raise ValueError(f"Unrecognized frame label: {line.strip()}")
    if not results:
        raise ValueError("No frame data provided")
    return results


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python classify_video.py <frame_results_file>")
        sys.exit(1)
    frames = parse_frame_file(sys.argv[1])
    print(classify_frame_results(frames))
