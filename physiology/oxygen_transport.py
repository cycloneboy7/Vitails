import numpy as np


def oxygen_saturation(
    pao2,
    p50=26.8,
    hill=2.7
):

    pao2 = max(pao2, 0)

    saturation = (
        pao2 ** hill /
        (p50 ** hill + pao2 ** hill)
    )

    return saturation * 100

def calculate_alveolar_oxygen(
    fio2,
    atmospheric_pressure,
    water_vapor_pressure,
    paco2,
    respiratory_exchange_ratio
):

    return (
        fio2 *
        (atmospheric_pressure - water_vapor_pressure)
        - paco2 / respiratory_exchange_ratio
    )


def estimate_arterial_oxygen(
    pao2,
    oxygen_gradient=10.0
):

    return max(
        0,
        pao2 - oxygen_gradient
    )

pao2 = calculate_alveolar_oxygen(
    0.21, 760, 47, 40, 0.8
)

pao2_arterial = estimate_arterial_oxygen(pao2)

spo2 = oxygen_saturation(pao2_arterial)

print("Alveolar PO2:", pao2)
print("Estimated arterial PO2:", pao2_arterial)
print("Estimated saturation:", spo2)