from tensorflow.lite.python.interpreter import Interpreter
import numpy as np

model = Interpreter("failure_model.tflite")
model.allocate_tensors()

def predict_failure(sensor_data):
    X = np.array([[sensor_data["temperature"], sensor_data["vibration"]]])
    model.set_tensor(model.get_input_details()[0]['index'], X.astype(np.float32))
    model.invoke()
    failure_prob = model.get_tensor(model.get_output_details()[0]['index'])[0]
    return failure_prob > 0.8
