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

        # Print every 100 steps (approximately once per second)
        if step % 100 == 0:
            print(
                f"Time: {step * DT:5.2f} s | "
                f"Workload: {workload.scene_complexity:.2f} | "
                f"Latency: {latency * 1000:6.2f} ms | "
                f"Power: {power:5.2f} W | "
                f"Energy: {energy * 1000:6.2f} mJ | "
                f"Accuracy: {accuracy * 100:6.2f}% | "
                f"Temp: {temperature:6.2f} °C"
            )


if __name__ == "__main__":
    main()