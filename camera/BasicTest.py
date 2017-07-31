import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

camera = PiCamera()
rawCapture = PiRGBArray(camera)

time.sleep(0.1)


while(True):
	camera.capture(rawCapture, format="bgr")
	frame = rawCapture.array

	cv2.imshow("Frame", frame)

camera.release()

