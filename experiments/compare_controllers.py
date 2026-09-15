import pandas as pd


BASELINE_FILE = "results/open_loop_baseline.csv"
RULE_BASED_FILE = "results/rule_based_controller.csv"


def analyze_controller(data):
    """
    Calculate summary metrics for one controller run.
    """

    latency_violations = (
        data["latency"] > data["deadline"]
    ).sum()

    accuracy_violations = (
        data["accuracy"] < 0.95
    ).sum()

    temperature_violations = (
        data["temperature"] > 85.0
    ).sum()

    power_violations = (
        data["power"] > 10.0
    ).sum()

    total_violations = (
        (data["latency"] > data["deadline"])
        | (data["accuracy"] < 0.95)
        | (data["temperature"] > 85.0)
        | (data["power"] > 10.0)
    ).sum()

    # Count configuration changes
    configuration_changes = (
        (
            data["frequency_level"].iloc[1:].values
            != data["frequency_level"].iloc[:-1].values
        )
        | (
            data["precision"].iloc[1:].values
            != data["precision"].iloc[:-1].values
        )
        | (
            data["sparsity"].iloc[1:].values
            != data["sparsity"].iloc[:-1].values
        )
    ).sum()

    return {
        "mean_latency_ms": data["latency"].mean() * 1000,
        "max_latency_ms": data["latency"].max() * 1000,
        "mean_power_w": data["power"].mean(),
        "max_power_w": data["power"].max(),
        "total_energy_j": data["energy"].sum(),
        "mean_energy_mj": data["energy"].mean() * 1000,
        "min_accuracy_percent": data["accuracy"].min() * 100,
        "max_temperature_c": data["temperature"].max(),
        "latency_violations": latency_violations,
        "accuracy_violations": accuracy_violations,
        "temperature_violations": temperature_violations,
        "power_violations": power_violations,
        "total_violations": total_violations,
        "configuration_changes": configuration_changes,
    }


def print_results(name, metrics):
    print(f"\n{name}")
    print("-" * 60)

    print(f"Mean latency          : {metrics['mean_latency_ms']:.3f} ms")
    print(f"Maximum latency       : {metrics['max_latency_ms']:.3f} ms")
    print(f"Mean power            : {metrics['mean_power_w']:.3f} W")
    print(f"Maximum power         : {metrics['max_power_w']:.3f} W")
    print(f"Total energy          : {metrics['total_energy_j']:.4f} J")
    print(f"Mean energy/inference : {metrics['mean_energy_mj']:.3f} mJ")
    print(
        f"Minimum accuracy      : "
        f"{metrics['min_accuracy_percent']:.2f}%"
    )
    print(
        f"Maximum temperature   : "
        f"{metrics['max_temperature_c']:.2f} °C"
    )

    print("\nConstraint violations:")
    print(f"  Latency             : {metrics['latency_violations']}")
    print(f"  Accuracy            : {metrics['accuracy_violations']}")
    print(f"  Temperature        : {metrics['temperature_violations']}")
    print(f"  Power               : {metrics['power_violations']}")
    print(f"  Total               : {metrics['total_violations']}")

    print(
        f"\nConfiguration changes : "
        f"{metrics['configuration_changes']}"
    )


def main():
    # --------------------------------------------------------
    # Load results
    # --------------------------------------------------------

    baseline_data = pd.read_csv(BASELINE_FILE)
    rule_based_data = pd.read_csv(RULE_BASED_FILE)

    # --------------------------------------------------------
    # Analyze
    # --------------------------------------------------------

    baseline_metrics = analyze_controller(
        baseline_data
    )

    rule_based_metrics = analyze_controller(
        rule_based_data
    )

    # --------------------------------------------------------
    # Display
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("FIXED vs RULE-BASED CONTROLLER")
    print("=" * 60)

    print_results(
        "FIXED BASELINE",
        baseline_metrics,
    )

    print_results(
        "RULE-BASED CONTROLLER",
        rule_based_metrics,
    )

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()