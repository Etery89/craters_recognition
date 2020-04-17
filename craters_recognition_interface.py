import sys
import os
from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtCore import Slot

from simple_cv import default_mosaic_filename
from simple_cv import create_stored_mosaic
from simple_cv import create_stored_shp
from simple_cv import get_colorized_image
from simple_cv import create_gradient
from simple_cv import crater_recognition
from simple_cv import store_marked_up_image


class MyWidget(QtWidgets.QWidget):

    def __init__(self):

        super().__init__()

        # QHBoxLayout 'Open tiff file"
        self.file_open_btn = QtWidgets.QPushButton('Open tiff file')
        self.file_open_le = QtWidgets.QLineEdit()

        layout_open_tiff_file = QtWidgets.QHBoxLayout()
        layout_open_tiff_file.addWidget(self.file_open_le)
        layout_open_tiff_file.addWidget(self.file_open_btn)

        # QHBoxLayout "Choose Shp-file"
        choose_shp_file_lb = QtWidgets.QLabel('Choose shp file name')
        self.choose_shp_file_le = QtWidgets.QLineEdit()

        choose_shp_file_layout = QtWidgets.QHBoxLayout()
        choose_shp_file_layout.addWidget(choose_shp_file_lb)
        choose_shp_file_layout.addWidget(self.choose_shp_file_le)

        # Algorithm button
        self.find_craters_btn = QtWidgets.QPushButton('Сircles calculation')

        # QHBoxLayout "Open shp file"
        self.shp_file_open_btn = QtWidgets.QPushButton('Open shp file')
        self.shp_file_open_le = QtWidgets.QLineEdit()

        layout_open_shp_file = QtWidgets.QHBoxLayout()
        layout_open_shp_file.addWidget(self.shp_file_open_le)
        layout_open_shp_file.addWidget(self.shp_file_open_btn)

        # Button for calculating additional parameters
        self.calc_additional_parameters_btn = QtWidgets.QPushButton('Сalculation of additional parameters')

        # QHBoxLayout
        min_distance_centers_lb = QtWidgets.QLabel('Minimum distance between centers')
        self.min_distance_centers_le = QtWidgets.QLineEdit('100')

        layout_for_min_distance = QtWidgets.QHBoxLayout()
        layout_for_min_distance.addWidget(min_distance_centers_lb)
        layout_for_min_distance.addWidget(self.min_distance_centers_le)

        # QGridLayout "Parameters"
        parametr_1_lb = QtWidgets.QLabel('Parameter 1')
        self.parametr_1_le = QtWidgets.QLineEdit('30')
        parametr_2_lb = QtWidgets.QLabel('Parameter 2')
        self.parametr_2_le = QtWidgets.QLineEdit('20')
        min_search_radius_lb = QtWidgets.QLabel('Minimum Search Radius')
        self.min_search_radius_le = QtWidgets.QLineEdit('100')
        max_search_radius_lb = QtWidgets.QLabel('Maximum Search Radius')
        self.max_search_radius_le = QtWidgets.QLineEdit('200')

        parameters_layout = QtWidgets.QGridLayout()
        parameters_layout.addWidget(parametr_1_lb, 0, 0)
        parameters_layout.addWidget(self.parametr_1_le, 0, 1)
        parameters_layout.addWidget(parametr_2_lb, 1, 0)
        parameters_layout.addWidget(self.parametr_2_le, 1, 1)
        parameters_layout.addWidget(min_search_radius_lb, 0, 2)
        parameters_layout.addWidget(self.min_search_radius_le, 0, 3)
        parameters_layout.addWidget(max_search_radius_lb, 1, 2)
        parameters_layout.addWidget(self.max_search_radius_le, 1, 3)

        # Program message output field
        self.program_message_field = QtWidgets.QTextEdit('Program messages')
        self.program_message_field.setFixedSize(500, 100)

        # QVBoxLayout "left parth"/"function parth"
        settings_layout = QtWidgets.QVBoxLayout()
        settings_layout.addLayout(layout_open_tiff_file)
        settings_layout.addLayout(choose_shp_file_layout)
        settings_layout.addLayout(layout_for_min_distance)
        settings_layout.addLayout(parameters_layout)
        settings_layout.addWidget(self.find_craters_btn)
        settings_layout.addLayout(layout_open_shp_file)
        settings_layout.addWidget(self.calc_additional_parameters_btn)
        settings_layout.addWidget(self.program_message_field)

        # QHBoxLayout "function part + image parth"
        self.image_lb = QtWidgets.QLabel()
        self.image_lb.setFixedWidth(500)
        self.image_lb.setFrameShape(QtWidgets.QFrame.Box)
        self.image_lb.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.image_lb.setLineWidth(4)
        self.image_lb.setFrameRect(QtCore.QRect(QtCore.QPoint(0, 0), QtCore.QSize(500, 470)))

        window_layout = QtWidgets.QHBoxLayout()
        window_layout.addLayout(settings_layout)
        window_layout.addWidget(self.image_lb)
        self.setLayout(window_layout)

        # Setting the main window icon
        self.setWindowTitle('Craters recognition')
        self.setWindowIcon(QtGui.QIcon('1492719120-moon_83629.png'))

        # Signal buttons
        self.file_open_btn.clicked.connect(self.open_tiff_handler)
        self.shp_file_open_btn.clicked.connect(self.open_shp_handler)
        self.find_craters_btn.clicked.connect(self.recognize_and_show_craters)

    # Функция демонстрации мозаики
    def show_mosaic(self, mosaic_image):
        mosaic_image_pixmap = QtGui.QPixmap(mosaic_image)
        self.image_lb.setPixmap(
            mosaic_image_pixmap.scaled(720, 920, QtCore.Qt.KeepAspectRatio)
            )

    # File open function
    @Slot()
    def open_tiff_handler(self):
        path_to_file, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Load Image', os.path.dirname(os.path.abspath(__file__)), 'Images (*.img *.TIF *.TIFF)'
         )
        self.file_open_le.setText(path_to_file)
        tiff_filename = self.file_open_le.text()
        shp_filename = self.default_shp_filename(tiff_filename)
        self.choose_shp_file_le.setText(shp_filename)
        self.mosaic_filename = default_mosaic_filename(tiff_filename)
        create_stored_mosaic(tiff_filename, self.mosaic_filename)
        self.show_mosaic(self.mosaic_filename)

    # Функция открытия Шейп-файла нажатием кнопки
    @Slot()
    def open_shp_handler(self):
        path_to_the_shp_file, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Load Shp file', os.path.dirname(os.path.abspath(__file__)), 'Files (*.Shp)'
            )
        self.shp_file_open_le.setText(path_to_the_shp_file)

    # Функция выбора имени шейп-файла
    def default_shp_filename(self, tiff_file_name):
        tiff_basename = os.path.basename(tiff_file_name)
        tiff_dirname = os.path.dirname(tiff_file_name)
        shp_basename_list = tiff_basename.split('.')
        shp_basename_list.pop(len(shp_basename_list)-1)
        shp_basename_list.append('craters.shp')
        delimiter = '_'
        shp_basename = delimiter.join(shp_basename_list)
        shp_file_name = os.path.join(tiff_dirname, shp_basename)
        return shp_file_name

    # Функция проверки значений параметров на соответствие типу данных
    def get_in_parameter(self, parameter_field_name, error_msg, errors_list):
        try:
            parameter_value_text = getattr(self, parameter_field_name)
            parameter_value = int(parameter_value_text.text())
            return parameter_value
        except ValueError:
            parameter_value_text.clear()
            errors_list.append(error_msg)
            return None

    @Slot()
    def recognize_and_show_craters(self, mosaic):
        messages_for_errors = []

        error_message_1 = 'Неправильный тип данных в поле "Minimum distance between centers". Введите целое число'
        error_message_2 = 'Неправильный тип данных в поле "Parameter 1". Введите целое число'
        error_message_3 = 'Неправильный тип данных в поле "Parameter 2". Введите целое число'
        error_message_4 = 'Неправильный тип данных в поле "Minimum Search Radius". Введите целое число'
        error_message_5 = 'Неправильный тип данных в поле "Maximum Search Radius". Введите целое число'

        min_distance_centers_value = self.get_in_parameter(
            'min_distance_centers_le', error_message_1, messages_for_errors
            )
        parametr1_value = self.get_in_parameter(
            'parametr_1_le', error_message_2, messages_for_errors
            )
        parametr2_value = self.get_in_parameter(
            'parametr_2_le', error_message_3, messages_for_errors
            )
        min_search_radius_value = self.get_in_parameter(
            'min_search_radius_le', error_message_4, messages_for_errors
            )
        max_search_radius_value = self.get_in_parameter(
            'max_search_radius_le', error_message_5, messages_for_errors
            )

        if len(messages_for_errors) == 0:
            self.program_message_field.clear()
        else:
            delimiter = '\n'
            self.program_message_field.setText(delimiter.join(messages_for_errors))
        try:
            mosaic_filename = self.mosaic_filename
            marked_up_image = get_colorized_image(mosaic_filename)
            gradient_image = create_gradient(mosaic_filename)

            shp_filename = self.choose_shp_file_le.text()
            tiff_filename = self.file_open_le.text()

            create_stored_shp(shp_name=shp_filename, dtm_input=tiff_filename)

            new_marked_up_image = crater_recognition(
                dtm_input=tiff_filename,
                gradient_image=gradient_image,
                marked_up_image=marked_up_image,
                shp_name=shp_filename,
                cv_start_radius=min_search_radius_value,
                cv_max_radius=max_search_radius_value,
                cv_param1=parametr1_value,
                cv_param2=parametr2_value,
                cv_min_distance=min_distance_centers_value
            )

            marked_up_image_filename = store_marked_up_image(new_marked_up_image)
            self.show_mosaic(marked_up_image_filename)

        except AttributeError:
            self.program_message_field.setText('Не выбран файл для обработки. Пожалуйста, откройте файл.')


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(1024, 530)
    widget.show()

    sys.exit(app.exec_())
