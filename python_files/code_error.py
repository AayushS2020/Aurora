import h5py
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline
import numpy as np
import re

# Function to load the saved model from the HDF5 file
def load_model(filename='error_detection_model.h5'):
    with h5py.File(filename, 'r') as file:
        weights = np.array(file['model_weights'])
        intercept = np.array(file['model_intercept'])
    return weights, intercept

# Function to preprocess a code snippet for error detection
def preprocess_code(code_snippet):
    vectorizer = CountVectorizer()
    X = vectorizer.transform([code_snippet])
    return X

# Function to detect errors in a code snippet using the loaded model
def detect_errors(code_snippet, weights, intercept):
    # Preprocess the code snippet
    X = preprocess_code(code_snippet)
    # Compute the model's prediction (1 if error, 0 if no error)
    prediction = np.dot(X.toarray(), weights.T) + intercept
    return prediction[0] == 1

# Main function to load the model, take user input, detect errors, and print results
def error_gen(code_snippet):
    # Load the saved model
    weights, intercept = load_model()
    
    # Detect errors in the user-provided code snippet
    has_error = detect_errors(code_snippet, weights, intercept)
    if has_error:
        print("Error detected in the code snippet.")
    else:
        print("No errors found in the code snippet.")

def main(user_input):

    code_snippet = user_input
    error_gen(code_snippet)
