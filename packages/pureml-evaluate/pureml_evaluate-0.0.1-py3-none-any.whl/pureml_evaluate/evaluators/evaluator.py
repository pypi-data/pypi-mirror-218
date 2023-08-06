from pydantic import BaseModel
from .grade import Grader
from typing import Any, Union
from importlib import import_module
import numpy as np
from collections import defaultdict


class Evaluator(BaseModel):
    y_true: Any
    y_pred: Any
    y_pred_scores: Any = None
    sensitive_features: Union[None, Any]

    evaluators: Union[list[str], str]
    grader: list[Grader] = []
    dataset: Any = None

    class Config:
        validate_assignment = True
        arbitrary_types_allowed = True

    def load_graders(self):
        if type(self.evaluators) == str:
            self.grader.append(Grader(task_type=self.evaluators))
        elif type(self.evaluators) == list:
            for e in self.evaluators:
                self.grader.append(Grader(task_type=e))
        else:
            print("Unknown Evaluators: ", self.evaluators)

    def load(self):
        self.load_graders()

    def evaluate(self):

        values_all = defaultdict(dict)

        for g in self.grader:
            grader_type = g.task_grader.evaluation_type

            values = g.compute(
                references=self.y_true, predictions=self.y_pred,
                sensitive_features=self.sensitive_features, prediction_scores=self.y_pred_scores
            )

            values_all[grader_type].update(values)

        values_all = dict(values_all)

        return values_all

    def evaluate_subsets(self):
        if self.sensitive_features is not None:
            subsets = self.give_subsets()

            values_subsets_all = {}

            for subset in subsets:
                values_all = defaultdict(dict)

                key = subset['key']
                y_true = subset['y_true']
                y_pred = subset['y_pred']
                sensitive_features = subset['sensitive_features']
                y_pred_scores = subset['y_pred_scores']

                for g in self.grader:
                    grader_type = g.task_grader.evaluation_type

                    values = g.compute(
                        references=y_true, predictions=y_pred,
                        sensitive_features=sensitive_features, prediction_scores=y_pred_scores
                    )

                    values_all[grader_type].update(values)

                values_all = dict(values_all)
                values_subsets_all[key] = values_all

        return values_subsets_all

    def give_subsets(self):
        subsets = []
        unique_values = np.unique(self.sensitive_features)

        for value in unique_values:
            ind = np.where(self.sensitive_features == value)

            sub_dict = {
                "key": value,
                "y_true": self.y_true[ind],
                "y_pred": self.y_pred[ind],
                "sensitive_features": self.sensitive_features[ind],
            }

            if self.y_pred_scores is not None:
                sub_dict.update({"y_pred_scores": self.y_pred_scores[ind]})
            else:
                sub_dict.update({"y_pred_scores": self.y_pred_scores})

            subsets.append(sub_dict)

        return subsets


def eval(y_true, y_pred, sensitive_features, evaluators, y_pred_scores=None):
    evaluator = Evaluator(
        y_true=y_true, y_pred=y_pred, sensitive_features=sensitive_features, evaluators=evaluators, y_pred_scores=y_pred_scores
    )

    evaluator.load()

    values_all = evaluator.evaluate()
    values_subset_all = evaluator.evaluate_subsets()

    values = {
        "complete": values_all,
        "subsets": values_subset_all
    }

    return values
