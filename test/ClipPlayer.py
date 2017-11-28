import argparse
import time
import cv2

from imutils.video import VideoStream

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--picamera", type=int, default=-1, help="whether or not the Raspberry Pi camera should be used")
args = vars(ap.parse_args())
vs = VideoStream(usePiCamera=args["picamera"] > 0, src="../test-data/3-cars.avi").start()

while True:
    frame = vs.read()
    if frame is None:
        break

    cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

cv2.destroyAllWindows()