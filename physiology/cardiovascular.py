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

    def __init__(self):

        self.pressure = 80.0

        self.compliance = 1.5

        self.resistance = 1.0

        self.time = 0.0

    def step(
        self,
        heart_rate,
        stroke_volume,
        dt
    ):

        period = 60 / heart_rate

        self.time += dt

        phase = self.time % period

        ejection_time = min(
            0.30,
            period * 0.40
        )

        if phase < ejection_time:

            inflow = stroke_volume / ejection_time

        else:

            inflow = 0.0

        outflow = (
            self.pressure / self.resistance
        )

        dp = (
            inflow - outflow
        ) / self.compliance

        self.pressure += dp * dt

        return self.pressure