import argparse
import cv2
from TrackingTag import TrackingTag
from imutils.video import WebcamVideoStream

# # construct the argument parse and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-v", "--video", help="path to the video file")
# args = vars(ap.parse_args())
#
# camera = WebcamVideoStream(src=1).start()

class ColourFinder():
    def __init__(self, camera):
        self.camera = camera

    def findTrackingTags(self):
        # Calibrate the colours of the squares to find
        tracking_tags = []

        while True:
            frame = self.camera.read()
            grabbed = True

            # convert the frame to grayscale, blur it, and detect edges
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (7, 7), 0)
            edged = cv2.Canny(blurred, 60, 90)

            # find contours in the edge map
            (_, cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
                                            cv2.CHAIN_APPROX_SIMPLE)
            # tracking_tags = []

            # loop over the contours
            for c in cnts:
                # approximate the contour
                peri = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, 0.01 * peri, True)

                # ensure that the approximated contour is "roughly" rectangular
                if len(approx) >= 4 and len(approx) <= 6:
                    # compute the bounding box of the approximated contour and
                    # use the bounding box to compute the aspect ratio
                    (x, y, w, h) = cv2.boundingRect(approx)
                    aspectRatio = w / float(h)

                    # compute the solidity of the original contour
                    area = cv2.contourArea(c)
                    hullArea = cv2.contourArea(cv2.convexHull(c))
                    solidity = area / float(hullArea)

                    # compute whether or not the width and height, solidity, and
                    # aspect ratio of the contour falls within appropriate bounds
                    keepDims = w > 25 and h > 25
                    keepSolidity = solidity > 0.8
                    keepAspectRatio = aspectRatio >= 0.8 and aspectRatio <= 1.2

                    # ensure that the contour passes all our tests
                    if keepDims and keepSolidity and keepAspectRatio:
                        # compute the center of the contour region
                        M = cv2.moments(approx)
                        (cX, cY) = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

                        tag = TrackingTag(cX, cY, frame)
                        tagExists = False
                        for currentTag in tracking_tags:
                            if tag.is_same_tag(currentTag):
                                tagExists = True
                                currentTag.add_to_range(cX, cY, frame)
                        if not tagExists:
                            tracking_tags.append(tag)

                        cv2.drawContours(frame, [approx], -1, (0, 0, 255), 4)

            y_position = 50
            for tag in tracking_tags:
                lower, upper = tag.get_colour_range()
                cv2.putText(frame, "===", (20, y_position), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            ((int(lower[0] + int(upper[0]))/2,
                             (int(lower[1]) + int(upper[1]))/2,
                             (int(lower[2]) + int(upper[2]))/2)), 2)
                y_position = y_position + 30

            # show the frame and record if a key is pressed
            cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF

            # if the 'q' key is pressed, stop the loop
            if key == ord("q"):
                break
            if key == ord("r"):
                tracking_tags = []

            print len(tracking_tags)
            # if len(tracking_tags) == 2:
            #     break

        cv2.destroyAllWindows()
        return tracking_tags
