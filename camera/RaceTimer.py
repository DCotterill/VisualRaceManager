import time
import argparse

from camera.VideoStream import VideoStream
from camera.TrackingTagFinder import TrackingTagFinder
from camera.RaceDetector import RaceDetector

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--picamera", type=int, default=-1, help="whether or not the Raspberry Pi camera should be used")
args = vars(ap.parse_args())

usePiCamera = args["picamera"] > 0

# Macbook has wierd camera app installed, so need to set src=1
if usePiCamera:
    src = 0
else:
    src = 1

vs = VideoStream(usePiCamera=usePiCamera, src=src).start()
time.sleep(2.0)

finder = TrackingTagFinder(vs)

tracking_tags = finder.find_tracking_tags()

for tag in tracking_tags:
    low, high = tag.get_colour_range()
    print low
    print tag.get_middle_colour()
    print high
    print "-----"

finder.save_tracking_tags_csv(tracking_tags, 'tracking-tags.csv')

detector = RaceDetector(vs, tracking_tags)
detector.watch_tracking_tags()

