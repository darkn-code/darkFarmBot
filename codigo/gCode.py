import csv
import serial
import numpy as np
import cv2
import time
from threading import Thread

arduinoString = []

def leerDatos():

    time.sleep(1.0)
    arduino.reset_input_buffer()
    while isRun:
        arduinoString = arduino.readline()
        print(arduinoString)

def ejecutarGcode():
    with open(filename,mode='r') as f:
        reader = csv.reader(f,delimiter=' ')
        arduino.reset_input_buffer()
        for row in reader:
            arduino.write((' '.join(row)+'\r\n').encode())
            arduinoString = arduino.readline()
            data = arduinoString.decode('utf-8',errors='replace')
            while data[0:3] != 'R02' :
                arduinoString = arduino.readline()
                data = arduinoString.decode('utf-8',errors='replace')
                print(data)
            
if __name__ == '__main__':
    global filename
    isRun = True
    try:
        arduino = serial.Serial('/dev/ttyACM0',115200)
    except:
        print('No se pudo conectar al arduino')

    filename = input('Nombre del archivo Gcode: ')
    filename = 'Desktop/darkFarmbot/gcode/' + filename + '.csv'
    #thread = Thread(target=leerDatos)
    #thread.start()
    ejecutarGcode()
    isRun = False
    #thread.join()
    arduino.close()

