import numpy as np
from scipy.signal import (
    butter,
    sosfiltfilt,
    find_peaks
)


def detect_r_peaks(ecg, sampling_rate=250):

    filtered = filter_ecg(ecg, sampling_rate)

    minimum_distance = int(
        sampling_rate * 60 / 200
    )

    prominence = max(
        0.5 * np.std(filtered),
        1e-8
    )

    peaks, properties = find_peaks(
        filtered,
        distance=minimum_distance,
        prominence=prominence
    )

    return peaks, filtered

def calculate_rr_intervals(
    peaks,
    sampling_rate=250
):

    rr_seconds = (
        np.diff(peaks) / sampling_rate
    )

    return rr_seconds * 1000

def calculate_rmssd(rr_intervals):
    differences = np.diff(rr_intervals)
    return np.sqrt(
        np.mean(differences ** 2)
    )


def filter_ecg(ecg, sampling_rate=250):

    ecg = np.asarray(ecg, dtype=float)

    if len(ecg) < 20:
        raise ValueError("ECG signal is too short")

    sos = butter(
        3,
        [0.5, 40],
        btype="bandpass",
        fs=sampling_rate,
        output="sos"
    )

    return sosfiltfilt(sos, ecg)