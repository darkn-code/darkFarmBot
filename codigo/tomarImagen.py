import numpy as np 
import cv2 
import datetime
import serial
import time
from threading import Thread

h = 0
planta_1 = [190,125,h]
planta_2 = [190,585,h]
planta_3 = [550,585,h]
planta_4 = [550,125,h]
planta_5 = [870,160,h]
planta_6 = [920,585,h]

plantas = [planta_1,planta_4,planta_5,planta_6,planta_3,planta_2]


def IrAPosicion(pos):
    posicion = 'G0 X' + str(pos[0]) +' Y'+ str(pos[1]) +' Z' + str(pos[2]) +'\r\n'
    return posicion


def realizarMovimiento(arduino,movimiento):
    arduino.write(movimiento.encode())
    arduino.reset_input_buffer()
    data = 'R00'
    while data[0:3] != 'R02':
        arduinoString = arduino.readline()
        data = arduinoString.decode('utf-8',errors='replace')
        #print(data)

def video():
    global frame
    camara = cv2.VideoCapture(0)
    while isRun:
        ret, frame = camara.read()
        frameR = cv2.resize(frame,(700,500))
        #cv2.imshow('planta',frameR)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    camara.release()

if __name__ == '__main__':
    isRun = True
    try:
        arduino = serial.Serial('/dev/ttyACM0',115200)
    except:
        print('no se puede conectar con el arduino')
    time.sleep(1.0)
    
    thread = Thread(target=video)
    thread.start()

    num_planta = 0
    arr_planta =[1,4,5,6,3,2]
    realizarMovimiento(arduino,'F22 P17 V1\r\n')
    realizarMovimiento(arduino,'G0 X100\r\n')
    
    for planta in plantas:
        #if num_planta == 3:
           # posBajada = IrAPosicion([970,160,250])
           # realizarMovimiento(arduino,posBajada)
           # posBajada = IrAPosicion([970,585,250])
           # realizarMovimiento(arduino,posBajada)
        posNueva = IrAPosicion(planta)
        realizarMovimiento(arduino,posNueva)
        path = '/home/darkfarmbot/Desktop/darkFarmbot/imagenes/'
        nombre = 'planta_' + str(arr_planta[num_planta]) + '-' + datetime.datetime.now().strftime('%d-%m-%y') + '.jpg'
        num_planta += 1
        #cv2.imshow(nombre,frame)
        nombre = path + nombre
        cv2.imwrite(nombre,frame)
    
    realizarMovimiento(arduino,'G0 X200 Y585 Z0\r\n')
    realizarMovimiento(arduino,'G0 X200 Z0\r\n')
    realizarMovimiento(arduino,'G0 X200\r\n')
    realizarMovimiento(arduino,'G0\r\n')
    realizarMovimiento(arduino,'F22 P17 V0\r\n')
    isRun = False
    thread.join()
    cv2.destroyAllWindows
    arduino.close()
