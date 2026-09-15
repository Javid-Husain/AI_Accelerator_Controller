import pandas as pd
import matplotlib.pyplot as plt


INPUT_FILE = "results/open_loop_baseline.csv"


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
        "Workload Variation",
        "results/plots/workload_variation.png",
    )

    # --------------------------------------------------------
    # Latency
    # --------------------------------------------------------

    save_plot(
        data["time"],
        data["latency"] * 1000,
        "Time (s)",
        "Latency (ms)",
        "Inference Latency",
        "results/plots/latency_baseline.png",
    )

    # --------------------------------------------------------
    # Power
    # --------------------------------------------------------

    save_plot(
        data["time"],
        data["power"],
        "Time (s)",
        "Power (W)",
        "Accelerator Power",
        "results/plots/power_baseline.png",
    )

    # --------------------------------------------------------
    # Temperature
    # --------------------------------------------------------

    save_plot(
        data["time"],
        data["temperature"],
        "Time (s)",
        "Temperature (°C)",
        "Accelerator Temperature",
        "results/plots/temperature_baseline.png",
    )

    print("\nAll baseline plots saved successfully.")


if __name__ == "__main__":
    main()