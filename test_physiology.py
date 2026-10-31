from physiology.respiratory import RespiratoryModel

from physiology.oxygen_transport import (
    calculate_alveolar_oxygen,
    estimate_arterial_oxygen,
    oxygen_saturation
)

from physiology.coupling import (
    respiratory_heart_rate,
    calculate_cardiac_output,
    calculate_map
)
#respiration test
resp = RespiratoryModel()

result = resp.step(
    respiratory_rate=15,
    tidal_volume=500,
    dt=0.004
)

print("Breathing:", result["breathing"])

print(
    "Minute ventilation:",
    result["minute_ventilation"]
)

#O2 transport 
pao2 = calculate_alveolar_oxygen(
    0.21, 760, 47, 40, 0.8
)

arterial_o2 = estimate_arterial_oxygen(pao2)

spo2 = oxygen_saturation(arterial_o2)

print("SpO2 estimate:", spo2)


#cardiovascular coupling
hr = respiratory_heart_rate(
    72,
    respiratory_phase=1.0
)

co = calculate_cardiac_output(
    hr,
    70
)

map_value = calculate_map(
    co,
    18
)

print("Heart rate:", hr)
print("Cardiac output:", co)
print("Mean arterial pressure:", map_value)