from typing import List, Tuple

import click
from pathlib import Path
import spacy
from spacy.cli import init_model


RAW_VECTORS_PATH = 'spacy_pl_utils/data/vectors_300.txt'
MODEL_PATH = 'data/pl-vectors-model'


class SimilarityCalculator(object):
    def __init__(self, model_path: str = MODEL_PATH):
        self.nlp = spacy.load(Path(model_path))
        self.tokens = []
        self.word_similarity_pairs = []

    @property
    def used_words(self):
        return [token.text for token in self.tokens]

    def calculate_pairwise_similarity(self, words: str) -> List[list]:
        self.tokens = [token for token in self.nlp(words) if token.is_alpha]
        self.word_similarity_pairs = [
            [word1.similarity(word2) for word2 in self.tokens]
            for word1 in self.tokens
        ]
        return self.word_similarity_pairs


@click.command("Initializes model with word vectors and saves it to model path.")
def preprocess(vectors_path: str = RAW_VECTORS_PATH, model_path: str = MODEL_PATH):
    nlp = init_model('pl', Path(model_path), vectors_loc=vectors_path)
    return nlp