import sys
import os
from PySide2 import QtWidgets, QtGui, QtCore

class MyWidget(QtWidgets.QWidget):

    def __init__(self):

        super().__init__()

        # QHBoxLayout 'open file"
        self.file_open_button = QtWidgets.QPushButton('Открыть изображение')
        self.file_open_lineedit = QtWidgets.QLineEdit()


        self.layout_open = QtWidgets.QHBoxLayout()
        self.layout_open.addWidget(self.file_open_lineedit)
        self.layout_open.addWidget(self.file_open_button)
        # self.layout_open.addStretch(0)
        

        #  QHBoxLayout "save file"
        self.file_save_button = QtWidgets.QPushButton('Сохранить изображение')
        self.file_save_lineedit = QtWidgets.QLineEdit()


        self.layout_save = QtWidgets.QHBoxLayout()
        self.layout_save.addWidget(self.file_save_lineedit)
        self.layout_save.addWidget(self.file_save_button)

        # Algorithm button
        self.algorithm_button = QtWidgets.QPushButton('Алгоритм расчёта окружностей')

        # QHBoxLayout "Open table file"
        self.table_file_open_button = QtWidgets.QPushButton('Открыть таблицу параметров')
        self.table_file_open_lineedit = QtWidgets.QLineEdit()

        self.layout_open_table_file = QtWidgets.QHBoxLayout()
        self.layout_open_table_file.addWidget(self.table_file_open_lineedit)
        self.layout_open_table_file.addWidget(self.table_file_open_button)
        
        # Button for calculating additional parameters
        self.additional_parameters_button = QtWidgets.QPushButton('Расчёт дополнительных параметров')

        # QGridLayout "Parameters"
        self.var_with_image_qlable = QtWidgets.QLabel('Переменная с изображением')
        self.var_with_image_qlineedit = QtWidgets.QLineEdit()
        self.min_distance_centers_ql = QtWidgets.QLabel('Минимальное расстояние между центрами')
        self.min_distance_centers_qle = QtWidgets.QLineEdit()
        self.parametr1_qlable = QtWidgets.QLabel('Параметр 1')
        self.parametr1_qlineedit = QtWidgets.QLineEdit()
        self.parametr2_qlable = QtWidgets.QLabel('Параметр 2')
        self.parametr2_qlineedit = QtWidgets.QLineEdit()
        self.min_search_radius_qlable = QtWidgets.QLabel('Минимальный радиус поиска')
        self.min_search_radius_qlineedit = QtWidgets.QLineEdit()
        self.max_search_radius_qlable = QtWidgets.QLabel('Максимальный радиус поиска')
        self.max_search_radius_qlineedit = QtWidgets.QLineEdit()

        self.parameters_layout = QtWidgets.QGridLayout()
        self.parameters_layout.addWidget(self.var_with_image_qlable, 0, 0)
        self.parameters_layout.addWidget(self.var_with_image_qlineedit, 0, 1)
        self.parameters_layout.addWidget(self.min_distance_centers_ql, 0, 2)
        self.parameters_layout.addWidget(self.min_distance_centers_qle, 0, 3)
        self.parameters_layout.addWidget(self.parametr1_qlable, 1, 0)
        self.parameters_layout.addWidget(self.parametr1_qlineedit, 1, 1)
        self.parameters_layout.addWidget(self.parametr2_qlable, 2, 0)
        self.parameters_layout.addWidget(self.parametr2_qlineedit, 2, 1)
        self.parameters_layout.addWidget(self.min_search_radius_qlable, 1, 2)
        self.parameters_layout.addWidget(self.min_search_radius_qlineedit, 1, 3)
        self.parameters_layout.addWidget(self.max_search_radius_qlable, 2, 2)
        self.parameters_layout.addWidget(self.max_search_radius_qlineedit, 2, 3)

        # QVBoxLayout "left parth"/"function parth"

        self.layout_function_parth =  QtWidgets.QVBoxLayout()
        self.layout_function_parth.addLayout(self.layout_open)
        self.layout_function_parth.addLayout(self.layout_save)
        self.layout_function_parth.addLayout(self.parameters_layout)
        self.layout_function_parth.addWidget(self.algorithm_button)
        self.layout_function_parth.addLayout(self.layout_open_table_file)
        self.layout_function_parth.addWidget(self.additional_parameters_button)
    
        self.setLayout(self.layout_function_parth)

        # QHBoxLayout "function part + image parth"
        






        self.setWindowTitle('Craters recognition')
        self.setWindowIcon(QtGui.QIcon('1492719120-moon_83629.png'))


















if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec_())