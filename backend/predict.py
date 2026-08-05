import numpy as np
import cv2
from tensorflow.keras.models import load_model

# ==========================================
# Load Model Only Once
# ==========================================

model = load_model("models/cnn_model.h5")


# ==========================================
# Predict Image
# ==========================================

def predict_image(image_path):

    # Read Image
    image = cv2.imread(image_path)

    if image is None:
        return {
            "prediction": "Error",
            "confidence": 0,
            "raw_prediction": 0,
            "risk_level": "Unknown",
            "message": "Unable to read image."
        }

    # Convert BGR to RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Resize according to model input
    image = cv2.resize(image, (128, 128))

    # Normalize
    image = image.astype("float32") / 255.0

    # Add Batch Dimension
    image = np.expand_dims(image, axis=0)

    # Predict
    prediction = float(model.predict(image, verbose=0)[0][0])

    print(f"\nRaw Prediction : {prediction}")

    # ==========================================
    # Classification
    # ==========================================

    if prediction >= 0.5:
        result = "Deepfake"
        confidence = prediction * 100
    else:
        result = "Real"
        confidence = (1 - prediction) * 100

    # ==========================================
    # Fake Probability
    # ==========================================

    fake_probability = prediction * 100

    # ==========================================
    # Risk Level (Based on Fake Probability)
    # ==========================================

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

    # ==========================================
    # Return Result
    # ==========================================

    return {
        "prediction": result,
        "confidence": round(confidence, 2),
        "raw_prediction": round(prediction, 4),
        "risk_level": risk_level
    }