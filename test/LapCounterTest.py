import unittest

from camera.CarSpotter import CarSpotter


class LapCounterTests(unittest.TestCase):
    def testCarsSpottedFirstTimeAddsNewCars(self):
        tracking_tags = []
        car_spotter = CarSpotter(tracking_tags, 0)

        car_spotter.register_car(1, 100)
        car_spotter.register_car(2, 105)

        laps = car_spotter.get_laps()

        self.assertEqual(laps, {1: [100], 2: [105]})

    def testCarsSpottedTwiceAddsTwoLaps(self):
        tracking_tags = []
        car_spotter = CarSpotter(tracking_tags, 0)

        car_spotter.register_car(1, 100)
        car_spotter.register_car(1, 205)

        laps = car_spotter.get_laps()

        self.assertEqual(laps, {1: [100, 205]})

    def testCarsSpottedTwiceWithinTimeThresholdOnlyAddsOnce(self):
        tracking_tags = []
        car_spotter = CarSpotter(tracking_tags, 50)

        car_spotter.register_car(1, 100)
        car_spotter.register_car(1, 110)
        car_spotter.register_car(1, 150)

        laps = car_spotter.get_laps()

        self.assertEqual(laps, {1: [100]})

    def testLapTimesCalculatedFromTimeStamps(self):
        tracking_tags = []
        car_spotter = CarSpotter(tracking_tags,10)

        car_spotter.register_car(1, 1)
        car_spotter.register_car(1, 2)
        car_spotter.register_car(1, 5)
        car_spotter.register_car(1, 12)
        car_spotter.register_car(1, 13)
        car_spotter.register_car(1, 15)
        car_spotter.register_car(1, 51)
        car_spotter.register_car(1, 52)
        car_spotter.register_car(1, 59)

        self.assertEqual(car_spotter.get_lap_times(), "1,11,39\n")


def main():
    unittest.main()

if __name__ == '__main__':
    main()


