from config.parameters import INITIAL_TEMPERATURE
from models.thermal import ThermalModel


thermal_model = ThermalModel(
    initial_temperature=INITIAL_TEMPERATURE
)

power = 10.0  # Watts — simulation test value

print(f"Initial temperature: {thermal_model.get_temperature():.2f} °C")

for step in range(10):
    temperature = thermal_model.update(power)

    print(
        f"Step {step + 1:02d}: "
        f"{temperature:.2f} °C"
    )