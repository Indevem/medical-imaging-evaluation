import typing as tp

import numpy as np


class Evaluator:

    #metrics = {
     #   'standard_avg': standard_distance_avg, 'standard_max': standard_distance_max,
     #   'symmetric_avg': symmetric_distance_avg, 'symmetric_max': symmetric_distance_max,
     #   'voe': volume_overlap_error, 'rvd': relative_volume_difference,
     #   'dice': dice_coefficient, 'hausdorff': hausdorff_distance
    #}

    def __init__(self):
        pass

    def _evaluate_3d(self) -> tp.Dict[str, np.ndarray]:
        pass

    def _evaluate_2d(self) -> tp.Dict[str, np.ndarray]:
        pass

    def fit(self, predicted: tp.List[np.ndarray], expert: tp.List[np.ndarray],
                 data: tp.List[np.ndarray] = None) -> None:
        pass

    def evaluate(self, metrics: tp.List[str] = []):# -> tp.List[int]:

        #return {'metric1': np.zeros(len(predicted)), 'metric2': np.array(list(range(len(predicted))))}
        
        return np.zeros(4)
