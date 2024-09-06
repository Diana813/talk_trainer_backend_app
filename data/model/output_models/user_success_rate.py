import json


class UserSuccessRate:
    def __init__(self, words_accuracy, transcription, accent_accuracy, accent, intonation_accuracy, intonation,
                 pronunciation_accuracy):
        self.words_accuracy = words_accuracy
        self.transcription = transcription
        self.accent_accuracy = accent_accuracy
        self.accent = accent
        self.intonation_accuracy = intonation_accuracy
        self.intonation = intonation
        self.pronunciation_accuracy = pronunciation_accuracy

    def to_json(self):
        return json.dumps({
            'wordsAccuracy': self.words_accuracy,
            'transcription': self.transcription.to_json(),
            'accentAccuracy': self.accent_accuracy,
            'accent': [accent_data.to_dict() for accent_data in self.accent],
            'intonationAccuracy': self.intonation_accuracy,
            'intonation': self.intonation.to_json(),
            'pronunciationAccuracy': self.pronunciation_accuracy
        })
