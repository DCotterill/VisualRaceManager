import csv


class CarSpotter:

    def __init__(self, tracking_tags, lap_threshold):
        self.tracking_tags = tracking_tags
        self.lap_threshold = lap_threshold
        self.laps = {}

    def register_car(self, id, time_in_millis):
        car_laps = self.laps.get(id, [])
        if len(car_laps) == 0 or (len(car_laps) > 0 and (time_in_millis - int(car_laps[-1])) > self.lap_threshold):
            car_laps.append(time_in_millis)
            print str(id) + ":" + str(time_in_millis)

            self.laps[id] = car_laps

            print self.get_lap_times()

    def get_laps(self):
        return self.laps

    def get_lap_times(self):
        lap_times = ""
        for id, times in self.laps.items():
            writer = csv.writer(open('../data/' 'laps-' + str(id) + '.csv', mode='w'))

            lap_times = lap_times + str(id)
            if len(times) > 1:
                start_of_lap_time = times[0]
                for time in times[1:]:
                    lap_time_millis = time - start_of_lap_time
                    start_of_lap_time = time
                    lap_times = lap_times + "," + str(lap_time_millis)

                    print ">" + str(lap_time_millis)
                    writer.writerow([str(lap_time_millis)])

            lap_times = lap_times + "\n"
        return lap_times