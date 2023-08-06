from enum import Enum

class ClassificationType(Enum):
    binary = "binary"


class ScoreFN(Enum):
    auc = "auc"
    accuracy = "accuracy"
    precision = "precision"
    recall = "recall"
    f1 = "f1"