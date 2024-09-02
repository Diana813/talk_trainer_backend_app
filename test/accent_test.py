import os

import librosa
import pytest

from service.accent_analysis_service import AccentAnalysisService
from utils.player import play_audio
from utils.plot_helper import plot_two_signals

base_dir = os.path.dirname(__file__)

paths = {}

for i in range(1, 51):
    for suffix in ['a', 'b', 'c']:
        key = f'path{i}{suffix}'
        path = os.path.join(base_dir, f'accent_audio_test_data/test{i}{suffix}.wav')
        paths[key] = path


accent_ok = [
    (paths['path2a'], paths['path2b'], 'lotka'),
    (paths['path3a'], paths['path3b'], 'komputer'),
    (paths['path4a'], paths['path4b'], 'koncentracja'),
    (paths['path5a'], paths['path5b'], 'szczebrzeszyn'),
    (paths['path6a'], paths['path6b'], 'rower'),
    (paths['path8a'], paths['path8b'], 'fotel'),
    (paths['path9a'], paths['path9b'], 'biegać'),
    (paths['path10a'], paths['path10b'], 'gitara'),
    (paths['path11a'], paths['path11b'], 'świecznik'),
    (paths['path12a'], paths['path12b'], 'historia'),
    (paths['path13a'], paths['path13b'], 'kubek'),
    (paths['path14a'], paths['path14b'], 'budda'),
    (paths['path15a'], paths['path15b'], 'piłka'),
    (paths['path16a'], paths['path16b'], 'osiedle'),
    (paths['path17a'], paths['path17b'], 'lodówka'),
    (paths['path18a'], paths['path18b'], 'kominek'),
    (paths['path19a'], paths['path19b'], 'poduszka'),
    (paths['path20a'], paths['path20b'], 'śniadanie'),
    (paths['path21a'], paths['path21b'], 'szczotka'),
    (paths['path22a'], paths['path22b'], 'pilot'),
    (paths['path23a'], paths['path23b'], 'samochód'),
    (paths['path24a'], paths['path24b'], 'kolumna'),
    (paths['path25a'], paths['path25b'], 'zeszyt'),
    (paths['path26a'], paths['path26b'], 'kuropatwa'),
    (paths['path27a'], paths['path27b'], 'nośnik'),
    (paths['path28a'], paths['path28b'], 'piesek'),
    (paths['path29a'], paths['path29b'], 'kotek'),
    (paths['path30a'], paths['path30b'], 'rejestr'),
    (paths['path31a'], paths['path31b'], 'ropucha'),
    (paths['path32a'], paths['path32b'], 'kwiatek'),
    (paths['path33a'], paths['path33b'], 'słóweczka'),
    (paths['path34a'], paths['path34b'], 'somatyczny'),
    (paths['path35a'], paths['path35b'], 'sympatyczny'),
    (paths['path36a'], paths['path36b'], 'głośność'),
    (paths['path37a'], paths['path37b'], 'serwetka'),
    (paths['path38a'], paths['path38b'], 'ołówek'),
    (paths['path39a'], paths['path39b'], 'wstążka'),
    (paths['path40a'], paths['path40b'], 'światło'),
    (paths['path41a'], paths['path41b'], 'komar'),
    (paths['path42a'], paths['path42b'], 'ręcznik'),
    (paths['path43a'], paths['path43b'], 'drzwiczki'),
    (paths['path44a'], paths['path44b'], 'talerz'),
    (paths['path45a'], paths['path45b'], 'obrazek'),
    (paths['path46a'], paths['path46b'], 'telewizor'),
    (paths['path47a'], paths['path47b'], 'płyta'),
    (paths['path48a'], paths['path48b'], 'sernik'),
    (paths['path49a'], paths['path49b'], 'obiad'),
    (paths['path50a'], paths['path50b'], 'twarzyczka')
]

accent_not_ok = [
    (paths['path2a'], paths['path2c'], 'lotka'),
    (paths['path3a'], paths['path3c'], 'komputer'),
    (paths['path4a'], paths['path4c'], 'koncentracja'),
    (paths['path5a'], paths['path5c'], 'szczebrzeszyn'),
    (paths['path6a'], paths['path6c'], 'rower'),
    (paths['path8a'], paths['path8c'], 'fotel'),
    (paths['path9a'], paths['path9c'], 'biegać'),
    (paths['path10a'], paths['path10c'], 'gitara'),
    (paths['path11a'], paths['path11c'], 'świecznik'),
    (paths['path12a'], paths['path12c'], 'historia'),
    (paths['path13a'], paths['path13c'], 'kubek'),
    (paths['path14a'], paths['path14c'], 'budda'),
    (paths['path15a'], paths['path15c'], 'piłka'),
    (paths['path16a'], paths['path16c'], 'osiedle'),
    (paths['path17a'], paths['path17c'], 'lodówka'),
    (paths['path18a'], paths['path18c'], 'kominek'),
    (paths['path19a'], paths['path19c'], 'poduszka'),
    (paths['path20a'], paths['path20c'], 'śniadanie'),
    (paths['path21a'], paths['path21c'], 'szczotka'),
    (paths['path22a'], paths['path22c'], 'pilot'),
    (paths['path23a'], paths['path23c'], 'samochód'),
    (paths['path24a'], paths['path24c'], 'kolumna'),
    (paths['path25a'], paths['path25c'], 'zeszyt'),
    (paths['path26a'], paths['path26c'], 'kuropatwa'),
    (paths['path27a'], paths['path27c'], 'nośnik'),
    (paths['path28a'], paths['path28c'], 'piesek'),
    (paths['path29a'], paths['path29c'], 'kotek'),
    (paths['path30a'], paths['path30c'], 'rejestr'),
    (paths['path31a'], paths['path31c'], 'ropucha'),
    (paths['path32a'], paths['path32c'], 'kwiatek'),
    (paths['path33a'], paths['path33c'], 'słóweczka'),
    (paths['path34a'], paths['path34c'], 'somatyczny'),
    (paths['path35a'], paths['path35c'], 'sympatyczny'),
    (paths['path36a'], paths['path36c'], 'głośność'),
    (paths['path37a'], paths['path37c'], 'serwetka'),
    (paths['path38a'], paths['path38c'], 'ołówek'),
    (paths['path39a'], paths['path39c'], 'wstążka'),
    (paths['path40a'], paths['path40c'], 'światło'),
    (paths['path41a'], paths['path41c'], 'komar'),
    (paths['path42a'], paths['path42c'], 'ręcznik'),
    (paths['path43a'], paths['path43c'], 'drzwiczki'),
    (paths['path44a'], paths['path44c'], 'talerz'),
    (paths['path45a'], paths['path45c'], 'obrazek'),
    (paths['path46a'], paths['path46c'], 'telewizor'),
    (paths['path47a'], paths['path47c'], 'płyta'),
    (paths['path48a'], paths['path48c'], 'sernik'),
    (paths['path49a'], paths['path49c'], 'obiad'),
    (paths['path50a'], paths['path50c'], 'twarzyczka')
]


@pytest.mark.parametrize("path1, path2, word", accent_ok)
def test_accent_ok(path1, path2, word):
    accent_service = AccentAnalysisService()

    signal1, sr1 = librosa.load(path1, sr=None)
    signal2, sr2 = librosa.load(path2, sr=None)

    # play_audio(path1)
    # play_audio(path2)

    is_accent_ok = accent_service.compare_accents_in_given_word(signal1, sr1, signal2, sr2)
    assert is_accent_ok == True


@pytest.mark.parametrize("path1, path2, word", accent_not_ok)
def test_accent_not_ok(path1, path2, word):
    accent_service = AccentAnalysisService()

    signal1, sr1 = librosa.load(path1, sr=None)
    signal2, sr2 = librosa.load(path2, sr=None)

    # play_audio(path1)
    # play_audio(path2)

    is_accent_ok = accent_service.compare_accents_in_given_word(signal1, sr1, signal2, sr2)
    assert is_accent_ok == False
