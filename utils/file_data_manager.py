import json

from pydub import AudioSegment

from data.model.output_models.time_range import TimeRange
from data.model.input_models.transcription_data import Word


class FileDataManager:
    @staticmethod
    def load_words_from_file(filepath):
        with open(filepath, 'r') as file:
            words_data = json.load(file)
        return [Word(**word_data) for word_data in words_data]

    @staticmethod
    def load_time_range_from_file(filepath):
        with open(filepath, 'r') as file:
            time_range_data = json.load(file)
        return TimeRange(**time_range_data)

    @staticmethod
    def save_words_to_file(words, filepath):
        words_dicts = [word.to_dict() for word in words if hasattr(word, 'to_dict')]
        with open(filepath, 'w') as file:
            json.dump(words_dicts, file, indent=4)

    @staticmethod
    def save_time_range_to_file(time_range, filepath):
        with open(filepath, 'w') as file:
            json.dump(time_range, file, indent=4)

    @staticmethod
    def save_audio_to_wav(uint8list_data, output_path):
        try:
            audio_segment = AudioSegment(
                uint8list_data,
                frame_rate=44100,
                sample_width=2,
                channels=2
            )

            audio_segment.export(output_path, format='wav')
            print(f"Audio saved successfully to {output_path}")

        except Exception as e:
            print(f"Error saving audio to wav: {e}")
