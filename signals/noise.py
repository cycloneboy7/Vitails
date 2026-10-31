import numpy as np


class SensorNoise:

    def __init__(self, seed=42):

        self.rng = np.random.default_rng(seed)

    def add_noise(
        self,
        signal,
        standard_deviation=0.01
    ):

        noise = self.rng.normal(
            0,
            standard_deviation,
            size=np.shape(signal)
        )

        return signal + noise