import unittest
from webapp import RaceManager

class RaceManagerTests(unittest.TestCase):
    def testFormatsSingleLapTime(self):
        raceData = {}
        raceData[1] = {'red':'100', 'green':'200', 'blue':'150', 'laps':['100560']}

        raceData, maxLaps = RaceManager.set_formatted_lap_times_and_totals(raceData)

        formattedLapTime = "01:40.560"
        self.assertEqual(formattedLapTime, raceData[1]['lap1'])

    def testFormatsMultipleLapTimesMultipleCars(self):
        raceData = {}
        raceData[1] = {'red':'100', 'green':'200', 'blue':'150', 'laps':['100560', '201110', '180350']}
        raceData[2] = {'red':'100', 'green':'200', 'blue':'150', 'laps':['100560', '181660']}

        raceData, maxLaps = RaceManager.set_formatted_lap_times_and_totals(raceData)

        self.assertEqual("01:40.560", raceData[1]['lap1'])
        self.assertEqual("03:21.110", raceData[1]['lap2'])
        self.assertEqual("03:00.350", raceData[1]['lap3'])
        self.assertEqual("01:40.560", raceData[2]['lap1'])
        self.assertEqual("03:01.660", raceData[2]['lap2'])
        self.assertEqual("", raceData[2]['lap3'])


    def testFormatsTotalTime(self):
        raceData = {}
        raceData[1] = {'red':'100', 'green':'200', 'blue':'150', 'laps':['100560', '201110', '180350']}

        raceData, maxLaps = RaceManager.set_formatted_lap_times_and_totals(raceData)

        #totalTime = 482020
        self.assertEqual("08:02.020", raceData[1]['totalTime'])

    def testFormatAddsZerosToTotalTime(self):
        raceData = {}
        raceData[1] = {'red':'100', 'green':'200', 'blue':'150', 'laps':['100560', '201110', '180330']}

        raceData, maxLaps = RaceManager.set_formatted_lap_times_and_totals(raceData)

        #totalTime = 482000
        self.assertEqual("08:02.000", raceData[1]['totalTime'])

    def testRaceOrderDeterminedByNumberOfLapsCompleted(self):

        raceData = {}
        raceData[1] = {'red': '100', 'green': '200', 'blue': '150', 'laps': ['100570', '201210']}
        raceData[2] = {'red': '100', 'green': '200', 'blue': '150', 'laps': ['100560', '201110', '180350']}
        raceData[3] = {'red': '100', 'green': '200', 'blue': '150', 'laps': []}

        RaceManager.set_formatted_lap_times_and_totals(raceData)
        raceOrder = RaceManager.calculate_race_orders(raceData)

        self.assertOrderOfValues([2, 1, 3], raceOrder, 'id')

    def testRaceOrderDeterminedByNumberOfLapsThenByTotalTime(self):

        raceData = {}
        raceData[1] = {'red': '100', 'green': '200', 'blue': '150', 'laps': ['100570', '201210']} #third
        raceData[2] = {'red': '100', 'green': '200', 'blue': '150', 'laps': ['100560', '201110', '180350']} #first
        raceData[3] = {'red': '100', 'green': '200', 'blue': '150', 'laps': ['100571', '201110']} #second
        raceData[4] = {'red': '100', 'green': '200', 'blue': '150', 'laps': ['101571', '201110']} #fourth

        RaceManager.set_formatted_lap_times_and_totals(raceData)
        raceOrder = RaceManager.calculate_race_orders(raceData)

        self.assertOrderOfValues([2, 3, 1, 4], raceOrder, 'id')

    def testRaceOrderDoesntBarfWithNoLapsProvided(self):

        raceData = {}
        raceData[1] = {'red': '100', 'green': '200', 'blue': '150', 'laps': ['100570', '201210']} #second
        raceData[2] = {'red': '100', 'green': '200', 'blue': '150', 'laps': ['100560', '201110', '180350']} #first
        raceData[3] = {'red': '100', 'green': '200', 'blue': '150'} #third

        RaceManager.set_formatted_lap_times_and_totals(raceData)
        raceOrder = RaceManager.calculate_race_orders(raceData)

        self.assertOrderOfValues([2, 1, 3], raceOrder, 'id')

    def testRaceOrderCalculatesNumberOfLapsCompleted(self):
        raceData = {}
        raceData[1] = {'red': '100', 'green': '200', 'blue': '150', 'laps': ['100570', '201210']} #second
        raceData[2] = {'red': '100', 'green': '200', 'blue': '150', 'laps': ['100560', '201110', '180350']} #first
        raceData[3] = {'red': '100', 'green': '200', 'blue': '150'} #third

        RaceManager.set_formatted_lap_times_and_totals(raceData)
        raceOrder = RaceManager.calculate_race_orders(raceData)
        self.assertOrderOfValues([3, 2, 0], raceOrder, 'numLaps')

    def assertOrderOfValues(self, order, arrayOfDicts, field):
        for i, element in enumerate(arrayOfDicts):
            self.assertEqual(order[i], element[field])



def main():
    unittest.main()

if __name__ == '__main__':
    main()


