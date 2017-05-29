# USAGE
# python drone.py --video FlightDemo.mp4

import argparse
import cv2

# ap = argparse.ArgumentParser()
# ap.add_argument("-v", "--video", help="path to the video file")
# args = vars(ap.parse_args())
import time

from CarSpotter import CarSpotter

COLOUR_COUNT_THRESHOLD = 50
RACE_LAP_THRESHOLD_MILLIS = 10000

class RaceDetector():
    def __init__(self, camera, trackingTags):
        self.camera = camera
        self.trackingTags = trackingTags
        self.carSpotter = CarSpotter(trackingTags, 10)

    def watchTrackingTags(self):

        while True:
            frame = self.camera.read()

            tag_number = 1
            mask = None

            for tag in self.trackingTags:

                lower, upper = tag.get_colour_range()

                tag_mask = cv2.inRange(frame, lower, upper)
                if (cv2.countNonZero(tag_mask) > COLOUR_COUNT_THRESHOLD):
                    self.carSpotter.registerCar(int(tag_number), int(time.time()))
                    print "Tag:" + str(tag_number) + ":" + str(cv2.countNonZero(tag_mask))

                tag_number = tag_number + 1
                if mask == None:
                    mask = tag_mask
                else:
                    mask = cv2.bitwise_or(mask, tag_mask)

            output = cv2.bitwise_and(frame, frame, mask=mask)
            frame = output

            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF

            # if the 'q' key is pressed, stop the loop
            if key == ord("q"):
                break

            if key == ord("r"):
                print "---------------------------"

