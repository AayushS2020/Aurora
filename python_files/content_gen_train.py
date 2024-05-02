import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np

# Load the data from text files
def load_data():
    with open('text_files/content_gen.txt', 'r') as f:
        texts = f.readlines()
    return texts

# Tokenize text data
tokenizer = Tokenizer()
tokenizer.fit_on_texts(texts)
word_index = tokenizer.word_index
sequences = tokenizer.texts_to_sequences(texts)
max_sequence_length = max([len(seq) for seq in sequences])
padded_sequences = pad_sequences(sequences, maxlen=max_sequence_length, padding='post')

# Example target data (assuming each input text generates the subsequent text)
targets = np.roll(padded_sequences, -1, axis=0)

# Define and compile the model
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(len(word_index) + 1, 100, input_length=max_sequence_length),
    tf.keras.layers.LSTM(100),
    tf.keras.layers.Dense(len(word_index) + 1, activation='softmax')
])

model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the model
model.fit(padded_sequences, targets, epochs=50)

# Save the trained model to an HDF5 file
model.save('text_generation_model.h5')
