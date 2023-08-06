"""
Text similarity testing.

Available functions:
- `edit_distance_score(text1, text2)`: Calculate the edit distance score between two texts.
"""

import nltk
from nltk.metrics import distance
from nltk.translate.bleu_score import sentence_bleu

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
    
def bleu_score(reference, candidate):
    """
    Calculate the BLEU score between a reference sentence and a candidate sentence.

    Parameters:
    - `reference` (str): The reference sentence.
    - `candidate` (str): The candidate sentence.

    Returns:
    - `float`: The BLEU score.
    """
    try:
        # Tokenize the reference and candidate sentences
        reference_tokens = nltk.word_tokenize(reference)
        candidate_tokens = nltk.word_tokenize(candidate)

        # Calculate the BLEU score
        bleu = sentence_bleu([reference_tokens], candidate_tokens)
        return bleu
    except Exception as e:
        print(f"An error occurred during BLEU score calculation: {str(e)}")
        return 0.0