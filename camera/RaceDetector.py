import cv2
import time
from imutils.video import VideoStream

from CarSpotter import CarSpotter

COLOUR_COUNT_THRESHOLD = 5
MIN_LAP_TIME_MS = 5000


class RaceDetector:
    def __init__(self, vs, tracking_tags):
        self.vs = vs
        self.tracking_tags = tracking_tags
        self.car_spotter = CarSpotter(tracking_tags, MIN_LAP_TIME_MS)

    def setCamera(self, vs):
        self.vs = vs

    def watch_tracking_tags(self):

        while (True):
            frame = self.vs.read()

            if frame is None:
                break;

            mask = None
            for tag in self.tracking_tags:

                lower, upper = tag.get_colour_range()
                tag_mask = cv2.inRange(frame, lower, upper)

                if cv2.countNonZero(tag_mask) > tag.get_max_background_count() + COLOUR_COUNT_THRESHOLD:
                    millis = int(round(time.time() * 1000))
                    self.car_spotter.register_car(tag.id, millis)

                #if mask == None:
                #    mask = tag_mask
                #else:
                #    mask = cv2.bitwise_or(mask, tag_mask)

            #output = cv2.bitwise_and(frame, frame, mask=mask)
            #frame = output

            # cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
               break
