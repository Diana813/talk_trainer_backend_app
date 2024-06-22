import librosa
import numpy as np
from pydub import AudioSegment


class AudioService:
    @staticmethod
    def convert_mp3_to_wav(path):
        audio = AudioSegment.from_file(path)
        wav_file = path.replace("mp3", "wav")
        audio.export(wav_file, format="wav")
        return wav_file

    @staticmethod
    def change_speed(audio_file, speed=1.0):
        sound = AudioSegment.from_file(audio_file)

        new_frame_rate = int(sound.frame_rate * speed)
        sound_with_changed_speed = sound._spawn(sound.raw_data, overrides={
            "frame_rate": new_frame_rate
        })
        sound_with_changed_speed.set_frame_rate(sound.frame_rate)

        return sound_with_changed_speed

    @staticmethod
    def sample_audio_segment_to_draw_chart(audio_segment, num_samples=500):
        length = len(audio_segment)

        sampled_indices = np.linspace(0, length - 1, num_samples, dtype=int)
        sampled_audio = audio_segment[sampled_indices]

        return sampled_audio.tolist()

    @staticmethod
    def load_audio_segment(filepath, start_in_seconds, end_in_seconds):
        audio, sr = librosa.load(filepath, sr=None)

        start_time = start_in_seconds
        end_time = end_in_seconds

        start_sample = int(start_time * sr)
        end_sample = int(end_time * sr)

        return audio[start_sample:end_sample], sr

    @staticmethod
    def extract_segment(audio, start_time, end_time, sr):
        start_sample = int(start_time * sr)
        end_sample = int(end_time * sr)
        return audio[start_sample:end_sample]
