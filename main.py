from models.workload import Workload


workload = Workload(
    scene_complexity=0.7,
    sensor_rate=0.5,
    object_density=0.6,
    illumination=0.8,
    deadline=0.020
)

print(workload)