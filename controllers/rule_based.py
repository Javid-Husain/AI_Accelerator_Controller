from models.accelerator import AcceleratorConfig
from models.workload import Workload
from config.parameters import (
    FREQUENCY_LEVELS,
    PRECISION_MODES,
    SPARSITY_LEVELS,
    MIN_ACCURACY,
)


class RuleBasedController:
    """
    Rule-based runtime controller.

    The controller reacts to constraint violations and
    selects an accelerator configuration using simple
    deterministic rules.

    Control priority:
        1. Maintain deadline
        2. Maintain minimum accuracy
        3. Avoid unnecessary configuration changes

    This controller is a baseline heuristic for comparison
    with the future MPC controller.
    """

    def __init__(self, initial_config: AcceleratorConfig):
        self.current_config = initial_config

    def select_configuration(
        self,
        workload: Workload,
    ) -> AcceleratorConfig:

        # ----------------------------------------------------
        # Evaluate current configuration
        # ----------------------------------------------------

        latency = self.current_config.calculate_latency(workload)
        accuracy = self.current_config.calculate_accuracy(workload)

        latency_ok = latency <= workload.deadline
        accuracy_ok = accuracy >= MIN_ACCURACY

        # If the current configuration is already safe,
        # keep it unchanged.
        if latency_ok and accuracy_ok:
            return self.current_config

        # ----------------------------------------------------
        # Generate candidate configurations
        # ----------------------------------------------------

        candidates = []

        for frequency_level in FREQUENCY_LEVELS:

            for precision in PRECISION_MODES:

                for sparsity in SPARSITY_LEVELS:

                    candidate = AcceleratorConfig(
                        frequency_level=frequency_level,
                        precision=precision,
                        sparsity=sparsity,
                    )

                    candidate_latency = candidate.calculate_latency(
                        workload
                    )

                    candidate_accuracy = candidate.calculate_accuracy(
                        workload
                    )

                    # Candidate must satisfy both constraints.
                    if (
                        candidate_latency <= workload.deadline
                        and candidate_accuracy >= MIN_ACCURACY
                    ):
                        candidates.append(candidate)

        # ----------------------------------------------------
        # No feasible configuration
        # ----------------------------------------------------

        if not candidates:
            return self.current_config

        # ----------------------------------------------------
        # Rule:
        #
        # Among feasible configurations, select the one with
        # the lowest energy consumption.
        #
        # If energy is equal, prefer lower latency.
        # ----------------------------------------------------

        selected_config = min(
            candidates,
            key=lambda config: (
                config.calculate_energy(workload),
                config.calculate_latency(workload),
            ),
        )

        self.current_config = selected_config

        return selected_config