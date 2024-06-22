class Transcription:
    def __init__(self, lector_transcription, user_transcription):
        self.lector_transcription = lector_transcription
        self.user_transcription = user_transcription

    def to_json(self):
        return {
            'lectorTranscription': self.lector_transcription,
            'userTranscription': self.user_transcription
        }
