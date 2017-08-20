import argparse
import time
import cv2

from camera.TrackingTagFinder import TrackingTagFinder
from camera.VideoStream import VideoStream

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--picamera", type=int, default=-1, help="whether or not the Raspberry Pi camera should be used")
args = vars(ap.parse_args())

# vs = VideoStream(usePiCamera=args["picamera"] > 0, src="../test-data/calibration-2-4-cars.mov").start()
vs = VideoStream(usePiCamera=args["picamera"] > 0, src="../test-data/capture4.mov").start()
time.sleep(2.0)

while (True):
    frame = vs.read()
    print frame
    if frame is None:
        break
    cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

# finder = TrackingTagFinder(vs)
# tracking_tags = finder.find_tracking_tags()
#
# finder.save_tracking_tags_csv(tracking_tags, "tracking-tags.csv")
#
vs.stop()
