class Intonation:
    def __init__(self, lector_intonation, user_intonation):
        self.lector_intonation = lector_intonation
        self.user_intonation = user_intonation

    def to_json(self):
        return {
            'lectorIntonation': self.lector_intonation if self.lector_intonation is not None else None,
            'userIntonation': self.user_intonation if self.user_intonation is not None else None
        }

