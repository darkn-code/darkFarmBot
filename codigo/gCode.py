import csv
import serial
import numpy as np
import cv2
import time
import argparse
from threading import Thread
import sys
arduinoString = []

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
    try:
        arduino = serial.Serial('/dev/ttyACM0',115200)
    except:
        print('No se pudo conectar al arduino')
    
    argv = sys.argv
    argparser = argparse.ArgumentParser()
    argparser.add_argument("gcode_dir",nargs='?')
    args = argparser.parse_args(argv[1:])
    filename = args.gcode_dir
    filename = './gcode/' + filename + '.csv'
    ejecutarGcode()
    arduino.close()
