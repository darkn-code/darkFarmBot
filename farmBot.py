from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys

fondo = "background-color:#203500;"
colorLetra = "color:#419f00;"
ColorBotones = "color:white;"
border = "border: 0px solid black;"
borderG = 'border:2px solid white;'

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()  
        self.setWindowTitle("Farmbot Chile Habanero")
        self.setStyleSheet(fondo)

        #Creacion Widget
        WFrame = QWidget(self)
        layout = QGridLayout()
        BFrame = QWidget()
        ZFrame = QWidget()
        blayout = QGridLayout()
        zlayout = QGridLayout()
        ZFrame.setLayout(zlayout)
        BFrame.setLayout(blayout)
        WFrame.setLayout(layout)

        #Imagen cicata
        cicata = QLabel(self)
        pixmap2 = QPixmap('./pictures/cicata.png')
        cicata.setStyleSheet(border)
        cicata.setPixmap(pixmap2)

        #titulo Header
        titulo = QLabel()
        titulo.setText("FarmBot Chile Habanero")
        titulo.setFont(QFont('SansSerif',15))
        titulo.setStyleSheet(colorLetra + border)

        lXY = QLabel()
        lXY.setText('XY')
        lXY.setStyleSheet(ColorBotones)
        lXY.setFont(QFont('SansSerif',10))
        
        lz = QLabel()
        lz.setText('Z')
        lz.setStyleSheet(ColorBotones)
        lz.setFont(QFont('SansSerif',10))
        
        #Modo manual
        bConectar = QPushButton("Conectar")
        bConectar.setStyleSheet(ColorBotones)
        bConectar.setFont(QFont("SansSerif",10))
        bConectar.clicked.connect(self.conectarArduino)

        tPuerto = QLineEdit("/dev/ttyACM0")
        tPuerto.setStyleSheet(ColorBotones)
        tPuerto.setFont(QFont('SansSerif',10))

        bArriba = QPushButton()
        bArriba.setIcon(QIcon('./pictures/flechaArr.png'))
        bAbajo = QPushButton()
        bAbajo.setIcon(QIcon('./pictures/flechaAba.png'))
        bDerecha = QPushButton()
        bDerecha.setIcon(QIcon('./pictures/flechaDer.png'))
        bIzquierda = QPushButton()
        bIzquierda.setIcon(QIcon('./pictures/flechaIzq.png'))
        
        bArribaZ = QPushButton()
        bArribaZ.setIcon(QIcon('./pictures/flechaArr.png'))
        bAbajoZ = QPushButton()
        bAbajoZ.setIcon(QIcon('./pictures/flechaAba.png'))

        bEnviar = QPushButton('Enviar')
        bEnviar.setStyleSheet(ColorBotones)
        bEnviar.setFont(QFont('SansSerif',10))

        tEnviar = QLineEdit()
        tEnviar.setStyleSheet(ColorBotones)
        tEnviar.setFont(QFont('SansSerif',10))
        

        #shortcut
        sConectar = QShortcut(QKeySequence("Enter"),WFrame)
        sConectar.activated.connect(self.conectarArduino)
            
        #LAYOUUT
        layout.addWidget(titulo,0,1)
        layout.addWidget(cicata,0,0)
        layout.addWidget(bConectar,1,0)
        layout.addWidget(tPuerto,1,1)
        layout.addWidget(BFrame,3,0)
        layout.addWidget(ZFrame,3,1)
        blayout.addWidget(bArriba,0,1)
        blayout.addWidget(bAbajo,1,1)
        blayout.addWidget(bDerecha,1,2)
        blayout.addWidget(bIzquierda,1,0)
        blayout.addWidget(lXY,0,0)
        zlayout.addWidget(lz,0,0)
        zlayout.addWidget(bArribaZ,0,1)
        zlayout.addWidget(bAbajoZ,1,1)
        zlayout.addWidget(tEnviar,0,2)
        zlayout.addWidget(bEnviar,1,2)
         
        WFrame.setFixedSize(layout.sizeHint()) 
        self.setFixedSize(layout.sizeHint()) 

    def conectarArduino(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("conectando")
        msgBox.setWindowTitle("QMessageBox Example")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msgBox.buttonClicked.connect(self.msgButtonClick)
        returnValue = msgBox.exec()

        if returnValue == QMessageBox.Ok:
            print('OK clicked')
                         
    def msgButtonClick(self,i):
        print("Button clicked is:",i.text())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
