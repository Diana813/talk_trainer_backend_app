import os

import librosa
import pytest

from service.vowels_detection_service import VowelsDetectionService
from utils.player import play_audio
from utils.plot_helper import plot_signal_with_highlighted_timeranges

base_dir = os.path.dirname(__file__)

path1 = os.path.join(base_dir, 'vowels_audio_test_data\\test1.wav')
path2 = os.path.join(base_dir, 'vowels_audio_test_data\\test2.wav')
path3 = os.path.join(base_dir, 'vowels_audio_test_data\\test3.wav')
path4 = os.path.join(base_dir, 'vowels_audio_test_data\\test4.wav')
path5 = os.path.join(base_dir, 'vowels_audio_test_data\\test5.wav')
path6 = os.path.join(base_dir, 'vowels_audio_test_data\\test6.wav')
path7 = os.path.join(base_dir, 'vowels_audio_test_data\\test7.wav')
path8 = os.path.join(base_dir, 'vowels_audio_test_data\\test8.wav')
path9 = os.path.join(base_dir, 'vowels_audio_test_data\\test9.wav')
path10 = os.path.join(base_dir, 'vowels_audio_test_data\\test10.wav')
path11 = os.path.join(base_dir, 'vowels_audio_test_data\\test11.wav')
path12 = os.path.join(base_dir, 'vowels_audio_test_data\\test12.wav')
path13 = os.path.join(base_dir, 'vowels_audio_test_data\\test13.wav')
path14 = os.path.join(base_dir, 'vowels_audio_test_data\\test14.wav')
path15 = os.path.join(base_dir, 'vowels_audio_test_data\\test15.wav')
path16 = os.path.join(base_dir, 'vowels_audio_test_data\\test16.wav')
path17 = os.path.join(base_dir, 'vowels_audio_test_data\\test17.wav')
path18 = os.path.join(base_dir, 'vowels_audio_test_data\\test18.wav')
path19 = os.path.join(base_dir, 'vowels_audio_test_data\\test19.wav')
path20 = os.path.join(base_dir, 'vowels_audio_test_data\\test20.wav')
path21 = os.path.join(base_dir, 'vowels_audio_test_data\\test21.wav')
path22 = os.path.join(base_dir, 'vowels_audio_test_data\\test22.wav')
path23 = os.path.join(base_dir, 'vowels_audio_test_data\\test23.wav')
path24 = os.path.join(base_dir, 'vowels_audio_test_data\\test24.wav')
path25 = os.path.join(base_dir, 'vowels_audio_test_data\\test25.wav')
path26 = os.path.join(base_dir, 'vowels_audio_test_data\\test26.wav')
path27 = os.path.join(base_dir, 'vowels_audio_test_data\\test27.wav')
path28 = os.path.join(base_dir, 'vowels_audio_test_data\\test28.wav')
path29 = os.path.join(base_dir, 'vowels_audio_test_data\\test29.wav')
path30 = os.path.join(base_dir, 'vowels_audio_test_data\\test30.wav')
path31 = os.path.join(base_dir, 'vowels_audio_test_data\\test31.wav')
path32 = os.path.join(base_dir, 'vowels_audio_test_data\\test32.wav')
path33 = os.path.join(base_dir, 'vowels_audio_test_data\\test33.wav')
path34 = os.path.join(base_dir, 'vowels_audio_test_data\\test34.wav')
path35 = os.path.join(base_dir, 'vowels_audio_test_data\\test35.wav')
path36 = os.path.join(base_dir, 'vowels_audio_test_data\\test36.wav')
path37 = os.path.join(base_dir, 'vowels_audio_test_data\\test37.wav')
path38 = os.path.join(base_dir, 'vowels_audio_test_data\\test38.wav')
path39 = os.path.join(base_dir, 'vowels_audio_test_data\\test39.wav')
path40 = os.path.join(base_dir, 'vowels_audio_test_data\\test40.wav')
path41 = os.path.join(base_dir, 'vowels_audio_test_data\\test41.wav')
path42 = os.path.join(base_dir, 'vowels_audio_test_data\\test42.wav')
path43 = os.path.join(base_dir, 'vowels_audio_test_data\\test43.wav')
path44 = os.path.join(base_dir, 'vowels_audio_test_data\\test44.wav')
path45 = os.path.join(base_dir, 'vowels_audio_test_data\\test45.wav')
path46 = os.path.join(base_dir, 'vowels_audio_test_data\\test46.wav')
path47 = os.path.join(base_dir, 'vowels_audio_test_data\\test47.wav')
path48 = os.path.join(base_dir, 'vowels_audio_test_data\\test48.wav')
path49 = os.path.join(base_dir, 'vowels_audio_test_data\\test49.wav')
path50 = os.path.join(base_dir, 'vowels_audio_test_data\\test50.wav')


vowels_audio_expected_vowels_count = [
    (path1, 1, 'to'),
    (path2, 2, 'lotka'),
    (path3, 3, 'komputer'),
    (path4, 4, 'koncentracja'),
    (path5, 3, 'szczebrzeszyn'),
    (path6, 2, 'rower'),
    (path7, 1, 'koc'),
    (path8, 2, 'fotel'),
    (path9, 2, 'biegać'),
    (path10, 3, 'gitara'),
    (path11, 2, 'świecznik'),
    (path12, 3, 'historia'),
    (path13, 2, 'kubek'),
    (path14, 2, 'budda'),
    (path15, 2, 'piłka'),
    (path16, 3, 'osiedle'),
    (path17, 3, 'lodówka'),
    (path18, 3, 'kominek'),
    (path19, 3, 'poduszka'),
    (path20, 3, 'śniadanie'),
    (path21, 2, 'szczotka'),
    (path22, 2, 'pilot'),
    (path23, 3, 'samochód'),
    (path24, 3, 'kolumna'),
    (path25, 2, 'zeszyt'),
    (path26, 4, 'kuropatwa'),
    (path27, 2, 'nośnik'),
    (path28, 2, 'piesek'),
    (path29, 2, 'kotek'),
    (path30, 2, 'rejestr'),
    (path31, 3, 'ropucha'),
    (path32, 2, 'kwiatek'),
    (path33, 3, 'słóweczka'),
    (path34, 4, 'somatyczny'),
    (path35, 4, 'sympatyczny'),
    (path36, 2, 'głośność'),
    (path37, 3, 'serwetka'),
    (path38, 3, 'ołówek'),
    (path39, 2, 'wstążka'),
    (path40, 2, 'światło'),
    (path41, 2, 'komar'),
    (path42, 2, 'ręcznik'),
    (path43, 2, 'drzwiczki'),
    (path44, 2, 'talerz'),
    (path45, 3, 'obrazek'),
    (path46, 4, 'telewizor'),
    (path47, 2, 'płyta'),
    (path48, 2, 'sernik'),
    (path49, 2, 'obiad'),
    (path50, 3, 'twarzyczka')
]


@pytest.mark.parametrize("path, count, word", vowels_audio_expected_vowels_count)
def test_vowels_count(path, count, word):
    vowels_service = VowelsDetectionService()
    signal, sr = librosa.load(path, sr=None)

    # play_audio(path)

    vowel_segments = vowels_service.find_vowels(signal, sr)

    # plot_signal_with_highlighted_timeranges(signal, sr, vowel_segments, f'expected vowel count: {count}, word: {word}')

    assert len(vowel_segments) == count
