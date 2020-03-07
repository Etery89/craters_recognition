import sys
from PyQt5.QtWidgets import QApplication, QWidget
import cv2

if __name__ =='__main__':
    pass
    app = QApplication(sys.argv)

    w = QWidget()
    w.resize(250, 150)
    w.move(300, 300)
    w.setWindowTitle('For_Example')
    w.show()

    sys.exit(app.exec_())
