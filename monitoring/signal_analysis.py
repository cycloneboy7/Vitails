from scipy.signal import find_peaks
import numpy as np


def detect_r_peaks(ecg, sampling_rate):

    peaks, properties = find_peaks(
        ecg,
        distance=int(sampling_rate * 0.35),
        prominence=0.5
    )

    return peaks

def calculate_rr_intervals(peaks, sampling_rate):
    rr = np.diff(peaks) / sampling_rate
    return rr * 1000

def calculate_rmssd(rr_intervals):
    differences = np.diff(rr_intervals)
    return np.sqrt(
        np.mean(differences ** 2)
    )