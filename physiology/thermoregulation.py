class ThermoregulationModel:

    def __init__(self):

        self.body_temp = 37.0

        self.thermal_capacity = 3500.0

        self.metabolic_heat = 80.0

    def step(
        self,
        room_temp,
        dt
    ):

        heat_loss = (
            3.0 * (self.body_temp - room_temp)
        )

        net_heat = (
            self.metabolic_heat - heat_loss
        )

        change = (
            net_heat / self.thermal_capacity
        )

        self.body_temp += change * dt

        return self.body_temp