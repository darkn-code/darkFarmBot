from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from threading import Thread
import serial
import time
import sys

from codigo.arduino import *
from codigo.FuncionesRobot import *

colorLetra = "color:#419f00;"
ColorBotones = "color:white;"
border = "border: 0px solid black;"
fondo = "background-color:#203500;" + ColorBotones 
borderG = 'border:2px solid white;'
letraTexto = QFont('SansSerif',10)
letraTextoBold = QFont('SansSerif',10,QFont.Bold)
letraTitulo = QFont('SansSerif',15,QFont.Bold)

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.port = ''
        self.isRun = True
        self.setWindowTitle("Farmbot Chile Habanero")
        self.setStyleSheet(fondo)

        #Creacion Widget
        win = QWidget(self)
        gridLayout = QGridLayout()
        win.setLayout(gridLayout)

        Header = QFrame()
        Body = QFrame()
        Footer = QGroupBox('Camara')
        self.estiloLetraBlanco(Footer)
        
        gridLayout.setVerticalSpacing(0)
        gridLayout.addWidget(Header,0,0)
        gridLayout.addWidget(Body,1,0)
        gridLayout.addWidget(Footer,2,0)

        HLayout = QHBoxLayout()
        Header.setLayout(HLayout)
     
        fModoManual = QGroupBox('MODO MANUAL')
        fModoManual.setFont(letraTextoBold)
        fModoManual.setStyleSheet(ColorBotones)
        
        fModoAuto = QGroupBox('MODO AUTOMATICO')
        fModoAuto.setFont(letraTextoBold)
        fModoAuto.setStyleSheet(ColorBotones)
        
        BodyLayout = QGridLayout()
        Body.setLayout(BodyLayout)

        BodyLayout.addWidget(fModoManual,0,0)
        BodyLayout.addWidget(fModoAuto,1,0)

        CLayout = QHBoxLayout()
        Footer.setLayout(CLayout)
        
        #Modo manual
        FEnviarDatos = QFrame()
        FControles = QFrame()
        FDatos = QFrame()
        FBotones = QFrame()

        DLayout = QVBoxLayout()
        FDatos.setLayout(DLayout)

        BLayout = QHBoxLayout()
        FBotones.setLayout(BLayout)

        FALayout = QGridLayout()
        FEnviarDatos.setLayout(FALayout)

        Mlayout = QGridLayout()
        fModoManual.setLayout(Mlayout)
        
        Mlayout.setVerticalSpacing(0)
        Mlayout.addWidget(FEnviarDatos,2,0)
        Mlayout.addWidget(FControles,0,0)
        Mlayout.addWidget(FDatos,1,0)
        Mlayout.addWidget(FBotones,3,0)

        LFrame = QGroupBox("XY")
        self.estiloLetraBlanco(LFrame)
        MFrame = QGroupBox("Z")
        self.estiloLetraBlanco(MFrame)
        RFrame = QGroupBox("Arduino")
        self.estiloLetraBlanco(RFrame)

        FLayout = QGridLayout()
        FControles.setLayout(FLayout)

        FLayout.addWidget(LFrame,0,1)
        FLayout.addWidget(MFrame,0,2)
        FLayout.addWidget(RFrame,0,0)

        ZLayout = QGridLayout()
        MFrame.setLayout(ZLayout)
        
        ArLayout = QGridLayout()
        RFrame.setLayout(ArLayout)

        layout = QGridLayout()
        LFrame.setLayout(layout)

        #modo automatico
        ALayout = QHBoxLayout()
        fModoAuto.setLayout(ALayout)

        #Imagen cicata
        cicata = QLabel(self)
        pixmap2 = QPixmap('./pictures/cicata.png')
        cicata.setPixmap(pixmap2)
        #cicata.setAlignment(Qt.AlignCenter)

        #titulo Header
        titulo = QLabel()
        titulo.setText("FarmBot Chile Habanero")
        titulo.setFont(letraTitulo)
        titulo.setStyleSheet(colorLetra)
        
        #Modo manual
        self.bConectar = QPushButton("Conectar")
        self.bConectar.clicked.connect(self.conectarArduino)
        self.estiloLetraBlanco(self.bConectar)

        tPuerto = QLineEdit("/dev/ttyACM0")
        self.port = tPuerto.text()
        self.estiloLetraBlanco(tPuerto)

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

        bLuz = QPushButton('Luz')
        self.estiloLetraBlanco(bLuz)
        
        bAgua = QPushButton('Agua')
        self.estiloLetraBlanco(bAgua)
         
        bVacio = QPushButton('Bomba Vacio')
        self.estiloLetraBlanco(bVacio)
      
        bEnviar = QPushButton('Enviar')
        bEnviar.clicked.connect(self.mandarDatos)
        self.estiloLetraBlanco(bEnviar)

        bRegar = QPushButton('Regar')
        self.estiloLetraBlanco(bRegar)

        bSembrar = QPushButton('Sembrar')
        self.estiloLetraBlanco(bSembrar)

        bHumedad = QPushButton('Humedad')
        bHumedad.clicked.connect(self.getInteger)
        self.estiloLetraBlanco(bHumedad)
        
        bCamara = QPushButton('Camara')
        self.estiloLetraBlanco(bCamara)

        bAi = QPushButton('AI')
        self.estiloLetraBlanco(bAi)
        
        self.tData = QLineEdit('Data del Arduino')
        self.tData.setReadOnly(True)
        self.estiloLetraBlanco(self.tData)

        tEnviar = QLineEdit()
        self.estiloLetraBlanco(tEnviar)
        

        #shortcut
        sConectar = QShortcut(QKeySequence("Enter"),win)
        sConectar.activated.connect(self.mandarDatos)
            
        #LAYOUUT
        HLayout.addWidget(cicata)
        HLayout.addWidget(titulo)
        
        ArLayout.addWidget(tPuerto,0,0)
        ArLayout.addWidget(self.bConectar,1,0)

        layout.setVerticalSpacing(0)
        layout.setHorizontalSpacing(0)
        layout.addWidget(bArriba,0,1)
        layout.addWidget(bAbajo,1,1)
        layout.addWidget(bDerecha,1,2)
        layout.addWidget(bIzquierda,1,0)
        
        ZLayout.setVerticalSpacing(0)
        ZLayout.addWidget(bArribaZ,0,0)
        ZLayout.addWidget(bAbajoZ,1,0)

        DLayout.addWidget(self.tData)
        
        FALayout.addWidget(bEnviar,0,1)
        FALayout.addWidget(tEnviar,0,0)
        
        BLayout.addWidget(bLuz)
        BLayout.addWidget(bAgua)
        BLayout.addWidget(bVacio)
        
        ALayout.addWidget(bRegar)
        ALayout.addWidget(bSembrar)
        ALayout.addWidget(bHumedad)

        CLayout.addWidget(bCamara)
        CLayout.addWidget(bAi)


        win.setFixedSize(gridLayout.sizeHint())
        self.setFixedSize(gridLayout.sizeHint()) 

    def getInteger(self):
        ventanaDialogo = QInputDialog()
        i,okPressed = ventanaDialogo.getInt(self,"Posicion","X:",100,0,500,1)
        if okPressed:
            print(i)


    def estiloLetraBlanco(self,widget):
        widget.setStyleSheet(ColorBotones)
        widget.setFont(letraTexto)
    
    def mandarDatos(self):
        dato = self.tData.text()
        self.farmbot.enviarDatos(dato+'\r\n')

    def leerDatos(self):
        time.sleep(1.0)
        self.farmbot.reinicarBuffer()
        while self.isRun:
            self.arduinoString = self.farmbot.recibirDatos()
            self.data = self.arduinoString.decode('utf-8',errors='replace')
            self.tData.setText(self.data)


    def conectarArduino(self):
        print(self.port)
        if self.bConectar.text() == 'Conectar':
            try:
                self.isRun = True
                self.farmbot = arduino(self.port)
                self.thread = Thread(target=leerDatos)
                self.thread.start()
                self.bConectar.setText('Desconectar')
                self.bConectar.setStyleSheet('color:red')
            except:
                print('No se pudo coenctar al arduino')
        else:
            self.isRun = False
            self.farmbot.close()
            self.bConectar.setText('Conectar')
            self.bConectar.setStyleSheet(ColorBotones)
                    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    main.isRun = False
    main.farmbot.close()
    sys.exit(app.exec_())
