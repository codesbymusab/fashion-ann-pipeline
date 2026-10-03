"""Stage 3 - build and train the ANN; save models/model.h5 and models/history.csv."""
from pathlib import Path

import numpy as np
import yaml
from tensorflow import keras

DATA_DIR = Path("data/processed")
MODEL_DIR = Path("models")


def load_params():
    with open("params.yaml") as f:
        return yaml.safe_load(f)["train"]


def build_model(units, dropout_rate, learning_rate):
    model = keras.Sequential([
        keras.Input(shape=(28, 28)),
        keras.layers.Flatten(),
        keras.layers.Dense(units, activation="relu"),
        keras.layers.Dropout(dropout_rate),
        keras.layers.Dense(10, activation="softmax"),
    ])
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model


def main():
    params = load_params()
    keras.utils.set_random_seed(params["seed"])

    x_train = np.load(DATA_DIR / "x_train.npy")
    y_train = np.load(DATA_DIR / "y_train.npy")
    x_val = np.load(DATA_DIR / "x_val.npy")
    y_val = np.load(DATA_DIR / "y_val.npy")

    model = build_model(params["dense_units"], params["dropout_rate"], params["learning_rate"])

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    model.fit(
        x_train, y_train,
        validation_data=(x_val, y_val),
        epochs=params["epochs"],
        batch_size=params["batch_size"],
        callbacks=[keras.callbacks.CSVLogger(str(MODEL_DIR / "history.csv"))],
    )
    model.save(MODEL_DIR / "model.h5")
    print(f"Saved {MODEL_DIR / 'model.h5'} and {MODEL_DIR / 'history.csv'}")


if __name__ == "__main__":
    main()
