import argparse
import time

from camera.TrackingTagFinder import TrackingTagFinder
from camera.VideoStream import VideoStream

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--picamera", type=int, default=-1, help="whether or not the Raspberry Pi camera should be used")
args = vars(ap.parse_args())

vs = VideoStream(usePiCamera=args["picamera"] > 0, src="../test-data/calibration-2-4-cars.mov").start()
time.sleep(2.0)

finder = TrackingTagFinder(vs)
tracking_tags = finder.find_tracking_tags()

finder.save_tracking_tags_csv(tracking_tags, "tracking-tags.csv")

vs.stop()
