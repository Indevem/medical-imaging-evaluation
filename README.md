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
- `test_predictions.csv` оценка тестовых данных алгоритмом.

### Основные технологии
- Модель: Python 3 + библиотеки numpy, pandas, scikit-learn
- Клиент: PyQt

### Руководство по использованию библиотеки
Создание объекта модели: `model = Evaluator()`.

Отправка оцениваемых данных: `model.fit(expert, predicted)`, где `predicted` - оцениваемая разметка, `expert` - правильная разметка (список grayscale изображений типа `np.ndarray`).

Получение значения метрик для всех объектов выборки: `model.evaluate()`.

## О решении
Для поиска различий между автоматической и экспертной разметками применяются **метрики**:
- Standard surface distance
<p align="center">
  <img src="https://latex.codecogs.com/svg.latex?AvD=\frac{1}{Y}\sum_{y\in%20Y}D_X(y)" /> 
</p>

- Symmetric surface distance
<p align="center">
  <img src="https://latex.codecogs.com/svg.latex?AvSD=\frac{1}{|X|+|Y|}\left(\sum_{x\in%20X}D_Y(x)+\sum_{y\in%20Y}D_X(y)\right)=\frac{|Y|AvD_Y(X,%20Y)+|X|AvD(Y,%20X)}{|X|+|Y|}" /> 
</p>

- Volume overlap error
<p align="center">
  <img src="https://latex.codecogs.com/svg.latex?VOE=100\times\left(1-\frac{|X\cap%20Y|}{|X|+|Y|}\right)" /> 
</p>

- Relative volume difference
<p align="center">
  <img src="https://latex.codecogs.com/svg.latex?RVD%20=%20100\times\frac{|X|-|Y|}{|Y|}" /> 
</p>

- Dice coefficient
<p align="center">
  <img src="https://latex.codecogs.com/svg.latex?DICE%20=%20\frac{2|X\cap%20Y|}{|X|+|Y|}" /> 
</p>

- Hausdorff distance
<p align="center">
  <img src="https://latex.codecogs.com/svg.latex?D=\max\{\max_{x\in%20X}\min_{y\in%20Y}d(x,%20y),%20\max_{y\in%20Y}\min_{x\in%20X}d(x,%20y)\}" /> 
</p>

и их модификации (surface dice at tolerance, surface overlap at tolerance с различными коэффициентами).

**Алгоритм оценки разметки**
1. Составление признаков из расстояний между разметкой эксперта и оцениваемой разметкой, заполнение пропусков, возникших при делении на 0.
2. Применение StandardScaler.
3. Получение оценки как взвешенного среднего по результату работы случайного леса, SVC с rbf ядром и логистической регрессии.

**Алгоритм выбора модели и обучения**
1. Разделение выборки на обучающую и валидационную.
2. Сравнение моделей машинного обучения среди SVC (RBF, linear, sigmoid), GaussianNB, SVR, KNeighborsRegressor, KNeighborsClassifier, RandomForestClassifier, RandomForestRegressor (MAE, MSE), LogisticRegression из библиотеки sklearn с помощью бутстрепа на 100-500 случайно выбранных подмножествах обучающей выборки.
3. Выбор трёх лучших моделей, подбор их гиперпараметров, построение VotingClassifier на них, выбор весов голосования.
4. Обучение итоговой модели на всей выборке с известными метками.

Подробное описание, результаты тестов и графики доступны в файле `solution.ipynb`.

### TODO
1. Кластеризация. Не все способы визуального выделения аномалий будут корректно обрабатываться простой моделью на метриках: из-за неравномерного распределения выделенных пикселей в области качество оценки может существенно упасть. Решить эту проблему может предварительная кластеризация пикселей.
2. Небинарные маски. Реализация решения для масок, состоящих из более, чем двух значений, возможно с помощью добавления веса каждому пикселю.
3. Обобщение на 3D.
4. Атласы. Использование цифровых атласов тела позволит исключить случайно затронутые выделением эксперта области и повысить точность оценки.

### Литература
- SergioVera, DeboraGil и др. “Medial structure generation for registration of anatomical structures”, Skeletonization, Chapter 11 (2017)
- Ramprasaath R. Selvaraju и др. “Grad-CAM: Visual Explanations from Deep Networks via Gradient-based Localization”, IEEE (2017).
- R. Padilla, S. L. Netto и E. A. B. da Silva, "A Survey on Performance Metrics for Object-Detection Algorithms", IWSSIP (2020)
- Dinu Dragan, и Dragan Vojo Ivetic, “Region Marking Software Tool for Medical Images”, eTELEMED (2012)
- Реализация метрик https://github.com/deepmind/surface-distance
