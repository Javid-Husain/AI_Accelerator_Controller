from dataclasses import dataclass

from config.parameters import (
    BASE_LATENCY,
    BASE_POWER,
    FREQUENCY_LEVELS,
    PRECISION_MODES,
    SPARSITY_LEVELS,
)
from models.workload import Workload


@dataclass
class AcceleratorConfig:
    """
    Runtime configuration selected by the controller.

    The controller can modify:
        - frequency level
        - precision
        - sparsity
    """

    frequency_level: int
    precision: str
    sparsity: float

    def __post_init__(self):
        if self.frequency_level not in FREQUENCY_LEVELS:
            raise ValueError(
                f"Invalid frequency level: {self.frequency_level}"
            )

        if self.precision not in PRECISION_MODES:
            raise ValueError(
                f"Invalid precision mode: {self.precision}"
            )

        if self.sparsity not in SPARSITY_LEVELS:
            raise ValueError(
                f"Invalid sparsity level: {self.sparsity}"
            )

    def _calculate_workload_factor(self, workload: Workload) -> float:
        """
        Calculate the effective workload based on the
        different workload characteristics.

        The weights are simulation assumptions.
        """

        return (
            0.5 * workload.scene_complexity
            + 0.3 * workload.sensor_rate
            + 0.2 * workload.object_density
        )

    def calculate_latency(self, workload: Workload) -> float:
        """
        Estimate inference latency in seconds.

        Expected behavior:
            - Higher workload -> higher latency
            - Higher frequency -> lower latency
            - Higher sparsity -> lower latency
            - Lower precision -> lower computational cost
        """

        frequency = FREQUENCY_LEVELS[self.frequency_level]
        compute_factor = PRECISION_MODES[self.precision]["compute_factor"]

        workload_factor = self._calculate_workload_factor(workload)

        effective_workload = (
            workload_factor
            * compute_factor
            * (1.0 - self.sparsity)
        )

        latency = (
            BASE_LATENCY
            * (1.0 + effective_workload)
            / frequency
        )

        return latency

    def calculate_power(self, workload: Workload) -> float:
        """
        Estimate accelerator power consumption in Watts.

        This is a simulation model, not measured hardware data.

        Expected behavior:
            - Higher frequency -> higher power
            - Higher workload -> higher power
            - Higher sparsity -> lower power
            - Lower precision -> lower power
        """

        frequency = FREQUENCY_LEVELS[self.frequency_level]

        compute_factor = PRECISION_MODES[self.precision]["compute_factor"]

        workload_factor = self._calculate_workload_factor(workload)

        effective_workload = (
            workload_factor
            * compute_factor
            * (1.0 - self.sparsity)
        )

        frequency_power_factor = frequency ** 3

        power = (
            BASE_POWER
            * frequency_power_factor
            * (1.0 + effective_workload)
        )

        return power

    def calculate_energy(self, workload: Workload) -> float:
        """
        Estimate energy consumed for one inference in Joules.

        Energy = Power × Execution Time
        """

        latency = self.calculate_latency(workload)
        power = self.calculate_power(workload)

        energy = power * latency

        return energy

    def calculate_accuracy(self, workload: Workload) -> float:
        """
        Estimate prediction accuracy.

        Accuracy primarily depends on:
            - precision
            - sparsity

        Frequency does not directly affect accuracy.

        The model is a simulation assumption and should
        eventually be replaced or calibrated using
        measured model accuracy.
        """

        base_accuracy = PRECISION_MODES[self.precision]["accuracy"]

        # Accuracy penalty due to sparsity.
        #
        # This is intentionally conservative: higher sparsity
        # causes a larger degradation in prediction accuracy.
        sparsity_penalty = 0.05 * self.sparsity

        accuracy = base_accuracy - sparsity_penalty

        # Keep accuracy within a physically meaningful range.
        accuracy = max(0.0, min(1.0, accuracy))

        return accuracy