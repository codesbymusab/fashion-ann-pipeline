"""Tiny helper: print the shapes of the processed arrays."""
import numpy as np

for name in ["x_train", "y_train", "x_val", "y_val", "x_test", "y_test"]:
    print(name, np.load(f"data/processed/{name}.npy").shape)
