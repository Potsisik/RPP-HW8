import numpy as np

class Math_Model():
    def __init__(self): #зачем нам конструктор?
        self.a = 70 #пока просто пример, с рандомными значениями
        self.b = 70
    def set_values(self, parametrs: dict): #устанавливаем значения из формочки
        self.a = parametrs["a"] 
        self.b = parametrs["b"] 
        self.x = parametrs["x"] 
        self.y = parametrs["y"] 
        self.n = parametrs["n"]
        self.time = parametrs["time"] 
        self.lym = parametrs["lym"] #длина волны

        #овал
        #потом узнать как понимать какая вкладка выбрана
        self.r1 = parametrs["r1"] 
        self.r2 = parametrs["r2"] 
        self.thickness = parametrs["thickness"]

    #
    # перенести сюда функции овала, круга и прямоугольника
    # при надобности их изменить
    #

    def calculate(self): #есть идея сначала привести полученные данные к нормальному виду
        res = {'integral':{}, 'graphs':{}} #возвращаем словарь
        #res {int{...}, grf{x{..}, y{y1, y2, y3...}} - структура
        integral = res['integral'] #получаю внутренние словари для удобства
        graphs = res['graphs']

        #
        # здесь нужно вызвать функцию овала или прямоугольника
        #

        integral['res_1'] = self.a * self.b #для примера
        
        return res