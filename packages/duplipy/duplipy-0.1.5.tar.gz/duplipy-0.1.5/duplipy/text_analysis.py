"""
For text analysis.

Available methods:
- `extract_named_entities(text)`: Extract named entities from the input text using spaCy's NER.
- `translate_text(text, target_language)`: Translate the input text to the specified target language using Google Translate.
- `analyze_sentiment(text)`: Analyze the sentiment of the input text using NLTK's SentimentIntensityAnalyzer.
"""

import spacy
from googletrans import Translator
from nltk.sentiment import SentimentIntensityAnalyzer


def extract_named_entities(text):
    """
    Extract named entities from the input text using spaCy's NER.

    Parameters:
    - `text` (str): The input text.

    Returns:
    - `list`: A list of named entities.
    """
    try:
        nlp = spacy.load('en_core_web_sm')
        doc = nlp(text)
        named_entities = [(ent.text, ent.label_) for ent in doc.ents]
        return named_entities
    except Exception as e:
        print(f"An error occurred during named entity recognition: {str(e)}")
        return []


def translate_text(text, target_language):
    """
    Translate the input text to the specified target language using Google Translate.

    Parameters:
    - `text` (str): The input text to be translated.
    - `target_language` (str): The target language code (e.g., 'en' for English, 'es' for Spanish).

    Returns:
    - `str`: The translated text.
    """
    try:
        translator = Translator()
        translation = translator.translate(text, dest=target_language)
        return translation.text
    except Exception as e:
        print(f"An error occurred during text translation: {str(e)}")
        return text


def analyze_sentiment(text):
    """
    Analyze the sentiment of the input text using NLTK's SentimentIntensityAnalyzer.

    Parameters:
    - `text` (str): The input text to be analyzed.

    Returns:
    - `float`: The sentiment score ranging from -1 (negative) to 1 (positive).
    """
    try:
        sid = SentimentIntensityAnalyzer()
        sentiment_scores = sid.polarity_scores(text)
        sentiment_score = sentiment_scores['compound']
        return sentiment_score
    except Exception as e:
        print(f"An error occurred during sentiment analysis: {str(e)}")
        return 0.0