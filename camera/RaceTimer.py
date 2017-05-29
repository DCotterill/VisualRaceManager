import argparse
import cv2
from TrackingTag import TrackingTag
from ColourFinder import ColourFinder
from RaceDetector import RaceDetector
from imutils.video import WebcamVideoStream

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
args = vars(ap.parse_args())

camera = WebcamVideoStream(src=1).start()

finder = ColourFinder(camera)
trackingTags = finder.findTrackingTags()

print trackingTags

detector = RaceDetector(camera, trackingTags)
detector.watchTrackingTags()

# camera.release()

