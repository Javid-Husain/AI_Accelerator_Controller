from models.accelerator import AcceleratorConfig
from models.workload import Workload


workload = Workload(
    scene_complexity=0.7,
    sensor_rate=0.5,
    object_density=0.6,
    illumination=0.8,
    deadline=0.020
)


for frequency_level in range(4):
    config = AcceleratorConfig(
        frequency_level=frequency_level,
        precision="FP16",
        sparsity=0.20
    )

    latency = config.calculate_latency(workload)

    print(
        f"Frequency level {frequency_level}: "
        f"{latency * 1000:.2f} ms"
    )