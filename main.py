import pandas as pd

from config.parameters import (
    INITIAL_TEMPERATURE,
    SIMULATION_TIME,
    DT,
)
from models.accelerator import AcceleratorConfig
from models.thermal import ThermalModel
from models.workload import generate_workload


def main():
    total_steps = int(SIMULATION_TIME / DT)

    # --------------------------------------------------------
    # Fixed accelerator configuration
    # --------------------------------------------------------

    accelerator = AcceleratorConfig(
        frequency_level=3,
        precision="FP16",
        sparsity=0.20,
    )

    # --------------------------------------------------------
    # Thermal model
    # --------------------------------------------------------

    thermal_model = ThermalModel(
        initial_temperature=INITIAL_TEMPERATURE
    )

    # --------------------------------------------------------
    # Telemetry storage
    # --------------------------------------------------------

    telemetry = []

    # --------------------------------------------------------
    # Simulation loop
    # --------------------------------------------------------

    for step in range(total_steps):

        workload = generate_workload(
            step=step,
            total_steps=total_steps,
        )

        latency = accelerator.calculate_latency(workload)
        power = accelerator.calculate_power(workload)
        energy = accelerator.calculate_energy(workload)
        accuracy = accelerator.calculate_accuracy(workload)

        temperature = thermal_model.update(power)

        telemetry.append(
            {
                "time": step * DT,
                "workload": workload.scene_complexity,
                "sensor_rate": workload.sensor_rate,
                "object_density": workload.object_density,
                "illumination": workload.illumination,
                "deadline": workload.deadline,
                "frequency_level": accelerator.frequency_level,
                "precision": accelerator.precision,
                "sparsity": accelerator.sparsity,
                "latency": latency,
                "power": power,
                "energy": energy,
                "accuracy": accuracy,
                "temperature": temperature,
            }
        )

    # --------------------------------------------------------
    # Convert telemetry to DataFrame
    # --------------------------------------------------------

    telemetry_df = pd.DataFrame(telemetry)

    # --------------------------------------------------------
    # Save simulation results
    # --------------------------------------------------------

    output_path = "results/open_loop_baseline.csv"

    telemetry_df.to_csv(
        output_path,
        index=False,
    )

    # --------------------------------------------------------
    # Display summary
    # --------------------------------------------------------

    print("\nSimulation completed successfully.")
    print(f"Total simulation steps: {total_steps}")
    print(f"Telemetry records: {len(telemetry_df)}")
    print(f"Results saved to: {output_path}")

    print("\nFirst 5 telemetry records:")
    print(telemetry_df.head())


if __name__ == "__main__":
    main()