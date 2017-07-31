import cv2
from camera.TrackingTagFinder import ColourFinder
from camera.ThreadedVideoCapture import ThreadedVideoCapture

camera = cv2.VideoCapture("../test-data/calibration-2-4-cars.mov")

finder = ColourFinder(camera)
tracking_tags = finder.find_tracking_tags()

