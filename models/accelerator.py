from dataclasses import dataclass

from config.parameters import (
    BASE_LATENCY,
    FREQUENCY_LEVELS,
    PRECISION_MODES,
    SPARSITY_LEVELS,
)
from models.workload import Workload


@dataclass
class AcceleratorConfig:
    """
    Runtime configuration selected by the controller.
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

    def calculate_latency(self, workload: Workload) -> float:
        """
        Estimate inference latency in seconds.

        Higher workload increases latency.
        Higher frequency decreases latency.
        Higher sparsity decreases effective computation.
        Precision affects computational cost.
        """

        frequency = FREQUENCY_LEVELS[self.frequency_level]
        compute_factor = PRECISION_MODES[self.precision]["compute_factor"]

        workload_factor = (
            0.5 * workload.scene_complexity
            + 0.3 * workload.sensor_rate
            + 0.2 * workload.object_density
        )

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