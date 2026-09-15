from dataclasses import dataclass

from config.parameters import FREQUENCY_LEVELS, PRECISION_MODES, SPARSITY_LEVELS


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