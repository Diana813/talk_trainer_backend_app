import unittest

from utils.vowel_checker import VowelChecker


class TestVowelChecker(unittest.TestCase):

    def setUp(self):
        self.vowel_checker = VowelChecker()

    def test_single_vowel(self):
        self.assertEqual(1, self.vowel_checker.count_syllables('a'))
        self.assertEqual(1, self.vowel_checker.count_syllables('i'))

    def test_simple_words(self):
        self.assertEqual(1, self.vowel_checker.count_syllables('cat'))
        self.assertEqual(1, self.vowel_checker.count_syllables('dog'))
        self.assertEqual(3, self.vowel_checker.count_syllables('syllable'))

    def test_words_with_combinations(self):
        self.assertEqual(2, self.vowel_checker.count_syllables('beauty'))
        self.assertEqual(4, self.vowel_checker.count_syllables('education'))
        self.assertEqual(3, self.vowel_checker.count_syllables('aesthetic'))

    def test_complex_words(self):
        self.assertEqual(6, self.vowel_checker.count_syllables('onomatopoeia'))
        self.assertEqual(5, self.vowel_checker.count_syllables('unbelievable'))

    def test_edge_cases(self):
        self.assertEqual(1, self.vowel_checker.count_syllables(''))
        self.assertEqual(1, self.vowel_checker.count_syllables('b'))

if __name__ == '__main__':
    unittest.main()