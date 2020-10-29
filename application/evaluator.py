import numpy as np
import typing as tp

class Evaluator:

    def __init__(self):
        pass

    def _evaluate_3d(self, predicted: tp.List[np.ndarray], expert: tp.List[np.ndarray]) -> tp.Dict[str, np.ndarray]:
        pass

    def _evaluate_2d(self, predicted: tp.List[np.ndarray], expert: tp.List[np.ndarray]) -> tp.Dict[str, np.ndarray]:
        pass

    def evaluate(self, predicted: tp.List[np.ndarray], expert: tp.List[np.ndarray],
                 data: tp.List[np.ndarray] = None) -> tp.Dict[str, np.ndarray]:

        return {'metric1': np.zeros(len(predicted)), 'metric2': np.array(list(range(len(predicted))))}
