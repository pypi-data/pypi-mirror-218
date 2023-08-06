from sklearn.metrics import f1_score
import numpy as np


def binary_f1(y_true: np.array, y_score: np.array, threshold: float=0.5) -> float:

    y_pred = (y_score > threshold).astype(int)
    f1 = f1_score(y_true, y_pred)

    return f1