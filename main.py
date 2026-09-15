from models.workload import generate_workload


total_steps = 20

for step in range(total_steps):
    workload = generate_workload(step, total_steps)

    print(
        f"Step {step:02d} | "
        f"Complexity={workload.scene_complexity:.1f} | "
        f"Sensor Rate={workload.sensor_rate:.1f} | "
        f"Objects={workload.object_density:.1f} | "
        f"Deadline={workload.deadline * 1000:.0f} ms"
    )