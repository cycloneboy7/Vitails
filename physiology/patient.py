from dataclasses import dataclass


@dataclass
class PatientParameters:
    patient_id: str = "VITALIS-001"

    age: int = 30
    # Cardiovascular
    resting_hr: float = 72.0
    stroke_volume: float = 70.0
    vascular_resistance: float = 1.0

    # Respiratory
    resting_rr: float = 15.0
    tidal_volume: float = 500.0

    # Oxygen
    initial_spo2: float = 98.0

    # Temperature
    body_temperature: float = 37.0


@dataclass
class PatientState:

    heart_rate: float = 72.0

    systolic_bp: float = 120.0
    diastolic_bp: float = 80.0

    cardiac_output: float = 5.0

    spo2: float = 98.0

    respiratory_rate: float = 15.0

    pulse: float = 72.0

    body_temperature: float = 37.0

    room_temperature: float = 24.0
    humidity: float = 50.0