from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys

fondo = "background-color:#203500;"


class MainWindow(QMainWindow):

    def __init__(self,*args):
        QMainWindow.__init__(self,*args)
        
        self.setWindowTitle("Farmbot Chile Habanero")
        self.setGeometry(50,25,500,500)
        self.setStyleSheet(fondo)


        #Imagen poli
        poli = QLabel(self)
        pixmap1 = QPixmap('./pictures/politecnico.png')
        poli.setPixmap(pixmap1)
        poli.resize(100,71)
        poli.move(420,10)

        #Imagen cicata
        cicata = QLabel(self)
        pixmap2 = QPixmap('./pictures/cicata.png')
        cicata.setPixmap(pixmap2)
        cicata.resize(100,100)
        cicata.move(5,-5)


        #titulo Header
        titulo = QLabel(self)
        titulo.setText("FarmBot Chile Habanero")
        titulo.setStyleSheet("color:#419f00;")
        titulo.setFont(QFont('SansSerif',20))
        titulo.resize(300,30)
        titulo.move(130,30)

        #win = QWidget(self)
        #layout = QGridLayout()
        #layout.addWidget(poli,0,0)
        #layout.addWidget(titulo,0,)
        #layout.addWidget(cicata,0,1)
        #win.setLayout(layout)
        #win.resize(700,100)


    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
