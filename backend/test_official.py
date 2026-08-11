import torch
import numpy as np

from decord import VideoReader, cpu
from PIL import Image

from transformers import (
    VideoMAEForVideoClassification,
    VideoMAEImageProcessor
)


MODEL_NAME = "Vansh180/VideoMae-ffc23-deepfake-detector"


print("Loading model...")

model = VideoMAEForVideoClassification.from_pretrained(
    MODEL_NAME
)

processor = VideoMAEImageProcessor.from_pretrained(
    MODEL_NAME
)

model.eval()


# ==========================================
# Load video exactly like model card
# ==========================================

video_path = "uploads/fake_test.mp4"

vr = VideoReader(
    video_path,
    ctx=cpu(0)
)

total_frames = len(vr)

indices = np.linspace(
    0,
    total_frames - 1,
    16
).astype(int)

frames = vr.get_batch(
    indices
).asnumpy()

frames = [
    Image.fromarray(frame)
    for frame in frames
]


print("Total frames:", total_frames)
print("Frames used:", len(frames))


# ==========================================
# Process
# ==========================================

inputs = processor(
    frames,
    return_tensors="pt"
)


# ==========================================
# Prediction
# ==========================================

with torch.no_grad():

    outputs = model(
        **inputs
    )

    probabilities = torch.softmax(
        outputs.logits,
        dim=1
    )[0]


print("\n==============================")
print("OFFICIAL MODEL TEST")
print("==============================")

print(
    "Real:",
    float(probabilities[0]) * 100,
    "%"
)

print(
    "Fake:",
    float(probabilities[1]) * 100,
    "%"
)

print(
    "Predicted class:",
    torch.argmax(probabilities).item()
)

print("==============================")
