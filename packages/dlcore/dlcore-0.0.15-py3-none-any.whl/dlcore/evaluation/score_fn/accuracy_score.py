from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
import numpy as np


def binary_accuracy(y_true: np.array, y_score: np.array, threshold: float=0.5):

    y_pred = (y_score > threshold).astype(int)
    accuracy = accuracy_score(y_true, y_pred)

    return accuracy