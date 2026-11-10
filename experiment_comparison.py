
import pandas as pd


def compare_experiments(df_a, df_b):
    if df_a.empty or df_b.empty:
        raise ValueError("Both experiments need valid metrics.")

    a = df_a.iloc[-1]
    b = df_b.iloc[-1]

    comparison = {
        "experiment_a": {
            "train_accuracy": float(a["train_acc"]),
            "val_accuracy": float(a["val_acc"]),
            "train_loss": float(a["train_loss"]),
            "val_loss": float(a["val_loss"])
        },
        "experiment_b": {
            "train_accuracy": float(b["train_acc"]),
            "val_accuracy": float(b["val_acc"]),
            "train_loss": float(b["train_loss"]),
            "val_loss": float(b["val_loss"])
        },
        "improvement": {
            "val_accuracy_change": float(
                b["val_acc"] - a["val_acc"]
            ),
            "val_loss_change": float(
                b["val_loss"] - a["val_loss"]
            )
        }
    }

    return comparison
