"""
Text similarity testing.

Available functions:
- `cosine_similarity_score(text1, text2)`: Calculate the cosine similarity score between two texts.
- `jaccard_similarity_score(text1, text2)`: Calculate the Jaccard similarity score between two texts.
- `edit_distance_score(text1, text2)`: Calculate the edit distance score between two texts.
"""

import nltk
from nltk.metrics import distance
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


nltk.download('stopwords', quiet=True)


def cosine_similarity_score(text1, text2):
    """
    Calculate the cosine similarity score between two texts.

    Parameters:
    - `text1` (str): The first text.
    - `text2` (str): The second text.

    Returns:
    - `float`: The cosine similarity score.
    """
    try:
        # Prepare the texts
        texts = [text1, text2]

        # Vectorize the texts
        vectorizer = TfidfVectorizer(stop_words=stopwords.words('english'))
        tfidf_matrix = vectorizer.fit_transform(texts)

        # Calculate the cosine similarity
        cosine_sim = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0]
        return cosine_sim
    except Exception as e:
        print(f"An error occurred during cosine similarity calculation: {str(e)}")
        return 0.0


def jaccard_similarity_score(text1, text2):
    """
    Calculate the Jaccard similarity score between two texts.

    Parameters:
    - `text1` (str): The first text.
    - `text2` (str): The second text.

    Returns:
    - `float`: The Jaccard similarity score.
    """
    try:
        # Tokenize the texts
        tokens1 = set(nltk.word_tokenize(text1.lower()))
        tokens2 = set(nltk.word_tokenize(text2.lower()))

        # Calculate the Jaccard similarity
        jaccard_sim = len(tokens1.intersection(tokens2)) / len(tokens1.union(tokens2))
        return jaccard_sim
    except Exception as e:
        print(f"An error occurred during Jaccard similarity calculation: {str(e)}")
        return 0.0


def edit_distance_score(text1, text2):
    """
    Calculate the edit distance score between two texts.

    Parameters:
    - `text1` (str): The first text.
    - `text2` (str): The second text.

    Returns:
    - `int`: The edit distance score.
    """
    try:
        # Calculate the edit distance
        edit_dist = distance.edit_distance(text1, text2)
        return edit_dist
    except Exception as e:
        print(f"An error occurred during edit distance calculation: {str(e)}")
        return 0