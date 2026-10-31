import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from physiology.oxygen_transport import oxygen_saturation
from signals.ecg import ECGGenerator


def test_oxygen_saturation():

    high = oxygen_saturation(100)
    low = oxygen_saturation(40)

    assert high > low


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