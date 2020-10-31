## Оценка качества разметки медицинских данных
Решение задачи "Разработка инструмента оценки качества работы алгоритмов разметки медицинских изображений" хакатона "Лидеры Цифровой Трансформации" команды trying to pretend.

### Структура проекта
- Папка model: код решения и пример использования.
  - `evaluator.py` модуль с обученной моделью.
  - `example.ipynb`: пример использования модуля `evaluator.py` для оценки разметки датасета.
  - `clean-solution.ipynb` финальное обучение модели и сохранение файлов.
  - `solution.ipynb` код и описание методов, применённых в процессе поиска лучшей модели и подбора гиперпараметров, содержит также не вошедшие в финальную версию, но потенциально полезные идеи.
  - папка metrics: реализация метрик для сравнения двух изображений.
- Папка application: клиент с графическим интерфейсом.

### Основные технологии
- Python 3 + библиотеки numpy, pandas, scikit-learn
- PyQt

### Руководство по использованию библиотеки
Создание объекта модели: `model = Evaluator()`.
Обучение модели: `model.fit(predicted, expert)`, где `predicted` -- оцениваемая разметка, `expert` -- правильная разметка, ожидаемые тип данных: `np.ndarray`.
Получение значения метрик для всех объектов выборки: `model.evaluate()`.

## О решении
Для поиска различий между автоматической и экспертной разметками применяются метрики:
- Standard surface distance
<p align="center">
  <img src="https://latex.codecogs.com/svg.latex?AvD=\frac{1}{Y}\sum_{y\in%20Y}D_X(y)" /> 
</p>

- Symmetric surface distance
```math
AvSD=\frac{1}{|X|+|Y|}\left(\sum_{x\in X}D_Y(x)+\sum_{y\in Y}D_X(y)\right)=\frac{|Y|AvD_Y(X, Y)+|X|AvD(Y, X)}{|X|+|Y|}
```
- Volume overlap error
```math
VOE=100\times\left(1-\frac{|X\cap Y|}{|X|+|Y|}\right)
```
- Relative volume difference
```math
RVD = 100\times{|X|-|Y|}{|Y|}
```
- Dice coefficient
```math
DICE = \frac{2|X\cap Y|}{|X|+|Y|}
```
- Метрика Хаусдорфа

и их модификации.


Алгоритм оценки разметки:

### Литература
- SergioVera, DeboraGil и др. “Medial structure generation for registration of anatomical structures”, Skeletonization, Chapter 11 (2017)
- Ramprasaath R. Selvaraju и др. “Grad-CAM: Visual Explanations from Deep Networks via Gradient-based Localization”, IEEE (2017).
- R. Padilla, S. L. Netto и E. A. B. da Silva, "A Survey on Performance Metrics for Object-Detection Algorithms", IWSSIP (2020)
Dinu Dragan, и Dragan Vojo Ivetic, “Region Marking Software Tool for Medical Images”, eTELEMED (2012)
- Реализация метрик https://github.com/deepmind/surface-distance
