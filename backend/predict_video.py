# import os
# import cv2
# import numpy as np
# import torch

# from PIL import Image
# from transformers import (
#     AutoImageProcessor,
#     AutoModelForVideoClassification
# )


# # ==========================================
# # Model
# # ==========================================

# MODEL_NAME = "shylhy/videomae-large-finetuned-deepfake-subset"

# DEVICE = torch.device(
#     "cuda" if torch.cuda.is_available() else "cpu"
# )

# print("\nLoading VideoMAE Large Deepfake Detector...")

# processor = AutoImageProcessor.from_pretrained(
#     MODEL_NAME
# )

# model = AutoModelForVideoClassification.from_pretrained(
#     MODEL_NAME
# )

# model.to(DEVICE)
# model.eval()

# print("Model loaded successfully.")
# print("Device:", DEVICE)
# print("Labels:", model.config.id2label)


# # ==========================================
# # Extract Video Frames
# # ==========================================

# def load_video_frames(video_path, num_frames=32):

#     cap = cv2.VideoCapture(video_path)

#     if not cap.isOpened():
#         raise ValueError("Unable to open video.")

#     total_frames = int(
#         cap.get(cv2.CAP_PROP_FRAME_COUNT)
#     )

#     if total_frames <= 0:
#         cap.release()
#         raise ValueError(
#             "Video contains no readable frames."
#         )

#     indices = np.linspace(
#         0,
#         total_frames - 1,
#         num_frames
#     ).astype(int)

#     frames = []

#     for index in indices:

#         cap.set(
#             cv2.CAP_PROP_POS_FRAMES,
#             int(index)
#         )

#         success, frame = cap.read()

#         if not success:
#             continue

#         frame = cv2.cvtColor(
#             frame,
#             cv2.COLOR_BGR2RGB
#         )

#         frames.append(
#             Image.fromarray(frame)
#         )

#     cap.release()

#     if len(frames) == 0:
#         raise ValueError(
#             "Unable to extract video frames."
#         )

#     while len(frames) < num_frames:
#         frames.append(frames[-1].copy())

#     return frames[:num_frames], total_frames


# # ==========================================
# # Predict Video
# # ==========================================

# def predict_video(video_path):

#     print("\n")
#     print("=" * 55)
#     print("VIDEO ANALYSIS - VideoMAE Large")
#     print("=" * 55)

#     if not os.path.exists(video_path):

#         return {
#             "prediction": "Error",
#             "confidence": 0,
#             "raw_prediction": 0,
#             "risk_level": "Unknown",
#             "message": "Video file not found."
#         }

#     try:

#         # --------------------------------------
#         # Extract frames
#         # --------------------------------------

#         frames, total_frames = load_video_frames(
#             video_path,
#             num_frames=32
#         )

#         print("Total Frames :", total_frames)
#         print("Frames Used  :", len(frames))

#         # --------------------------------------
#         # Process frames
#         # --------------------------------------

#         inputs = processor(
#             frames,
#             return_tensors="pt"
#         )

#         inputs = {
#             key: value.to(DEVICE)
#             for key, value in inputs.items()
#         }

#         # --------------------------------------
#         # Prediction
#         # --------------------------------------

#         with torch.no_grad():

#             outputs = model(**inputs)

#             probabilities = torch.softmax(
#                 outputs.logits,
#                 dim=-1
#             )[0]

#         # --------------------------------------
#         # Print all classes
#         # --------------------------------------

#         print("\nClass Probabilities:")

#         for class_id, probability in enumerate(
#             probabilities
#         ):

#             label = model.config.id2label.get(
#                 class_id,
#                 str(class_id)
#             )

#             print(
#                 f"{label}: "
#                 f"{probability.item() * 100:.2f}%"
#             )

#         # --------------------------------------
#         # Predicted class
#         # --------------------------------------

#         predicted_class = torch.argmax(
#             probabilities
#         ).item()

#         predicted_label = model.config.id2label.get(
#             predicted_class,
#             str(predicted_class)
#         )

#         confidence = (
#             probabilities[predicted_class].item()
#             * 100
#         )

#         # --------------------------------------
#         # Determine fake probability
#         # --------------------------------------

#         fake_probability = 0.0
#         real_probability = 0.0

#         for class_id, label in model.config.id2label.items():

#             probability = (
#                 probabilities[int(class_id)].item()
#                 * 100
#             )

#             label_lower = label.lower()

#             if "fake" in label_lower:

#                 fake_probability = probability

#             elif "real" in label_lower:

#                 real_probability = probability

#         # --------------------------------------
#         # Final classification
#         # --------------------------------------

#         label_lower = predicted_label.lower()

#         if "fake" in label_lower:

#             prediction = "Deepfake"

#         elif "real" in label_lower:

#             prediction = "Real"

#         else:

#             prediction = "Deepfake" \
#                 if fake_probability >= real_probability \
#                 else "Real"

#         # --------------------------------------
#         # Risk Level
#         # --------------------------------------

#         if fake_probability >= 90:

#             risk_level = "Very High"

#         elif fake_probability >= 70:

#             risk_level = "High"

#         elif fake_probability >= 50:

#             risk_level = "Medium"

#         elif fake_probability >= 30:

#             risk_level = "Low"

#         else:

#             risk_level = "Very Low"

#         # --------------------------------------
#         # Output
#         # --------------------------------------

#         print("\nFinal Result:")
#         print("Prediction :", prediction)
#         print("Confidence :", round(confidence, 2))
#         print("Real       :", round(real_probability, 2))
#         print("Deepfake   :", round(fake_probability, 2))
#         print("Risk Level :", risk_level)

#         print("=" * 55)

#         return {

#             "prediction": prediction,

#             "confidence": round(
#                 confidence,
#                 2
#             ),

#             "raw_prediction": round(
#                 fake_probability / 100,
#                 4
#             ),

#             "risk_level": risk_level,

#             "real_probability": round(
#                 real_probability,
#                 2
#             ),

#             "fake_probability": round(
#                 fake_probability,
#                 2
#             ),

#             "frames_analyzed": len(frames),

#             "total_frames": total_frames
#         }

#     except Exception as e:

#         print("\nVIDEO PREDICTION ERROR:")
#         print(e)

#         return {

#             "prediction": "Error",

#             "confidence": 0,

#             "raw_prediction": 0,

#             "risk_level": "Unknown",

#             "message": str(e)
#         }
    

import os
import cv2
import numpy as np
import torch

from PIL import Image
from transformers import (
    AutoImageProcessor,
    AutoModelForVideoClassification
)


# ==========================================
# Model
# ==========================================

MODEL_NAME = "shylhy/videomae-large-finetuned-deepfake-subset"

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print("\nLoading VideoMAE Large Deepfake Detector...")

processor = AutoImageProcessor.from_pretrained(
    MODEL_NAME
)

model = AutoModelForVideoClassification.from_pretrained(
    MODEL_NAME
)

model.to(DEVICE)
model.eval()

print("Model loaded successfully.")
print("Device:", DEVICE)
print("Labels:", model.config.id2label)


# ==========================================
# Fast Frame Extraction
# ==========================================

def load_video_frames(video_path, num_frames=32):

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise ValueError("Unable to open video.")

    total_frames = int(
        cap.get(cv2.CAP_PROP_FRAME_COUNT)
    )

    if total_frames <= 0:
        cap.release()
        raise ValueError("Video contains no readable frames.")

    # Frame positions we actually need
    target_indices = np.linspace(
        0,
        total_frames - 1,
        num_frames
    ).astype(int)

    frames = []
    target_position = 0
    current_frame = 0

    while (
        target_position < len(target_indices)
        and current_frame < total_frames
    ):

        success, frame = cap.read()

        if not success:
            break

        if current_frame == target_indices[target_position]:

            frame = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            frames.append(
                Image.fromarray(frame)
            )

            target_position += 1

        current_frame += 1

    cap.release()

    if not frames:
        raise ValueError(
            "Unable to extract video frames."
        )

    # Fill missing frames if necessary
    while len(frames) < num_frames:
        frames.append(frames[-1].copy())

    return frames[:num_frames], total_frames


# ==========================================
# Predict Video
# ==========================================

def predict_video(video_path):

    print("\n")
    print("=" * 55)
    print("VIDEO ANALYSIS - VideoMAE Large")
    print("=" * 55)

    if not os.path.exists(video_path):

        return {
            "prediction": "Error",
            "confidence": 0,
            "raw_prediction": 0,
            "risk_level": "Unknown",
            "message": "Video file not found."
        }

    try:

        # --------------------------------------
        # Extract 32 frames
        # --------------------------------------

        frames, total_frames = load_video_frames(
            video_path,
            num_frames=32
        )

        print("Total Frames :", total_frames)
        print("Frames Used  :", len(frames))

        # --------------------------------------
        # Preprocessing
        # --------------------------------------

        inputs = processor(
            frames,
            return_tensors="pt"
        )

        inputs = {
            key: value.to(DEVICE)
            for key, value in inputs.items()
        }

        # --------------------------------------
        # Model prediction
        # --------------------------------------

        with torch.no_grad():

            outputs = model(**inputs)

            probabilities = torch.softmax(
                outputs.logits,
                dim=-1
            )[0]

        # --------------------------------------
        # Probabilities
        # --------------------------------------

        real_probability = 0
        fake_probability = 0

        for class_id, label in model.config.id2label.items():

            probability = (
                probabilities[int(class_id)].item()
                * 100
            )

            if "fake" in label.lower():
                fake_probability = probability

            elif "real" in label.lower():
                real_probability = probability

        # --------------------------------------
        # Prediction
        # --------------------------------------

        if fake_probability > real_probability:

            prediction = "Deepfake"
            confidence = fake_probability

        else:

            prediction = "Real"
            confidence = real_probability

        # --------------------------------------
        # Risk
        # --------------------------------------

        if fake_probability >= 90:
            risk_level = "Very High"

        elif fake_probability >= 70:
            risk_level = "High"

        elif fake_probability >= 50:
            risk_level = "Medium"

        elif fake_probability >= 30:
            risk_level = "Low"

        else:
            risk_level = "Very Low"

        # --------------------------------------
        # Output
        # --------------------------------------

        print("\nClass Probabilities:")
        print(f"Real      : {real_probability:.2f}%")
        print(f"Deepfake  : {fake_probability:.2f}%")

        print("\nFinal Result:")
        print("Prediction :", prediction)
        print("Confidence :", round(confidence, 2))
        print("Risk Level :", risk_level)

        print("=" * 55)

        return {
            "prediction": prediction,
            "confidence": round(confidence, 2),
            "raw_prediction": round(
                fake_probability / 100,
                4
            ),
            "risk_level": risk_level,
            "real_probability": round(
                real_probability,
                2
            ),
            "fake_probability": round(
                fake_probability,
                2
            ),
            "frames_analyzed": len(frames),
            "total_frames": total_frames
        }

    except Exception as e:

        print("\nVIDEO PREDICTION ERROR:")
        print(e)

        return {
            "prediction": "Error",
            "confidence": 0,
            "raw_prediction": 0,
            "risk_level": "Unknown",
            "message": str(e)
        }
    