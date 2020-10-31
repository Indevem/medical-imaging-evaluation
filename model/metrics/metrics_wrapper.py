from os.path import join

import cv2

from model.metrics import metrics_processor


class Metrics:
    def __init__(self, img_expert, img_model, spacing_mm=(2, 1)):
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
        return 100*(1-2*self._intersection().sum() / (self.img_expert.astype(int).sum() + self.img_model.astype(int).sum()))

    def relative_volume_difference(self):
        expert_sum = self.img_expert.astype(int).sum()
        model_sum =  self.img_model.astype(int).sum()
        return 100*(expert_sum - model_sum) / model_sum, 100*(model_sum - expert_sum) / expert_sum

    def compute_all(self):
        expert_sum = self.img_expert.astype(int).sum()
        model_sum =  self.img_model.astype(int).sum()
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



if __name__ == "__main__":
    path_expert = join('Dataset', 'Expert')
    path_model1 = join('Dataset', 'sample_1')

    img1_expert_path = join(path_expert, "00000211_019_expert.png")
    img1_model1_path = join(path_model1, '00000211_019_s1.png')
    print(img1_expert_path)

    img1_expert = cv2.imread(img1_expert_path, cv2.IMREAD_GRAYSCALE)
    img1_model1 = cv2.imread(img1_model1_path, cv2.IMREAD_GRAYSCALE)

    metrics_test = Metrics(img1_expert, img1_model1)
    print(metrics_test.average_surface_distance())
    print(metrics_test.dice_coefficient())
    print(metrics_test.dice_coefficient_tolerance())
    print(metrics_test.robust_hausdorff(95))
    print(metrics_test.surface_overlap_tolerance())
    print()
    print()
    print("testing same img")
    metrics_test = Metrics(img1_expert, img1_expert)
    print(metrics_test.average_surface_distance())
    print(metrics_test.dice_coefficient())
    print(metrics_test.dice_coefficient_tolerance())
    print(metrics_test.robust_hausdorff(95))
    print(metrics_test.surface_overlap_tolerance())
