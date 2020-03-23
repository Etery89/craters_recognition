import sys
import os
from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtCore import Slot


class MyWidget(QtWidgets.QWidget):

    def __init__(self):

        super().__init__()

        # QHBoxLayout 'open file"
        self.file_open_button = QtWidgets.QPushButton('Открыть изображение')
        self.file_open_lineedit = QtWidgets.QLineEdit()


        self.layout_open = QtWidgets.QHBoxLayout()
        self.layout_open.addWidget(self.file_open_lineedit)
        self.layout_open.addWidget(self.file_open_button)
        

        #  QHBoxLayout "save file"
        self.file_save_button = QtWidgets.QPushButton('Сохранить изображение')
        self.file_save_lineedit = QtWidgets.QLineEdit()


        self.layout_save = QtWidgets.QHBoxLayout()
        self.layout_save.addWidget(self.file_save_lineedit)
        self.layout_save.addWidget(self.file_save_button)

        # Algorithm button
        self.algorithm_button = QtWidgets.QPushButton('Алгоритм расчёта окружностей')

        # QHBoxLayout "Open Shp file"
        self.shp_file_open_button = QtWidgets.QPushButton('Открыть Shp-файл')
        self.shp_file_open_lineedit = QtWidgets.QLineEdit()

        self.layout_open_shp_file = QtWidgets.QHBoxLayout()
        self.layout_open_shp_file.addWidget(self.shp_file_open_lineedit)
        self.layout_open_shp_file.addWidget(self.shp_file_open_button)
        
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
        self.layout_function_parth.addLayout(self.layout_open_shp_file)
        self.layout_function_parth.addWidget(self.additional_parameters_button)

        # QHBoxLayout "function part + image parth"
        self.image_label = QtWidgets.QLabel()
        self.image_label.setFixedWidth(500)
        self.image_label.setFrameShape(QtWidgets.QFrame.Box)
        self.image_label.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.image_label.setLineWidth(4)
        

        self.function_with_image_layout = QtWidgets.QHBoxLayout()
        self.function_with_image_layout.addLayout(self.layout_function_parth)
        self.function_with_image_layout.addWidget(self.image_label)
        self.setLayout(self.function_with_image_layout)

        # Setting the main window icon
        self.setWindowTitle('Craters recognition')
        self.setWindowIcon(QtGui.QIcon('1492719120-moon_83629.png'))

        # Signal buttons
        self.file_open_button.clicked.connect(self.open_tiff_file)
        self.shp_file_open_button.clicked.connect(self.open_shp_file)
        self.file_save_button.clicked.connect(self.save_shp_file)

    # File open function
    @Slot()
    def open_tiff_file(self):
        path_to_file, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Load Image',
            os.path.dirname(os.path.abspath(__file__)),
             'Images (*.jpg *.png *.bmp *.TIF *.TIFF)'
         )
        path_to_file_text = self.file_open_lineedit.setText(path_to_file)
        file_image = QtGui.QPixmap(path_to_file)
        image_to_image_lable = self.image_label.setPixmap(file_image.scaled(500, 900, QtCore.Qt.KeepAspectRatio))

    @Slot()
    def open_shp_file(self):
        path_to_the_shp_file, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Load Sph-file', os.path.dirname(os.path.abspath(__file__)), 'Files (*.Shp)')
        path_to_the_shp_file_text = self.shp_file_open_lineedit.setText(path_to_the_shp_file)

    @Slot()
    def save_shp_file(self):
        file_name = QtWidgets.QFileDialog.getSaveFileName(self, 'Save Shp-file', os.path.dirname(os.path.abspath(__file__)), 'Files (*.Shp)')
        file_name_text = self.file_save_lineedit.setText(file_name)
        



if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(1024, 600)
    widget.show()

    sys.exit(app.exec_())
