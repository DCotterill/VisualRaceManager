from TrackingTagFinder import ColourFinder
from RaceDetector import RaceDetector
from imutils.video import WebcamVideoStream

camera = WebcamVideoStream(src=1).start()

finder = ColourFinder(camera)
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

