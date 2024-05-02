import wikipedia
import random
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Load the trained model from the HDF5 file
model = tf.keras.models.load_model('text_generation_model.h5')

max_sequence_length = 100

# Define a function to generate text using the trained model
def generate_text(seed_text, max_length=500):
    input_seq = tokenizer.texts_to_sequences([seed_text])
    input_seq = pad_sequences(input_seq, maxlen=max_sequence_length, padding='post')
    
    generated_text = ''
    while True:
        predicted_word_index = model.predict_classes(input_seq, verbose=0)[0]
        predicted_word = next(word for word, index in word_index.items() if index == predicted_word_index)
        
        if predicted_word == '<pad>' or len(generated_text.split()) >= max_length:
            break
        
        generated_text += predicted_word + ' '
        input_seq[0, :-1] = input_seq[0, 1:]
        input_seq[0, -1] = predicted_word_index
    
    return generated_text.strip()

def get_wikipedia_content(topic):
    try:
        wikipedia.set_lang("en")  # Set Wikipedia language to English
        page = wikipedia.page(topic)
        content = page.content
        return content
    except wikipedia.exceptions.PageError:
        return "Error: Page not found."
    except wikipedia.exceptions.DisambiguationError as e:
        page = wikipedia.page(e.options[random.randint(0, len(e.options) - 1)])
        content = page.content
        return content

def extract_best_parts(text1, text2):
    # Split text into sentences
    sentences1 = text1.split('.')
    sentences2 = text2.split('.')
    
    # Sort sentences
    sentences1_scores = {sentence: len(sentence.split()) for sentence in sentences1}
    sentences2_scores = {sentence: len(sentence.split()) for sentence in sentences2}
    
    sorted_sentences1 = sorted(sentences1_scores.items(), key=lambda x: x[1], reverse=True)
    sorted_sentences2 = sorted(sentences2_scores.items(), key=lambda x: x[1], reverse=True)
    
    # Keep the top sentences from each text
    top_sentences1 = [sentence[0] for sentence in sorted_sentences1[:5]]  # Adjust the number as needed
    top_sentences2 = [sentence[0] for sentence in sorted_sentences2[:5]]  # Adjust the number as needed
    
    # Combine the top sentences from both texts
    combined_text = ' '.join(top_sentences1 + top_sentences2)
    return combined_text

def main(user_input):
    seed_text = get_wikipedia_content(user_input)
    generated_text = generate_text(seed_text)
    
    combined_text = extract_best_parts(generated_text, seed_text)
    
    return combined_text