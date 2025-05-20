import numpy as np
import fdtd
#from ellipse import ellipse

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
        self.lym = parametrs["lym"] * 10 **-9 #длина волны
        self.thickness = parametrs["thickness"]

        self.figure = parametrs["figure"]

        if self.figure == 1:
            #овал
            self.r1 = parametrs["r1"] 
            self.r2 = parametrs["r2"]
        elif self.figure == 0:
            #круг
            self.r = parametrs["r"] 
        else:
            #квадрат
            self.side_length = parametrs["side_length"]
                

        self.c = 3*10**8 #скорость света

    def ellipse(self, x1, x2, y1, y2, r1, r2):
        fdtd.set_backend("numpy")
        grid = fdtd.Grid(shape=(self.a, self.b, 1), grid_spacing=0.0000001, permittivity=1)

        # Сетка
        grid[y1:y2, x1, 0] = fdtd.LineSource(period=self.lym / self.c, name="source")
        grid[y1:y2, x2, 0] = fdtd.LineDetector(name="detector")

        grid[0:self.thickness, :, :] = fdtd.PML(name="pml_xlow")
        grid[-self.thickness:, :, :] = fdtd.PML(name="pml_xhigh")
        grid[:, 0:self.thickness, :] = fdtd.PML(name="pml_ylow")
        grid[:, -self.thickness:, :] = fdtd.PML(name="pml_yhigh")

        # Эллипс
        X, Y = np.ogrid[:self.a, :self.b]
        ellipse_mask = ((X - self.a // 2) / r1) ** 2 + ((Y - self.b // 2) / r2) ** 2 < 1
        permittivity = np.ones([self.a, self.b, 1])
        permittivity[ellipse_mask, 0] = self.n ** 2
        grid[:, :, 0] = fdtd.Object(permittivity=permittivity, name="circle")

        return grid

    def square_scatter(self, x1, x2, y1, y2):
        fdtd.set_backend("numpy")
        grid = fdtd.Grid(shape=(self.a, self.b, 1), grid_spacing=0.0000001, permittivity=1)

        # Сетка
        grid[y1:y2, x1, 0] = fdtd.LineSource(period=self.lym / self.c, name="source")
        grid[y1:y2, x2, 0] = fdtd.LineDetector(name="detector")

        grid[0:self.thickness, :, :] = fdtd.PML(name="pml_xlow")
        grid[-self.thickness:, :, :] = fdtd.PML(name="pml_xhigh")
        grid[:, 0:self.thickness, :] = fdtd.PML(name="pml_ylow")
        grid[:, -self.thickness:, :] = fdtd.PML(name="pml_yhigh")

        # Создание квадрата
        X, Y = np.ogrid[:self.a, :self.b]
        half_side = self.side_length // 2
        center_x, center_y = self.a // 2, self.b // 2

        # Маска для квадрата
        square_mask = (np.abs(X - center_x) <= half_side) & (np.abs(Y - center_y) <= half_side)

        permittivity = np.ones([self.a, self.b, 1])
        permittivity[square_mask, 0] = self.n ** 2
        grid[:, :, 0] = fdtd.Object(permittivity=permittivity, name="square")

        return grid

    def calculate(self):

        if self.figure == 1: #овал
            return self.ellipse(self.x, (self.a - self.x), self.y, (self.b - self.y), self.r1, self.r2)
        elif self.figure == 0: #круг
            return self.ellipse(self.x, (self.a - self.x), self.y, (self.b - self.y), self.r, self.r)
        elif self.figure == 2: #квадрат
            return self.square_scatter(self.x, (self.a - self.x), self.y, (self.b - self.y))
        else:
            print("фигня какая-то")
            return None
