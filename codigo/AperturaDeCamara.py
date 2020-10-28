import numpy as np 
import cv2
import os

cap = cv2.VideoCapture(0)#identificador de la camara
while (True):
 	#capturar frame por frame
 	ret,frame = cap.read()

 	#operacion que se realiza a cada frame
 	frameR = cv2.resize(frame,(700,500))

 	#Se muestra cada frame
 	cv2.imshow('chile',frameR)
 	if cv2.waitKey(1) & 0xff == ord('q'):
            path ='Desktop/darkfarmbot/imagenes'
            cv2.imwrite('/home/darkfarmbot/Desktop/darkFarmbot/test.png',frameR)
            cv2.waitKey(0)
            break

#librero memoria
cap.release()
cv2.destroyAllWindows
 	
