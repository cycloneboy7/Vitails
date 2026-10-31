import numpy as np


def respiratory_heart_rate(
    baseline_hr,
    respiratory_phase,
    amplitude=2.0
):

    modulation = (
        amplitude * np.sin(respiratory_phase)
    )

    return baseline_hr + modulation


def cardiac_output(
    heart_rate,
    stroke_volume
):

    return (
        heart_rate * stroke_volume / 1000
    )

def respiratory_heart_rate(
    baseline_hr,
    respiratory_phase,
    amplitude=2.0
):

    return (
        baseline_hr +
        amplitude * np.sin(respiratory_phase)
    )

def calculate_cardiac_output(
    heart_rate,
    stroke_volume
):

    return (
        heart_rate * stroke_volume / 1000
    )

def calculate_map(
    cardiac_output,
    vascular_resistance
):

    return cardiac_output * vascular_resistance * 60 / 1000