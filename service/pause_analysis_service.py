import numpy as np


class PauseAnalysisService:

    def get_pauses(self, lector_words):
        silence_segments = self.get_silence_segments_between_utterances(lector_words)
        segments_with_filtered_out_anomalies = self.filter_out_duration_anomalies(
            silence_segments)
        pause_times = self.get_silence_middle_times(segments_with_filtered_out_anomalies)

        return self.convert_pause_times_to_millis(pause_times)

    @staticmethod
    def get_silence_segments_between_utterances(lector_words):
        silence_segments = []
        for i in range(1, len(lector_words)):
            start_of_pause = lector_words[i - 1].end
            end_of_pause = lector_words[i].start
            pause_duration = end_of_pause - start_of_pause
            if pause_duration > 0.20:
                silence_segments.append({"start": start_of_pause, "end": end_of_pause, "duration": pause_duration})
        return silence_segments

    @staticmethod
    def filter_out_duration_anomalies(silence_segments):
        durations = [pause['duration'] for pause in silence_segments]
        threshold_duration = np.percentile(durations, 0)

        filtered_pauses = [pause for pause in silence_segments if pause['duration'] >= threshold_duration]
        return filtered_pauses

    @staticmethod
    def get_silence_segments_longer_than_average(average_duration, pauses_segments):
        pauses_between_phrases = []
        for segment in pauses_segments:
            if segment['duration'] >= average_duration:
                pauses_between_phrases.append(segment)

        return pauses_between_phrases

    @staticmethod
    def get_silence_middle_times(pauses_range_list):
        middle_times = []

        for pause in pauses_range_list:
            pause_start = pause['start']
            duration = pause['duration']
            middle_time = pause_start + (duration / 2)
            middle_times.append(middle_time)

        return middle_times

    @staticmethod
    def convert_pause_times_to_millis(pauses):
        pause_in_millis = []
        for pause_time in pauses:
            pause_in_millis.append(round(pause_time * 1000, 0))
        return pause_in_millis
