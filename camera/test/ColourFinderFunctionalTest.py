import cv2
from camera.TrackingTagFinder import ColourFinder

camera = cv2.VideoCapture("../test-data/calibration-2-4-cars.mov")

finder = ColourFinder(camera, testing=True)
tracking_tags = finder.find_tracking_tags()

camera.release()

