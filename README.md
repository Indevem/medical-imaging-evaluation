## Решение задачи "Разработка инструмента оценки качества работы алгоритмов разметки медицинских изображений" команды trying to pretend

### Структура проекта
- Папка application: итоговое приложение с графическим интерфейсом.
- Папка model: код решения и пример использования.

### Основные технологии
- Python 3
- Qt
- PyTorch

### Руководство по применению приложения

### Руководство по использованию библиотеки
Создание объекта модели: `model = Evaluator()`.
Обучение модели: `model.fit(predicted, expert)`, где `predicted` -- оцениваемая разметка, `expert` -- правильная разметка, ожидаемые тип данных: `np.ndarray`.
Получение значения метрик для всех объектов выборки: `model.evaluate()`.

## О решении
Для поиска различий между автоматической и экспертной разметками применяются метрики:

Алгоритм оценки разметки:

### Литература
- SergioVera, DeboraGil и др. “Medial structure generation for registration of anatomical structures”, Skeletonization, Chapter 11 (2017)
- Ramprasaath R. Selvaraju и др. “Grad-CAM: Visual Explanations from Deep Networks via Gradient-based Localization”, IEEE (2017).
- R. Padilla, S. L. Netto и E. A. B. da Silva, "A Survey on Performance Metrics for Object-Detection Algorithms", IWSSIP (2020)
Dinu Dragan, и Dragan Vojo Ivetic, “Region Marking Software Tool for Medical Images”, eTELEMED (2012)
- Реализация метрик https://github.com/deepmind/surface-distance
