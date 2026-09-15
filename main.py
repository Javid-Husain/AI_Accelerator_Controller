from models.accelerator import AcceleratorConfig
from models.workload import Workload


workload = Workload(
    scene_complexity=0.7,
    sensor_rate=0.5,
    object_density=0.6,
    illumination=0.8,
    deadline=0.020,
)

config = AcceleratorConfig(
    frequency_level=3,
    precision="FP16",
    sparsity=0.20,
)

latency = config.calculate_latency(workload)
power = config.calculate_power(workload)
energy = config.calculate_energy(workload)
accuracy = config.calculate_accuracy(workload)

print(f"Latency : {latency * 1000:.2f} ms")
print(f"Power   : {power:.2f} W")
print(f"Energy  : {energy * 1000:.2f} mJ")
print(f"Accuracy: {accuracy * 100:.2f}%")