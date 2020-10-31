from dataclasses import dataclass
from typing import Callable, Dict, List

import numpy as np
import pandas as pd
from scipy.spatial import distance

FILENAME_COL = 'file_name'
USERNAME_COL = ' user_name'
X_COL = ' xcenter'
Y_COL = ' ycenter'
WIDTH_COL = ' rhorizontal'
HEIGHT_COL = ' rvertical'
SHAPE_COL = ' shape'
FILE_FORMAT = '.png'


@dataclass
class Shape:
    x: float
    y: float

    # actually, half a width/height
    width: float
    height: float

    shape: str

    @property
    def coordinates(self):
        return self.x, self.y

    @property
    def sizes(self):
        return self.width, self.height

    # naive, assumes that every shape is rectangle
    @property
    def area(self):
        return self.width * self.height * 4


# for each shape on the first image, calculates distance to the nearest shape on the other image
# then aggregates it
def get_aggregated_min_center_distance(shapes_from: List[Shape], shapes_to: List[Shape],
                                       distance_function: Callable = distance.euclidean,
                                       aggregation_function: Callable = np.mean) -> float:
    if len(shapes_from) == 0 and len(shapes_to) == 0:
        return 0
    if len(shapes_from) == 0 or len(shapes_to) == 0:
        return np.NaN

    return aggregation_function(
        [min(distance_function(shape_from.coordinates, shape_to.coordinates) for shape_to in shapes_to)
         for shape_from in shapes_from])


def get_rectangle_area_ratio(shapes_1: List[Shape], shapes_2: List[Shape]) -> float:
    if len(shapes_1) == 0 and len(shapes_2) == 0:
        return 0
    if len(shapes_1) == 0 or len(shapes_2) == 0:
        return np.NaN

    return sum(i.area for i in shapes_1) / sum(i.area for i in shapes_2)


def get_shapes_count_ratio(shapes_1: List[Shape], shapes_2: List[Shape]) -> float:
    if len(shapes_1) == 0 and len(shapes_2) == 0:
        return 0
    if len(shapes_1) == 0 or len(shapes_2) == 0:
        return np.NaN

    return len(shapes_1) / len(shapes_2)


class TableMetricsCalculator:
    def __init__(self, path):
        self.rect_data = pd.read_csv(path)

    def calc_table_metrics_for_image_pair(self, image_name: str, user_name_1: str,
                                          user_name_2: str) -> Dict[str, float]:
        image_name = image_name.strip(FILE_FORMAT)

        data = self.rect_data[self.rect_data[FILENAME_COL] == image_name]
        first_data = data[data[USERNAME_COL] == user_name_1]
        second_data = data[data[USERNAME_COL] == user_name_2]

        first_shapes = [Shape(*i[3:-1]) for i in first_data.itertuples()]
        second_shapes = [Shape(*i[3:-1]) for i in second_data.itertuples()]

        metrics = {}

        for aggregation_function in (np.median, np.mean, np.min, np.max):
            prefix = '{}_min_center_distance_'.format(aggregation_function.__name__)
            metrics.update({
                prefix + '1to2_L2': get_aggregated_min_center_distance(first_shapes, second_shapes,
                                                                       aggregation_function=aggregation_function),
                prefix + '2to1_L2': get_aggregated_min_center_distance(second_shapes, first_shapes,
                                                                       aggregation_function=aggregation_function),
                prefix + '1to2_L1': get_aggregated_min_center_distance(first_shapes, second_shapes,
                                                                       distance_function=distance.cityblock,
                                                                       aggregation_function=aggregation_function),
                prefix + '2to1_L1': get_aggregated_min_center_distance(second_shapes, first_shapes,
                                                                       distance_function=distance.cityblock,
                                                                       aggregation_function=aggregation_function),
            })

        #     metrics['shape_count_1'] = len(first_shapes)
        #     metrics['shape_count_2'] = len(second_shapes)
        if len(first_shapes) == 0 and len(second_shapes) == 0:
            metrics['shape_count_ratio'] = 1
        elif len(second_shapes) == 0:
            metrics['shape_count_ratio'] = np.NaN
        else:
            metrics['shape_count_ratio'] = len(first_shapes) / len(second_shapes)
        metrics['rectangle_area_ratio'] = get_rectangle_area_ratio(first_shapes, second_shapes)
        return metrics

    def get_coordinates_of_shapes_for_image(self, image_name: str, user_name: str) -> List[Dict[str, float]]:
        image_name = image_name.strip(FILE_FORMAT)

        data = self.rect_data[self.rect_data[FILENAME_COL] == image_name]
        data = data[data[USERNAME_COL] == user_name]

        shapes = [Shape(*i[3:-1]) for i in data.itertuples()]

        return [i.__dict__ for i in shapes]
