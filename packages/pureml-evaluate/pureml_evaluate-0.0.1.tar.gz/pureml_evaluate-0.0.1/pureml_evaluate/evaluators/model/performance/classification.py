from pureml_evaluate.metrics.model.accuracy.accuracy import Accuracy
from pureml_evaluate.metrics.model.precision.precision import Precision
from pureml_evaluate.metrics.model.recall.recall import Recall
from pureml_evaluate.metrics.model.f1_score.f1_score import F1
from pureml_evaluate.metrics.model.confusion_matrix.confusion_matrix import ConfusionMatrix


class Classification:
    def __init__(self):
        self.task_type = "classification"
        self.evaluation_type = "performance"

        self.kwargs = None

        self.references = None
        self.predictions = None
        self.prediction_scores = None

        self.label_type = "binary"

        self.metrics = [
            Accuracy(),
            Precision(),
            Recall(),
            F1(),
            ConfusionMatrix(),
        ]  # , ROC_AUC()]
        self.scores = {}

    def compute(self):
        self.setup()

        for m in self.metrics:
            # Adding  prediction scores to kwargs. It will be utilized my metrics needing it(roc_auc).

            try:

                self.kwargs["prediction_scores"] = self.prediction_scores
                score = m.compute(
                    references=self.references, predictions=self.predictions, **self.kwargs
                )

                self.scores.update(score)
            except Exception as e:
                print("Unable to compute", m)

        return self.scores

    def setup(self):
        self.is_multiclass()
        self.setup_kwargs()

    def get_predictions(self):
        pass

    def is_multiclass(self):
        # print(self.predictions)
        # print(self.references)
        if self.predictions is not None:
            labels_all = set(self.references).union(self.predictions)
            if len(labels_all) > 2:
                self.label_type = "multilabel"

    def setup_kwargs(self):
        if "average" not in self.kwargs:
            if self.label_type == "multilabel":
                self.kwargs["average"] = "micro"
