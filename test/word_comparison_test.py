import unittest
from unittest.mock import Mock

from service.words_analysis_service import WordsAnalysisService


class TestPercentOfWordsInOrder(unittest.TestCase):

    def create_mock_word(self, word):
        mock_word = Mock()
        mock_word.word = word
        return mock_word

    def test_exact_match(self):
        user_words = [self.create_mock_word("this"), self.create_mock_word("is"), self.create_mock_word("a"),
                      self.create_mock_word("test")]
        lector_words = [self.create_mock_word("this"), self.create_mock_word("is"), self.create_mock_word("a"),
                        self.create_mock_word("test")]
        self.assertEqual(WordsAnalysisService.calculate_word_sequence_accuracy(user_words, lector_words),
                         (1.0, 'this is a test', 'this is a test'))

    def test_extra_words_by_user(self):
        user_words = [self.create_mock_word("this"), self.create_mock_word("is"), self.create_mock_word("a"),
                      self.create_mock_word("simple"),
                      self.create_mock_word("test")]
        lector_words = [self.create_mock_word("this"), self.create_mock_word("is"), self.create_mock_word("a"),
                        self.create_mock_word("test")]
        self.assertEqual(WordsAnalysisService.calculate_word_sequence_accuracy(user_words, lector_words),
                         (1.0, 'this is a test', 'this is a simple test'))

    def test_extra_words_by_user_2(self):
        user_words = [self.create_mock_word("this"), self.create_mock_word("this"), self.create_mock_word("is"), self.create_mock_word("a"),
                      self.create_mock_word("simple"),
                      self.create_mock_word("test"), self.create_mock_word("simple")]
        lector_words = [self.create_mock_word("this"), self.create_mock_word("is"), self.create_mock_word("a"),
                        self.create_mock_word("test")]
        self.assertEqual(WordsAnalysisService.calculate_word_sequence_accuracy(user_words, lector_words),
                         (1.0, 'this is a test', 'this this is a simple test simple'))

    def test_extra_words_by_lector(self):
        user_words = [self.create_mock_word("this"), self.create_mock_word("is"), self.create_mock_word("a"),
                      self.create_mock_word("test")]
        lector_words = [self.create_mock_word("this"), self.create_mock_word("is"), self.create_mock_word("a"),
                        self.create_mock_word("simple"),
                        self.create_mock_word("test")]
        self.assertEqual(WordsAnalysisService.calculate_word_sequence_accuracy(user_words, lector_words),
                         (0.8, 'this is a simple test', 'this is a test'))

    def test_no_match(self):
        user_words = [self.create_mock_word("different"), self.create_mock_word("words")]
        lector_words = [self.create_mock_word("these"), self.create_mock_word("are"), self.create_mock_word("not"),
                        self.create_mock_word("same")]
        self.assertEqual(WordsAnalysisService.calculate_word_sequence_accuracy(user_words, lector_words),
                         (0.05, 'these are not same', 'different words'))

    def test_empty_user_words(self):
        user_words = []
        lector_words = [self.create_mock_word("some"), self.create_mock_word("words")]
        self.assertEqual(WordsAnalysisService.calculate_word_sequence_accuracy(user_words, lector_words),
                         (0.05, 'some words', ''))

    def test_empty_lector_words(self):
        user_words = [self.create_mock_word("some"), self.create_mock_word("words")]
        lector_words = []
        self.assertEqual(WordsAnalysisService.calculate_word_sequence_accuracy(user_words, lector_words),
                         (0.05, '', 'some words'))


if __name__ == '__main__':
    unittest.main()
