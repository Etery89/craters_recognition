import sys
import os
from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtCore import Slot

from simple_cv import default_mosaic_filename
from simple_cv import create_stored_mosaic
from simple_cv import create_stored_shp
from simple_cv import get_colorized_image
from simple_cv import create_gradient
from simple_cv import detect_craters
from simple_cv import store_features
from simple_cv import draw_circles


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

        def add_param_to_grid(label, value, grid, row, col):
            label_widget = QtWidgets.QLabel(label)
            lineedit_widget = QtWidgets.QLineEdit(value)
            grid.addWidget(label_widget, row, col)
            grid.addWidget(lineedit_widget, row, col+1)
            return lineedit_widget

        parameters_layout = QtWidgets.QGridLayout()
        self.parametr_1_le = add_param_to_grid('Parameter 1', '30', parameters_layout, 0, 0)
        self.parametr_2_le = add_param_to_grid('Parameter 2', '20', parameters_layout, 1, 0)
        self.min_search_radius_le = add_param_to_grid('Minimum Search Radius', '100', parameters_layout, 0, 2)
        self.max_search_radius_le = add_param_to_grid('Maximum Search Radius', '200', parameters_layout, 1, 2)

        # Program message output layout
        program_message_lb = QtWidgets.QLabel('Program messages')
        program_message_lb.setFixedSize(100, 15)
        self.program_message_field = QtWidgets.QTextEdit()
        self.program_message_field.setFixedSize(500, 100)

        program_msg_layout = QtWidgets.QVBoxLayout()
        program_msg_layout.addWidget(program_message_lb)
        program_msg_layout.addWidget(self.program_message_field)

        # QVBoxLayout "left parth"/"function parth"
        settings_layout = QtWidgets.QVBoxLayout()
        settings_layout.addLayout(layout_open_tiff_file)
        settings_layout.addLayout(choose_shp_file_layout)
        settings_layout.addLayout(layout_for_min_distance)
        settings_layout.addLayout(parameters_layout)
        settings_layout.addWidget(self.find_craters_btn)
        settings_layout.addLayout(layout_open_shp_file)
        settings_layout.addWidget(self.calc_additional_parameters_btn)
        settings_layout.addLayout(program_msg_layout)

        # QHBoxLayout "function part + image parth"
        self.image_lb = QtWidgets.QLabel()
        self.image_lb.setFixedWidth(620)
        self.image_lb.setFrameShape(QtWidgets.QFrame.Box)
        self.image_lb.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.image_lb.setLineWidth(4)
        self.image_lb.setFrameRect(QtCore.QRect(QtCore.QPoint(0, 0), QtCore.QSize(620, 470)))

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
            mosaic_image_pixmap.scaled(600, 500, QtCore.Qt.IgnoreAspectRatio)
            )

    # File open function
    @Slot()
    def open_tiff_handler(self):
        path_to_file, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Load Image', os.path.dirname(os.path.abspath(__file__)), 'Images (*.img *.TIF *.TIFF)'
         )
        if path_to_file != '':
            path_to_file_for_wind = QtCore.QDir.toNativeSeparators(path_to_file)
            self.file_open_le.setText(path_to_file_for_wind)
            tiff_filename = self.file_open_le.text()
            self.mosaic_filename = default_mosaic_filename(tiff_filename)
            msg = create_stored_mosaic(tiff_filename, self.mosaic_filename)
            if msg == '':
                self.show_mosaic(self.mosaic_filename)
                shp_filename = self.default_shp_filename(tiff_filename)
                self.choose_shp_file_le.setText(shp_filename)
                self.program_message_field.clear()
            else:
                self.program_message_field.setText(msg)
                self.choose_shp_file_le.clear()
        else:
            self.program_message_field.setText('Вы не выбрали файл.')

    # Функция открытия Шейп-файла нажатием кнопки
    @Slot()
    def open_shp_handler(self):
        path_to_the_shp_file, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Load Shp file', os.path.dirname(os.path.abspath(__file__)), 'Files (*.Shp)'
            )
        path_to_the_shp_file_for_wind = QtCore.QDir.toNativeSeparators(path_to_the_shp_file)
        self.shp_file_open_le.setText(path_to_the_shp_file_for_wind)

    # Функция выбора имени шейп-файла
    def default_shp_filename(self, tiff_file_name):
        tiff_basename = os.path.basename(tiff_file_name)
        tiff_dirname = os.path.dirname(tiff_file_name)
        shp_basename_list = tiff_basename.split('.')
        shp_basename_list.pop(len(shp_basename_list)-1)
        shp_basename_list.append('craters.shp')
        delimiter = '_'
        shp_basename = delimiter.join(shp_basename_list)
        shp_file_name = os.path.join(*os.path.split(tiff_dirname), shp_basename)
        return shp_file_name

    # Функция проверки значений параметров на соответствие типу данных
    def get_in_parameter(self, parameter_field_name, error_msg_1, error_msg_2, errors_list):
        try:
            parameter_value_text = getattr(self, parameter_field_name)
            parameter_value = int(parameter_value_text.text())
            if parameter_value > 0:
                return parameter_value
            else:
                parameter_value_text.clear()
                errors_list.append(error_msg_2)
                return None
        except(ValueError, TypeError):
            parameter_value_text.clear()
            errors_list.append(error_msg_1)
            return None

    @Slot()
    def recognize_and_show_craters(self, mosaic):
        self.program_message_field.clear()
        messages_for_errors = []

        error_message_1 = 'Неправильный тип данных в поле "Minimum distance between centers". Введите целое число.'
        error_message_2 = 'Неправильный тип данных в поле "Parameter 1". Введите целое число.'
        error_message_3 = 'Неправильный тип данных в поле "Parameter 2". Введите целое число.'
        error_message_4 = 'Неправильный тип данных в поле "Minimum Search Radius". Введите целое число.'
        error_message_5 = 'Неправильный тип данных в поле "Maximum Search Radius". Введите целое число.'
        error_message_6 = 'Введите неотрицательное число в поле "Minimum distance between centers".'
        error_message_7 = 'Введите неотрицательное число в поле "Parameter 1".'
        error_message_8 = 'Введите неотрицательное число в поле "Parameter 2".'
        error_message_9 = 'Введите неотрицательное число в поле "Minimum Search Radius".'
        error_message_10 = 'Введите неотрицательное число в поле "Maximum Search Radius".'

        min_distance_centers_value = self.get_in_parameter(
            'min_distance_centers_le', error_message_1, error_message_6, messages_for_errors
            )
        parametr_1_value = self.get_in_parameter(
            'parametr_1_le', error_message_2, error_message_7, messages_for_errors
            )
        parametr_2_value = self.get_in_parameter(
            'parametr_2_le', error_message_3, error_message_8, messages_for_errors
            )
        min_search_radius_value = self.get_in_parameter(
            'min_search_radius_le', error_message_4, error_message_9, messages_for_errors
            )
        max_search_radius_value = self.get_in_parameter(
            'max_search_radius_le', error_message_5, error_message_10, messages_for_errors
            )

        try:
            if len(messages_for_errors) == 0:
                self.program_message_field.clear()
                mosaic_filename = self.mosaic_filename
                marked_up_image = get_colorized_image(mosaic_filename)
                gradient_image = create_gradient(mosaic_filename)

                shp_filename = self.choose_shp_file_le.text()
                check_shp_filename = os.path.exists(shp_filename)
                if check_shp_filename is True:
                    self.program_message_field.setText('Shp файл с таким именем уже существует')
                else:
                    tiff_filename = self.file_open_le.text()

                    create_stored_shp(shp_name=shp_filename, dtm_input=tiff_filename)
                    circle_list = detect_craters(
                        gradient_image=gradient_image,
                        cv_start_radius=min_search_radius_value,
                        cv_max_radius=max_search_radius_value,
                        cv_param1=parametr_1_value,
                        cv_param2=parametr_2_value,
                        cv_min_distance=min_distance_centers_value
                    )
                    get_stored_info = store_features(
                        dtm_input=tiff_filename,
                        circle_list=circle_list,
                        shp_name=shp_filename
                    )
                    marked_up_image_filename = 'detected_crat.tif'
                    draw_circles(
                        marked_up_image=marked_up_image,
                        circle_list=circle_list,
                        crat_id=get_stored_info[0],
                        marked_up_image_filename=marked_up_image_filename
                        )

                    self.show_mosaic(marked_up_image_filename)
            else:
                delimiter = '\n'
                self.program_message_field.setText(delimiter.join(messages_for_errors))
        except AttributeError:
            self.program_message_field.setText('Не выбран файл для обработки. Пожалуйста, откройте файл.')


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(1024, 530)
    widget.show()

    sys.exit(app.exec_())
