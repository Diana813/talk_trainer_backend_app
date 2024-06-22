import threading

import numpy as np
import sounddevice as sd
import wavio

fs = 44100


def record_audio(start_signal, stop_signal, output_path, fs):
    print("Oczekiwanie na sygnał startu...")
    start_signal.wait()

    print("Nagrywanie...")
    audio_data = []
    with sd.InputStream(samplerate=fs, channels=1, callback=lambda indata, frames, time, status: audio_data.append(indata.copy())):
        print("Oczekiwanie na sygnał stopu...")
        stop_signal.wait()

    print(f"Zapisywanie do pliku {output_path}...")
    audio_data_array = np.concatenate(audio_data, axis=0)
    wavio.write(output_path, audio_data_array, fs, sampwidth=2)

    print(f"Nagranie zapisane jako '{output_path}'.")

if __name__ == "__main__":

    start_signal = threading.Event()
    stop_signal = threading.Event()

    output_path = input("Podaj ścieżkę do pliku WAV, do którego chcesz zapisać nagranie: ")

    recording_thread = threading.Thread(target=record_audio, args=(start_signal, stop_signal, output_path, fs))
    recording_thread.start()

    input("Naciśnij Enter, aby rozpocząć nagrywanie...")
    start_signal.set()

    input("Naciśnij Enter, aby zakończyć nagrywanie...")
    stop_signal.set()

    recording_thread.join()
