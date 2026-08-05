import cv2
import numpy as np
from tensorflow.keras.models import load_model

# ==========================================
# Load CNN Model
# ==========================================

model = load_model("models/cnn_model.h5")


# ==========================================
# Predict Video
# ==========================================

def predict_video(video_path):

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():

        return {

            "prediction": "Error",
            "confidence": 0,
            "raw_prediction": 0,
            "risk_level": "Unknown",
            "real_votes": 0,
            "fake_votes": 0,
            "frames": 0

        }

    total_frames = 0
    analyzed_frames = 0

    real_votes = 0
    fake_votes = 0

    probabilities = []

    while True:

        success, frame = cap.read()

        if not success:

            break

        total_frames += 1

        # Analyze every 10th frame
        if total_frames % 10 != 0:

            continue

        analyzed_frames += 1

        # ----------------------------
        # Preprocess
        # ----------------------------

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        frame = cv2.resize(frame, (128, 128))

        frame = frame.astype("float32") / 255.0

        frame = np.expand_dims(frame, axis=0)

        prediction = float(model.predict(frame, verbose=0)[0][0])

        print(f"Frame {analyzed_frames}: {prediction:.4f}")

        print(prediction)

        probabilities.append(prediction)

        # Same logic as image detection

        if prediction >= 0.5:

            fake_votes += 1

        else:

            real_votes += 1

    cap.release()

    if analyzed_frames == 0:

        return {

            "prediction": "Error",
            "confidence": 0,
            "raw_prediction": 0,
            "risk_level": "Unknown",
            "real_votes": 0,
            "fake_votes": 0,
            "frames": 0

        }

    # ==========================================
    # Majority Voting
    # ==========================================

    if fake_votes > real_votes:

        prediction = "Deepfake"

        confidence = (fake_votes / analyzed_frames) * 100

    else:

        prediction = "Real"

        confidence = (real_votes / analyzed_frames) * 100

    raw_prediction = float(np.mean(probabilities))

    fake_probability = raw_prediction * 100

    # ==========================================
    # Risk Level
    # ==========================================

    if fake_probability >= 90:

        risk = "Very High"

    elif fake_probability >= 70:

        risk = "High"

    elif fake_probability >= 50:

        risk = "Medium"

    elif fake_probability >= 30:

        risk = "Low"

    else:

        risk = "Very Low"

    # ==========================================
    # Debug
    # ==========================================

    print("\n================ VIDEO ANALYSIS ================")

    print("Total Frames      :", total_frames)

    print("Frames Analysed   :", analyzed_frames)

    print("Real Votes        :", real_votes)

    print("Fake Votes        :", fake_votes)

    print("Average Prediction:", round(raw_prediction, 4))

    print("Final Result      :", prediction)

    print("Confidence        :", round(confidence, 2))

    print("Risk Level        :", risk)

    print("===============================================\n")

    # ==========================================
    # Return
    # ==========================================

    return {

        "prediction": prediction,

        "confidence": round(confidence, 2),

        "raw_prediction": round(raw_prediction, 4),

        "risk_level": risk,

        "real_votes": real_votes,

        "fake_votes": fake_votes,

        "frames": analyzed_frames

    }