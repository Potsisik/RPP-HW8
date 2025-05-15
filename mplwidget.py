# Модуль отвечающий за корректное использование виджета-графика
from PySide6 import QtWidgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
import matplotlib

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

    def clear_graph(self):
        self.canvas.ax.cla()
        self.canvas.ax.set_xlabel('Длина L') #может потом переделать как передаваемую переменную

    def draw_graph(self, graph: dict, new_label: str):
        #self.clear_graph()
        self.canvas.ax.plot(graph['x'], graph['y'], label=new_label)
        self.canvas.ax.legend()
        self.canvas.draw()
