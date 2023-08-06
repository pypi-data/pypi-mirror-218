from dataclasses import dataclass
from sklearn.metrics import accuracy_score as _accuracy_score
from sklearn.metrics import roc_auc_score as _roc_auc_score
from typing import Any


@dataclass
class Metric:
    name: str
    value: float


def auc_score(y_true: list[Any], y_pred: list[Any], **kwargs: Any) -> Metric:

    if len(set(y_true)) > 1:
        value = float(_roc_auc_score(y_true, y_pred))
    else:
        value = None
    return Metric(name="auc", value=value)


def accuracy_score(y_true: list[Any], y_score: list[Any], **kwargs: Any) -> Metric:

    if len(set(y_true)) > 1:
        value = float(_accuracy_score(y_true, y_score))
    else:
        value = None
    return Metric(name="accuracy", value=value)
