import numpy as np
from sklearn.metrics import precision_score


def binary_precision(y_true: np.array, y_score: np.array, threshold: float=0.5) -> float:

    y_pred = (y_score > threshold).astype(int)
    precision = precision_score(y_true, y_pred)

    return precision