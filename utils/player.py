from pydub import AudioSegment
from pydub.playback import play
import sounddevice as sd


def play_with_pauses_and_resume(audio_path, pauses):
    audio = AudioSegment.from_file(audio_path)
    if not pauses:
        play(audio)
        return

    start_time = 0

    for pause_time in pauses:
        play(audio[start_time:pause_time])
        play(AudioSegment.silent(duration=2000))
        start_time = pause_time
        print(f"Stop audio: {pause_time}")
    play(audio[start_time:])


def play_audio_segment(audio_segment, sr):
    sd.play(audio_segment, sr)
    sd.wait()


def play_audio(filepath):
    audio = AudioSegment.from_wav(filepath)

    samples = audio.get_array_of_samples()
    sample_rate = audio.frame_rate

    sd.play(samples, sample_rate)
    sd.wait()

