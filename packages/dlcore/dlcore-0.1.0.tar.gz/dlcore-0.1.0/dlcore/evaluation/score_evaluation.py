from typing import List, Any, Set
import pandas as pd
import numpy as np

from .score_types import ClassificationType, ScoreFN
from .score_fn import binary_auc, binary_accuracy, binary_f1, binary_precision, binary_recall


from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import io

class EvaluationManager:
    
    def __init__(self, threshold: float = 0.5, classification_type: ClassificationType=ClassificationType.binary):
        
        self.scores : Set[ScoreFN] = set()
        self.threshold = threshold
        self.classification_type = classification_type
        
        
    def add(self, score_fn: ScoreFN):
        self.scores.add(score_fn)
    
    def evaluate_scores(self, y_true: Any, y_score: Any) -> pd.DataFrame:
        
        if self.classification_type == ClassificationType.binary:
            return self._evaluate_binary(y_true=y_true, y_score=y_score)
    
    
    
    def confusion_matrix(self, y_true: Any, y_score: Any) -> Image.Image:
        
        y_pred = (y_score > self.threshold).astype(int)
        cm = confusion_matrix(y_true, y_pred)

        # Plot confusion matrix
        fig, ax = plt.subplots(figsize=(10,7))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax)
        ax.set_xlabel('Predicted')
        ax.set_ylabel('Truth')

        # Save it to a BytesIO object
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        
        # Load buffer to PIL image
        img = Image.open(buf)
        return img

    def _evaluate_binary(self, y_true: Any, y_score: Any) -> pd.DataFrame:

        scores: List[float] = []
        scores_names: List[str] = []
        for score_fn in self.scores:
            if score_fn == ScoreFN.accuracy:
                score = binary_accuracy(y_true=y_true, y_score=y_score, threshold=self.threshold)
                name = ScoreFN.accuracy.name
            elif score_fn == ScoreFN.precision:
                score = binary_precision(y_true=y_true, y_score=y_score, threshold=self.threshold)
                name = ScoreFN.precision.name
            elif score_fn == ScoreFN.recall:
                score = binary_recall(y_true=y_true, y_score=y_score, threshold=self.threshold)
                name = ScoreFN.recall.name
            elif score_fn == ScoreFN.f1:
                score = binary_f1(y_true=y_true, y_score=y_score, threshold=self.threshold)       
                name = ScoreFN.f1.name
            elif score_fn == ScoreFN.auc:
                score = binary_auc(y_true=y_true, y_score=y_score)        
                name = ScoreFN.auc.name
            else:
                continue
            scores_names.append(name)
            scores.append(score)  
            
        count_0 = np.count_nonzero(y_true == 0)
        count_1 = np.count_nonzero(y_true == 1)
        
        scores_names.append("y_true==0")
        scores_names.append("y_true==1")
        
        scores.append(count_0)  
        scores.append(count_1)  
        
        return pd.DataFrame([scores], columns=scores_names)
        
# evaluation_manager = EvaluationManager()
# evaluation_manager.add(accuracy_score)
# evaluation_manager.add(auc_score)
# evaluation_manager.evaluate_scores(y_true, y_score)