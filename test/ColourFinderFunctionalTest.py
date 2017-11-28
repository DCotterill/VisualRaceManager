import argparse
import time

from camera.TrackingTagFinder import TrackingTagFinder
from imutils.video import VideoStream

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--picamera", type=int, default=-1, help="whether or not the Raspberry Pi camera should be used")
args = vars(ap.parse_args())

vs = VideoStream(usePiCamera=args["picamera"] > 0, src="../test/output2.mp4").start()

time.sleep(2.0)

finder = TrackingTagFinder(vs)
tracking_tags = finder.find_tracking_tags()

# finder.save_tracking_tags_csv(tracking_tags, "tracking-tags.csv")
#
vs.stop()
