import pandas as pd
import matplotlib.pyplot as plt


INPUT_FILE = "results/rule_based_controller.csv"


def save_plot(x, y, xlabel, ylabel, title, output_file):
    plt.figure()
    plt.plot(x, y)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_file, dpi=300)
    plt.show()
    plt.close()


def main():
    data = pd.read_csv(INPUT_FILE)

    # --------------------------------------------------------
    # Workload variation
    # --------------------------------------------------------

    save_plot(
        data["time"],
        data["workload"],
        "Time (s)",
        "Workload",
        "Rule-Based Controller: Workload",
        "results/plots/workload_rule_based.png",
    )

    # --------------------------------------------------------
    # Latency
    # --------------------------------------------------------

    save_plot(
        data["time"],
        data["latency"] * 1000,
        "Time (s)",
        "Latency (ms)",
        "Rule-Based Controller: Inference Latency",
        "results/plots/latency_rule_based.png",
    )

    # --------------------------------------------------------
    # Power
    # --------------------------------------------------------

    save_plot(
        data["time"],
        data["power"],
        "Time (s)",
        "Power (W)",
        "Rule-Based Controller: Accelerator Power",
        "results/plots/power_rule_based.png",
    )

    # --------------------------------------------------------
    # Temperature
    # --------------------------------------------------------

    save_plot(
        data["time"],
        data["temperature"],
        "Time (s)",
        "Temperature (°C)",
        "Rule-Based Controller: Accelerator Temperature",
        "results/plots/temperature_rule_based.png",
    )

    print("\nAll rule-based controller plots saved successfully.")


if __name__ == "__main__":
    main()