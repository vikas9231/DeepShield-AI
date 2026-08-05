from tensorflow.keras.models import load_model

model = load_model("models/cnn_model.h5")

print("\n========== MODEL SUMMARY ==========\n")

model.summary()

print("\n========== INPUT SHAPE ==========\n")

print(model.input_shape)

print("\n========== OUTPUT SHAPE ==========\n")

print(model.output_shape)

print("\n========== OUTPUT ACTIVATION ==========\n")

print(model.layers[-1].activation.__name__)