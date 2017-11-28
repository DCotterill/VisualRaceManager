# import the necessary packages
from __future__ import print_function
from imutils.video import VideoStream
import numpy as np
import argparse
import imutils
import time
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", required=True,
                help="path to output video file")
ap.add_argument("-p", "--picamera", type=int, default=-1,
                help="whether or not the Raspberry Pi camera should be used")
ap.add_argument("-f", "--fps", type=int, default=20,
                help="FPS of output video")
ap.add_argument("-c", "--codec", type=str, default="MJPG",
                help="codec of output video")
args = vars(ap.parse_args())

# initialize the video stream and allow the camera
# sensor to warmup
print("[INFO] warming up camera...")

usePiCamera = args["picamera"] > 0

# Macbook has wierd camera app installed, so need to set src=1
if usePiCamera:
    src = 0
else:
    src = 1

vs = VideoStream(usePiCamera=usePiCamera, src=src).start()
time.sleep(2.0)

# initialize the FourCC, video writer, dimensions of the frame, and
# zeros array
fourcc = cv2.VideoWriter_fourcc(*args["codec"])
writer = None
(h, w) = (None, None)
zeros = None

# loop over frames from the video stream
while True:
    frame = vs.read()

    # check if the writer is None
    if writer is None:
        # store the image dimensions, initialzie the video writer,
        # and construct the zeros array
        (h, w) = frame.shape[:2]
        writer = cv2.VideoWriter(args["output"], fourcc, args["fps"],
                                 (w, h), True)
        zeros = np.zeros((h, w), dtype="uint8")

    writer.write(frame)

    # show the frames
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

print("[INFO] cleaning up...")
cv2.destroyAllWindows()
vs.stop()
writer.release()