import os
import pickle
import numpy as np
from .Tokenizer import Tokenizer


class NgramGenerator:
    def __init__(self, num_grams: int = 2, tokenizer: Tokenizer = None) -> None:
        self.num_grams = num_grams
        self.grams = dict()
        self.tokenizer = tokenizer

    def train(self, file_path: str = None, text: str = None) -> None:
        if (file_path is None) and (text is None):
            raise ValueError('You must specify one of file_path or text')
        if file_path is not None:
            with open(file_path, 'r') as file:
                text = file.read()

        if self.tokenizer is None:
            self.tokenizer = Tokenizer(text=text)

        jokes = text.split('<eoa>')

        tokenized_jokes = []
        for idx in range(len(jokes)):
            tokenized_jokes.append(self.tokenizer.tokenize(jokes[idx]))

        for joke in tokenized_jokes:
            self.__add_joke(joke)

        self.__make_probabilities('laplace')

    def generate(self, num_words: int = -1, start: str = ''):
        current_joke = [self.tokenizer.w2i['<soj>']] + self.tokenizer.tokenize(start, add_special_tokens=False)

        for i in range(num_words):
            left_ngram_idx = max(0, len(current_joke) - self.num_grams + 1)
            ngram = tuple(current_joke[left_ngram_idx:])

            while ngram not in self.grams.keys():
                ngram = ngram[1:]

            next_word = self.__choose_next_word(self.grams[ngram]['words'], self.grams[ngram]['probs'])
            current_joke.append(next_word)

            if next_word == self.tokenizer.w2i['<eoj>']:
                break

        result = self.tokenizer.detokenize(current_joke)
        return result

    def save(self, file_name: str) -> None:
        model = {
            'num_grams': self.num_grams,
            'grams': self.grams,
            'tokenizer': self.tokenizer
        }

        pickle.dump(model, open(file_name + '.pkl', 'w+b'))

    def load(self, file_path: str) -> None:
        with open(file_path, 'rb') as file:
            model = pickle.load(file)

        if self.num_grams != model['num_grams']:
            raise ValueError(
                '''Model parameter \'num_grams\' does not match. 
                Expected \'num_grams\' value is {}'''.format(model['num_grams'])
            )

        self.num_grams = model['num_grams']
        self.grams = model['grams']
        self.tokenizer = model['tokenizer']

    def __add_joke(self, joke: list) -> None:
        for right_idx in range(len(joke)):
            for left_idx in range(max(0, right_idx - self.num_grams + 1), right_idx + 1):
                self.__add_ngram(tuple(joke[left_idx:right_idx+1]))

    def __add_ngram(self, ngram: tuple) -> None:
        tuple_key = ngram[:-1]
        word = ngram[-1]

        if tuple_key not in self.grams.keys():
            self.grams[tuple_key] = {
                'words': [word],
                'probs': [1]
            }
        else:
            pos = -1
            for idx, cur_word in enumerate(self.grams[tuple_key]['words']):
                if word == cur_word:
                    pos = idx

            if pos == -1:
                self.grams[tuple_key]['words'].append(word)
                self.grams[tuple_key]['probs'].append(1)
            else:
                self.grams[tuple_key]['probs'][pos] += 1

    def __make_probabilities(self, probs_type: str = None, temperature: int = 5) -> None:
        for key in self.grams.keys():
            counts = self.grams[key]['probs']
            if probs_type == 'laplace':
                self.grams[key]['probs'] = self.__make_laplace_smoothing(counts)
            elif probs_type == 'softmax':
                self.grams[key]['probs'] = self.__softmax_with_temperature(counts, temperature=temperature)
            else:
                self.grams[key]['probs'] = self.__get_probs(counts)

    @staticmethod
    def __choose_next_word(words: list, probs: list) -> int:
        words = np.array(words)
        probs = np.array(probs)

        next_word = np.random.choice(words, p=probs)
        return next_word

    @staticmethod
    def __get_probs(counts: list) -> list:
        probs = np.array(counts, dtype=float)
        probs /= probs.sum()
        return list(probs)

    @staticmethod
    def __make_laplace_smoothing(counts: list, laplace_smoothing_constant: int = 1e-6) -> list:
        probs = np.array(counts, dtype=float)
        ngram_count = probs.sum()

        for idx, p in enumerate(probs):
            probs[idx] = (p + laplace_smoothing_constant) / (laplace_smoothing_constant * len(probs) + ngram_count)

        return list(probs)

    @staticmethod
    def __softmax_with_temperature(counts: list, temperature: int = 1) -> list:
        probs = np.array(counts, dtype=float)

        probs /= temperature
        e_probs = np.exp(probs - probs.max())
        return list(e_probs / e_probs.sum())
