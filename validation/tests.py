import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from physiology.oxygen_transport import oxygen_saturation
from signals.ecg import ECGGenerator

from config.parameters import SimulationConfig
from physiology.engine import PhysiologicalEngine


def test_ecg_generation():

    model = ECGGenerator()

    samples = []

    for _ in range(2500):

        value = model.step(72, 1/250)

        samples.append(value)

    assert len(samples) == 2500

    assert np.all(np.isfinite(samples))


def test_patient_sampling():

    duration = 10
    sampling_rate = 250

    samples = int(duration * sampling_rate)

    assert samples == 2500




def test_engine_initialization():

    config = SimulationConfig()

    engine = PhysiologicalEngine(config)

    assert engine.state.heart_rate == 72.0


def test_simulation_time():

    config = SimulationConfig()

    engine = PhysiologicalEngine(config)

    engine.step()

    assert np.isclose(
        engine.simulation_time,
        config.time_step
    )


def test_signal_generation():

    config = SimulationConfig()

    engine = PhysiologicalEngine(config)

    result = engine.step()

    assert np.isfinite(result["ecg"])

    assert np.isfinite(result["ppg"])

    assert np.isfinite(result["respiration"])


def test_oxygen_saturation_range():

    config = SimulationConfig()

    engine = PhysiologicalEngine(config)

    result = engine.step()

    assert 0 <= result["spo2"] <= 100