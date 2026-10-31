import numpy as np
import matplotlib.pyplot as plt

from signals.ecg import ECGGenerator

from monitoring.signal_analysis import (
    detect_r_peaks,
    calculate_rr_intervals
)

from monitoring.hrv_analysis import calculate_hrv


fs = 250

ecg_model = ECGGenerator()

signal = []

for _ in range(fs * 60):

    value = ecg_model.step(
        heart_rate=72,
        dt=1/fs
    )

    signal.append(value)


peaks, filtered = detect_r_peaks(
    signal,
    fs
)

rr = calculate_rr_intervals(
    peaks,
    fs
)

hrv = calculate_hrv(rr)

print("R peaks:", len(peaks))
print("RR intervals:", rr)
print("HRV results:", hrv)


plt.figure(figsize=(14, 5))

plt.plot(
    np.arange(len(filtered))/fs,
    filtered
)

plt.scatter(
    peaks/fs,
    filtered[peaks],
    color="red",
    label="Detected R-peaks"
)

plt.title("VITALIS ECG Analysis")

plt.xlabel("Time (seconds)")
plt.ylabel("Amplitude (model units)")

plt.legend()
plt.grid()

plt.show()