import sys
import os
import random
from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtCore import Slot


class MyWidget(QtWidgets.QWidget):

    def __init__(self):


        super().__init__()

        self.test_qlable1 = QtWidgets.QLabel('1')
        self.test_qlable2 = QtWidgets.QLabel('2')
        self.test_qlable3 = QtWidgets.QLabel('3')
        self.test_qlable4 = QtWidgets.QLabel('4')


        self.test_qlineedit1 = QtWidgets.QLineEdit('1')
        self.test_qlineedit2 = QtWidgets.QLineEdit('2')
        self.test_qlineedit3 = QtWidgets.QLineEdit('3')
        self.test_qlineedit4 = QtWidgets.QLineEdit('4')

        self.test_layout = QtWidgets.QGridLayout()
        self.test_layout.addWidget(self.test_qlable1, 0, 0)
        self.test_layout.addWidget(self.test_qlineedit1, 0, 1)
        self.test_layout.addWidget(self.test_qlable2, 0, 2)
        self.test_layout.addWidget(self.test_qlineedit2, 0, 3)
        self.test_layout.addWidget(self.test_qlable3, 1, 0)
        self.test_layout.addWidget(self.test_qlineedit3, 1, 1)
        self.test_layout.addWidget(self.test_qlable4, 1, 2)
        self.test_layout.addWidget(self.test_qlineedit4, 1, 3)
        
        self.open_file_qlineedit = QtWidgets.QLineEdit()
        self.open_file_button = QtWidgets.QPushButton('Open file')

        self.layout_file_dialog = QtWidgets.QHBoxLayout()
        self.layout_file_dialog.addWidget(self.open_file_qlineedit)
        self.layout_file_dialog.addWidget(self.open_file_button)


        self.test_label = QtWidgets.QLabel()
        self.test_label.setFixedWidth(500)
        self.test_label.setFrameShape(QtWidgets.QFrame.Box)
        self.test_label.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.test_label.setLineWidth(5)
        self.test_label.setFrameRect(QtCore.QRect( 0, 0, 0, 0))
        # self.test_label.setFrameStyle(100)
        # self.test_lable.StyledPanel()
        # self.test_lable.frameShape()
        # self.test_lable.setFrameStyle(100)

        self.button_image = QtWidgets.QPushButton('Download image')

        
        self.layout_qv = QtWidgets.QVBoxLayout()
        self.layout_qv.addLayout(self.test_layout)
        self.layout_qv.addLayout(self.layout_file_dialog)
        self.layout_qv.addWidget(self.button_image)

        self.layout_with_image = QtWidgets.QHBoxLayout()
        self.layout_with_image.addLayout(self.layout_qv)
        self.layout_with_image.addWidget(self.test_label)
        self.setLayout(self.layout_with_image)

        self.open_file_button.clicked.connect(self.open_file_dialog)
        self.button_image.clicked.connect(self.download_image)

    @Slot()
    def open_file_dialog(self):
        path_to_file, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Load Image", os.path.dirname(os.path.abspath(__file__)), "Images (*.jpg *.png *.bmp *.TIF)")
        print(type(path_to_file))
        file_to_lineedit = self.open_file_qlineedit.setText(path_to_file)
        file_image = QtGui.QPixmap(path_to_file)
        image_ = self.test_label.setPixmap(file_image.scaled(500, 900, QtCore.Qt.KeepAspectRatio))
        

    
    @Slot()
    def download_image(self):
        file_image = QtGui.QPixmap("cats.jpg")
        image_ = self.test_label.setPixmap(file_image)

        self.setWindowTitle('Test_cat_image')


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(1024, 600)
    widget.show()

    sys.exit(app.exec_())



