from models.accelerator import AcceleratorConfig


config = AcceleratorConfig(
    frequency_level=3,
    precision="FP16",
    sparsity=0.20
)

print(config)