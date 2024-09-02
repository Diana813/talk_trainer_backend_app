from deepgram import DeepgramClient, PrerecordedOptions, FileSource

from data.model.input_models.transcription_data import JSONResponse
from utils import keys


class TranscriptService:
    def __init__(self):
        self.deepgram_client = DeepgramClient(keys.DEEPGRAM_API_KEY)

    def get_transcript_data_from_deepgram(self, audio_filepath):
        try:
            with open(audio_filepath, "rb") as file:
                buffer_data = file.read()

            payload: FileSource = {"buffer": buffer_data}
            options = self._get_default_options()

            response = self.deepgram_client.listen.prerecorded.v("1").transcribe_file(payload, options)
            response_dict = response.to_dict()

            return JSONResponse(**response_dict)

        except Exception as e:
            print(f"Exception: {e}")

    def get_transcript_data_from_deepgram_url(self, url):
        try:
            source = {'url': url}
            options = self._get_default_options()

            response = self.deepgram_client.listen.prerecorded.v("1").transcribe_url(source, options)
            response_json = response.to_json(indent=4)
            with open('audio_source_transcription_youtube.json', 'w') as file:
                file.write(response_json)

        except Exception as e:
            print(f"Exception: {e}")

    # @staticmethod
    # def get_transcript_dummy_data():
    #     with open(
    #             '/audio_speach_analizer_tool/utils/audio_dict.txt',
    #             'r') as file:
    #         data = file.read()
    #     data_dict = ast.literal_eval(data)
    #     return JSONResponse(**data_dict)
    #
    # @staticmethod
    # def get_user_transcript_dummy_data():
    #     with open(
    #             '/audio_speach_analizer_tool/utils/user_audio_dict.txt',
    #             'r') as file:
    #         data = file.read()
    #     data_dict = ast.literal_eval(data)
    #     return JSONResponse(**data_dict)

    @staticmethod
    def _get_default_options():
        return PrerecordedOptions(
            model="nova",
            smart_format=True,
            punctuate=True,
            diarize=True,
            detect_language=True,
        )
