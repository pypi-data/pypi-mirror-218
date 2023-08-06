from sklearn.metrics import log_loss
from pureml_evaluate.metrics.metric_base import MetricBase
from typing import Any

class LogLoss(MetricBase):

    name = 'log_loss'
    input_type = 'float'
    output_type: Any = None
    kwargs = { }
        

    def parse_data(self, data):
        
        return data



    def compute(self, references, predictions=None, prediction_scores=None, sample_weight=None,
                normalize=True, labels=None, **kwargs):
        
        if prediction_scores is None and predictions is None:
            score = None
        elif predictions is None:
            score = log_loss(y_true=references, y_pred=prediction_scores, sample_weight=sample_weight,
                                 normalize=normalize, labels=labels)
            score = float(score)
        elif prediction_scores is None:
            score = log_loss(y_true=references, y_pred=predictions,  sample_weight=sample_weight,
                                normalize=normalize, labels=labels)
            score = float(score)
        
        score = {
            self.name : score
            }
 

        return score