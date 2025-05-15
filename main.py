from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QFileDialog, QMessageBox
import sys 
from ui_mainWindow import Ui_MainWindow
import json

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        #потом добавлю эти функции
        self.pushButton_3.clicked.connect(self.calculate) 
        #self.pushButton.clicked.connect(self.save_project)
        #self.pushButton_2.clicked.connect(self.load_project)

    def get_values(self): #собираем значения полей делаем из них словарь
        parametrs = {}

        parametrs["a"] = self.lineEdit_2.text() #сохраняем сначала текст
        parametrs["b"] = self.lineEdit_3.text()
        parametrs["x"] = self.lineEdit_4.text()
        parametrs["y"] = self.lineEdit_5.text()
        parametrs["n"] = self.lineEdit_6.text()
        parametrs["time"] = self.lineEdit_7.text()
        parametrs["lym"] = self.lineEdit_8.text()

        #овал
        #потом узнать как понимать какая вкладка выбрана
        parametrs["r1"] = self.lineEdit_9.text()
        parametrs["r2"] = self.lineEdit_10.text()
        parametrs["thickness"] = self.lineEdit_11.text()

        for key, value in parametrs.items(): #проверка на пустые строки
            if value is None or value == '':
                print(f"У ключа '{key} нет значения")
                QMessageBox.critical(None, "Ошибка", "Заполните все поля")
                return None
            
        for key, value in parametrs.items(): #преобразуем строки во float
            if isinstance(value, str):
                try:
                    parametrs[key] = float(value)
                except ValueError: # Обработка случая, когда строка не может быть преобразована в float
                    print(f"Значение '{value}' для ключа '{key}' не может быть преобразовано в float")
                    QMessageBox.critical(None, "Ошибка", "Поля заполненны некорректно")
                    return None
                
        print(parametrs)
        return parametrs
    
    def calculate(self):
        print("выполняется расчет")
        dict_ = self.get_values()

        if dict_ is None:
            return
        #потом тут надо что нибудь посчитать

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())