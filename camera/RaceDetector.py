# USAGE
# python drone.py --video FlightDemo.mp4

import argparse
import cv2

# ap = argparse.ArgumentParser()
# ap.add_argument("-v", "--video", help="path to the video file")
# args = vars(ap.parse_args())
import time

from LapTimeManager import CarSpotter

COLOUR_COUNT_THRESHOLD = 5
MIN_LAP_TIME_MS = 5000


class RaceDetector:
    def __init__(self, camera, tracking_tags, rawCapture, testing=False):
        self.camera = camera
        self.tracking_tags = tracking_tags
        self.rawCapture = rawCapture
        self.car_spotter = CarSpotter(tracking_tags, MIN_LAP_TIME_MS)
        self.testing = testing

    def setCamera(self, camera):
        self.camera = camera

    def watch_tracking_tags(self):

        for image in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
            # grab the raw NumPy array representing the image, then initialize the timestamp
            # and occupied/unoccupied text
            frame = image.array
        # while True:
        #     if self.testing:
        #         (grabbed, frame) = self.camera.read()
        #         if not grabbed:
        #             break
        #     else:
        #         frame = self.camera.read()

            mask = None
            for tag in self.tracking_tags:

                lower, upper = tag.get_colour_range()
                tag_mask = cv2.inRange(frame, lower, upper)

                if cv2.countNonZero(tag_mask) > COLOUR_COUNT_THRESHOLD:
                    millis = int(round(time.time() * 1000))
                    self.car_spotter.register_car(tag.id, millis)

                #if mask == None:
                #    mask = tag_mask
                #else:
                #    mask = cv2.bitwise_or(mask, tag_mask)

            #output = cv2.bitwise_and(frame, frame, mask=mask)
            #frame = output

            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF

            self.rawCapture.truncate(0)

            if key == ord("q"):
               break
