import duplipy
from .formatting import remove_stopwords, remove_numbers, remove_whitespace, normalize_whitespace, separate_symbols, remove_special_characters, standardize_text, tokenize_text, stem_words, lemmatize_words, pos_tag
from .replication import replace_word_with_synonym, augment_text_with_synonyms, load_text_file, augment_file_with_synonyms, backtranslate, insert_random_word, delete_random_word, insert_synonym, paraphrase
from .similarity import cosine_similarity_score, jaccard_similarity_score, edit_distance_score
from .text_analysis import extract_named_entities, translate_text, analyze_sentiment