import string
import pickle
from nltk import word_tokenize


class Tokenizer:
    def __init__(self, pretrained: bool = False, file_path: str = None, text: str = None) -> None:
        self.vocab = {'<soj>', '<eoj>'}
        self.w2i = dict({'<soj>': 0, '<eoj>': 1})
        self.i2w = ['<soj>', '<eoj>']

        if pretrained:
            if file_path is None:
                raise ValueError('File path is not specified')

            self.load(file_path)
        else:
            if text is None:
                raise ValueError('Text data is not specified')

            jokes = self.__joke_split(text)
            for joke in jokes:
                tokenized = self._tokenize_to_words(joke)
                self.__add_to_vocab(tokenized)

    def tokenize(self, text: str, add_special_tokens: bool = True) -> list:
        tokenized = self._tokenize_to_words(text)
        if add_special_tokens:
            tokenized = ['<soj>'] + tokenized + ['<eoj>']

        tokens = []
        for word in tokenized:
            if word in self.vocab:
                tokens.append(self.w2i[word])

        return tokens

    def detokenize(self, tokenized: list) -> str:
        words = self._detokenize_to_words(tokenized)

        if len(words) == 0:
            return ''

        text = words[0].capitalize()
        for i in range(1, len(words)):
            if words[i - 1] in '.!?-—':
                text += ' ' + words[i].capitalize()
                continue

            if words[i - 1] == '\n':
                text += words[i].capitalize()
                continue

            if words[i] in '-—':
                text += ' ' + words[i]
                continue

            if words[i] in string.punctuation:
                text += words[i]
                continue

            text += ' ' + words[i]

        return text

    def vocab_size(self) -> int:
        return len(self.vocab)

    def save(self, file_name: str) -> None:
        tokenizer = {
            'vocab': self.vocab,
            'w2i': self.w2i,
            'i2w': self.i2w,
        }

        pickle.dump(tokenizer, open(file_name + '.pkl', 'wb'))

    def load(self, file_path: str) -> None:
        with open(file_path, 'rb') as pkl_file:
            tokenizer = pickle.load(pkl_file)

        self.vocab = tokenizer['vocab']
        self.w2i = tokenizer['w2i']
        self.i2w = tokenizer['i2w']

    @staticmethod
    def _tokenize_to_words(text: str) -> list:
        if len(text) == 0:
            return []

        if text[0] == '\n':
            text = text[1:]

        text = text.lower().replace('\n', ' eol ')
        pre_tokenized = word_tokenize(text)

        tokenized = []

        for idx, word in enumerate(pre_tokenized):
            if word in ' \"#$%&\'()+/<=>@[]^_`{|}~\\':
                continue

            if idx == 0:
                tokenized.append(word)
                continue

            if word.find('eol') != -1:
                tokenized.append('\n')
                continue

            if word in '.?!-—':
                tokenized.append(word)
                continue

            if word in ',;:':
                if len(tokenized) != 0:
                    tokenized[-1] += word
                continue

            tokenized.append(word)

        return tokenized

    def _detokenize_to_words(self, tokenized: list) -> list:
        words = []
        for token in tokenized:
            word = self.i2w[token]
            if word not in ['<soj>', '<eoj>']:
                words.append(word)

        return words

    def __add_to_vocab(self, tokenized: list) -> None:
        for word in tokenized:
            if word not in self.vocab:
                self.vocab.add(word)
                self.w2i[word] = len(self.i2w)
                self.i2w.append(word)

    @staticmethod
    def __joke_split(text: string) -> list:
        jokes = text.split('<eoa>')
        return jokes
