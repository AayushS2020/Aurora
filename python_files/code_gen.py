import numpy as np
from tensorflow.keras.models import load_model

# Load the trained model
model = load_model("code_model.h5")

# Define token mappings
input_characters = sorted(list(set("abcdefghijklmnopqrstuvwxyz ")))
target_characters = sorted(list(set("abcdefghijklmnopqrstuvwxyz\t\n ")))
num_encoder_tokens = len(input_characters)
num_decoder_tokens = len(target_characters)
max_encoder_seq_length = 100
max_decoder_seq_length = 100
input_token_index = dict([(char, i) for i, char in enumerate(input_characters)])
target_token_index = dict([(char, i) for i, char in enumerate(target_characters)])
reverse_target_char_index = dict((i, char) for char, i in target_token_index.items())

# Function to preprocess input text
def preprocess_input(input_text):
    input_text = input_text.lower()
    input_seq = np.zeros((1, max_encoder_seq_length, num_encoder_tokens), dtype="float32")
    for t, char in enumerate(input_text):
        input_seq[0, t, input_token_index[char]] = 1.0
    input_seq[0, t + 1 :, input_token_index[" "]] = 1.0
    return input_seq

# Function to decode output sequences
def decode_sequence(input_seq):
    states_value = [np.zeros((1, 256)), np.zeros((1, 256))]  # Initial states for LSTM
    target_seq = np.zeros((1, 1, num_decoder_tokens))
    target_seq[0, 0, target_token_index["\t"]] = 1.0
    stop_condition = False
    decoded_sentence = ""
    while not stop_condition:
        output_tokens, h, c = model.predict([input_seq] + states_value)
        sampled_token_index = np.argmax(output_tokens[0, -1, :])
        sampled_char = reverse_target_char_index[sampled_token_index]
        decoded_sentence += sampled_char
        if sampled_char == "\n" or len(decoded_sentence) > max_decoder_seq_length:
            stop_condition = True
        target_seq = np.zeros((1, 1, num_decoder_tokens))
        target_seq[0, 0, sampled_token_index] = 1.0
        states_value = [h, c]
    return decoded_sentence

def main(user_input):
    user_input = user_input
    input_seq = preprocess_input(user_input)
    generated_code = decode_sequence(input_seq)
    print(generated_code)
