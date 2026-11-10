import re
import pandas as pd

def parse_training_log(log_content):
    pattern = (
        r"Epoch\s+(\d+)/\d+\s+-\s+"
        r"train_loss:\s*([\d.]+)\s+-\s+"
        r"val_loss:\s*([\d.]+)\s+-\s+"
        r"train_acc:\s*([\d.]+)%\s+-\s+"
        r"val_acc:\s*([\d.]+)%"
    )

    matches = re.findall(pattern, log_content)

    if not matches:
        return pd.DataFrame()

    df = pd.DataFrame(
        matches,
        columns=[
            "epoch",
            "train_loss",
            "val_loss",
            "train_acc",
            "val_acc"
        ]
    )

    return df.apply(pd.to_numeric)