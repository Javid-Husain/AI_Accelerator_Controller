from models.accelerator import AcceleratorConfig
from models.workload import Workload
from config.parameters import (
    FREQUENCY_LEVELS,
    PRECISION_MODES,
    SPARSITY_LEVELS,
    MIN_ACCURACY,
)


def main():
    # --------------------------------------------------------
    # Critical workload scenario
    # --------------------------------------------------------

    workload = Workload(
        scene_complexity=0.9,
        sensor_rate=0.9,
        object_density=0.9,
        illumination=0.7,
        deadline=0.003,
    )

    feasible_configurations = []

    total_configurations = 0

    # --------------------------------------------------------
    # Evaluate every possible configuration
    # --------------------------------------------------------

    for frequency_level in FREQUENCY_LEVELS:

        for precision in PRECISION_MODES:

            for sparsity in SPARSITY_LEVELS:

                total_configurations += 1

                accelerator = AcceleratorConfig(
                    frequency_level=frequency_level,
                    precision=precision,
                    sparsity=sparsity,
                )

                latency = accelerator.calculate_latency(workload)
                power = accelerator.calculate_power(workload)
                energy = accelerator.calculate_energy(workload)
                accuracy = accelerator.calculate_accuracy(workload)

                latency_ok = latency <= workload.deadline
                accuracy_ok = accuracy >= MIN_ACCURACY

                if latency_ok and accuracy_ok:
                    feasible_configurations.append(
                        {
                            "frequency_level": frequency_level,
                            "frequency": FREQUENCY_LEVELS[frequency_level],
                            "precision": precision,
                            "sparsity": sparsity,
                            "latency_ms": latency * 1000,
                            "power_w": power,
                            "energy_mj": energy * 1000,
                            "accuracy_percent": accuracy * 100,
                        }
                    )

    # --------------------------------------------------------
    # Print results
    # --------------------------------------------------------

    print("\n" + "=" * 75)
    print("FEASIBLE CONFIGURATION ANALYSIS")
    print("=" * 75)

    print(f"\nTotal configurations evaluated: {total_configurations}")

    print(
        f"Critical workload: {workload.scene_complexity:.2f}"
    )

    print(
        f"Deadline: {workload.deadline * 1000:.2f} ms"
    )

    print(
        f"Minimum accuracy: {MIN_ACCURACY * 100:.2f}%"
    )

    print(
        f"\nFeasible configurations: "
        f"{len(feasible_configurations)}"
    )

    if not feasible_configurations:
        print("\nNo feasible configuration found.")

    else:
        print("\nConfigurations satisfying both constraints:")
        print("-" * 75)

        for config in feasible_configurations:
            print(
                f"Freq Level: {config['frequency_level']} | "
                f"Freq: {config['frequency']:.2f} | "
                f"Precision: {config['precision']:>4} | "
                f"Sparsity: {config['sparsity']:.2f} | "
                f"Latency: {config['latency_ms']:.3f} ms | "
                f"Power: {config['power_w']:.3f} W | "
                f"Energy: {config['energy_mj']:.3f} mJ | "
                f"Accuracy: {config['accuracy_percent']:.2f}%"
            )

    print("=" * 75)


if __name__ == "__main__":
    main()