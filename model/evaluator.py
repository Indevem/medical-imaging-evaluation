import typing as tp

import cv2
import joblib
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.ensemble import RandomForestRegressor, VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

from model.metrics.metrics_wrapper import Metrics


class RoundClassifier(BaseEstimator, ClassifierMixin):
    """
    Округление предсказаний модели до целых чисел.
    """
    def __init__(self, model, round_model=True):
        self.model = model
        self.round_model = round_model

    def fit(self, X, y):
        self.model.fit(X, y)
        return self

    def predict(self, X):
        pred = self.model.predict(X)
        if self.round_model:
            pred = np.round(pred, 0).astype(int)
        return pred


class Evaluator:

    def __init__(self):
        self.scaler = joblib.load('model/scaler_dump.pkl')
        self.model = joblib.load('model/model_dump.pkl')

    def _compute_metrics(self, ex, pred):
        """
        Подсчёт значения метрик для двух изображений -- экспертной и оцениваемой разметок.
        Метрики: на основе расстояний, на основе объёма множеств и на основе расположения геометрических фигур (опционально).
        """
        result = []
        num_metrics = 12

        result.append(ex.sum() / 255)
        result.append(pred.sum() / 255)

        # обработка случаев, когда на одной или обеих разметках нет выделенных областей
        if ex.sum() == 0 and pred.sum() == 0:
            return result + [0] * num_metrics
        elif ex.sum() == 0 or pred.sum() == 0:
            return result + [np.NaN] * num_metrics

        metrics = Metrics(ex, pred)
        result = metrics.compute_all()

        return result

    def _make_dataframe(self):
        """
        Создание pd.DataFrame из метрик, рассчитанных для каждой пары объектов из выборок expert и predicted.
        """
        data = []
        for i in range(len(self.expert)):
            data.append(np.array(self._compute_metrics(self.expert[i], self.predicted[i])))
        return pd.DataFrame(data)

    def fit(self, predicted: tp.List[np.ndarray], expert: tp.List[np.ndarray],
            data: tp.List[np.ndarray] = None) -> None:
        self.predicted = predicted
        self.expert = expert
        self.data = data # необходимо для пока не реализованного классификатора данных

    def evaluate(self, metrics: tp.List[str] = []) -> np.ndarray:
        X = self._make_dataframe().fillna(-1).to_numpy()
        X = self.scaler.transform(X)
        return self.model.predict(X)
