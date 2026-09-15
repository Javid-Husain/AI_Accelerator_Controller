import pandas as pd

from config.parameters import (
    INITIAL_TEMPERATURE,
    SIMULATION_TIME,
    DT,
)
from models.accelerator import AcceleratorConfig
from models.thermal import ThermalModel
from models.workload import generate_workload
from controllers.rule_based import RuleBasedController


def main():
    total_steps = int(SIMULATION_TIME / DT)

    # --------------------------------------------------------
    # Initial accelerator configuration
    # --------------------------------------------------------

    initial_config = AcceleratorConfig(
        frequency_level=3,
        precision="FP16",
        sparsity=0.20,
    )

    # --------------------------------------------------------
    # Controller
    # --------------------------------------------------------

    controller = RuleBasedController(
        initial_config=initial_config
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

        # Controller selects configuration
        accelerator = controller.select_configuration(
            workload
        )

        # Accelerator performance
        latency = accelerator.calculate_latency(workload)
        power = accelerator.calculate_power(workload)
        energy = accelerator.calculate_energy(workload)
        accuracy = accelerator.calculate_accuracy(workload)

        # Thermal dynamics
        temperature = thermal_model.update(power)

        # ----------------------------------------------------
        # Store telemetry
        # ----------------------------------------------------

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

        # ----------------------------------------------------
        # Print approximately once per second
        # ----------------------------------------------------

        if step % 100 == 0:
            print(
                f"Time: {step * DT:5.2f} s | "
                f"Workload: {workload.scene_complexity:.2f} | "
                f"Deadline: {workload.deadline * 1000:5.2f} ms | "
                f"Freq: {accelerator.frequency_level} | "
                f"Precision: {accelerator.precision:>4} | "
                f"Sparsity: {accelerator.sparsity:.2f} | "
                f"Latency: {latency * 1000:6.2f} ms | "
                f"Power: {power:5.2f} W | "
                f"Temp: {temperature:6.2f} °C"
            )

    # --------------------------------------------------------
    # Save controller results
    # --------------------------------------------------------

    telemetry_df = pd.DataFrame(telemetry)

    output_path = "results/rule_based_controller.csv"

    telemetry_df.to_csv(
        output_path,
        index=False,
    )

    print("\nSimulation completed successfully.")
    print(f"Telemetry records: {len(telemetry_df)}")
    print(f"Results saved to: {output_path}")


if __name__ == "__main__":
    main()