import numpy as np
import plotly.graph_objects as go
from matplotlib import pyplot as plt


def plot_signal_with_highlighted_timeranges(audio_signal, sr, time_ranges, title):
    duration = len(audio_signal) / sr
    times = np.linspace(0, duration, len(audio_signal))

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=times, y=audio_signal, mode='lines', name='Audio'))

    for start, end in time_ranges:
        fig.add_vrect(x0=start, x1=end, fillcolor="red", opacity=0.3, line_width=0)

    fig.update_layout(
        title=title,
        xaxis_title='Czas [s]',
        yaxis_title='Amplituda',
        xaxis_rangeslider_visible=True
    )

    fig.show()


def plot_probability_chart(vowel_probabilities, audio_signal, sr):
    timestamps, vowel_probs = zip(*vowel_probabilities)

    high_prob_timestamps = [t for t, p in zip(timestamps, vowel_probs) if p > 0.9]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=[i / sr for i in range(len(audio_signal))],
        y=audio_signal,
        mode='lines',
        name='Audio Signal'))

    fig.add_trace(go.Scatter(
        x=high_prob_timestamps,
        y=[audio_signal[int(t * sr)] for t in high_prob_timestamps],  # Corrected this line
        mode='markers',
        marker=dict(color='red', size=5),
        name='High Vowel Probability (>90%)'))

    fig.update_layout(
        title='Audio Signal and Vowel Probabilities',
        xaxis_title='Time (seconds)',
        yaxis_title='Amplitude/Probability',
        xaxis_rangeslider_visible=True)

    fig.show()


def plot_signal_with_highlighted_timestamps(signal, sr, timestamps, title):
    times = np.linspace(0, len(signal) / sr, len(signal))

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=times, y=signal, mode='lines', name='Audio Waveform'))

    for time in timestamps:
        fig.add_vline(x=time, line_width=2, line_dash="dash", line_color="red")

    fig.update_layout(
        title=title,
        xaxis_title='Czas [s]',
        yaxis_title='Amplituda',
        xaxis_rangeslider_visible=True
    )

    fig.show()


def plot_signal_with_highlighted_timeranges_and_timestamps(audio_signal, sr, time_ranges, timestamps, title):
    duration = len(audio_signal) / sr
    times = np.linspace(0, duration, len(audio_signal))

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=times, y=audio_signal, mode='lines', name='Audio'))

    for start, end in time_ranges:
        fig.add_vrect(x0=start, x1=end, fillcolor="red", opacity=0.3, line_width=0)

    for change_time in timestamps:
        fig.add_vline(x=change_time, line_width=2, line_dash="dash", line_color="blue")

    fig.update_layout(
        title=title,
        xaxis_title='Czas [s]',
        yaxis_title='Amplituda',
        xaxis_rangeslider_visible=True
    )

    fig.show()


def plot_two_signals(signal, sr, segments, rms_values):
    max_signal_value = np.max(signal)

    rms_values = [v / 100 * max_signal_value for v in rms_values]

    fig = go.Figure()

    fig.add_trace(go.Scatter(y=signal, mode='lines', name='Sygnał'))

    middle_segments = [(start + end) / 2 * sr for start, end in segments]

    fig.add_trace(go.Scatter(x=middle_segments, y=rms_values, mode='lines+markers', name='Punkty charakterystyczne'))

    fig.show()


def plot_pitch_lector_user(pitch1, pitch2, title):
    plt.figure(figsize=(12, 6))

    plt.plot(pitch1, label='Nagranie 1', alpha=0.7)
    plt.plot(pitch2, label='Nagranie 2', alpha=0.7)

    plt.title(title)
    plt.xlabel('Czas')
    plt.ylabel('Wysokość Tonu')
    plt.legend()

    plt.show()
