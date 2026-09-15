import pandas as pd

from config.parameters import (
    MAX_LATENCY,
    MIN_ACCURACY,
    MAX_TEMPERATURE,
    MAX_POWER,
)


INPUT_FILE = "results/open_loop_baseline.csv"


def main():
    data = pd.read_csv(INPUT_FILE)

    # --------------------------------------------------------
    # Constraint checks
    # --------------------------------------------------------

    data["latency_violation"] = data["latency"] > MAX_LATENCY
    data["accuracy_violation"] = data["accuracy"] < MIN_ACCURACY
    data["temperature_violation"] = data["temperature"] > MAX_TEMPERATURE
    data["power_violation"] = data["power"] > MAX_POWER

    data["any_violation"] = (
        data["latency_violation"]
        | data["accuracy_violation"]
        | data["temperature_violation"]
        | data["power_violation"]
    )

    # --------------------------------------------------------
    # Summary statistics
    # --------------------------------------------------------

    max_latency = data["latency"].max()
    min_accuracy = data["accuracy"].min()
    max_temperature = data["temperature"].max()
    max_power = data["power"].max()

    total_steps = len(data)

    latency_violations = data["latency_violation"].sum()
    accuracy_violations = data["accuracy_violation"].sum()
    temperature_violations = data["temperature_violation"].sum()
    power_violations = data["power_violation"].sum()
    total_violations = data["any_violation"].sum()

    # --------------------------------------------------------
    # Print analysis
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("OPEN-LOOP BASELINE CONSTRAINT ANALYSIS")
    print("=" * 60)

    print(f"\nTotal simulation steps: {total_steps}")

    print("\nObserved maximum/minimum values:")
    print(f"Maximum latency    : {max_latency * 1000:.2f} ms")
    print(f"Minimum accuracy   : {min_accuracy * 100:.2f}%")
    print(f"Maximum temperature: {max_temperature:.2f} °C")
    print(f"Maximum power      : {max_power:.2f} W")

    print("\nConstraint limits:")
    print(f"Maximum latency    : {MAX_LATENCY * 1000:.2f} ms")
    print(f"Minimum accuracy   : {MIN_ACCURACY * 100:.2f}%")
    print(f"Maximum temperature: {MAX_TEMPERATURE:.2f} °C")
    print(f"Maximum power      : {MAX_POWER:.2f} W")

    print("\nConstraint violations:")
    print(f"Latency violations    : {latency_violations}")
    print(f"Accuracy violations   : {accuracy_violations}")
    print(f"Temperature violations: {temperature_violations}")
    print(f"Power violations      : {power_violations}")
    print(f"Total violating steps : {total_violations}")

    # --------------------------------------------------------
    # Overall baseline status
    # --------------------------------------------------------

    if total_violations == 0:
        print("\nBaseline status: ALL CONSTRAINTS SATISFIED")
    else:
        print("\nBaseline status: CONSTRAINT VIOLATIONS DETECTED")

    print("=" * 60)


if __name__ == "__main__":
    main()