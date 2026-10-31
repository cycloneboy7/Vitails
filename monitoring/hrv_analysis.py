import numpy as np


def calculate_hrv(rr_intervals):

    rr = np.asarray(
        rr_intervals,
        dtype=float
    )

    if len(rr) < 2:
        raise ValueError(
            "At least 3 detected R-peaks are required"
        )

    differences = np.diff(rr)

    mean_rr = np.mean(rr)

    sdnn = np.std(rr, ddof=1)

    rmssd = np.sqrt(
        np.mean(differences ** 2)
    )

    pnn50 = (
        np.sum(np.abs(differences) > 50)
        / len(differences)
    ) * 100

    mean_hr = 60000 / mean_rr

    return {
        "mean_hr": mean_hr,
        "mean_rr": mean_rr,
        "sdnn": sdnn,
        "rmssd": rmssd,
        "pnn50": pnn50
    }