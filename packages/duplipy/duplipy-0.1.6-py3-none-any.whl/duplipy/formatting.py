"""
Formatting for text using common NLP techniques.

Available functions:
- `remove_stopwords(text)`: Remove stopwords from the input text using NLTK's stopwords.
- `remove_numbers(text)`: Remove numbers from the input text.
- `remove_whitespace(text)`: Remove excess whitespace from the input text.
- `normalize_whitespace(text)`: Normalize multiple whitespaces into a single whitespace in the input text.
- `seperate_symbols(text)`: Separate symbols and words with a space to ease tokenization.
- `remove_special_characters(text)`: Remove special characters from the input text.
- `standardize_text(text)`: Standardize the formatting of the input text.
- `tokenize_text(text)`: Tokenize the input text into individual words.
- `stem_words(words)`: Stem the input words using Porter stemming algorithm.
- `lemmatize_words(words)`: Lemmatize the input words using WordNet lemmatization.
- `pos_tag(text)`: Perform part-of-speech (POS) tagging on the input text.
"""


import string
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer

nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)

def remove_stopwords(text):
    """
    Remove stopwords from the input text using NLTK's stopwords.

    Parameters:
    - `text` (str): The input text from which stopwords should be removed.

    Returns:
    - `str`: The text without stopwords.
    """
    try:
        stop_words = set(stopwords.words('english'))
        tokens = text.split()
        filtered_tokens = [token for token in tokens if token.lower() not in stop_words]
        filtered_text = ' '.join(filtered_tokens)
        return filtered_text
    except Exception as e:
        print(f"An error occurred during stopwords removal: {str(e)}")
        return text

def remove_numbers(text):
    """
    Remove numbers from the input text.

    Parameters:
    - `text` (str): The input text from which numbers should be removed.

    Returns:
    - `str`: The text without numbers.
    """
    try:
        text = re.sub(r'\d+', '', text)
        return text
    except Exception as e:
        print(f"An error occurred during number removal: {str(e)}")
        return text

def remove_whitespace(text):
    """
    Remove excess whitespace from the input text.

    Parameters:
    - `text` (str): The input text from which excess whitespace should be removed.

    Returns:
    - `str`: The text with the removed excess whitespace.
    """
    try:
        text = ' '.join(text.split())
        return text
    except Exception as e:
        print(f"An error occurred during whitespace removal: {str(e)}")
        return text

def normalize_whitespace(text):
    """
    Normalize multiple whitespaces into a single whitespace in the input text.

    Parameters:
    - `text` (str): The input text from which whitespace should be normalized.

    Returns:
    - `str`: The text with normalized whitespace.
    """
    try:
        text = re.sub(r'\s+', ' ', text)
        return text
    except Exception as e:
        print(f"An error occurred during whitespace normalization: {str(e)}")
        return text

def separate_symbols(text):
    """
    Separate symbols and words with a space to ease tokenization.

    Parameters:
    - `text` (str): The input text from which symbols needs to be seperated.

    Returns:
    - `str`: The text from which symbols have been seperated.
    """
    try:
        pattern = r"([\W])"
        separated_text = re.sub(pattern, r" \1 ", text)
        return separated_text
    except Exception as e:
        print(f"An error occurred during symbol separation: {str(e)}")
        return text

def remove_special_characters(text):
    """
    Remove special characters from the input text.

    Parameters:
    - `text` (str): The input text from which special characters should be removed.

    Returns:
    - `str`: The text with special characters removed.
    """
    try:
        text = text.translate(str.maketrans("", "", string.punctuation))
        special_characters = "@#$%^&*"
        text = ''.join(char for char in text if char not in special_characters)
        return text
    except Exception as e:
        print(f"An error occurred during special character removal: {str(e)}")
        return text

def standardize_text(text):
    """
    Standardize the formatting of the input text.

    Parameters:
    - `text` (str): The input text which needs to be standardized.

    Returns:
    - `str`: The standardized text.
    """
    try:
        text = text.lower()
        text = text.strip()
        return text
    except Exception as e:
        print(f"An error occurred during text standardization: {str(e)}")
        return text

def tokenize_text(text):
    """
    Tokenize the input text into individual words.

    Parameters:
    - `text` (str): The input text to be tokenized.

    Returns:
    - `list`: A list of tokens (words) from the input text.
    """
    tokens = word_tokenize(text)
    return tokens

def stem_words(words):
    """
    Stem the input words using Porter stemming algorithm.

    Parameters:
    - `words` (list): A list of words to be stemmed.

    Returns:
    - `list`: A list of stemmed words.
    """
    stemmer = PorterStemmer()
    stemmed_words = [stemmer.stem(word) for word in words]
    return stemmed_words

def lemmatize_words(words):
    """
    Lemmatize the input words using WordNet lemmatization.

    Parameters:
    - `words` (list): A list of words to be lemmatized.

    Returns:
    - `list`: A list of lemmatized words.
    """
    lemmatizer = WordNetLemmatizer()
    lemmatized_words = [lemmatizer.lemmatize(word) for word in words]
    return lemmatized_words

def pos_tag(text):
    """
    Perform part-of-speech (POS) tagging on the input text.

    Parameters:
    - `text` (str): The input text to be POS tagged.

    Returns:
    - `list`: A list of tuples containing (word, tag) pairs.
    """
    try:
        tokens = nltk.word_tokenize(text)
        tagged_words = nltk.pos_tag(tokens)
        return tagged_words
    except Exception as e:
        print(f"An error occurred during POS tagging: {str(e)}")
        return []