import numpy as np


class RespiratoryModel:

    def __init__(self):

        self.phase = 0.0

    def step(
        self,
        respiratory_rate,
        tidal_volume,
        dt
    ):

        frequency = respiratory_rate / 60

        self.phase += (
            2 * np.pi * frequency * dt
        )

        self.phase %= 2 * np.pi

        # Normalized breathing waveform
        breathing = np.sin(self.phase)

        # Approximate airflow
        airflow = (
            tidal_volume *
            frequency *
            np.cos(self.phase)
        )

        # Minute ventilation in L/min
        minute_ventilation = (
            respiratory_rate *
            tidal_volume / 1000
        )

        return {
            "phase": self.phase,
            "breathing": breathing,
            "airflow": airflow,
            "minute_ventilation": minute_ventilation
        }