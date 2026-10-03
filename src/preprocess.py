"""Stage 2 - normalize pixels, carve out a validation split, save to data/processed/."""
from pathlib import Path

import numpy as np
import yaml
from sklearn.model_selection import train_test_split

RAW_DIR = Path("data/raw")
OUT_DIR = Path("data/processed")


def load_params():
    with open("params.yaml") as f:
        return yaml.safe_load(f)["preprocess"]


def normalize(x):
    """Main approach: scale to [0, 1], then center to [-0.5, 0.5]."""
    return x.astype("float32") / 255.0 - 0.5


def main():
    params = load_params()

    x_train = np.load(RAW_DIR / "x_train.npy")
    y_train = np.load(RAW_DIR / "y_train.npy")
    x_test = np.load(RAW_DIR / "x_test.npy")
    y_test = np.load(RAW_DIR / "y_test.npy")

    x_train, x_test = normalize(x_train), normalize(x_test)

    x_tr, x_val, y_tr, y_val = train_test_split(
        x_train,
        y_train,
        test_size=params["test_size"],
        random_state=params["seed"],
        stratify=y_train,
    )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for name, arr in {
        "x_train": x_tr, "y_train": y_tr,
        "x_val": x_val, "y_val": y_val,
        "x_test": x_test, "y_test": y_test,
    }.items():
        np.save(OUT_DIR / f"{name}.npy", arr)

    print(f"Saved processed data to {OUT_DIR}: train={x_tr.shape}, val={x_val.shape}, test={x_test.shape}")
    print(f"[debug] val fraction = {len(x_val) / len(x_train):.2%}")


if __name__ == "__main__":
    main()
