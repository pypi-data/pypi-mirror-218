from pureml_evaluate.metrics.model.mean_absolute_error.mean_absolute_error import MeanAbsoluteError
from pureml_evaluate.metrics.model.mean_squared_error.mean_squared_error import MeanSquaredError


class Regression():
    def __init__(self):
        self.task_type = 'regression'
        self.evaluation_type = "performance"

        self.kwargs = None
        self.evaluator = None
        self.metrics = [MeanAbsoluteError(), MeanSquaredError()]

        self.scores = {}

    def compute(self):

        for m in self.metrics:
            # Adding  prediction scores to kwargs. It will be utilized my metrics needing it(roc_auc).
            try:
                self.kwargs['prediction_scores'] = self.prediction_scores

                score = m.compute(references=self.references,
                                  predictions=self.predictions, **self.kwargs)

                self.scores.update(score)

            except Exception as e:
                print("Unable to compute", m)

        return self.scores
