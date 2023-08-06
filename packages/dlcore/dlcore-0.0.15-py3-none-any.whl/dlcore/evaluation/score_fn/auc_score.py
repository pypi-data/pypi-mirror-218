import numpy as np
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import LabelBinarizer


def multiclass_auc(y_true: np.array, y_score: np.array):
    lb = LabelBinarizer()
    lb.fit(y_true)

    y_true = lb.transform(y_true)
    y_score = lb.transform(y_score)

    return roc_auc_score(y_true, y_score, average="macro")


def binary_auc(y_true: np.array, y_score: np.array):
    binary_auc = roc_auc_score(y_true, y_score)
    return binary_auc