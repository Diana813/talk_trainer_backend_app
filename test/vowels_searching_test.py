import os

import librosa
import pytest

from service.vowels_detection_service import VowelsDetectionService
from utils.player import play_with_pauses_and_resume
from utils.plot_helper import plot_signal_with_highlighted_timeranges

base_dir = os.path.dirname(__file__)

path1 = os.path.join(base_dir, 'vowels_audio_test_data\\test1.wav')
path2 = os.path.join(base_dir, 'vowels_audio_test_data\\test2.wav')
path3 = os.path.join(base_dir, 'vowels_audio_test_data\\test3.wav')
path4 = os.path.join(base_dir, 'vowels_audio_test_data\\test4.wav')

vowels_audio_expected_vowels_count = [
    (path1, 1, 'to'),
    (path2, 2, 'lotka'),
    (path3, 3, 'komputer'),
    (path4, 4, 'koncentracja'),
]


@pytest.mark.parametrize("path, count, word", vowels_audio_expected_vowels_count)
def test_vowels_count(path, count, word):
    vowels_service = VowelsDetectionService()

    signal, sr = librosa.load(path, sr=None)
    vowel_segments = vowels_service.find_vowels(signal, sr)

    plot_signal_with_highlighted_timeranges(signal, sr, vowel_segments, f'expected vowel count: {count}, word: {word}')

    assert len(vowel_segments) == count
