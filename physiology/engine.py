import numpy as np

from physiology.patient import (
    PatientParameters,
    PatientState
)

from physiology.respiratory import RespiratoryModel

from physiology.cardiovascular import (
    HeartRateModel,
    WindkesselModel
)

from physiology.oxygen_transport import (
    calculate_alveolar_oxygen,
    estimate_arterial_oxygen,
    oxygen_saturation,
    calculate_paco2
)

from physiology.thermoregulation import (
    ThermoregulationModel
)

from physiology.coupling import (
    calculate_cardiac_output
)

from signals.ecg import ECGGenerator
from signals.ppg import PPGGenerator


class PhysiologicalEngine:

    def __init__(self, config):

        self.config = config

        self.parameters = PatientParameters()

        self.state = PatientState()

        # Physiological models
        self.respiratory = RespiratoryModel()

        self.heart_model = HeartRateModel(
            seed=config.random_seed
        )

        self.ecg = ECGGenerator()

        self.ppg = PPGGenerator()

        self.thermal = ThermoregulationModel()

        # Simulation state
        self.simulation_time = 0.0

        self.arterial_pressure = 80.0

        self.windkessel = WindkesselModel()

    def step(self):

        dt = self.config.time_step

        p = self.parameters
        s = self.state

        # 1. Respiratory model
        resp = self.respiratory.step(
            respiratory_rate=s.respiratory_rate,
            tidal_volume=p.tidal_volume,
            dt=dt
        )

        # 2. Heart rate variability
        s.heart_rate = self.heart_model.calculate_hr(
            baseline_hr=p.resting_hr,
            respiration=resp["breathing"],
            dt=dt
        )

        # 3. Cardiac output
        s.cardiac_output = calculate_cardiac_output(
            s.heart_rate,
            p.stroke_volume
        )

        # 4. ECG
        ecg_value = self.ecg.step(
            heart_rate=s.heart_rate,
            dt=dt
        )

        # 5. PPG
        ppg_value = self.ppg.step(
            heart_rate=s.heart_rate,
            dt=dt
        )

        # 6. Oxygen transport
        paco2=calculate_paco2(
            respiratory_rate=s.respiratory_rate,
            tidal_volume=p.tidal_volume
        ),

        arterial_o2 = estimate_arterial_oxygen(pao2)

        s.spo2 = oxygen_saturation(
            arterial_o2,
            p50=self.config.p50
        )

        # 7. Thermoregulation
        s.body_temperature = self.thermal.step(
            room_temp=s.room_temperature,
            dt=dt
        )

        # 8. Pulse approximation
        s.pulse = s.heart_rate

        # 9. Simulation time
        self.simulation_time += dt

        arterial_pressure = self.windkessel.step(
            heart_rate=s.heart_rate,
            stroke_volume=p.stroke_volume,
            dt=dt
        )

        return {
            "time": self.simulation_time,

            "ecg": ecg_value,
            "ppg": ppg_value,

            "respiration": resp["breathing"],
            "airflow": resp["airflow"],

            "heart_rate": s.heart_rate,
            "spo2": s.spo2,
            "respiratory_rate": s.respiratory_rate,

            "cardiac_output": s.cardiac_output,
            "pulse": s.pulse,

            "body_temperature": s.body_temperature,
            "room_temperature": s.room_temperature,
            "humidity": s.humidity,

            "arterial_pressure": arterial_pressure,
        }