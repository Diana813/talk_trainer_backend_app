from concurrent.futures import ThreadPoolExecutor, as_completed

import numpy as np
from scipy.interpolate import interp1d
from scipy.stats import pearsonr

from data.model.output_models.accent_data import AccentData
from service.audio_service import AudioService
from service.vowels_detection_service import VowelsDetectionService


class AccentAnalysisService:
    def __init__(self):
        self.vowels_service = VowelsDetectionService()
        self.audio_service = AudioService()

    def compare_accents(self, lector_audio, lsr, time_range, user_audio, usr, words_lector, words_user):
        if not words_user or not words_lector:
            return []

        for word in words_lector:
            word.start -= time_range.start
            word.end -= time_range.start

        long_words_lector, long_words_user = self.get_long_user_words_matching_lector_words(words_lector, words_user)

        if len(long_words_lector) < 1 or len(long_words_user) < 1:
            return []

        difference = []
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(
                lambda pair: self.process_word_pair(lector_audio, lsr, user_audio, usr, *pair),
                pair) for pair in zip(long_words_lector, long_words_user)]

            for future in as_completed(futures):
                try:
                    result = future.result()
                    if result is not None:
                        difference.append(result)
                except Exception as e:
                    print(f"Exception occurred: {e}")
                    return difference

        executor.shutdown()
        return difference

    def process_word_pair(self, lector_audio, lsr, user_audio, usr, word_lector, word_user):

        expected_number_of_vowels = self.count_syllables(word_lector.word)

        segment_lector = self.audio_service.extract_segment(lector_audio, word_lector.start, word_lector.end, lsr)
        segment_user = self.audio_service.extract_segment(user_audio, word_user.start, word_user.end, usr)

        lector_duration = word_lector.end - word_lector.start
        user_duration = word_user.end - word_user.start

        is_accent_the_same = self.compare_accents_in_given_word(segment_lector, lsr, lector_duration, segment_user, usr,
                                                                user_duration, expected_number_of_vowels)

        if not is_accent_the_same:
            lector_signal_data_to_send = self.audio_service.sample_audio_segment_to_draw_chart(segment_lector)
            user_signal_data_to_send = self.audio_service.sample_audio_segment_to_draw_chart(segment_user)
            return AccentData(word_lector.word, lector_signal_data_to_send, user_signal_data_to_send)
        return None

    def compare_accents_in_given_word(self, lector_signal, lsr, lector_duration, user_signal, usr, user_duration,
                                      expected_number_of_vowels):
        lector_vowels = self.vowels_service.find_vowels(lector_signal, lsr)
        user_vowels = self.vowels_service.find_vowels(user_signal, usr)

        while len(lector_vowels) > expected_number_of_vowels:
            lector_vowels = self.vowels_service.merge_closest_intervals(lector_vowels)

        while len(user_vowels) > expected_number_of_vowels:
            user_vowels = self.vowels_service.merge_closest_intervals(user_vowels)

        if len(user_vowels) < 1 or len(lector_vowels) < 1:
            return False

        lector_syllables = self.vowels_service.find_syllables(0, lector_duration, lector_vowels)
        user_syllables = self.vowels_service.find_syllables(0, user_duration, user_vowels)

        if len(lector_syllables) < 1 or len(user_syllables) < 1:
            return False

        energy_lector = self.calculate_rms_percentage_for_segments(lector_signal, lsr, lector_syllables)
        energy_user = self.calculate_rms_percentage_for_segments(user_signal, usr, user_syllables)

        correlation = self.calculate_correlation_between_energy(energy_lector, energy_user)
        similarity = (correlation + 1) / 2

        return similarity > 0.9

    def calculate_rms_percentage_for_segments(self, audio, sr, segments):
        def calculate_rms(segment):
            return np.sqrt(np.mean(np.square(segment)))

        try:
            rms_values = [
                calculate_rms(self.audio_service.extract_segment(audio, start, end, sr))
                for start, end in segments
            ]

            total_rms = sum(rms_values)
            if total_rms == 0:
                return 0

            rms_percentages = [(rms / total_rms) * 100 for rms in rms_values]

            return rms_percentages
        except Exception as e:
            print(e)
            return 0

    def get_long_user_words_matching_lector_words(self, lector_transcript_fragment, user_transcript):
        common_words_lector = []
        common_words_user = []

        user_index = 0

        for word_lector in lector_transcript_fragment:
            if self.count_syllables(word_lector.word) > 1:
                while user_index < len(user_transcript):
                    word_user = user_transcript[user_index]
                    user_index += 1

                    if word_lector.word == word_user.word:
                        common_words_lector.append(word_lector)
                        common_words_user.append(word_user)
                        break

        return common_words_lector, common_words_user,

    def count_syllables(self, word):
        syllable_count = 0

        for char in word:
            if self.is_vowel(char):
                syllable_count += 1

        return max(syllable_count, 1)

    @staticmethod
    def is_vowel(letter):
        return letter.lower() in 'aeiou'

    @staticmethod
    def calculate_accent_accuracy(utterance_length, difference_list_length):
        return (utterance_length - difference_list_length) / utterance_length

    def calculate_correlation_between_energy(self, energy1, energy2):
        interp_energy1, interp_energy2 = self.interpolate(energy1, energy2)
        correlation, _ = pearsonr(interp_energy1, interp_energy2)
        return correlation

    @staticmethod
    def interpolate(signal1, signal2):
        len1, len2 = len(signal1), len(signal2)

        if len1 < 2 or len2 < 2:
            return

        x1 = np.linspace(0, 1, len1)
        x2 = np.linspace(0, 1, len2)

        interp_func1 = interp1d(x1, signal1, kind='linear')
        interp_func2 = interp1d(x2, signal2, kind='linear')

        common_length = max(len1, len2)
        common_x = np.linspace(0, 1, common_length)

        interp_signal1 = interp_func1(common_x)
        interp_signal2 = interp_func2(common_x)

        return interp_signal1, interp_signal2
