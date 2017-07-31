import csv
import cv2
from camera.RaceDetector import RaceDetector
from camera.TrackingTag import TrackingTag
import numpy as np
import time


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

tracking_tags = load_tracking_tags_csv()
camera = cv2.VideoCapture("../test-data/car-laps-blue-then-green.mov")

detector = RaceDetector(camera, tracking_tags, testing=True)
detector.watch_tracking_tags()

detector.setCamera(cv2.VideoCapture("../test-data/orange-car-slow.mov"))
detector.watch_tracking_tags()

time.sleep(4)

detector.setCamera(cv2.VideoCapture("../test-data/car-laps-blue-then-green.mov"))
detector.watch_tracking_tags()

detector.setCamera(cv2.VideoCapture("../test-data/orange-car-slow.mov"))
detector.watch_tracking_tags()

time.sleep(6)

detector.setCamera(cv2.VideoCapture("../test-data/orange-car-slow.mov"))
detector.watch_tracking_tags()


# camera.release()

