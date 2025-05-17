from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QFileDialog, QMessageBox
import sys 
from ui_mainWindow import Ui_MainWindow
from backend import Math_Model
import json

math_model = Math_Model() #создали матмодель

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        #потом добавлю эти функции
        self.pushButton_3.clicked.connect(self.calculate) 
        self.pushButton.clicked.connect(self.save_project)
        self.pushButton_2.clicked.connect(self.load_project)

    def get_values(self): #собираем значения полей делаем из них словарь
        parametrs = {}

        parametrs["a"] = self.lineEdit_2.text() #сохраняем сначала текст
        parametrs["b"] = self.lineEdit_3.text()
        parametrs["x"] = self.lineEdit_4.text()
        parametrs["y"] = self.lineEdit_5.text()
        parametrs["n"] = self.lineEdit_6.text()
        parametrs["time"] = self.lineEdit_7.text()
        parametrs["lym"] = self.lineEdit_8.text()
        parametrs["thickness"] = self.lineEdit_13.text()

        #овал
        #потом узнать как понимать какая вкладка выбрана
        parametrs["r1"] = self.lineEdit_9.text()
        parametrs["r2"] = self.lineEdit_10.text()
        #круг
        parametrs["r"] = self.lineEdit_11.text()
        #квадрат
        parametrs["side_length"] = self.lineEdit_12.text()


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
                
        parametrs["figure"] = self.tabWidget_2.currentIndex()
        # 0 - круг, 1 - овал, 2 - квадрат
                
        print(parametrs)
        return parametrs
    
    def save_project(self):  # Сохранение проекта в виде файла
        filename = QFileDialog.getSaveFileName(self, "Выберите файл", '', 'Файл проекта (*.json)')
        data = self.get_values()

        #проверка на ошибки
        if data == None:
            return
        if filename[0] == '':
            print("ошибка: название файла пустое")
            return 
        
        self.lineEdit.setText(filename[0])
        with open(filename[0], 'w') as f:
            json.dump(data, f)

    def set_values(self, parametrs): #Заполняет текстовые поля значениями из словаря
        if not parametrs or not isinstance(parametrs, dict): #проверка что мы передали именно словарь
            print("parametrs не является словарем")
            QMessageBox.critical(None, "Ошибка", "Неверный формат данных")
            return False
        
        try:
            self.lineEdit_2.setText(str(parametrs["a"]))
            self.lineEdit_3.setText(str(parametrs["b"]))
            self.lineEdit_4.setText(str(parametrs["x"]))
            self.lineEdit_5.setText(str(parametrs["y"]))
            self.lineEdit_6.setText(str(parametrs["n"]))
            self.lineEdit_7.setText(str(parametrs["time"]))
            self.lineEdit_8.setText(str(parametrs["lym"]))

            #овал
            self.lineEdit_9.setText(str(parametrs["r1"]))
            self.lineEdit_10.setText(str(parametrs["r2"]))
            self.lineEdit_11.setText(str(parametrs["thickness"]))
            
            return True
        
        except Exception as e:
            print(f"Ошибка при установке значений: {e}")
            QMessageBox.critical(None, "Ошибка", "Данные некорректны")
            return False
        
    def load_project(self):  # Загрузка проекта из файла
        filename = QFileDialog.getOpenFileName(self, "Выберите файл", '', 'Файл проекта (*.json)')
        if filename[0] == '':
            print("ошибка: название файла пустое")
            return
        self.lineEdit.setText(filename[0])

        with open(filename[0], 'r') as f:
            data = json.load(f) #отловить тут ошибку
        
        if data == None:
            print("файл пустой")
            return
        self.set_values(data)
    
    def calculate(self):
        print("выполняется расчет")
        dict_ = self.get_values()

        if dict_ is None:
            return
        
        #потом тут надо что нибудь посчитать
        math_model.set_values(dict_) #передавать словарь
        res = math_model.calculate() #получаем тоже словарь

        self.label_0.setText("что-то посчиталось") #временно
        # в будущем вызывать тут отдельный метод отвечающий за нарисовку графиков
        #self.draw_graphs(res['graphs'])

    def draw_graphs(self, graphs: dict): #пока нерабочий
        self.widget.clear_graph()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())