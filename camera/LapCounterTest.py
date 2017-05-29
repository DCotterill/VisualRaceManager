import unittest

from CarSpotter import CarSpotter


class LapCounterTests(unittest.TestCase):
    def testCarsSpottedFirstTimeAddsNewCars(self):
        trackingTags = []
        carSpotter = CarSpotter(trackingTags, 0)

        carSpotter.registerCar(1, 100)
        carSpotter.registerCar(2, 105)

        laps = carSpotter.getLaps()

        self.assertEqual(laps, {1: [100], 2: [105]})

    def testCarsSpottedTwiceAddsTwoLaps(self):
        trackingTags = []
        carSpotter = CarSpotter(trackingTags, 0)

        carSpotter.registerCar(1, 100)
        carSpotter.registerCar(1, 205)

        laps = carSpotter.getLaps()

        self.assertEqual(laps, {1: [100, 205]})

    def testCarsSpottedTwiceWithinTimeThresholdOnlyAddsOnce(self):
        trackingTags = []
        carSpotter = CarSpotter(trackingTags, 50)

        carSpotter.registerCar(1, 100)
        carSpotter.registerCar(1, 110)
        carSpotter.registerCar(1, 150)

        laps = carSpotter.getLaps()

        self.assertEqual(laps, {1: [100]})


def main():
    unittest.main()

if __name__ == '__main__':
    main()


