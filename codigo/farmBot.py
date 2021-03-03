from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys


def window():
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setGeometry(100,25,700,1000)
    win.setWindowTitle("Farmbot Chile Habanero")
    label = QLabel(win)
    label.setText('hola')

    win.show()
    sys.exit(app.exec_())
if __name__ == '__main__':
    window()
