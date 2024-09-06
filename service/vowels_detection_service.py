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

    @staticmethod
    def calculate_autocorrelation(y, frame_length, hop_length):
        autocorrelation = []
        for i in range(0, len(y) - frame_length, hop_length):
            frame = y[i:i + frame_length]
            correlation = np.correlate(frame, frame, mode='full')
            autocorrelation.append(correlation[len(correlation) // 2])
        return np.array(autocorrelation)

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
