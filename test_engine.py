from config.parameters import SimulationConfig

from physiology.engine import PhysiologicalEngine

import numpy as np
import matplotlib.pyplot as plt


# Initialize configuration
config = SimulationConfig()

# Initialize virtual patient engine
engine = PhysiologicalEngine(config)

# Store generated readings
records = []

# Simulate 10 seconds
for i in range(2500):

    reading = engine.step()

    records.append(reading)


# Convert to DataFrame
import pandas as pd

df = pd.DataFrame(records)

print(df.head())

print("\nSimulation summary:")

print(df.describe())

fig, axes = plt.subplots(
    4, 1,
    figsize=(14, 12)
)

axes[0].plot(
    df["time"],
    df["ecg"]
)

axes[0].set_title("ECG")
axes[0].set_ylabel("Amplitude")

axes[1].plot(
    df["time"],
    df["ppg"]
)

axes[1].set_title("Photoplethysmography")
axes[1].set_ylabel("Amplitude")

axes[2].plot(
    df["time"],
    df["respiration"]
)

axes[2].set_title("Respiration")
axes[2].set_ylabel("Amplitude")

axes[3].plot(
    df["time"],
    df["arterial_pressure"]
)

axes[3].set_title("Arterial Pressure")
axes[3].set_ylabel("mmHg")

axes[3].set_xlabel("Time (seconds)")

plt.tight_layout()

plt.show()