from concurrent.futures import ThreadPoolExecutor

import librosa
import numpy as np
from parselmouth import Sound
from scipy.interpolate import interp1d
from scipy.stats import pearsonr

from service.audio_service import AudioService
from service.thread_helper import ThreadHelper


class IntonationAnalysisService:

    def __init__(self):
        self.audio_service = AudioService()
        self.thread_helper = ThreadHelper()

    def get_intonation_success_rate(self, lector_signal, user_signal):
        self.thread_helper.run_in_threads(self.get_pitch_array, (lector_signal,), 'pitch1')
        self.thread_helper.run_in_threads(self.get_pitch_array, (user_signal,), 'pitch2')

        self.thread_helper.wait_for_completion()

        pitch1 = self.thread_helper.results['pitch1']
        pitch2 = self.thread_helper.results['pitch2']

        # self.thread_helper.run_in_threads(self.filter, (pitch1,), 'filtered_pitch1')
        # self.thread_helper.run_in_threads(self.filter, (pitch2,), 'filtered_pitch2')

        # self.thread_helper.wait_for_completion()

        # filtered_pitch1 = self.thread_helper.results['filtered_pitch1']
        # filtered_pitch2 = self.thread_helper.results['filtered_pitch2']

        self.thread_helper.threads.clear()
        # pitch1 = self.get_pitch_array(lector_signal)
        # pitch2 = self.get_pitch_array(user_signal)
        # print("get pitch")
        #
        # filtered_pitch1 = self.filter(pitch1)
        # filtered_pitch2 = self.filter(pitch2)
        # print("filtered pitch")

        pitch_interpolated1, pitch_interpolated2 = self.interpolate(pitch1, pitch2)

        sampling_rate = 10
        processed1 = self.calculate_amplitude_rate(pitch_interpolated1, sampling_rate)
        processed2 = self.calculate_amplitude_rate(pitch_interpolated2, sampling_rate)

        correlation = self.calculate_correlation_between_pitches(processed1, processed2)
        similarity = (correlation + 1) / 2
        return processed1.tolist(), processed2.tolist(), similarity

    def interpolate(self, pitch_changes1, pitch_changes2):
        min_length = min(len(pitch_changes1), len(pitch_changes2))

        if len(pitch_changes1) > min_length:
            pitch_changes1 = self.interpolate_sequence(pitch_changes1, min_length)
        if len(pitch_changes2) > min_length:
            pitch_changes2 = self.interpolate_sequence(pitch_changes2, min_length)

        return pitch_changes1, pitch_changes2

    @staticmethod
    def filter(pitch):
        mean_pitch = np.mean(pitch)
        std_dev = np.std(pitch)
        threshold = 2 * std_dev
        return pitch[(pitch >= mean_pitch - threshold) & (pitch <= mean_pitch + threshold)]

    #
    # def get_pitch_array(audio):
    #     fmin = librosa.note_to_hz('C2')
    #     fmax = librosa.note_to_hz('C7')
    #     f0, _, _ = librosa.pyin(audio, fmin=fmin, fmax=fmax)
    #     f0_valid = f0[~np.isnan(f0)]
    #     return f0_valid

    @staticmethod
    def get_pitch_array(audio):
        sound = Sound(audio)
        pitch = sound.to_pitch_ac(time_step=0.01)
        pitch_values = pitch.selected_array['frequency']
        pitch_values = pitch_values[pitch_values > 0]
        return pitch_values

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
