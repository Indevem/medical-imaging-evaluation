# %%
import sys

from evaluator import Evaluator
from PyQt5.QtCore import QThread, pyqtSignal

sys.path.append('..\\model')

# %%
class ModelResponse(QThread):
    """Класс является оболочкой для QThread.
    Методы класса реализуют обращение приложения
    к обученной модели и получение результата.
    Объекты данного класса передаются главным окном
    для выполнения в отдельный поток.
    
    """
    TR = pyqtSignal(dict, name="throw_results")
    
    def __init__(self, list1, list2):
        """Конструктор класса. 
        
        """
        QThread.__init__(self)
        self.list1 = list1
        self.list2 = list2
    
    def __del__(self):
        self.wait()

    def run(self):
        """В функции создаётся объект 
        модели. Данные передаются в модель.
        Модель возвращает результат
        
        """
        evaluator = Evaluator()   
        evaluator.fit(self.list1, self.list2)
        results = evaluator.evaluate()
        self.throw_results.emit(results)

# %%
