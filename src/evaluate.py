"""Stage 4 - evaluate on the test set; write metrics.json and confusion_matrix.png."""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # no display needed
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix
from tensorflow import keras

DATA_DIR = Path("data/processed")
CLASS_NAMES = ["T-shirt/top", "Trouser", "Pullover", "Dress", "Coat",
               "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot"]


def main():
    model = keras.models.load_model("models/model.h5")
    x_test = np.load(DATA_DIR / "x_test.npy")
    y_test = np.load(DATA_DIR / "y_test.npy")

    loss, acc = model.evaluate(x_test, y_test, verbose=0)
    y_pred = np.argmax(model.predict(x_test, verbose=0), axis=1)

    cm = confusion_matrix(y_test, y_pred)
    fig, ax = plt.subplots(figsize=(9, 9))
    ConfusionMatrixDisplay(cm, display_labels=CLASS_NAMES).plot(
        ax=ax, xticks_rotation=45, colorbar=False
    )
    fig.tight_layout()
    fig.savefig("confusion_matrix.png", dpi=150)

    with open("metrics.json", "w") as f:
        json.dump({"test_loss": float(loss), "test_accuracy": float(acc)}, f, indent=2)

    print(f"test_loss={loss:.4f}  test_accuracy={acc:.4f}")


if __name__ == "__main__":
    main()
