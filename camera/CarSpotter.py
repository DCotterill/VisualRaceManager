class CarSpotter():

    def __init__(self, trackingTags, lapThreshold):
        self.trackingTags = trackingTags
        self.lapThreshold = lapThreshold
        self.laps = {}

    def registerCar(self, id, timeInSeconds):
        carLaps = self.laps.get(id, [])
        if len(carLaps) == 0 or (len(carLaps) > 0 and (timeInSeconds - int(carLaps[-1])) > self.lapThreshold):
            carLaps.append(timeInSeconds)
            print str(id) + ":" + str(timeInSeconds)

        self.laps[id] = carLaps

    def getLaps(self):
        return self.laps

    def getLapTimes(self):
        return