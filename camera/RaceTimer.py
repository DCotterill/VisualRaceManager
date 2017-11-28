import time
import argparse

from imutils.video import VideoStream
from camera.TrackingTagFinder import TrackingTagFinder
from camera.RaceDetector import RaceDetector
from camera.BackgroundLevelDetector import BackgroundLevelDetector

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--picamera", type=int, default=-1, help="whether or not the Raspberry Pi camera should be used")
ap.add_argument("-t", "--test", type=int, default=-1, help="Run with test videos")
args = vars(ap.parse_args())

usePiCamera = args["picamera"] > 0
useTestVideos = args["test"] > 0

# Macbook has wierd camera app installed, so need to set src=1
if usePiCamera:
    src = 0
else:
    src = 1

if useTestVideos:
    vs = VideoStream(src="../test-data/3-cars-final.avi").start()
else:
    vs = VideoStream(usePiCamera=usePiCamera, src=src).start()
    time.sleep(2.0)

print "Place cars in detection position then press 'q'. Press 'r' to reset detection."
finder = TrackingTagFinder(vs)
tracking_tags = finder.find_tracking_tags()

print "Move cars to detect background levels, then press 'q'"
if useTestVideos:
    vs = VideoStream(src="../test-data/background-final.avi").start()

b_detector = BackgroundLevelDetector(vs, tracking_tags)

b_detector.watch_background()

for tag in tracking_tags:
    low, high = tag.get_colour_range()
    print low
    print tag.get_middle_colour()
    print high
    print "-----"

finder.save_tracking_tags_csv(tracking_tags, 'tracking-tags.csv')

print "Cars Detected: " + str(len(tracking_tags))

for tag in tracking_tags:
    print str(tag.get_middle_colour()) + ":" + str(tag.get_max_background_count())

if useTestVideos:
    vs = VideoStream(src="../test-data/driving-final.avi").start()

detector = RaceDetector(vs, tracking_tags)
detector.watch_tracking_tags()

