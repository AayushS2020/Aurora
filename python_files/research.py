import scholarly
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser

# Function to summarize text using LSA (Latent Semantic Analysis)
def summarize_text(text, num_sentences=3):
    summarizer = LsaSummarizer()
    summarizer.stop_words = ['']
    summary = summarizer(text, num_sentences)
    return " ".join([str(sentence) for sentence in summary])

def research_find(query):
    
    # Perform the search
    search_results = scholarly.search_pubs(query)

    # List to store summaries
    summaries = []

    # Iterate through search results
    for i, result in enumerate(search_results):
        if i >= 5:  # Limiting to the first 5 search results for demonstration
            break
        try:
            title = result.bib['title']
            abstract = result.bib['abstract']
            # Tokenize the abstract for LSA summarization
            tokenizer = Tokenizer("english")
            parser = PlaintextParser.from_string(abstract, tokenizer)
            summary = summarize_text(parser.document.as_text())
            summaries.append((title, summary))
        except (KeyError, AttributeError) as e:
            print(f"Error processing result {i + 1}: {e}")

    # Print the summaries
    for title, summary in summaries:
        print(f"Title: {title}")
        print(f"Summary: {summary}\n")

def main(user_input):
    research_find(user_input)