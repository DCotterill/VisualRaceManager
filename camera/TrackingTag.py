import numpy as np


class TrackingTag():

    # def __init__(self, x, y, w, h, frame):
    #     self.colour_range_low = np.array ([255,255,255], dtype="uint8")
    #     self.colour_range_high = np.array ([0, 0, 0], dtype="uint8")
    #     self.coord_top_left =  np.array [x - w/2, y - h/2]
    #     self.coord_bottom_right = np.array [x + w/2, y + h/2]
    #
    #     for y_offset in range(-6, 6):
    #         for x_offset in range(-6, 6):
    #             colour = frame[y + y_offset * 3, x + x_offset * 3]
    #             self.update_colour_range(colour)

    def __init__(self, x, y, frame):
        self.colour_range_low = np.array ([255,255,255], dtype="uint8")
        self.colour_range_high = np.array ([0, 0, 0], dtype="uint8")
        self.x = x
        self.y = y

        self.add_to_range(x, y, frame)

    def add_to_range(self, x, y, frame):
        for y_offset in range(-6, 6):
            for x_offset in range(-6, 6):
                colour = frame[y + y_offset * 1, x + x_offset * 1]
                self.update_colour_range(colour)

    def update_colour_range (self, colour):
        if colour[0] < self.colour_range_low[0]: self.colour_range_low[0] = colour[0] - 1
        if colour[0] > self.colour_range_high[0]: self.colour_range_high[0] = colour[0] + 1

        if colour[1] < self.colour_range_low[1]: self.colour_range_low[1] = colour[1] - 1
        if colour[1] > self.colour_range_high[1]: self.colour_range_high[1] = colour[1] + 1

        if colour[2] < self.colour_range_low[2]: self.colour_range_low[2] = colour[2] - 1
        if colour[2] > self.colour_range_high[2]: self.colour_range_high[2] = colour[2] + 1

    def get_colour_range(self):
        return self.colour_range_low, self.colour_range_high

    def is_same_tag(self, otherTag):
        return abs(self.x - otherTag.x) < 50 and abs(self.y - otherTag.y) < 50
