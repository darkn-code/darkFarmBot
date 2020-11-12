import cv2 as cv
import numpy as np
import time
import glob
import serial
from threading import Thread

def video():
    global frame
    camara = cv.VideoCapture(0)
    while isRun:
        ret, frame = camara.read()
        if ret:
            cv.imshow('calibar',frame)
        if cv.waitKey(1) & 0XFF == ord('q'):
            break
    camara.release()

def calibrarCamara(path):
    criterio = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    
    objp = np.zeros((6*7,3),np.float32)
    objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)
    global gris 
    images = glob.glob(path)
    print(images)
    objpoints = []
    imgpoints = []
    for image in images:
        img = cv.imread(image)
        gris = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
        ret,corners = cv.findChessboardCorners(gris,(7,6),None)
        if ret:
            objpoints.append(objp)
            corners2 = cv.cornerSubPix(gris,corners,(11,11),(-1,-1),criterio)
            imgpoints.append(corners)
            cv.drawChessboardCorners(img,(7,6),corners2,ret)
            cv.imwrite('img.png',img)
            cv.waitKey(500)
    ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gris.shape[::-1], None, None)
    return mtx,dist

def resultadoCalibrado(imageName,path,isUndistort,mtx,dist):
    img = cv.imread(path)
    h,  w = img.shape[:2]
    newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
    
    if isUndistort:
        dst = cv.undistort(img, mtx, dist, None, newcameramtx)
    else:
        mapx, mapy = cv.initUndistortRectifyMap(mtx, dist, None, newcameramtx, (w,h), 5)
        dst = cv.remap(img, mapx, mapy, cv.INTER_LINEAR)
    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]
    cv.imwrite(imageName, dst)


def realizarMovimiento(arduino,movimiento):
    arduino.write(movimiento.encode())
    arduino.reset_input_buffer()
    data = 'R00'
    while data[0:3] != 'R02':
        arduinoString = arduino.readline()
        data = arduinoString.decode('utf-8',errors='replace')
        print(data)

def IrAPosicion(pos):
    posicion = 'G0 X' + str(pos[0]) +' Y'+ str(pos[1]) +' Z' + str(pos[2]) +'\r\n'
    return posicion


if __name__ == '__main__':
    global arduino
    isRun = True
    port = '/dev/ttyACM0'
    baud = 115200
    posiciones = [[450,300,200],[450,450,200],[450,150,200],[600,300,200],[300,300,200]]
    try:
        arduino = serial.Serial(port,baud)
    except:
        print('no se puede conectar')
        IsRun = False
    time.sleep(1)
    thread = Thread(target=video)
    thread.start()
    #posInit = IrAPosicion([0,0,200])
    #realizarMovimiento(arduino,posInit)
    #posCalibracion = IrAPosicion([450,300,200])
    #realizarMovimiento(arduino,posCalibracion)
    IsReady = 'y'
    num = 0
    if IsReady == 'y':
        path = '/home/darkfarmbot/Desktop/darkFarmbot/calibrarParametros/'
        #for posicion in posiciones:
         #   pos = IrAPosicion(posicion)
          #  realizarMovimiento(arduino,pos)
           #  time.sleep(1)
          #  nombreImagen = path + 'imagen{0}.0.png'.format(num)
           # cv.imwrite(nombreImagen,frame)
            #time.sleep(1)
            #nombreImagen = path + 'imagen{0}.1.png'.format(num)
            #cv.imwrite(nombreImagen,frame)
            #num += 1
        path = path + '*.png'
        mtx,dist = calibrarCamara(path)
        np.savetxt('mtx.txt',mtx,fmt='%d')
        np.savetxt('dist.txt',dist,fmt='%d')
        mtx = np.loadtxt('mtx.txt',dtype=int)
        dist = np.loadtxt('dist.txt',dtype=int)
        resultadoCalibrado('resultado1.png','/home/darkfarmbot/Desktop/darkFarmbot/calibrarParametros/imagen0.0.png',False,mtx,dist)
    isRun = False
    arduino.close()
    cv.destroyAllWindows
