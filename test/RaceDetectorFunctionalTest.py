import csv
import argparse
import numpy as np
import time

from camera.VideoStream import VideoStream
from camera.RaceDetector import RaceDetector
from camera.TrackingTag import TrackingTag


def load_tracking_tags_csv():
    tracking_tags = []

    try:
        with open('../test-data/' 'tracking-tags-2-4-cars.csv', mode='r') as tracking_tags_file:
            reader = csv.reader(tracking_tags_file)
            for row in reader:
                tag = TrackingTag(int(row[0]), 0, 0, None)
                tag.set_colour_average(np.array([int(row[3]), int(row[2]), int(row[1])], dtype="uint8"))
                tracking_tags.append(tag)
    except IOError:
        tracking_tags = []

    return tracking_tags

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--picamera", type=int, default=-1, help="whether or not the Raspberry Pi camera should be used")
args = vars(ap.parse_args())

vs = VideoStream(usePiCamera=args["picamera"] > 0, src="../test-data/calibration-2-4-cars.mov").start()
time.sleep(2.0)

detector = RaceDetector(vs, load_tracking_tags_csv())
detector.watch_tracking_tags()

detector.setCamera(VideoStream(usePiCamera=args["picamera"] > 0, src="../test-data/orange-car-slow.mov").start())
detector.watch_tracking_tags()

time.sleep(4)

detector.setCamera(VideoStream(usePiCamera=args["picamera"] > 0, src="../test-data/car-laps-blue-then-green.mov").start())
detector.watch_tracking_tags()

detector.setCamera(VideoStream(usePiCamera=args["picamera"] > 0, src="../test-data/orange-car-slow.mov").start())
detector.watch_tracking_tags()

time.sleep(6)

detector.setCamera(VideoStream(usePiCamera=args["picamera"] > 0, src="../test-data/orange-car-slow.mov").start())
detector.watch_tracking_tags()


