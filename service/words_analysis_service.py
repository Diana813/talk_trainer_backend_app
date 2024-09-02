from data.remote_data_source.transcription_remote_data_source import TranscriptService
from utils.file_data_manager import FileDataManager


class WordsAnalysisService:
    def __init__(self):
        self.transcript_service = TranscriptService()
        self.file_manager = FileDataManager()

    @staticmethod
    def calculate_word_sequence_accuracy(user_words, lector_words):
        matched_words = 0
        lector_word_list = [word.word for word in lector_words]
        user_word_list = [word.word for word in user_words]

        for user_word in user_word_list:
            if user_word in lector_word_list:
                matched_words += 1

        total_words = len(lector_word_list)
        success_rate = min((matched_words / total_words) if total_words > 0 and matched_words > 0 else 0.1, 1)
        return success_rate, ' '.join(lector_word_list), ' '.join(user_word_list)

    def get_lector_words_for_time_range(self, start, end, lector_words_filepath):
        words = self.file_manager.load_words_from_file(lector_words_filepath)

        result = []
        for word in words:
            if start <= word.start and word.end <= end:
                result.append(word)
        return result
