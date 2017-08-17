# -*- coding: utf-8 -*-
import os
import sys
from icenine.core import CONFIG

# secrets module is python>=3.6
try:
    from secrets import randbelow
except ImportError:
    import random
    random.seed(os.urandom(32))
    randbelow = lambda x: random.randrange(x)

BURN_CYCLES=10061


class SeedWords:
    """ Generate seed words from a file dictionary 

        Usage
        -----
        >>> from icenine.core.seedwords import SeedWords
        >>> sw = SeedWords("icenine/contrib/words.txt")
        >>> sw.word_count
        40089
        >>> sw.random_seed_words()
        ['fado', 'amuses', 'covey', 'swine', 'crazy', 'boobie', 'dope', 'offers', 'cagots', 'roined', 'crews', 'skewed']
    """

    def __init__(self, dict_file):
        if type(dict_file) is not str:
            raise TypeError("Invalid filename")
        elif not os.path.exists(dict_file):
            raise FileNotFoundError("Dictionary file not found")

        self.dictionary_file = dict_file
        self.words = []

        self._load_file()

    def _load_file(self):
        """ Load the dictionary file """

        # Load the file into a list of words
        with open(self.dictionary_file) as d:
            self.words = d.read().splitlines()

        # Get count
        self.word_count = len(self.words)

        # Let's use an arbitrary number!
        if self.word_count < 1024:
            raise ValueError("List is too short.  Not enough entropy!")

    def random_seed_words(self, count=12):
        """ Get random seed words """

        seed_words = []
        cycle = 0

        while len(seed_words) < count:
            if cycle < BURN_CYCLES:
                cycle += 1
                randbelow(self.word_count)
                continue
            else:
                seed_words.append(self.words[randbelow(self.word_count)])

        return seed_words
