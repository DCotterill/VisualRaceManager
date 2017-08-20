import cv2
import time
import csv

from TrackingTag import TrackingTag


class TrackingTagFinder():
    def __init__(self, vs):
        self.vs = vs
        self.start_time = time.time()

    def find_tracking_tags(self):
        tracking_tags = []

        while (True):
            frame = self.vs.read()
            if frame is None:
                break

            # convert the frame to grayscale, blur it, and detect edges
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (7, 7), 0)
            edged = cv2.Canny(blurred, 60, 90)

            # find contours in the edge map
            (_, cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
                                            cv2.CHAIN_APPROX_SIMPLE)
            # loop over the contours
            # print "----"
            for c in cnts:
                # approximate the contour
                peri = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, 0.01 * peri, True)

                # ensure that the approximated contour is "roughly" rectangular
                if len(approx) >= 4 and len(approx) <=6:
                    # print len(approx)
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
                    keepDims = w > 30 and h > 30
                    keepSolidity = solidity > 0.8
                    keepAspectRatio = aspectRatio >= 0.75 and aspectRatio <= 1.15
                    # if keepDims and keepSolidity: print "++" + str(solidity)
                    # ensure that the contour passes all our tests
                    # print str(keepDims) + "," + str(keepSolidity) + "," + str(keepAspectRatio)
                    if keepDims and keepSolidity and keepAspectRatio:
                        # compute the center of the contour region
                        M = cv2.moments(approx)
                        (cX, cY) = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

                        id = len(tracking_tags) + 1
                        tag = TrackingTag(id, cX, cY, frame)
                        tagExists = False
                        for currentTag in tracking_tags:
                            if tag.is_same_tag(currentTag):
                                tagExists = True
                                currentTag.add_to_range(cX, cY, frame)
                        if not tagExists:
                            print str(len(approx)) + "," + str(w) + "," + str(h) + "," + str(solidity) + "," + str(aspectRatio)
                            tracking_tags.append(tag)

                        cv2.drawContours(frame, [approx], -1, (0, 0, 255), 4)

            y_position = 100
            for tag in tracking_tags:
                lower, upper = tag.get_colour_range()
                cv2.putText(frame, "===", (20, y_position), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (int(tag.get_middle_colour()[0]), int(tag.get_middle_colour()[1]), int(tag.get_middle_colour()[2])), 2)
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
            current_time = time.time()
            # if current_time - self.start_time > 20:
            #     break

            # print len(tracking_tags)

        cv2.destroyAllWindows()
        return tracking_tags


    def save_tracking_tags_csv(self, tracking_tags, filename):
        writer = csv.writer(open('../data/' + str(filename), 'w'))
        id = 1
        for tag in tracking_tags:
            writer.writerow([id, tag.get_middle_colour()[0], tag.get_middle_colour()[1], tag.get_middle_colour()[2]])
            id = id + 1
