from TrackingTagFinder import ColourFinder
from RaceDetector import RaceDetector
from ThreadedVideoCapture import  ThreadedVideoCapture
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
# import csv
#
# writer = csv.writer(open('../data/' + str("blah.csv"), 'w'))

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

# allow the camera to warmup
time.sleep(0.1)
camera = ThreadedVideoCapture(src=1).start()

finder = ColourFinder(camera, rawCapture)

tracking_tags = finder.find_tracking_tags()

for tag in tracking_tags:
    low, high = tag.get_colour_range()
    print low
    print tag.get_middle_colour()
    print high
    print "-----"

finder.save_tracking_tags_csv(tracking_tags, 'tracking-tags.csv')

detector = RaceDetector(camera, tracking_tags)
detector.watch_tracking_tags()

