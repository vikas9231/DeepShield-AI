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
            "risk_level": "Unknown"

        }

    predictions = []

    frame_count = 0

    while True:

        ret, frame = cap.read()

        if not ret:

            break

        frame_count += 1

        # Analyze every 15th frame
        if frame_count % 15 != 0:

            continue

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        frame = cv2.resize(frame, (128, 128))

        frame = frame.astype("float32") / 255.0

        frame = np.expand_dims(frame, axis=0)

        pred = float(model.predict(frame, verbose=0)[0][0])

        predictions.append(pred)

    cap.release()

    if len(predictions) == 0:

        return {

            "prediction": "Error",
            "confidence": 0,
            "raw_prediction": 0,
            "risk_level": "Unknown"

        }

    avg_prediction = np.mean(predictions)

    if avg_prediction >= 0.5:

        prediction = "Deepfake"

        confidence = avg_prediction * 100

    else:

        prediction = "Real"

        confidence = (1 - avg_prediction) * 100

    fake_probability = avg_prediction * 100

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

    return {

        "prediction": prediction,

        "confidence": round(confidence, 2),

        "raw_prediction": round(avg_prediction, 4),

        "risk_level": risk

    }