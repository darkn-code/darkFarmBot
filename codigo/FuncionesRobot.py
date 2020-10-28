import numpy as np 
import cv2 
import datetime
import serial
import time
import csv


def IrAPosicion(pos):
    posicion = 'G0 X' + str(pos[0]) +' Y'+ str(pos[1]) +' Z' + str(pos[2]) +'\r\n'
    return posicion

def LeerPin(pin,mode):
    comando = 'F42 P' + str(pin) + ' M' + str(mode) + '\r\n'
    return comando

def DarValorPin(pin,valor,mode):
    comando = 'F41 P' + str(pin) + ' V' + str(valor)  + ' M' + str(mode) + '\r\n'
    return comando

def SetearPin(pin,mode):
    comando = 'F43 P' + str(pin) + ' M' + str(mode) + '\r\n'
    return comando

def DarValorParametro(parametro,valor):
    comando = 'F22 P' + str(parametro) + ' V' + str(valor) + '\r\n'
    return comando

def realizarMovimiento(movimiento):
    arduino.write(movimiento.encode())
    data = 'R00'
    while data[0:3] != 'R02':
        arduinoString = arduino.readline()
        data = arduinoString.decode('utf-8',errors='replace')
        #print(data)

def leerArchivos(nombreArchivo):
    with open(nombreArchivo,mode='r') as f:
        reader = csv.reader(f,delimiter=' ')
        for row in reader:
            realizarMovimiento((' '.join(row)+'\r\n'))

def mapArduino(x,in_min,in_max,out_min,out_max):
    return out_min + (x - in_min) * (out_max - out_min) / (in_max - in_min)


if __name__ == '__main__':
    global arduino
    
    try:
        arduino = serial.Serial('/dev/ttyACM0',115200)
    except:
        print('no se puede conectar con el arduino')
    time.sleep(1.0)
    
    nombreArchivo = '/./gcode/SensorDeHumedad.csv'
    leerArchivos(nombreArchivo)
    x = int(input('valor x: '))
    y = int(input('valor y: '))
    comando = SetearPin(59,0)
    realizarMovimiento(comando)
    comando = IrAPosicion([x,y,2])
    realizarMovimiento(comando)
    comando = IrAPosicion([x,y,-190])
    realizarMovimiento(comando)
    comando = LeerPin(59,1)
    arduino.write(comando.encode())
    data = 'R00'
    while data[0:3] != 'R41':
        arduinoString = arduino.readline()
        data = arduinoString.decode('utf-8',errors='replace')
    dataHumedad = int(data[9:13])
    time.sleep(1.0)
    valorHumedad = mapArduino(dataHumedad,255,580,100,0)
    print(dataHumedad)
    print('humedad Del Suelo {0}%'.format(str(round(valorHumedad,2))))
    comando = IrAPosicion([x,y,2])
    realizarMovimiento(comando)
    nombreArchivo = '/home/darkfarmbot/Desktop/darkFarmbot/regresoHumedad.csv'
    leerArchivos(nombreArchivo)
    arduino.close()
