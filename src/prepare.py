"""Stage 1 - download Fashion-MNIST and save the raw arrays to data/raw/."""
from pathlib import Path

import numpy as np
from tensorflow import keras

RAW_DIR = Path("data/raw")


def main():
    (x_train, y_train), (x_test, y_test) = keras.datasets.fashion_mnist.load_data()

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    # Plain .npy files (not .npz) so the bytes are identical on every run;
    # that keeps DVC hashes stable and lets unchanged stages be skipped.
    np.save(RAW_DIR / "x_train.npy", x_train)
    np.save(RAW_DIR / "y_train.npy", y_train)
    np.save(RAW_DIR / "x_test.npy", x_test)
    np.save(RAW_DIR / "y_test.npy", y_test)

    print(f"Saved raw data to {RAW_DIR}: train={x_train.shape}, test={x_test.shape}")


if __name__ == "__main__":
    main()
