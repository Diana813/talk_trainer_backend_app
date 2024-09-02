import librosa
import numpy as np
import parselmouth
from librosa import feature
import soundfile as sf


class VowelsDetectionService:

    def find_vowels(self, audio_signal, sample_rate, frame_length=0.001):
        hop_length = int(frame_length * sample_rate)

        high_rms_time_ranges = self.find_high_rms(audio_signal, sample_rate)
        low_zcr_time_ranges = self.find_low_zcr(audio_signal, sample_rate)
        high_autocorrelation_time_ranges = self.find_high_autocorrelation(audio_signal, sample_rate)

        vowels_segments = []

        for i in range(0, len(audio_signal), hop_length):
            frame_start_time = i / sample_rate
            frame_end_time = (i + hop_length) / sample_rate

            conditions_met = sum([
                any(start <= frame_start_time < end for start, end in high_rms_time_ranges),
                any(start <= frame_start_time < end for start, end in low_zcr_time_ranges),
                any(start <= frame_start_time < end for start, end in high_autocorrelation_time_ranges),
            ])

            probability = min(100, 35 * conditions_met)

            if probability > 90:
                vowels_segments.append((frame_start_time, frame_end_time))

        vowel_time_ranges = self.vowels_to_time_ranges(vowels_segments)

        return vowel_time_ranges

    def find_high_rms(self, audio_signal, sample_rate):
        frame_length = int(0.01 * sample_rate)
        hop_length = frame_length

        rms = feature.rms(y=audio_signal, frame_length=frame_length, hop_length=hop_length)[0]
        rms_threshold = np.mean(rms)

        rms_indices = []

        for i in range(0, len(audio_signal) - frame_length, hop_length):

            if rms[i // hop_length] > rms_threshold:
                rms_indices.append(i)

        rms_time_ranges = self.indices_to_time_ranges(rms_indices, sample_rate, frame_length)
        long_time_ranges = self.filter_time_ranges(rms_time_ranges, frame_length, sample_rate)
        return long_time_ranges

    def find_low_zcr(self, audio_signal, sample_rate):
        frame_length = int(0.01 * sample_rate)
        hop_length = frame_length

        zcr = librosa.feature.zero_crossing_rate(y=audio_signal, frame_length=frame_length, hop_length=hop_length)[0]
        zcr_threshold = np.mean(zcr)

        indices = []

        for i in range(0, len(audio_signal) - frame_length, hop_length):

            if zcr[i // hop_length] < zcr_threshold:
                indices.append(i)

        low_zcr_time_ranges = self.indices_to_time_ranges(indices, sample_rate, frame_length)
        long_time_ranges = self.filter_time_ranges(low_zcr_time_ranges, frame_length, sample_rate)
        return long_time_ranges

    def find_high_autocorrelation(self, audio_signal, sample_rate):
        frame_length = int(0.01 * sample_rate)
        hop_length = frame_length

        autocorrelation = self.calculate_autocorrelation(audio_signal, frame_length, hop_length)
        autocorrelation_threshold = np.mean(autocorrelation)

        indices = []

        for i in range(0, len(audio_signal) - frame_length, hop_length):
            if autocorrelation[i // hop_length] > autocorrelation_threshold:
                indices.append(i)

        low_autocorrelation_time_ranges = self.indices_to_time_ranges(indices, sample_rate, frame_length)
        long_time_ranges = self.filter_time_ranges(low_autocorrelation_time_ranges, frame_length, sample_rate)

        return long_time_ranges

    def calculate_autocorrelation(self, y, frame_length, hop_length):
        autocorrelation = []
        for i in range(0, len(y) - frame_length, hop_length):
            frame = y[i:i + frame_length]
            correlation = np.correlate(frame, frame, mode='full')
            autocorrelation.append(correlation[len(correlation) // 2])
        return np.array(autocorrelation)

    def find_stable_formants(self, audio_signal, sample_rate):
        temp_file = "temp_audio.wav"
        sf.write(temp_file, audio_signal, sample_rate)
        sound = parselmouth.Sound(temp_file)

        time_step = 0.01
        formant = sound.to_formant_burg(time_step)

        end_time = sound.get_total_duration()
        times = np.arange(0, end_time, time_step)
        formant_values = []

        for time in times:
            f1 = formant.get_value_at_time(1, time)
            f2 = formant.get_value_at_time(2, time)
            formant_values.append((time, f1, f2))

        stable_vowel_segments = self.analyze_stability(formant_values)
        return stable_vowel_segments

    def analyze_stability(self, formant_values, segment_length=0.05):
        threshold = self.calculate_formants_threshold(formant_values)
        stable_vowel_segments = []

        segment_start = 0
        while segment_start < formant_values[-1][0]:
            segment_end = segment_start + segment_length
            segment_formants = [vals for vals in formant_values if segment_start <= vals[0] < segment_end]

            f1_values = [f1 for _, f1, _ in segment_formants if f1 is not None]
            f2_values = [f2 for _, _, f2 in segment_formants if f2 is not None]

            if f1_values and f2_values:
                f1_mean, f1_std = np.mean(f1_values), np.std(f1_values)
                f2_mean, f2_std = np.mean(f2_values), np.std(f2_values)

                if f1_std < threshold[0] and f2_std < threshold[1]:
                    stable_vowel_segments.append((segment_start, segment_end, f1_mean, f2_mean))

            segment_start = segment_end

        return stable_vowel_segments

    @staticmethod
    def calculate_formants_threshold(formant_values):
        all_f1_values = [f1 for _, f1, _ in formant_values if f1 is not None]
        all_f2_values = [f2 for _, _, f2 in formant_values if f2 is not None]

        if not all_f1_values or not all_f2_values:
            return None, None

        mean_f1_std = np.std(all_f1_values)
        mean_f2_std = np.std(all_f2_values)

        return mean_f1_std, mean_f2_std

    @staticmethod
    def find_syllables(start_time, end_time, vowels):
        syllables = []

        if not vowels:
            return [(start_time, end_time)]

        for i in range(len(vowels)):
            if i == 0:
                if start_time < vowels[0][0]:
                    syllable_start = start_time
                else:
                    syllable_start = vowels[0][0]
            else:
                syllable_start = vowels[i - 1][1]

            syllable_end = vowels[i][1]
            syllables.append((syllable_start, syllable_end))

        if vowels[-1][1] < end_time:
            syllables.append((vowels[-1][1], end_time))

        return syllables

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

    @staticmethod
    def indices_to_time_ranges(indices, sample_rate, frame_length):
        if not indices:
            return []

        time_ranges = []
        start_index = indices[0]
        end_index = start_index + frame_length

        for i in range(1, len(indices)):
            if indices[i] > end_index:
                time_ranges.append((start_index / sample_rate, end_index / sample_rate))
                start_index = indices[i]
            end_index = indices[i] + frame_length

        time_ranges.append((start_index / sample_rate, end_index / sample_rate))

        return time_ranges

    @staticmethod
    def vowels_to_time_ranges(indices):
        if not indices:
            return []

        time_ranges = []
        current_start, current_end = indices[0]

        for start, end in indices[1:]:
            if start <= current_end:
                current_end = max(current_end, end)
            else:
                time_ranges.append((current_start, current_end))
                current_start, current_end = start, end

        time_ranges.append((current_start, current_end))

        return time_ranges

    @staticmethod
    def filter_time_ranges(time_ranges, frame_length, sample_rate):
        min_duration = 3 * frame_length / sample_rate

        filtered_ranges = [time_range for time_range in time_ranges if (time_range[1] - time_range[0]) >= min_duration]

        return filtered_ranges
