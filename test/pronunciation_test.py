# import os
#
# import librosa
# import pytest
#
# from audio_speach_analizer_tool.service.accent_analysis_service import AccentAnalysisService
#
# base_dir = os.path.dirname(__file__)
#
# path1 = os.path.join(base_dir, 'accent_audio_test_data\\test1a.wav')
# path2 = os.path.join(base_dir, 'accent_audio_test_data\\test1b.wav')
#
#
#
# @pytest.mark.parametrize("path1, path2, word", accent_ok)
# def test_accent_ok(path1, path2, word):
#     accent_service = AccentAnalysisService()
#
#     signal1, sr1 = librosa.load(path1, sr=None)
#     duration1 = librosa.get_duration(y=signal1, sr=sr1)
#     signal2, sr2 = librosa.load(path2, sr=None)
#     duration2 = librosa.get_duration(y=signal2, sr=sr2)
#
#     is_accent_ok = accent_service.compare_accents_in_given_word(signal1, sr1, duration1, signal2, sr2, duration2)
#     assert is_accent_ok == True
#
#
# @pytest.mark.parametrize("path1, path2, word", accent_not_ok)
# def test_accent_not_ok(path1, path2, word):
#     accent_service = AccentAnalysisService()
#
#     signal1, sr1 = librosa.load(path1, sr=None)
#     duration1 = librosa.get_duration(y=signal1, sr=sr1)
#     signal2, sr2 = librosa.load(path2, sr=None)
#     duration2 = librosa.get_duration(y=signal2, sr=sr2)
#
#     is_accent_ok = accent_service.compare_accents_in_given_word(signal1, sr1, duration1, signal2, sr2, duration2)
#     assert is_accent_ok == False
