from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys

fondo = "background-color:#203500;"
colorLetra = "color:#419f00;"
ColorBotones = "color:white;"
border = "border: 0px solid black;"
borderG = 'border:2px solid white;'
letraTexto = QFont('SansSerif',10)
letraTextoBold = QFont('SansSerif',10,QFont.Bold)

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()  
        self.setWindowTitle("Farmbot Chile Habanero")
        self.setStyleSheet(fondo)

        #Creacion Widget
        win = QWidget(self)
        gridLayout = QGridLayout()
        win.setLayout(gridLayout)

        Header = QFrame()
        Body = QFrame()
        Footer = QFrame()

        gridLayout.addWidget(Header,0,0)
        gridLayout.addWidget(Body,1,0)
        gridLayout.addWidget(Footer,2,0)

        HLayout = QGridLayout()
        Header.setLayout(HLayout)
     
        fModoManual = QGroupBox('MODO MANUAL')
        fModoManual.setFont(letraTexto)
        fModoManual.setStyleSheet(ColorBotones)
        
        fModoAuto = QGroupBox('MODO AUTOMATICO')
        fModoAuto.setFont(letraTexto)
        fModoAuto.setStyleSheet(ColorBotones)
        
        BodyLayout = QGridLayout()
        Body.setLayout(BodyLayout)

        BodyLayout.addWidget(fModoManual,0,0)
        BodyLayout.addWidget(fModoAuto,1,0)

        FArduino = QFrame()
        FControles = QFrame()
        FBotones = QFrame()

        FALayout = QGridLayout()
        FArduino.setLayout(FALayout)

        Mlayout = QGridLayout()
        fModoManual.setLayout(Mlayout)
        
        Mlayout.addWidget(FArduino,0,0)
        Mlayout.addWidget(FControles,1,0)
        Mlayout.addWidget(FBotones,2,0)

        LFrame = QGroupBox("XY")
        LFrame.setFont(letraTexto)
        LFrame.setStyleSheet(ColorBotones)
        MFrame = QGroupBox("Z")
        MFrame.setFont(letraTexto)
        MFrame.setStyleSheet(ColorBotones)
        RFrame = QGroupBox("Enviar datos")
        RFrame.setFont(letraTexto)
        RFrame.setStyleSheet(ColorBotones)

        FLayout = QGridLayout()
        FControles.setLayout(FLayout)

        FLayout.addWidget(LFrame,0,0)
        FLayout.addWidget(MFrame,0,1)
        FLayout.addWidget(RFrame,0,2)

        ZLayout = QGridLayout()
        MFrame.setLayout(ZLayout)
        
        EnvDatos = QGridLayout()
        RFrame.setLayout(EnvDatos)

        layout = QGridLayout()
        LFrame.setLayout(layout)

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
        
        #Modo manual
        bConectar = QPushButton("Conectar")
        bConectar.setStyleSheet(ColorBotones)
        bConectar.setFont(letraTexto)
        bConectar.clicked.connect(self.conectarArduino)

        tPuerto = QLineEdit("/dev/ttyACM0")
        tPuerto.setStyleSheet(ColorBotones)
        tPuerto.setFont(letraTexto)

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
        bEnviar.setFont(letraTexto)

        tEnviar = QLineEdit()
        tEnviar.setStyleSheet(ColorBotones)
        tEnviar.setFont(letraTexto)
        

        #shortcut
        sConectar = QShortcut(QKeySequence("Enter"),win)
        sConectar.activated.connect(self.conectarArduino)
            
        #LAYOUUT
        HLayout.addWidget(cicata,0,0)
        HLayout.addWidget(titulo,0,1)

        FALayout.addWidget(bConectar,0,0)
        FALayout.addWidget(tPuerto,0,1)
        
        layout.addWidget(bArriba,0,1)
        layout.addWidget(bAbajo,1,1)
        layout.addWidget(bDerecha,1,2)
        layout.addWidget(bIzquierda,1,0)

        ZLayout.addWidget(bArribaZ,0,0)
        ZLayout.addWidget(bAbajoZ,1,0)

        EnvDatos.addWidget(tEnviar,0,0)
        EnvDatos.addWidget(bEnviar,1,0)
         
        win.setFixedSize(gridLayout.sizeHint())
        self.setFixedSize(gridLayout.sizeHint()) 

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
