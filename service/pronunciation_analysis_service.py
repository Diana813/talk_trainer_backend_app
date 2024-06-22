import librosa
from scipy.interpolate import interp1d

from service.audio_service import AudioService
from service.vowels_detection_service import VowelsDetectionService

import parselmouth
import numpy as np


class PronunciationAnalysisService:
    def __init__(self):
        self.vowels_service = VowelsDetectionService()
        self.audio_service = AudioService()

    def compare_vowels_pronunciation(self, user_audio_filepath, lector_audio_filepath, lector_time_range, user_words,
                                     lector_words):
        for word in lector_words:
            word.start -= lector_time_range.start
            word.end -= lector_time_range.start

        lector_audio, lsr = self.audio_service.load_audio_segment(lector_audio_filepath, lector_time_range.start,
                                                                  lector_time_range.end)
        user_audio, usr = librosa.load(user_audio_filepath, sr=None)

        common_words_lector, common_words_user = self.get_user_words_matching_lector_words(lector_words, user_words)

        lector_vowels = self.get_vowels_for_each_word(common_words_lector, lector_audio, lsr)
        user_vowels = self.get_vowels_for_each_word(common_words_user, user_audio, usr)

        while len(lector_vowels) != len(user_vowels):
            if len(lector_vowels) > len(user_vowels):
                break

            if len(lector_vowels) > len(user_vowels):
                lector_vowels = self.merge_closest_intervals(lector_vowels)
            else:
                user_vowels = self.merge_closest_intervals(user_vowels)

        lector_formants_list = self.get_formants_for_each_vowel(lector_audio_filepath, lector_vowels)

        user_formants_list = self.get_formants_for_each_vowel(user_audio_filepath, user_vowels)

        low_correlation_formants, pronunciation_accuracy = (
            self.identify_low_correlation_formants_with_words(lector_formants_list, user_formants_list))

        return low_correlation_formants, pronunciation_accuracy

    def identify_low_correlation_formants_with_words(self, lector_formants_list, user_formants_list):
        flatten_lector_formants = [(word, vowel, formants) for (word, vowel, formants) in lector_formants_list]
        flatten_user_formants = [(word, vowel, formants) for (word, vowel, formants) in user_formants_list]

        lf1_mean, lf1_std, lf2_mean, lf2_std = self.get_mean_and_std_for_utterance(flatten_lector_formants)
        uf1_mean, uf1_std, uf2_mean, uf2_std = self.get_mean_and_std_for_utterance(flatten_user_formants)

        normalized_lector_formants = []
        for word, vowel, formants in flatten_lector_formants:
            normalized_vowel_formants = self.normalize_formants_lobanov(lf1_mean, lf1_std, lf2_mean, lf2_std, word,
                                                                        vowel,
                                                                        formants)
            normalized_lector_formants.append(normalized_vowel_formants)

        normalized_user_formants = []
        for word, vowel, formants in flatten_user_formants:
            normalized_vowel_formants = self.normalize_formants_lobanov(uf1_mean, uf1_std, uf2_mean, uf2_std, word,
                                                                        vowel,
                                                                        formants)
            normalized_user_formants.append(normalized_vowel_formants)

        low_correlation_formants = self.identify_low_correlation_formants(normalized_user_formants,
                                                                          normalized_lector_formants)

        pronunciation_accuracy = self.calculate_pronunciation_accuracy(low_correlation_formants,
                                                                       flatten_lector_formants)
        return low_correlation_formants, pronunciation_accuracy

    def get_formants_for_each_vowel(self, file_path, vowels):
        snd_lector = parselmouth.Sound(file_path)
        formants_list = []
        for word_vowel in vowels:
            word, vowel = word_vowel
            start, end = vowel
            sound_fragment = snd_lector.extract_part(from_time=start, to_time=end)
            formants = self.extract_formants(sound_fragment, start, end)

            formants_list.append((word, vowel, formants))
        return formants_list

    @staticmethod
    def calculate_pronunciation_accuracy(low_correlation_formants, all_formants):
        accuracy = 0
        if len(all_formants) > 0:
            accuracy = (len(all_formants) - len(low_correlation_formants)) / len(all_formants)
        return accuracy

    def get_vowels_for_each_word(self, words, audio_signal, sr):
        vowels = []

        for word in words:
            audio_segment = self.audio_service.extract_segment(audio_signal, word.start, word.end, sr)
            vowel_list = self.vowels_service.find_vowels(audio_segment, sr)
            vowels_with_word_info = [(word, vowel) for vowel in vowel_list]
            vowels.append(vowels_with_word_info)

        flattened_vowels = [vowel for sublist in vowels for vowel in sublist]
        return flattened_vowels

    @staticmethod
    def extract_formants(sound_fragment, start_time, end_time, time_step=0.01):
        formants = sound_fragment.to_formant_burg(time_step=time_step)

        formant_data = []

        for time in np.arange(start_time, end_time, time_step):
            f1 = formants.get_value_at_time(1, time)
            f2 = formants.get_value_at_time(2, time)

            if not np.isnan(f1) and not np.isnan(f2):
                formant_data.append((time, f1, f2))

        return formant_data

    @staticmethod
    def normalize_formants_lobanov(f1_mean, f1_std, f2_mean, f2_std, word, vowel, formants):
        if not formants:
            return word, vowel, []

        normalized_data = []

        for val in formants:
            norm_f1 = (val[0] - f1_mean) / f1_std if f1_std else 0
            norm_f2 = (val[1] - f2_mean) / f2_std if f2_std else 0
            normalized_data.append((norm_f1, norm_f2))

        return word, vowel, normalized_data

    @staticmethod
    def get_mean_and_std_for_utterance(vowel_formant_list):
        all_f1_values = []
        all_f2_values = []

        for _, _, formants in vowel_formant_list:
            if not formants or len(formants) < 2:
                continue

            f1_values, f2_values = formants[0], formants[1]

            all_f1_values.extend(f1_values)
            all_f2_values.extend(f2_values)

        f1_mean = np.nanmean(all_f1_values) if all_f1_values else float('nan')
        f1_std = np.nanstd(all_f1_values) if all_f1_values else float('nan')
        f2_mean = np.nanmean(all_f2_values) if all_f2_values else float('nan')
        f2_std = np.nanstd(all_f2_values) if all_f2_values else float('nan')

        return f1_mean, f1_std, f2_mean, f2_std

    @staticmethod
    def get_user_words_matching_lector_words(lector_transcript_fragment, user_transcript):
        common_words_lector = []
        common_words_user = []

        for word_lector in lector_transcript_fragment:
            for word_user in user_transcript:
                if word_lector.word == word_user.word:
                    common_words_lector.append(word_lector)
                    common_words_user.append(word_user)
                    break

        return common_words_lector, common_words_user

    def identify_low_correlation_formants(self, user_formants, lector_formants, threshold=0.7):
        low_correlation_formants = []

        for (user_word, user_vowel, user_formants_data), (lector_word, lector_vowel, lector_formants_data) in zip(
                user_formants, lector_formants):
            if len(user_formants_data) == 0 or len(lector_formants_data) == 0:
                continue

            user_f1_values = [val[0] for val in user_formants_data]
            user_f2_values = [val[1] for val in user_formants_data]
            lector_f1_values = [val[0] for val in lector_formants_data]
            lector_f2_values = [val[1] for val in lector_formants_data]

            target_length = max(len(user_f1_values), len(lector_f1_values))

            user_f1_values = self.interpolate_formants(user_f1_values, target_length)
            lector_f1_values = self.interpolate_formants(lector_f1_values, target_length)
            user_f2_values = self.interpolate_formants(user_f2_values, target_length)
            lector_f2_values = self.interpolate_formants(lector_f2_values, target_length)

            correlation_f1 = np.corrcoef(user_f1_values, lector_f1_values)[0, 1]

            correlation_f2 = np.corrcoef(user_f2_values, lector_f2_values)[0, 1]

            if correlation_f1 < threshold or correlation_f2 < threshold:
                low_correlation_formants.append((user_word, lector_word, user_vowel, lector_vowel))

        return low_correlation_formants

    @staticmethod
    def merge_shortest_vowel_with_neighbor(vowel_word_pairs):
        if not vowel_word_pairs:
            return []

        shortest_syllable_index = min(range(len(vowel_word_pairs)),
                                      key=lambda i: vowel_word_pairs[i][1][1] - vowel_word_pairs[i][1][0])

        neighbor_index = None
        if shortest_syllable_index > 0 and (shortest_syllable_index == len(vowel_word_pairs) - 1 or
                                            (vowel_word_pairs[shortest_syllable_index - 1][1][1] -
                                             vowel_word_pairs[shortest_syllable_index - 1][1][0]) <
                                            (vowel_word_pairs[shortest_syllable_index + 1][1][1] -
                                             vowel_word_pairs[shortest_syllable_index + 1][1][0])):
            neighbor_index = shortest_syllable_index - 1
        else:
            neighbor_index = shortest_syllable_index + 1

        merged_syllable = (vowel_word_pairs[shortest_syllable_index][0],
                           (
                               min(vowel_word_pairs[shortest_syllable_index][1][0],
                                   vowel_word_pairs[neighbor_index][1][0]),
                               max(vowel_word_pairs[shortest_syllable_index][1][1],
                                   vowel_word_pairs[neighbor_index][1][1])))

        new_vowel_word_pairs = vowel_word_pairs[:min(shortest_syllable_index, neighbor_index)] + \
                               [merged_syllable] + \
                               vowel_word_pairs[max(shortest_syllable_index, neighbor_index) + 1:]

        return new_vowel_word_pairs

    @staticmethod
    def interpolate_formants(original_formant_values, target_length):
        if len(original_formant_values) == target_length:
            return original_formant_values

        original_times = np.linspace(0, len(original_formant_values) - 1, num=len(original_formant_values))
        target_times = np.linspace(0, len(original_formant_values) - 1, num=target_length)

        interpolator = interp1d(original_times, original_formant_values, kind='linear', fill_value='extrapolate')
        interpolated_formants = interpolator(target_times)
        return interpolated_formants

    @staticmethod
    def merge_closest_intervals(intervals):
        if len(intervals) < 2:
            return intervals

        intervals.sort(key=lambda x: x[0])

        min_gap = float('inf')
        pair_to_merge = None

        for i in range(len(intervals) - 1):
            gap = intervals[i + 1][0] - intervals[i][1]
            if gap < min_gap:
                min_gap = gap
                pair_to_merge = i

        if pair_to_merge is not None:
            merged_interval = (intervals[pair_to_merge][0], intervals[pair_to_merge + 1][1])
            intervals[pair_to_merge:pair_to_merge + 2] = [merged_interval]

        return intervals
