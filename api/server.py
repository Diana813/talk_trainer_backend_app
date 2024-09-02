import json
import os

import librosa
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS

from data.model.output_models.intonation_data import Intonation
from data.model.output_models.transcription_response import Transcription
from data.model.output_models.user_success_rate import UserSuccessRate
from service.accent_analysis_service import AccentAnalysisService
from service.audio_service import AudioService
from service.intonation_analysis_service import IntonationAnalysisService
from service.pause_analysis_service import PauseAnalysisService
from service.pronunciation_analysis_service import PronunciationAnalysisService
from service.thread_helper import ThreadHelper
from data.remote_data_source.transcription_remote_data_source import TranscriptService
from service.words_analysis_service import WordsAnalysisService
from service.youtube_downloader import YouTubeDownloader
from utils.file_data_manager import FileDataManager


class FlaskAppWrapper:
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app)

        self.transcript_service = TranscriptService()
        self.words_analysis_service = WordsAnalysisService()
        self.intonation_analysis_service = IntonationAnalysisService()
        self.accent_analysis_service = AccentAnalysisService()
        self.pronunciation_analysis_service = PronunciationAnalysisService()
        self.pause_analysis_service = PauseAnalysisService()
        self.youtube_downloader = YouTubeDownloader()
        self.file_manager = FileDataManager()
        self.audio_service = AudioService()

        self.user_audio_file_path = os.path.join('./user_files', 'user_audio.wav')
        self.user_words_file_path = os.path.join('./user_files', 'user_transcription.json')
        self.current_time_range_file_path = os.path.join('./user_files', 'current_time_range.json')
        os.makedirs('./user_files', exist_ok=True)

        self.lector_audio_file_path = os.path.join('./lector_files', 'lector_audio.mp3')
        self.lector_audio_file_path_wav = os.path.join('./lector_files', 'lector_audio.wav')
        self.lector_words_file_path = os.path.join('./lector_files', 'lector_words.json')
        self.video_file_path = os.path.join('./lector_files', 'lector_video.mp4')
        os.makedirs('./lector_files', exist_ok=True)

        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/api/video')
        def upload_video():
            youtube_url = request.args.get('youtube_url')
            print("upload video url:")
            print(youtube_url)
            self.youtube_downloader.download_youtube_video(youtube_url)

            content_length = os.path.getsize(self.video_file_path)
            content_length_str = str(content_length)

            response = send_file(self.video_file_path, mimetype='video/mp4')
            response.headers['Content-Length'] = content_length_str
            return response

        @self.app.route('/api/pauses_timestamps', methods=['GET'])
        def get_timestamps():
            youtube_url = request.args.get('youtube_url')
            print("upload audio url:")
            print(youtube_url)
            self.youtube_downloader.download_youtube_audio(youtube_url)
            self.audio_service.convert_mp3_to_wav(self.lector_audio_file_path)

            lector_transcription = self.transcript_service.get_transcript_data_from_deepgram(
                self.lector_audio_file_path)

            lector_words = lector_transcription.results.channels[0].alternatives[0].words

            pause_times_in_millis = self.pause_analysis_service.get_pauses(lector_words)

            self.file_manager.save_words_to_file(lector_words, self.lector_words_file_path)

            return jsonify(pause_times_in_millis)

        @self.app.route('/api/upload_audio', methods=['POST'])
        def upload_audio():

            if 'audio' in request.files:
                audio = request.files['audio'].read()

                self.file_manager.save_audio_to_wav(audio, self.user_audio_file_path)

            if 'timeRange' in request.form:
                time_range_json = request.form['timeRange']
                time_range = json.loads(time_range_json)
                self.file_manager.save_time_range_to_file(time_range, self.current_time_range_file_path)

            user_transcript = self.transcript_service.get_transcript_data_from_deepgram(
                self.user_audio_file_path)
            if not user_transcript:
                return jsonify({"message": "Transkrypt nie został pobrany"}), 500

            user_words = user_transcript.results.channels[0].alternatives[0].words
            self.file_manager.save_words_to_file(user_words, self.user_words_file_path)

            return jsonify({"message": "Plik audio został zapisany poprawnie"}), 200

        @self.app.route('/api/get_user_audio', methods=['GET'])
        def get_user_audio():
            response = send_file(self.user_audio_file_path, mimetype='audio/wav')
            return response

        @self.app.route('/api/get_user_success_rate', methods=['GET'])
        def get_user_success_rate():

            time_range = self.file_manager.load_time_range_from_file(self.current_time_range_file_path)

            lector_words = self.words_analysis_service.get_lector_words_for_time_range(time_range.start, time_range.end,
                                                                                       self.lector_words_file_path)

            user_words = self.file_manager.load_words_from_file(self.user_words_file_path)

            lector_audio, lsr = self.audio_service.load_audio_segment(self.lector_audio_file_path_wav, time_range.start,
                                                                      time_range.end)
            user_audio, usr = librosa.load(self.user_audio_file_path, sr=None)

            helper = ThreadHelper()

            def get_accent_data():
                accent_differences = self.accent_analysis_service.compare_accents(lector_audio, lsr, time_range,
                                                                                  user_audio, usr, lector_words,
                                                                                  user_words)
                accent_accuracy = self.accent_analysis_service.calculate_accent_accuracy(len(user_words),
                                                                                         len(accent_differences))

                print("got accent data")
                return accent_differences, accent_accuracy

            def get_intonation_data():
                lector_intonation, user_intonation, intonation_accuracy = self.intonation_analysis_service.get_intonation_success_rate(
                    lector_audio, user_audio)
                print("got intonation data")
                return lector_intonation, user_intonation, intonation_accuracy

            def get_transcription_data():
                words_accuracy, lector_transcription, user_transcription = self.words_analysis_service.calculate_word_sequence_accuracy(
                    user_words, lector_words)
                print("got transcription data")
                return words_accuracy, Transcription(lector_transcription=lector_transcription,
                                                     user_transcription=user_transcription)

            def get_pronunciation_data():
                _, pronunciation_accuracy = self.pronunciation_analysis_service.compare_vowels_pronunciation(
                    self.user_audio_file_path, self.lector_audio_file_path_wav, time_range, user_words, lector_words)
                return pronunciation_accuracy

            helper.run_in_threads(get_accent_data, [], 'accent_data')
            helper.run_in_threads(get_intonation_data, [], 'intonation_data')
            helper.run_in_threads(get_transcription_data, [], 'transcription_data')
            #helper.run_in_threads(get_pronunciation_data, [], 'pronunciation_data')

            helper.wait_for_completion()
            print("threads completed")

            accent_differences, accent_accuracy = helper.results['accent_data']
            lector_intonation, user_intonation, intonation_accuracy = helper.results['intonation_data']
            words_accuracy, transcription_data = helper.results['transcription_data']
            #pronunciation_accuracy = helper.results['pronunciation_data']

            helper.threads.clear()

            user_success_rate = UserSuccessRate(words_accuracy, transcription_data, accent_accuracy,
                                                accent_differences, intonation_accuracy,
                                                Intonation(lector_intonation=lector_intonation,
                                                           user_intonation=user_intonation), 0.6)

            return user_success_rate.to_json(), 200, {'Content-Type': 'application/json'}

    def run(self, debug=True):
        self.app.run(host='0.0.0.0', port=5000, debug=debug)


if __name__ == '__main__':
    flask_app = FlaskAppWrapper()
    flask_app.run()
