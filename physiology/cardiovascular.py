import numpy as np


class HeartRateModel:

    def __init__(self, seed=42):
        self.rng = np.random.default_rng(seed)
        self.time = 0.0

    def calculate_hr(
        self,
        baseline_hr,
        respiration,
        dt
    ):

        self.time += dt

        low_frequency = (
            1.5 * np.sin(2 * np.pi * 0.1 * self.time)
        )

        high_frequency = (
            2.0 * respiration
        )

        noise = self.rng.normal(0, 0.2)

        hr = (
            baseline_hr
            + low_frequency
            + high_frequency
            + noise
        )

        return max(hr, 1.0)

    def calculate_cardiac_output(
        heart_rate,
        stroke_volume
    ):
        return (
            heart_rate * stroke_volume / 1000
        )


#Windkessel model for simulating arterial pressure dynamics
class WindkesselModel:

    def __init__(
        self,
        compliance=1.5,
        resistance=15.0,
        initial_pressure=80.0
    ):

        self.compliance = compliance
        self.resistance = resistance
        self.pressure = initial_pressure

    def step(self, inflow, dt):

        outflow = (
            self.pressure / self.resistance
        )

        dp = (
            inflow - outflow
        ) / self.compliance

        self.pressure += dp * dt

        return self.pressure