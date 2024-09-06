import sounddevice as sd
import numpy as np

import wavio


def record_audio(sample_rate=44100, channels=1):
    print("Nagrywanie... Naciśnij Enter, aby zakończyć.")

    audio_data = []

    def callback(indata, frames, time, status):
        audio_data.append(indata.copy())

    stream = sd.InputStream(samplerate=sample_rate, channels=channels, callback=callback)
    stream.start()

    input()

    stream.stop()
    stream.close()

    audio_data = np.concatenate(audio_data, axis=0)

    return audio_data, sample_rate


def save_audio(audio_data, sample_rate, output_file='../test/accent_audio_test_data/test33c.wav'):
    wavio.write(output_file, audio_data, sample_rate, sampwidth=2)
    print(f"Zapisano plik audio jako {output_file}")


def main():
    audio_data, sample_rate = record_audio()
    save_audio(audio_data, sample_rate)


if __name__ == "__main__":
    main()