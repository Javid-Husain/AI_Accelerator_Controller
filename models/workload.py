from dataclasses import dataclass


@dataclass
class Workload:
    """
    Represents the workload and environmental conditions
    observed by the accelerator controller.

    Normalized workload variables must be in [0, 1].
    Deadline is specified in seconds.
    """

    scene_complexity: float
    sensor_rate: float
    object_density: float
    illumination: float
    deadline: float

    def __post_init__(self):
        normalized_values = {
            "scene_complexity": self.scene_complexity,
            "sensor_rate": self.sensor_rate,
            "object_density": self.object_density,
            "illumination": self.illumination,
        }

        for name, value in normalized_values.items():
            if not 0.0 <= value <= 1.0:
                raise ValueError(
                    f"{name} must be between 0 and 1, got {value}"
                )

        if self.deadline <= 0:
            raise ValueError(
                f"deadline must be greater than 0, got {self.deadline}"
            )


def generate_workload(step: int, total_steps: int) -> Workload:
    """
    Generate a deterministic workload that changes over time.

    Workload progression:
        low -> medium -> high -> medium

    During the high-workload period, the deadline becomes
    more demanding to represent a navigation-critical
    perception task.

    The scenario is a simulation assumption.
    """

    if total_steps <= 0:
        raise ValueError("total_steps must be greater than 0")

    progress = step / (total_steps - 1) if total_steps > 1 else 0.0

    if progress < 0.25:
        workload_level = 0.2
        deadline = 0.020

    elif progress < 0.50:
        workload_level = 0.5
        deadline = 0.020

    elif progress < 0.75:
        workload_level = 0.9
        deadline = 0.003

    else:
        workload_level = 0.4
        deadline = 0.020

    return Workload(
        scene_complexity=workload_level,
        sensor_rate=workload_level,
        object_density=workload_level,
        illumination=0.7,
        deadline=deadline,
    )