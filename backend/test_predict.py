from predict import predict_image

result = predict_image("uploads/test4.jpg")

print("\n==============================")
print("DeepShield AI Prediction")
print("==============================")
print(f"Prediction     : {result['prediction']}")
print(f"Confidence     : {result['confidence']}%")
print(f"Raw Prediction : {result['raw_prediction']}")
print(f"Risk Level     : {result['risk_level']}")
print("==============================")