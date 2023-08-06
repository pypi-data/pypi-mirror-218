import numpy as np
from sklearn.metrics import recall_score


def binary_recall(y_true: np.array, y_score: np.array, threshold: float=0.5) -> float:

    y_pred = (y_score > threshold).astype(int)
    recall = recall_score(y_true, y_pred)

    return recall

