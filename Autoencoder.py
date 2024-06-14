
import numpy as np
from os.path import join
from tflite_runtime.interpreter import Interpreter

# Settings
MODELS_PATH = 'models'
TFLITE_MODEL_FILE = 'modelo_df'  # .tflite will be added
THRESHOLD = 0.3500242427984803;    # Any MAE over this is an anomaly
MEAN_TRAINING = 26.403898673843077;    # Mean of the training process
STD_TRAINING = 10.86128076630132;   # Standar desviation of the training process

################################################################################
# Functions

# Load model
def load_model():
    global input_details
    global output_details
    interpreter = Interpreter(join(MODELS_PATH, TFLITE_MODEL_FILE) + '.tflite')
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    return interpreter


# Normalize values to be evaluated for the model.
def normalize_data(data):

    norm = []

    for i in data:
        if np.isnan(i):
            norm.append(i)
        else:
            norm.append((i - MEAN_TRAINING)/STD_TRAINING)

    return norm

# Autoencoder prediction
def Autoencoder(data, interpreter):

    values = normalize_data(data)
    txt = ""
   
    # Make prediction from model
    for n, d in zip(values, data):
        n = np.array([n])
        in_tensor = np.float32(n.reshape(1, 1, 1, n.shape[0]))
        interpreter.set_tensor(input_details[0]['index'], in_tensor)
        interpreter.invoke()
        output_data = interpreter.get_tensor(output_details[0]['index'])
        pred = output_data[0]

        acum = 0
        for i in range(pred.shape[0]):
            acum += pred[i][0]

        pred_val = acum/pred.shape[0]
        #print("Prediction:", pred_val)

        # Calculate MSE
        mae = np.abs(n - pred_val)[0]
        #print("MAE:", mae)
        
        # Compare MSE the threshold
        if mae > THRESHOLD:
            outlier = "Y"
        else:
            outlier = "N"
              
        #print(f"{d:.5f},{outlier},{mae:.5f}")
        txt += f"{d:.5f},{outlier},{mae:.5f}\n"
    
    return txt