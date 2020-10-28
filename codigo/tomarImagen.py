import numpy as np 
import cv2 
import datetime
import serial
import time
from threading import Thread

planta_1 = [190,125,0]
planta_2 = [190,585,0]
planta_3 = [530,585,0]
planta_4 = [530,125,0]
planta_5 = [870,125,0]
planta_6 = [870,585,0]

plantas = [planta_1,planta_2,planta_3,planta_4,planta_5,planta_6]


def IrAPosicion(pos):
    posicion = 'G0 X' + str(pos[0]) +' Y'+ str(pos[1]) +' Z' + str(pos[2]) +'\r\n'
    return posicion


def realizarMovimiento(movimiento):
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
    realizarMovimiento('G0 X100\r\n')
    
    for planta in plantas:
        posNueva = IrAPosicion(planta)
        realizarMovimiento(posNueva)
        num_planta += 1
        path = '/home/darkfarmbot/Desktop/darkFarmbot/imagenes/'
        nombre = 'planta_' + str(num_planta) + '-' + datetime.datetime.now().strftime('%d-%m-%y') + '.jpg'
        #cv2.imshow(nombre,frame)
        nombre = path + nombre
        cv2.imwrite(nombre,frame)

    realizarMovimiento('G0 X100\r\n')
    realizarMovimiento('G0\r\n')
    isRun = False
    thread.join()
    cv2.destroyAllWindows
    arduino.close()
