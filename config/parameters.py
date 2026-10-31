from dataclasses import dataclass


@dataclass
class SimulationConfig:
    # Sampling time
    sampling_rate: int = 250
    # Simulation frequency
    duration: float = 60.0
    # Numerical integration
    time_step: float = 1 / 250
    # Reproducibility
    random_seed: int = 42

    @property
    def total_samples(self):
        return int(self.duration * self.sampling_rate)

    # Physiological simulation
    initial_heart_rate: float = 72.0
    initial_respiratory_rate: float = 15.0

    initial_spo2: float = 98.0

    initial_body_temperature: float = 37.0

    # Cardiovascular
    stroke_volume: float = 70.0

    # Oxygen model
    inspired_oxygen: float = 0.21
    atmospheric_pressure: float = 760.0
    water_vapor_pressure: float = 47.0
    respiratory_exchange_ratio: float = 0.8
    p50: float = 26.8
