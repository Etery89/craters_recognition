import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QLabel, QLineEdit
from PyQt5.QtGui import QIcon


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        self.lbl = QLabel(self)
        qle = QLineEdit(self)
        
        qle.resize(600, 20)

        qle.move(60, 60)
        self.lbl.move(60, 40)

        self.resize(800, 600)
        self.center()
        self.setWindowTitle('Craters recognition')
        self.setWindowIcon(QIcon('1492719120-moon_83629.png'))

        self.show()

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())