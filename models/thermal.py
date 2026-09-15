from config.parameters import (
    AMBIENT_TEMPERATURE,
    THERMAL_RESISTANCE,
    THERMAL_TIME_CONSTANT,
    DT,
)


class ThermalModel:
    """
    First-order thermal model of the accelerator.

    Temperature evolves over time according to accelerator
    power consumption and heat dissipation to the environment.

    This is a simulation model, not measured hardware data.
    """

    def __init__(self, initial_temperature: float):
        if initial_temperature < AMBIENT_TEMPERATURE:
            raise ValueError(
                "Initial temperature cannot be below ambient temperature."
            )

        self.temperature = initial_temperature

    def update(self, power: float) -> float:
        """
        Update accelerator temperature for one simulation timestep.

        Parameters
        ----------
        power : float
            Accelerator power in Watts.

        Returns
        -------
        float
            Updated temperature in degrees Celsius.
        """

        if power < 0:
            raise ValueError(
                f"Power cannot be negative, got {power}"
            )

        equilibrium_temperature = (
            AMBIENT_TEMPERATURE
            + THERMAL_RESISTANCE * power
        )

        temperature_change = (
            DT
            / THERMAL_TIME_CONSTANT
            * (equilibrium_temperature - self.temperature)
        )

        self.temperature += temperature_change

        return self.temperature

    def get_temperature(self) -> float:
        """
        Return the current accelerator temperature.
        """

        return self.temperature

    def reset(self, temperature: float) -> None:
        """
        Reset the thermal model to a specified temperature.
        """

        if temperature < AMBIENT_TEMPERATURE:
            raise ValueError(
                "Reset temperature cannot be below ambient temperature."
            )

        self.temperature = temperature