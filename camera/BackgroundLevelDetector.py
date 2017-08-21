import cv2
import time


class RaceDetector:
    def __init__(self, vs, tracking_tags):
        self.vs = vs
        self.tracking_tags = tracking_tags

    def setCamera(self, vs):
        self.vs = vs

    def watch_tracking_tags(self):

        while True:
            frame = self.vs.read()

            if frame is None:
                break;

            for tag in self.tracking_tags:

                lower, upper = tag.get_colour_range()
                tag_mask = cv2.inRange(frame, lower, upper)

                tag.update_max_background_count(cv2.countNonZero(tag_mask))

            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
               break
