class AccentData:
    def __init__(self, word, sampled_audio_lector, sampled_audio_user):
        self.word = word
        self.sampled_audio_lector = sampled_audio_lector
        self.sampled_audio_user = sampled_audio_user

    def to_dict(self):
        return self.__dict__
