import numpy as np


class TrackingTag:

    def __init__(self, id, x, y, frame):
        self.id = id
        self.colour_range_low = np.array ([255,255,255], dtype="uint8")
        self.colour_range_high = np.array ([0, 0, 0], dtype="uint8")
        self.colour_average = np.array ([0, 0, 0], dtype="uint8")
        self.x = x
        self.y = y
        self.colour_samples = 0
        self.max_background_count = 0

        if frame != None:
            self.add_to_range(x, y, frame)

    # def __init__(self, id, colour_average):
    #     self.id = id
    #     self.colour_range_low = np.array ([255,255,255], dtype="uint8")
    #     self.colour_range_high = np.array ([0, 0, 0], dtype="uint8")
    #     self.colour_average = colour_average

    def set_colour_average(self, colour_average):
        self.colour_average = colour_average

    def update_max_background_count(self, background_count):
        if background_count > self.max_background_count:
            self.max_background_count = background_count

    def get_max_background_count(self):
        return self.max_background_count

    def add_to_range(self, x, y, frame):
        for y_offset in range(-6, 6):
            for x_offset in range(-6, 6):
                colour = frame[y + y_offset * 1, x + x_offset * 1]
                self.update_colour_range(colour)

    def update_colour_range (self, colour):
        self.colour_samples = self.colour_samples + 1
        if self.colour_samples == 1:
            self.colour_average[0] = int(colour[0])
            self.colour_average[1] = int(colour[1])
            self.colour_average[2] = int(colour[2])
        else:
            self.colour_average[0] = int((self.colour_average[0] * self.colour_samples + colour[0])
                                            /(self.colour_samples + 1))
            self.colour_average[1] = int((self.colour_average[1] * self.colour_samples + colour[1])
                                            /(self.colour_samples + 1))
            self.colour_average[2] = int((self.colour_average[2] * self.colour_samples + colour[2])
                                            /(self.colour_samples + 1))

        if colour[0] < self.colour_range_low[0]: self.colour_range_low[0] = colour[0] - 1
        if colour[0] > self.colour_range_high[0]: self.colour_range_high[0] = colour[0] + 1

        if colour[1] < self.colour_range_low[1]: self.colour_range_low[1] = colour[1] - 1
        if colour[1] > self.colour_range_high[1]: self.colour_range_high[1] = colour[1] + 1

        if colour[2] < self.colour_range_low[2]: self.colour_range_low[2] = colour[2] - 1
        if colour[2] > self.colour_range_high[2]: self.colour_range_high[2] = colour[2] + 1

    def get_colour_range(self):

        COLOUR_WIDTH = 30
        if self.colour_average[0] > COLOUR_WIDTH:
            self.colour_range_low[0] = self.colour_average[0] - COLOUR_WIDTH
        else: self.colour_range_low[0] = 0

        if self.colour_average[1] > COLOUR_WIDTH:
            self.colour_range_low[1] = self.colour_average[1] - COLOUR_WIDTH
        else: self.colour_range_low[1] = 0

        if self.colour_average[2] > COLOUR_WIDTH:
            self.colour_range_low[2] = self.colour_average[2] - COLOUR_WIDTH
        else: self.colour_range_low[2] = 0

        if self.colour_average[0] < 255 - COLOUR_WIDTH:
            self.colour_range_high[0] = self.colour_average[0] + COLOUR_WIDTH
        else: self.colour_range_high[0] = 255

        if self.colour_average[1] < 255 - COLOUR_WIDTH:
            self.colour_range_high[1] = self.colour_average[1] + COLOUR_WIDTH
        else: self.colour_range_high[1] = 255

        if self.colour_average[2] < 255 - COLOUR_WIDTH:
            self.colour_range_high[2] = self.colour_average[2] + COLOUR_WIDTH
        else: self.colour_range_high[2] = 255

        # print self.colour_average
        # print self.colour_range_low
        # print self.colour_range_high

        return self.colour_range_low, self.colour_range_high

    def is_same_tag(self, otherTag):
        return abs(self.x - otherTag.x) < 50 and abs(self.y - otherTag.y) < 50

    def get_middle_colour(self):
        return self.colour_average

