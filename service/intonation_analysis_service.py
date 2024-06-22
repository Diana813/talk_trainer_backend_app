from concurrent.futures import ThreadPoolExecutor

import librosa
import numpy as np
from scipy.interpolate import interp1d
from scipy.stats import pearsonr

from service.audio_service import AudioService


class IntonationAnalysisService:

    def __init__(self):
        self.audio_service = AudioService()

    def get_intonation_success_rate(self, lector_signal, user_signal):
        with ThreadPoolExecutor() as executor:
            future_pitch1 = executor.submit(self.get_pitch_array, lector_signal)
            future_pitch2 = executor.submit(self.get_pitch_array, user_signal)

            pitch1 = future_pitch1.result()
            pitch2 = future_pitch2.result()

            future_filtered_pitch1 = executor.submit(self.filter, pitch1)
            future_filtered_pitch2 = executor.submit(self.filter, pitch2)

            filtered_pitch1 = future_filtered_pitch1.result()
            filtered_pitch2 = future_filtered_pitch2.result()

            future_interpolated = executor.submit(self.interpolate, filtered_pitch1, filtered_pitch2)
            pitch_interpolated1, pitch_interpolated2 = future_interpolated.result()

            sampling_rate = 10
            future_processed1 = executor.submit(self.calculate_amplitude_rate, pitch_interpolated1, sampling_rate)
            future_processed2 = executor.submit(self.calculate_amplitude_rate, pitch_interpolated2, sampling_rate)

            processed1 = future_processed1.result().tolist()
            processed2 = future_processed2.result().tolist()

        executor.shutdown()

        correlation = self.calculate_correlation_between_pitches(processed1, processed2)
        similarity = (correlation + 1) / 2
        return processed1, processed2, similarity

    def interpolate(self, pitch_changes1, pitch_changes2):
        min_length = min(len(pitch_changes1), len(pitch_changes2))
        pitch_changes1 = self.interpolate_sequence(pitch_changes1, min_length)
        pitch_changes2 = self.interpolate_sequence(pitch_changes2, min_length)
        return pitch_changes1, pitch_changes2

    @staticmethod
    def filter(pitch):
        mean_pitch = np.mean(pitch)
        std_dev = np.std(pitch)
        threshold = 2 * std_dev
        return pitch[(pitch >= mean_pitch - threshold) & (pitch <= mean_pitch + threshold)]

    @staticmethod
    def get_pitch_array(audio):
        f0, _, _ = librosa.pyin(audio, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'))
        return f0[~np.isnan(f0)]

    @staticmethod
    def interpolate_sequence(sequence, target_length):
        if len(sequence) == target_length:
            return sequence
        x = np.linspace(0, len(sequence) - 1, num=len(sequence))
        f = interp1d(x, sequence, kind='linear')
        new_x = np.linspace(0, len(sequence) - 1, num=target_length)
        return f(new_x)

    @staticmethod
    def calculate_correlation_between_pitches(pitch_changes1, pitch_changes2):
        return pearsonr(pitch_changes1, pitch_changes2)[0]

    @staticmethod
    def calculate_amplitude_rate(data, sampling_rate):
        total_f0 = np.sum(data)
        if total_f0 == 0:
            return np.zeros(len(data) // sampling_rate)
        segment_sums = np.add.reduceat(data, np.arange(0, len(data), sampling_rate))
        percent_f0 = segment_sums / total_f0
        return percent_f0

# class IntonationAnalysisService:
#
#     def __init__(self):
#         self.audio_service = AudioService()
#
#     def get_intonation_success_rate(self, lector_signal, user_signal):
#         pitch1 = self.get_pitch_array(lector_signal)
#         pitch2 = self.get_pitch_array(user_signal)
#
#         filtered_pitch1 = self.filter(pitch1)
#         filtered_pitch2 = self.filter(pitch2)
#
#         pitch_interpolated1, pitch_interpolated2 = self.interpolate(filtered_pitch1, filtered_pitch2)
#
#         sampling_rate = 10
#         processed1 = self.calculate_amplitude_rate(pitch_interpolated1, sampling_rate).tolist()
#         processed2 = self.calculate_amplitude_rate(pitch_interpolated2, sampling_rate).tolist()
#
#         correlation = self.calculate_correlation_between_pitches(processed1, processed2)
#         similarity = (correlation + 1) / 2
#         return processed1, processed2, similarity
#
#     def interpolate(self, pitch_changes1, pitch_changes2):
#         min_length = min(len(pitch_changes1), len(pitch_changes2))
#         pitch_changes1 = self.interpolate_sequence(pitch_changes1, min_length)
#         pitch_changes2 = self.interpolate_sequence(pitch_changes2, min_length)
#         return pitch_changes1, pitch_changes2
#
#     @staticmethod
#     def filter(pitch):
#         mean_pitch = np.mean(pitch)
#         std_dev = np.std(pitch)
#         threshold = 2 * std_dev
#         return pitch[(pitch >= mean_pitch - threshold) & (pitch <= mean_pitch + threshold)]
#
#     @staticmethod
#     def get_pitch_array(audio):
#         f0, _, _ = librosa.pyin(audio, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'))
#         return f0[~np.isnan(f0)]
#
#     @staticmethod
#     def interpolate_sequence(sequence, target_length):
#         if len(sequence) == target_length:
#             return sequence
#         x = np.linspace(0, len(sequence) - 1, num=len(sequence))
#         f = interp1d(x, sequence, kind='linear')
#         new_x = np.linspace(0, len(sequence) - 1, num=target_length)
#         return f(new_x)
#
#     @staticmethod
#     def calculate_correlation_between_pitches(pitch_changes1, pitch_changes2):
#         return pearsonr(pitch_changes1, pitch_changes2)[0]
#
#     @staticmethod
#     def calculate_amplitude_rate(data, sampling_rate):
#         total_f0 = np.sum(data)
#         if total_f0 == 0:
#             return np.zeros(len(data) // sampling_rate)
#         segment_sums = np.add.reduceat(data, np.arange(0, len(data), sampling_rate))
#         percent_f0 = segment_sums / total_f0
#         return percent_f0

# class IntonationAnalysisService:
#
#     def __init__(self):
#         self.audio_service = AudioService()
#
#     def get_intonation_success_rate(self, lector_signal, user_signal):
#         pitch1 = self.get_pitch_array(lector_signal)
#         pitch2 = self.get_pitch_array(user_signal)
#
#         filtered_pitch1 = self.filter(pitch1)
#         filtered_pitch2 = self.filter(pitch2)
#
#         pitch_interpolated1, pitch_interpolated2 = self.interpolate(filtered_pitch1, filtered_pitch2)
#
#         sampling_rate = 10
#         processed1 = self.calculate_amplitude_rate(pitch_interpolated1, sampling_rate)
#         processed2 = self.calculate_amplitude_rate(pitch_interpolated2, sampling_rate)
#
#         correlation = self.calculate_correlation_between_pitches(processed1, processed2)
#         similarity = (correlation + 1) / 2
#         return processed1, processed2, similarity
#
#     def interpolate(self, pitch_changes1, pitch_changes2):
#         min_length = min(len(pitch_changes1), len(pitch_changes2))
#         pitch_changes1 = self.interpolate_sequence(pitch_changes1, min_length)
#         pitch_changes2 = self.interpolate_sequence(pitch_changes2, min_length)
#         return pitch_changes1, pitch_changes2
#
#     @staticmethod
#     def filter(pitch):
#         mean_pitch = np.mean(pitch)
#         std_dev = np.std(pitch)
#
#         threshold = 2 * std_dev
#
#         return pitch[
#             (pitch >= mean_pitch - threshold) & (pitch <= mean_pitch + threshold)]
#
#     @staticmethod
#     def get_pitch_array(audio):
#         f0, _, _ = librosa.pyin(audio, fmin=librosa.note_to_hz('C2'),
#                                 fmax=librosa.note_to_hz('C7'))
#
#         return f0[~np.isnan(f0)]
#
#     @staticmethod
#     def interpolate_sequence(sequence, target_length):
#         original_length = len(sequence)
#         x = np.arange(original_length)
#         f = interp1d(x, sequence, kind='linear')
#         new_x = np.linspace(0, original_length - 1, target_length)
#         interpolated_sequence = f(new_x)
#
#         return interpolated_sequence
#
#     @staticmethod
#     def calculate_correlation_between_pitches(pitch_changes1, pitch_changes2):
#         correlation, _ = pearsonr(pitch_changes1, pitch_changes2)
#         return correlation
#
#     @staticmethod
#     def calculate_shift(chart1, chart2):
#         peaks1, _ = find_peaks(chart1)
#         peaks2, _ = find_peaks(chart2)
#
#         if len(peaks1) == 0 or len(peaks2) == 0:
#             return 0
#
#         shift = peaks1[0] - peaks2[0]
#         return shift
#
#     @staticmethod
#     def calculate_amplitude_rate(data, sampling_rate):
#         total_f0 = np.sum(data)
#         segments = [data[i:i + sampling_rate] for i in range(0, len(data), sampling_rate)]
#
#         percent_f0 = [np.sum(segment) / total_f0 for segment in segments]
#         return percent_f0
