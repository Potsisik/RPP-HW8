from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QFileDialog, QMessageBox
import sys 
from ui_mainWindow import Ui_MainWindow
import json

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        #потом добавлю эти функции
        #self.pushButton_3.clicked.connect(self.calculate) 
        #self.pushButton.clicked.connect(self.save_project)
        #self.pushButton_2.clicked.connect(self.load_project)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())