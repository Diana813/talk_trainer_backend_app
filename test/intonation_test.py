import os

import librosa
import pytest

from service.intonation_analysis_service import IntonationAnalysisService
from utils.plot_helper import plot_pitch_lector_user

base_dir = os.path.dirname(__file__)

path1 = os.path.join(base_dir, 'intonation_audio_test_data\\test1a.wav')
path2 = os.path.join(base_dir, 'intonation_audio_test_data\\test1b.wav')

path3 = os.path.join(base_dir, 'intonation_audio_test_data\\test2a.wav')
path4 = os.path.join(base_dir, 'intonation_audio_test_data\\test2b.wav')

path5 = os.path.join(base_dir, 'intonation_audio_test_data\\test3a.wav')
path6 = os.path.join(base_dir, 'intonation_audio_test_data\\test3b.wav')

path7 = os.path.join(base_dir, 'intonation_audio_test_data\\test4a.wav')
path8 = os.path.join(base_dir, 'intonation_audio_test_data\\test4b.wav')

path9 = os.path.join(base_dir, 'intonation_audio_test_data\\test5a.wav')
path10 = os.path.join(base_dir, 'intonation_audio_test_data\\test5b.wav')

low_similarity_data = [
    (path1, path2),
    (path5, path6),
]

high_similarity_data = [
    (path3, path4),
    (path7, path8),
    (path9, path10)
]


@pytest.mark.parametrize("path1, path2", high_similarity_data)
def test_high_similarity(path1, path2):
    intonation_service = IntonationAnalysisService()

    signal1, sr1 = librosa.load(path1, sr=None)
    signal2, sr2 = librosa.load(path2, sr=None)
    pitch1, pitch2, similarity = intonation_service.get_intonation_success_rate(signal1, signal2)

    plot_pitch_lector_user(pitch1, pitch2, f'oczekiwana wysoka zbieżność, uzyskana zbieżność: {similarity * 100}%')

    assert similarity > 0.5


@pytest.mark.parametrize("path1, path2", low_similarity_data)
def test_low_similarity(path1, path2):
    intonation_service = IntonationAnalysisService()

    signal1, sr1 = librosa.load(path1, sr=None)
    signal2, sr2 = librosa.load(path2, sr=None)
    _, _, similarity = intonation_service.get_intonation_success_rate(signal1, signal2)

    assert similarity <= 0.5
