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

def calculate_paco2(
    respiratory_rate,
    tidal_volume,
    dead_space=150,
    co2_production=0.2
):

    alveolar_ventilation = (
        (tidal_volume - dead_space)
        * respiratory_rate / 1000
    )

    if alveolar_ventilation <= 0:
        raise ValueError("Alveolar ventilation must be positive")

    paco2 = (
        863 * co2_production /
        alveolar_ventilation
    )

    return paco2


