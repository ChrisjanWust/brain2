import random

from .word_lists import *


def is_question(sentence):
    first_words = sentence.strip().lower().split()[:2]
    first_words = " ".join(first_words)
    return sentence.endswith("?") or first_words in QUESTION_SENTENCE_STARTS


def random_okay_sentence():
    return random.choice(OKAY_SYNONYMS)


def is_top_english_word(word: str):
    return word in TOP_ENGLISH_WORDS
