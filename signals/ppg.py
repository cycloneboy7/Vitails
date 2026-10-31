import numpy as np


class PPGGenerator:

    def __init__(self):

        self.phase = 0.0

    def step(self, heart_rate, dt):

        frequency = heart_rate / 60

        self.phase += (
            2 * np.pi * frequency * dt
        )

        self.phase %= 2 * np.pi

        phase = self.phase / (2 * np.pi)

        systolic = np.exp(
            -((phase - 0.20) / 0.09)**2
        )

        diastolic = 0.25 * np.exp(
            -((phase - 0.48) / 0.12)**2
        )

        return systolic + diastolic