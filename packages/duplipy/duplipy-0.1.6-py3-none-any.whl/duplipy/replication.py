"""
Text replication for NLP.

Available functions:
- `replace_word_with_synonym(word)`: Replace the given word with a synonym.
- `augment_text_with_synonyms(text, augmentation_factor, probability, progress=True)`: Augment the input text by replacing words with synonyms.
- `load_text_file(filepath)`: Load the contents of a text file.
- `augment_file_with_synonyms(file_path, augmentation_factor, probability, progress=True)`: Augment a text file by replacing words with synonyms.
- `insert_random_word(text, word)`: Insert a random word into the input text.
- `delete_random_word(text)`: Delete a random word from the input text.
- `insert_synonym(text, word)`: Insert a synonym of the given word into the input text.
- `paraphrase(text)`: Paraphrase the input text.
"""

import random
import time
import nltk
from nltk.corpus import wordnet

nltk.download("wordnet", quiet=True)
nltk.download("averaged_perceptron_tagger", quiet=True)
nltk.download("punkt", quiet=True)

def replace_word_with_synonym(word):
    """
    Replace the given word with a synonym.

    Params:
    - `word` (str): The input word to replace with a synonym.

    Returns:
    - `str`: The synonym for the word.
    """
    try:
        synonyms = []
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                synonyms.append(lemma.name())
        
        if synonyms:
            synonym = random.choice(synonyms)
            return synonym
        
        return word
    except Exception as e:
        print(f"An error occurred during word replacement: {str(e)}")
        return word

def augment_text_with_synonyms(text, augmentation_factor, probability, progress=True):
    """
    Augment the input text by replacing words with synonyms.

    Parameters:
    - `text` (str): The input text to be augmented.
    - `augmentation_factor` (int): The number of times to augment the text.
    - `probability` (float): The probability of replacing a random word with a synonym.
    - `progress` (bool): Whether or not to return current progress during augmentation.

    Returns:
    - `list`: A list of augmented text.
    """
    augmented_text = []
    try:
        if probability is None:
            raise ValueError("Probability value cannot be of NoneType. Choose a float from 0 to 1")

        tokens = text.split()
        num_tokens = len(tokens)
        processed_tokens = 0

        start_time = time.time()

        for _ in range(augmentation_factor):
            augmented_tokens = []

            for token in tokens:
                if random.random() < probability:
                    replaced_token = replace_word_with_synonym(token)
                    augmented_tokens.append(replaced_token)
                else:
                    augmented_tokens.append(token)

                processed_tokens += 1

                # Print progress
                if progress:
                    elapsed_time = time.time() - start_time
                    if elapsed_time == 0:
                        elapsed_time = 1e-6  # Set a small value to avoid division by zero
                    tokens_per_sec = processed_tokens / elapsed_time
                    print(f"Progress: {processed_tokens}/{num_tokens} tokens | {tokens_per_sec:.2f} tokens/sec", end="\r")

            augmented_text.append(' '.join(augmented_tokens))
        
        # Print completion message
        if progress:
            print(" " * 100, end="\r")  # Clear progress line
            print("Augmentation complete.")

    except Exception as e:
        print(f"An error occurred during text augmentation: {str(e)}")
        return []

    return augmented_text

def load_text_file(file_path):
    """
    Load the contents of a text file.

    Parameters:
    - `file_path` (str): The path to the target input data.

    Returns:
    - `str`: The read text from the file.
    """
    try:
        with open(file_path, 'r') as file:
            text = file.read()
        return text
    except Exception as e:
        print(f"An error occurred during text file loading: {str(e)}")
        return ""

def augment_file_with_synonyms(file_path, augmentation_factor, probability, progress=True):
    """
    Augment a text file by replacing words with synonyms.

    Parameters:
    - `file_path` (str): The path to the target input data.
    - `augmentation_factor` (int): The number of times to augment the data.
    - `probability` (float): The probability of replacing a random word with its synonym.
    - `progress` (bool): Whether or not to print the current progress during augmentation.

    Returns:
    - `list`: A list of augmented text.
    """
    try:
        text = load_text_file(file_path)
        augmented_text = augment_text_with_synonyms(text, augmentation_factor, probability, progress)
        return augmented_text
    except Exception as e:
        print(f"An error occurred during text file augmentation: {str(e)}")
        return []


def insert_random_word(text, word):
    """
    Insert a random word into the input text.

    Parameters:
    - `text` (str): The input text for word insertion.
    - `word` (str): The word to be inserted into the text.

    Returns:
    - `str`: The text with the randomly inserted word.
    """
    try:
        words = nltk.word_tokenize(text)
        words.insert(random.randint(0, len(words)), word)
        modified_text = " ".join(words)
        return modified_text
    except Exception as e:
        print(f"An error occurred during word insertion: {str(e)}")
        return text


def delete_random_word(text):
    """
    Delete a random word from the input text.

    Parameters:
    - `text` (str): The input text for word deletion.

    Returns:
    - `str`: The text with a randomly deleted word.
    """
    try:
        words = nltk.word_tokenize(text)
        if len(words) > 1:
            words.pop(random.randint(0, len(words) - 1))
        modified_text = " ".join(words)
        return modified_text
    except Exception as e:
        print(f"An error occurred during word deletion: {str(e)}")
        return text


def insert_synonym(text, word):
    """
    Insert a synonym of the given word into the input text.

    Parameters:
    - `text` (str): The input text for synonym insertion.
    - `word` (str): The word for which a synonym will be inserted.

    Returns:
    - `str`: The text with a synonym of the word inserted.
    """
    try:
        synonym = replace_word_with_synonym(word)
        modified_text = text.replace(word, synonym)
        return modified_text
    except Exception as e:
        print(f"An error occurred during synonym insertion: {str(e)}")
        return text


def paraphrase(text):
    """
    Paraphrase the input text.

    Parameters:
    - `text` (str): The input text to be paraphrased.

    Returns:
    - `str`: The paraphrased text.
    """
    try:
        tokens = nltk.word_tokenize(text)
        tagged_tokens = nltk.pos_tag(tokens)
        paraphrased_tokens = [replace_word_with_synonym(token) if tag.startswith(("VB", "NN", "JJ")) else token for token, tag in tagged_tokens]
        paraphrased_text = " ".join(paraphrased_tokens)
        return paraphrased_text
    except Exception as e:
        print(f"An error occurred during paraphrasing: {str(e)}")
        return text