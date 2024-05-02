import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Embedding

def load_data():
    with open('text_files/inputs.txt', 'r') as f:
        inputs = f.readlines()
    with open('text_files/outputs.txt', 'r') as f:
        outputs = f.readlines()
    return inputs, outputs

# Convert text data to integer sequences (tokenization)
input_texts = inputs
output_texts = outputs

input_characters = sorted(list(set(" ".join(input_texts))))
target_characters = sorted(list(set(" ".join(output_texts))))

num_encoder_tokens = len(input_characters)
num_decoder_tokens = len(target_characters)

max_encoder_seq_length = max([len(txt) for txt in input_texts])
max_decoder_seq_length = max([len(txt) for txt in output_texts])

input_token_index = dict([(char, i) for i, char in enumerate(input_characters)])
target_token_index = dict([(char, i) for i, char in enumerate(target_characters)])

encoder_input_data = np.zeros(
    (len(input_texts), max_encoder_seq_length, num_encoder_tokens), dtype="float32"
)
decoder_input_data = np.zeros(
    (len(input_texts), max_decoder_seq_length, num_decoder_tokens), dtype="float32"
)
decoder_target_data = np.zeros(
    (len(input_texts), max_decoder_seq_length, num_decoder_tokens), dtype="float32"
)

for i, (input_text, target_text) in enumerate(zip(input_texts, output_texts)):
    for t, char in enumerate(input_text):
        encoder_input_data[i, t, input_token_index[char]] = 1.0
    encoder_input_data[i, t + 1 :, input_token_index[" "]] = 1.0
    for t, char in enumerate(target_text):
        decoder_input_data[i, t, target_token_index[char]] = 1.0
        if t > 0:
            decoder_target_data[i, t - 1, target_token_index[char]] = 1.0
    decoder_input_data[i, t + 1 :, target_token_index[" "]] = 1.0
    decoder_target_data[i, t:, target_token_index[" "]] = 1.0

# Define the model
model = Sequential()
model.add(LSTM(256, input_shape=(None, num_encoder_tokens)))
model.add(Dense(num_decoder_tokens, activation="softmax"))

# Compile the model
model.compile(optimizer="rmsprop", loss="categorical_crossentropy")

# Train the model
model.fit(
    encoder_input_data,
    decoder_target_data,
    batch_size=64,
    epochs=100,
    validation_split=0.2
)

# Save the model as an H5 file
model.save("code_model.h5")
