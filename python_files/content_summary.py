import numpy as np
from tensorflow.keras.models import load_model

# Load the trained model
model = load_model('text_summarization_model.h5')

# Function to preprocess input text
def preprocess_input(text, max_length=1000):
    words = text.lower().split()
    words = words[:max_length] if len(words) > max_length else words + ['<PAD>'] * (max_length - len(words))
    return np.array([word_to_index.get(word, 0) for word in words]).reshape(1, -1)

# Function to generate summary using the model
def generate_summary(text):
    preprocessed_text = preprocess_input(text)
    predicted_summary = model.predict(preprocessed_text)
    predicted_summary_words = [index_to_word[idx] for idx in np.argmax(predicted_summary, axis=-1).flatten() if idx != 0]
    return ' '.join(predicted_summary_words)

def main(user_input):
    text = user_input
    generate_summary(text)

