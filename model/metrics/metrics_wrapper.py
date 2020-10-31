from os.path import join

import cv2
import numpy as np

<<<<<<< HEAD
import metrics_processor
=======
from metrics import metrics_processor
>>>>>>> c67ce97089f537ebcc52a079534ebc027051f2af


class Metrics:
    """Вычисляет различные метрики для двух заданных изображений
    """

    def __init__(self, img_expert: np.ndarray, img_model: np.ndarray, spacing_mm: tuple = (2, 1)):
        self.img_expert = img_expert.astype('bool')
        self.img_model = img_model.astype('bool')
        self.spacing_mm = spacing_mm

        self.surface_dist = metrics_processor.compute_surface_distances(self.img_expert, self.img_model, spacing_mm)

    def average_surface_distance(self):
        return metrics_processor.compute_average_surface_distance(self.surface_dist)

    def dice_coefficient(self):
        return metrics_processor.compute_dice_coefficient(self.img_expert, self.img_model)

    def robust_hausdorff(self, percent: float):
        return metrics_processor.compute_robust_hausdorff(self.surface_dist, percent)

    def surface_overlap_tolerance(self, tolerance_mm=1):
        return metrics_processor.compute_surface_overlap_at_tolerance(self.surface_dist, tolerance_mm)

    def dice_coefficient_tolerance(self, tolerance_mm=1):
        return metrics_processor.compute_surface_dice_at_tolerance(self.surface_dist, tolerance_mm)

    def _intersection(self):
        return (self.img_model ^ self.img_expert).astype(int)

    def volume_overlap(self):
        return 100 * (1 - 2 * self._intersection().sum() / (
                self.img_expert.astype(int).sum() + self.img_model.astype(int).sum()))

    def relative_volume_difference(self):
        expert_sum = self.img_expert.astype(int).sum()
        model_sum = self.img_model.astype(int).sum()
        return 100 * (expert_sum - model_sum) / model_sum, 100 * (model_sum - expert_sum) / expert_sum

    def compute_all(self):
        expert_sum = self.img_expert.astype(int).sum()
        model_sum = self.img_model.astype(int).sum()

        asd = self.average_surface_distance()
        rvd = self.relative_volume_difference()
        sot = self.surface_overlap_tolerance()

        metrics = [
            asd[0], asd[1], (asd[0] * expert_sum + asd[1] * model_sum) / (expert_sum + model_sum),
            self.dice_coefficient(),
            self.robust_hausdorff(0),
            self.robust_hausdorff(50),
            self.robust_hausdorff(100),
            sot[0], sot[1],
            self.dice_coefficient_tolerance(),
            self.dice_coefficient_tolerance(0.5),
            self.volume_overlap(),
            rvd[0], rvd[1]
        ]
        return metrics
