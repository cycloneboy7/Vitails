import numpy as np
import matplotlib.pyplot as plt


class ECGGenerator:
    def __init__(self):

        self.x = 1.0
        self.y = 0.0
        self.z = 0.0

        # P, Q, R, S, T
        self.a = np.array([
            1.2, -5.0, 30.0, -7.5, 0.75
        ])

        self.b = np.array([
            0.25, 0.10, 0.10, 0.10, 0.40
        ])

        self.theta = np.array([
            -np.pi / 3,
            -np.pi / 12,
            0,
            np.pi / 12,
            np.pi / 2
        ])


    def step(self, heart_rate, dt):

        omega = 2 * np.pi * heart_rate / 60

        alpha = 1 - np.sqrt(
            self.x**2 + self.y**2
        )

        angle = np.arctan2(self.y, self.x)

        dx = alpha * self.x - omega * self.y

        dy = alpha * self.y + omega * self.x

        delta = np.arctan2(
            np.sin(angle - self.theta),
            np.cos(angle - self.theta)
        )

        dz = -np.sum(
            self.a * delta *
            np.exp(-(delta**2) / (2 * self.b**2))
        ) - self.z

        self.x += dx * dt
        self.y += dy * dt
        self.z += dz * dt

        return self.z


ecg = ECGGenerator()

signal = []

for i in range(2500):

    value = ecg.step(
        heart_rate=72,
        dt=1/250
    )

    signal.append(value)

plt.figure(figsize=(14, 4))

plt.plot(np.arange(2500)/250, signal)

plt.title("VITALIS - Dynamical ECG")
plt.xlabel("Time (seconds)")
plt.ylabel("ECG amplitude (arbitrary units)")

plt.grid()
plt.show()