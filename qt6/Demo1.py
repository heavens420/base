import sys
from PyQt6.QtWidgets import (QWidget, QToolTip, QPushButton, QApplication)
from PyQt6.QtGui import QFont


class Demo1(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.app = QApplication(sys.argv)

    def initUI(self):
        QToolTip.setFont(QFont('SansSerif', 10))

        self.setToolTip('This is a <b>QWidget</b> widget')

        btn = QPushButton('Button', self)
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.resize(btn.sizeHint())
        btn.move(50, 50)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Tooltips')
        self.show()

    def createWindow(self):
        w = QWidget()
        w.resize(550, 500)
        w.move(300, 300)

        w.setWindowTitle('Too Simple')
        w.show()

        sys.exit(self.app.exec())

def createWindow2():
    app = QApplication(sys.argv)
    ex = Demo1()
    sys.exit(app.exec())


if __name__ == '__main__':
    createWindow2()
