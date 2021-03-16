from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from threading import Thread
import serial
import time
import sys
import os

from codigo.arduino import *
from codigo.FuncionesRobot import *

colorLetra = "color:#419f00;"
ColorBotones = "color:white;"
ColorRojo = 'color:red;'
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
        self.step = 20
        self.x = 0
        self.y = 0
        self.z = 0
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

        self.tPuerto = QLineEdit("/dev/ttyACM0")
        self.estiloLetraBlanco(self.tPuerto)

        bArriba = QPushButton()
        bArriba.setIcon(QIcon('./pictures/flechaArr.png'))
        bArriba.clicked.connect(self.moverXPositivo)
        bAbajo = QPushButton()
        bAbajo.setIcon(QIcon('./pictures/flechaAba.png'))
        bAbajo.clicked.connect(self.moverXNegativo)
        bDerecha = QPushButton()
        bDerecha.setIcon(QIcon('./pictures/flechaDer.png'))
        bDerecha.clicked.connect(self.moverYPositivo)
        bIzquierda = QPushButton()
        bIzquierda.setIcon(QIcon('./pictures/flechaIzq.png'))
        bIzquierda.clicked.connect(self.moverYNegativo)
        
        bArribaZ = QPushButton()
        bArribaZ.setIcon(QIcon('./pictures/flechaArr.png'))
        bArribaZ.clicked.connect(self.moverZPositivo)
        bAbajoZ = QPushButton()
        bAbajoZ.setIcon(QIcon('./pictures/flechaAba.png'))
        bAbajoZ.clicked.connect(self.moverZNegativo)

        self.bLuz = QPushButton('Luz')
        self.bLuz.clicked.connect(self.PinLuz)
        self.estiloLetraBlanco(self.bLuz)
        
        self.bAgua = QPushButton('Agua')
        self.bAgua.clicked.connect(self.PinAgua)
        self.estiloLetraBlanco(self.bAgua)
         
        self.bVacio = QPushButton('Bomba Vacio')
        self.bVacio.clicked.connect(self.PinBombaVacio)
        self.estiloLetraBlanco(self.bVacio)
      
        bEnviar = QPushButton('Enviar')
        bEnviar.clicked.connect(self.mandarDatos)
        self.estiloLetraBlanco(bEnviar)

        bRegar = QPushButton('Regar')
        bRegar.clicked.connect(self.mRegar)
        self.estiloLetraBlanco(bRegar)

        bSembrar = QPushButton('Sembrar')
        bSembrar.clicked.connect(self.mSembrar)
        self.estiloLetraBlanco(bSembrar)

        bHumedad = QPushButton('Humedad')
        bHumedad.clicked.connect(self.mHumedad)
        self.estiloLetraBlanco(bHumedad)
        
        bCamara = QPushButton('Camara')
        bCamara.clicked.connect(self.mCamara)
        self.estiloLetraBlanco(bCamara)

        bAi = QPushButton('AI')
        self.estiloLetraBlanco(bAi)
        
        self.tData = QLineEdit('Data del Arduino')
        self.tData.setReadOnly(True)
        self.estiloLetraBlanco(self.tData)

        self.tEnviar = QLineEdit()
        self.estiloLetraBlanco(self.tEnviar)
        

        #shortcut
        sConectar = QShortcut(QKeySequence("C"),win)
        sConectar.activated.connect(self.conectarArduino)
        
        sLuz = QShortcut(QKeySequence('L'),win)
        sLuz.activated.connect(self.PinLuz)
        
        sAgua = QShortcut(QKeySequence('K'),win)
        sAgua.activated.connect(self.PinAgua)
        
        sBomba = QShortcut(QKeySequence('J'),win)
        sBomba.activated.connect(self.PinBombaVacio)

        sRegar = QShortcut(QKeySequence('B'),win)
        sRegar.activated.connect(self.mRegar)
        
        sSembrar = QShortcut(QKeySequence('N'),win)
        sSembrar.activated.connect(self.mSembrar)
        
        sHumedad = QShortcut(QKeySequence('M'),win)
        sHumedad.activated.connect(self.mHumedad)
        
        sCamara = QShortcut(QKeySequence('Z'),win)
        sCamara.activated.connect(self.mCamara)
        
        sMandarDatos = QShortcut(QKeySequence("Enter"),win)
        sMandarDatos.activated.connect(self.mandarDatos)

        sMoverXPos = QShortcut(QKeySequence('W'),win)
        sMoverXPos.activated.connect(self.moverXPositivo)
        
        sMoverXNeg = QShortcut(QKeySequence('S'),win)
        sMoverXNeg.activated.connect(self.moverXNegativo)
        
        sMoverYPos = QShortcut(QKeySequence('D'),win)
        sMoverYPos.activated.connect(self.moverYPositivo)
        
        sMoverYNeg = QShortcut(QKeySequence('A'),win)
        sMoverYNeg.activated.connect(self.moverYNegativo)
        
        sMoverZPos = QShortcut(QKeySequence('R'),win)
        sMoverZPos.activated.connect(self.moverZPositivo)
        
        sMoverZNeg = QShortcut(QKeySequence('F'),win)
        sMoverZNeg.activated.connect(self.moverZNegativo)
            
        #LAYOUUT
        HLayout.addWidget(cicata)
        HLayout.addWidget(titulo)
        
        ArLayout.addWidget(self.tPuerto,0,0)
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
        FALayout.addWidget(self.tEnviar,0,0)
        
        BLayout.addWidget(self.bLuz)
        BLayout.addWidget(self.bAgua)
        BLayout.addWidget(self.bVacio)
        
        ALayout.addWidget(bRegar)
        ALayout.addWidget(bSembrar)
        ALayout.addWidget(bHumedad)

        CLayout.addWidget(bCamara)
        CLayout.addWidget(bAi)


        win.setFixedSize(gridLayout.sizeHint())
        self.setFixedSize(gridLayout.sizeHint()) 

    def getInteger(self,varName='x'):
        ventanaDialogo = QInputDialog()
        i,okPressed = ventanaDialogo.getInt(self,"Posicion",f"{varName}:",100,0,500,1)
        if okPressed:
            print(i)
            return i

    def moverXPositivo(self):
        self.x = self.x + self.step
        if self.x <= 900:
            self.moverPos()
        else:
            self.x = 900
            print('se excedio de los limites')
        
    def moverXNegativo(self):
        self.x = self.x - self.step
        if self.x >= 0:
            self.moverPos()
        else:
            self.x = 0
            print('se excedio de los limites')
   
    def moverYPositivo(self):
        self.y = self.y + self.step
        if self.y <= 600:
            self.moverPos()
        else:
            self.y = 600
            print('se excedio de los limites')
    
    def moverYNegativo(self):
        self.y = self.y - self.step
        if self.y >= 0:
            self.moverPos()
        else:
            self.y = 0
            print('se excedio de los limites')
    
    def enviarFarmbot(self,mensaje): 
        self.farmbot.enviarDatos(mensaje)
        self.tData.setText(mensaje)

    def PinLuz(self):
        if self.bLuz.text() == 'Luz':
            self.bLuz.setText('Apagar Luz')
            self.bLuz.setStyleSheet(ColorRojo)
            valorPin = DarValorPin(9,1,0)
            self.enviarFarmbot(valorPin)
        else:
            self.bLuz.setStyleSheet(ColorBotones)
            self.bLuz.setText('Luz') 
            valorPin = DarValorPin(9,0,0)
            self.enviarFarmbot(valorPin)
    
    def PinAgua(self):
        if self.bAgua.text() == 'Agua':
            self.bAgua.setText('Apagar Agua')
            self.bAgua.setStyleSheet(ColorRojo)
            valorPin = DarValorPin(8,1,0)
            self.enviarFarmbot(valorPin)
        else:
            self.bAgua.setStyleSheet(ColorBotones)
            self.bAgua.setText('Agua') 
            valorPin = DarValorPin(8,0,0)
            self.enviarFarmbot(valorPin)
    
    def PinBombaVacio(self):
        if self.bVacio.text() == 'Bomba Vacio':
            self.bVacio.setText('Apagar Bomba')
            self.bVacio.setStyleSheet(ColorRojo)
            valorPin = DarValorPin(10,1,0)
            self.enviarFarmbot(valorPin)
        else:
            self.bVacio.setStyleSheet(ColorBotones)
            self.bVacio.setText('Bomba Vacio') 
            valorPin = DarValorPin(10,0,0)
            self.enviarFarmbot(valorPin)

    def moverZPositivo(self):
        self.z = self.z + self.step
        if self.z <= 300:
            self.moverPos()
        else:
            self.z = 300
            print('se excedio de los limites')
    def moverZNegativo(self):
        self.z = self.z - self.step
        if self.z >= 0:
            self.moverPos()
        else:
            self.z = 0
            print('se excedio de los limites')

    def moverPos(self):
            posicion = IrAPosicion([self.x,self.y,self.z])
            self.enviarFarmbot(posicion)

    def estiloLetraBlanco(self,widget):
        widget.setStyleSheet(ColorBotones)
        widget.setFont(letraTexto)
    
    def mandarDatos(self):
        dato = self.tEnviar.text() +'\r\n'
        self.enviarFarmbot(dato)

    def leerDatos(self):
        time.sleep(1.0)
        self.farmbot.reinicarBuffer()
        while self.isRun:
            self.arduinoString = self.farmbot.recibirDatos()
            self.data = self.arduinoString.decode('utf-8',errors='replace')
            print(self.data)

        self.farmbot.arduino.close()

    def llamarArchivo(self,nombreDeCodigo,pCodigo='',dirA='.'):
        try:
            self.farmbot.arduino.close()
            print('Puerto de arduino cerrado')
        except:
            print('El puerto de arduino ya esta cerrado')
        print(nombreDeCodigo)
        os.system(pCodigo+f'python3 {dirA}/codigo/{nombreDeCodigo}')
    
    def mRegar(self):
        self.llamarArchivo('gCode.py regar')

    def mSembrar(self):
        self.llamarArchivo('gCode.py sembrar')
    
    def mHumedad(self):
        x = self.getInteger()
        y = self.getInteger('y')
        self.llamarArchivo(f'FuncionesRobot.py --x-value={x} --y-value={y}','cd ~;','Desktop/darkFarmbot')

    def mCamara(self):
        self.llamarArchivo('AperturaDeCamara.py')
    
    def closeEvent(self,event):
        self.isRun = False
        print("Estoy cerrando el programa")
        time.sleep(0.5)


    def conectarArduino(self):
        self.port = self.tPuerto.text()
        print(self.port)
        if self.bConectar.text() == 'Conectar':
            try:
                self.isRun = True
                self.farmbot = arduino(self.port)
                self.thread = Thread(target=self.leerDatos)
                self.thread.start()
                self.bConectar.setText('Desconectar')
                self.bConectar.setStyleSheet(ColorRojo)
            except Exception as e:
                print(e)
        else:
            self.isRun = False
            self.bConectar.setText('Conectar')
            self.bConectar.setStyleSheet(ColorBotones)
                    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
