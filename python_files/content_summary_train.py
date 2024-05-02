import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Load the data from files
def load_data(text_file, summary_file):
    with open(text_file, 'r', encoding='utf-8') as f:
        texts = f.readlines()
    with open(summary_file, 'r', encoding='utf-8') as f:
        summaries = f.readlines()
    return texts, summaries

# Example usage to load data
texts, summaries = load_data('text_files/text_file.txt', 'text_files/summary_file.txt')

# Tokenize the data
tokenizer = Tokenizer()
tokenizer.fit_on_texts(texts + summaries)

# Convert text sequences to integer sequences
text_sequences = tokenizer.texts_to_sequences(texts)
summary_sequences = tokenizer.texts_to_sequences(summaries)

# Pad sequences to a fixed length
max_length = 100  # Choose an appropriate maximum length
padded_text_sequences = pad_sequences(text_sequences, maxlen=max_length, padding='post', truncating='post')
padded_summary_sequences = pad_sequences(summary_sequences, maxlen=max_length, padding='post', truncating='post')

# Define the model
model = Sequential()
model.add(Embedding(input_dim=len(tokenizer.word_index) + 1, output_dim=128, input_length=max_length))
model.add(LSTM(units=256, return_sequences=True))
model.add(Dense(units=len(tokenizer.word_index) + 1, activation='softmax'))

# Compile the model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Define a checkpoint to save the best model
checkpoint_callback = ModelCheckpoint('text_summarization_model.h5', save_best_only=True)

# Train the model
model.fit(padded_text_sequences, padded_summary_sequences, epochs=10, batch_size=32, validation_split=0.2, callbacks=[checkpoint_callback])

# The best model will be saved automatically due to the ModelCheckpoint callback
