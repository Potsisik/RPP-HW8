# Модуль отвечающий за корректное использование виджета-графика
from PySide6 import QtWidgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
import matplotlib
import numpy as np
import matplotlib.patches as patches

# Ensure using PyQt5 backend
matplotlib.use('QT5Agg')


# Matplotlib canvas class to create figure
class MplCanvas(FigureCanvasQTAgg):
    def __init__(self):
        self.fig = Figure(tight_layout=True)
        self.ax = self.fig.add_subplot(111)
        FigureCanvasQTAgg.__init__(self, self.fig)
        FigureCanvasQTAgg.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        FigureCanvasQTAgg.updateGeometry(self)


# Matplotlib widget
class MPLWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)   # Inherit from QWidget
        self.canvas = MplCanvas()                  # Create canvas object
        self.toolbar = NavigationToolbar2QT(canvas=self.canvas, parent=self)
        self.save_results_button = QtWidgets.QPushButton(text='Сохр.')
        self.toolbar.addWidget(self.save_results_button)
        self.vbl = QtWidgets.QVBoxLayout()         # Set box for plotting
        self.vbl.addWidget(self.toolbar)
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)

    def visualize_square(self, tension, a, b, side_length, x, y):
        """Визуализация поля с квадратным рассеивателем в виджете"""
        # Очищаем предыдущий график
        self.canvas.ax.clear()
        
        # Отображаем поле
        img = self.canvas.ax.imshow(np.transpose(tension),
                                  extent=[0, a, 0, b],
                                  cmap='RdBu',
                                  origin='lower',
                                  vmin=-0.02,
                                  vmax=0.02)

        # Добавляем квадратный рассеиватель
        center_x, center_y = a // 2, b // 2
        square = patches.Rectangle((center_x - side_length / 2, center_y - side_length / 2),
                                 side_length,
                                 side_length,
                                 linewidth=2,
                                 edgecolor='black',
                                 facecolor='none',
                                 linestyle='--')
        self.canvas.ax.add_patch(square)

        # Добавляем источник и детектор
        self.canvas.ax.scatter([x], [y], c='green', marker='*', s=100, label='Source')
        self.canvas.ax.scatter([a - x], [b - y], c='red', marker='o', s=100, label='Detector')

        # Настройки графика
        if not hasattr(self, 'cbar'):
            self.cbar = self.canvas.fig.colorbar(img, ax=self.canvas.ax)
            self.cbar.set_label("E(x, y)")

        self.canvas.ax.set_title(f'Рассеяние на квадрате (t)')
        self.canvas.ax.set_xlabel('x (узлы сетки)')
        self.canvas.ax.set_ylabel('y (узлы сетки)')
        self.canvas.ax.legend()
        self.canvas.ax.grid(True, alpha=0.3)
        
        # Перерисовываем холст
        self.canvas.draw()

    def draw_elipse(self, tension, a, b, r1, r2, x, y):
        """Визуализация распределения напряженностей с эллиптическим рассеивателем"""
        # Очищаем предыдущий график
        self.canvas.ax.clear()
        
        # Отображаем поле напряженностей
        img = self.canvas.ax.imshow(np.transpose(tension),
                                extent=[0, a, 0, b],
                                cmap="RdBu",
                                origin="lower",
                                vmin=-0.02,
                                vmax=0.02)
        
        # Добавляем эллиптический рассеиватель
        border = patches.Ellipse((a // 2, b // 2), 
                                2 * r1, 
                                2 * r2, 
                                edgecolor='black', 
                                facecolor='none', 
                                linewidth=0.5)
        self.canvas.ax.add_patch(border)

        # Добавляем источник и детектор
        self.canvas.ax.scatter([x], [y], c='green', marker='*', s=100, label='Source')
        self.canvas.ax.scatter([a - x], [b - y], c='red', marker='o', s=100, label='Detector')

        # Настройки графика
        self.canvas.ax.set_title("Распределение напряженностей")
        self.canvas.ax.set_xlabel("x")
        self.canvas.ax.set_ylabel("y")
        
        # Создаем новую цветовую шкалу и сохраняем ссылку
        if not hasattr(self, 'cbar'):
            self.cbar = self.canvas.fig.colorbar(img, ax=self.canvas.ax)
            self.cbar.set_label("E(x, y)")
        
        # Автоматическая подгонка layout'а и перерисовка
        self.canvas.fig.tight_layout()
        self.canvas.draw()
