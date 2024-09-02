class Word:
    def __init__(self, word, start, end, confidence, punctuated_word, speaker, speaker_confidence):
        self.word = word
        self.start = start
        self.end = end
        self.confidence = confidence
        self.punctuated_word = punctuated_word
        self.speaker = speaker
        self.speaker_confidence = speaker_confidence

    def to_dict(self):
        return {
            "word": self.word,
            "start": self.start,
            "end": self.end,
            "confidence": self.confidence,
            "punctuated_word": self.punctuated_word,
            "speaker": self.speaker,
            "speaker_confidence": self.speaker_confidence
        }


class Sentence:
    def __init__(self, text, start, end):
        self.text = text
        self.start = start
        self.end = end


class ParagraphText:
    def __init__(self, sentences, start, end, num_words, speaker):
        self.sentences = [Sentence(**sentence) for sentence in sentences]
        self.start = start
        self.end = end
        self.num_words = num_words
        self.speaker = speaker


class Paragraphs:
    def __init__(self, transcript, paragraphs):
        self.transcript = transcript
        self.paragraphs = [self.create_paragraph(paragraph) for paragraph in paragraphs]

    @staticmethod
    def create_paragraph(paragraph):
        if paragraph is None or not isinstance(paragraph, dict):
            raise ValueError("Each paragraph must be a non-None dictionary")
        return ParagraphText(**paragraph)


class Alternative:
    def __init__(self, transcript, confidence, words, paragraphs, entities=None, translations=None, topics=None, summaries=None):
        self.transcript = transcript
        self.confidence = confidence
        self.words = [Word(**word) for word in words]
        self.paragraphs = Paragraphs(**paragraphs)
        self.entities = entities
        self.translations = translations
        self.topics = topics
        self.summaries = summaries


class Channel:
    def __init__(self, alternatives, detected_language, language_confidence, search=None):
        self.search = search
        self.alternatives = [Alternative(**alternative) for alternative in alternatives]
        self.detected_language = detected_language
        self.language_confidence = language_confidence


class Utterance:
    def __init__(self, start, end, confidence, channel, transcript, words, speaker, id):
        self.start = start
        self.end = end
        self.confidence = confidence
        self.channel = channel
        self.transcript = transcript
        self.words = [Word(**word) for word in words]
        self.speaker = speaker
        self.id = id


class Results:
    def __init__(self, channels, utterances=None, summary=None):
        self.channels = [Channel(**channel) for channel in channels]
        # self.utterances = [Utterance(**utterance) for utterance in utterances]
        # self.summary = summary


class ModelInfo:
    def __init__(self, name, version, arch):
        self.name = name
        self.version = version
        self.arch = arch


class Metadata:
    def __init__(self, transaction_key=None, request_id=None, sha256=None, created=None, duration=None, channels=None, models=None, model_info=None, warnings=None,
                 summary_info=None):
        self.transaction_key = transaction_key
        self.request_id = request_id
        self.sha256 = sha256
        self.created = created
        self.duration = duration
        self.channels = channels
        self.models = models
        self.warnings = warnings
        self.model_info = {model: ModelInfo(**info) for model, info in model_info.items()}
        self.summary_info = summary_info


class JSONResponse:
    def __init__(self, metadata, results):
        self.metadata = Metadata(**metadata)
        self.results = Results(**results)
