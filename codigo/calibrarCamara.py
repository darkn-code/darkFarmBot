import cv2 as cv
import numpy as np
import time
import glob
import serial
from threading import Thread
from tomarImagen import IrAPosicion
from tomarImatgen import realizarMovimiento


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
    
    images = glob.glob(path)
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



if __name__ == '__main__':
    isRun = True
    thread = Thread(target=video)
    thread.start()
    port = '/dev/ttyACM0'
    baud = 115200i
    posiciones = [[450,300,300],[450,450,300],[450,150,300],[600,300,300],[300,300,300]]
    try:
        arduino = serial.Serial(port,baud)
    except:
        print('no se puede conectar')
        IsRun = False

    posInit = IrAPosicion([0,0,300])
    realizarMovimiento(posInit)
    posCalibracion = IrAPosicion([450,300,300])
    realizarMovimiento(posCalibracion)
    IsReady = input('Esta listo? ')
    num = 0
    if IsReady == 'y':
        path = '/home/darkfarmbot/Desktop/darkFarmbot/calibarParametros/'
        for posicion in posiciones:
            pos = IrAPosicion(posicion)
            realizarMovimiento(pos)
            time.sleep(1)
            nombreImagen = path + 'imagen{0}.0.png'.format(num)
            cv.imwrite(nombreImagen,frame)
            timesleep(1)
            nombreImagen = path + 'imagen{0}.1.png'.format(num)
            cv.imwrite(nombreImagen,frame)
            num += 1
        path = './calibrarParametros/*.png'
        mtx,dist = calibrarCamara(path)
        np.savetxt('./calibrarParametros/mtx.txt',mtx,fmt='%d')
        np.savetxt('./calibrarParametros/dist.txt',dist,fmt='%d')
        mtx = np.loadtxt('mtx.txt',dtype=int)
        dist = np.loadtxt('dist.txt',dtype=int)
        resultadoCalibrado('resultado1.png','./calibrarParametros/imagenR.png',False,mtx,dist)
    isRun = False
    cv.destroyAllWindows
