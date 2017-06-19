from bottle import route, run, request, template, static_file
import csv

race_data = {}
@route('/initialize')
def initialize():
    return template ('templates/initialize')

@route('/showTags', method='POST')
def showTags():

    tags = []
    global race_data
    race_data = {}

    try:
        with open("../test-data/tracking-tags-2-4-cars.csv", 'r') as lines:
            reader = csv.reader(lines)
            for row in reader:
                tag = {}
                tag['id'] = row[0]
                tag['blue'] = row[1]
                tag['green'] = row[2]
                tag['red'] = row[3]

                race_data[row[0]] = tag
                tags.append(tag)
    except IOError:
        print IOError.message
    return template("templates/initialize", tags=tags)


@route('/addDetails', method='POST')
def addDetails():

    for id, details in race_data.items():
        name = request.forms.get("name" + str(id))

    return template("templates/initialize")


def set_formatted_lap_times_and_totals(race_data):
    max_laps = 0
    for id, car_data in race_data.items():
        if len(car_data.get('laps', [])) > max_laps:
            max_laps = len(car_data['laps'])

    for id, car_data in race_data.items():
        current_laps = race_data[id].get('laps', [])
        total_time = 0
        for lap_index in range(0, max_laps):
            if len(current_laps) > lap_index:
                lap_time_millis = int(current_laps[lap_index])
                total_time = total_time + lap_time_millis
                minutes = int((lap_time_millis / (1000*60))%60)
                seconds = int((lap_time_millis / 1000) % 60)
                race_data[id]['lap' + str(lap_index + 1)] = str(minutes).zfill(2) + ":" + str(seconds).zfill(2) + '.' \
                                                           + race_data[id]['laps'][lap_index][-3:]
            else:
                race_data[id]['lap' + str(lap_index + 1)] = ""
            total_minutes = int((total_time / (1000*60))%60)
            total_seconds = int((total_time / 1000) % 60)

            race_data[id]['totalTime'] = str(total_minutes).zfill(2) + ":" + str(total_seconds).zfill(2) + '.' \
                                         + str(total_time)[-3:]
    return race_data, max_laps


def calculate_race_orders(race_data):
    ordered_data = {}
    for id, car_data in race_data.items():
        laps = car_data.get('laps', [])
        lap_multiplier = 10000000 * len(laps)
        total_lap_time = 0
        for lap in laps:
            total_lap_time = total_lap_time + int(lap)
        ordered_data [lap_multiplier + (10000000 - total_lap_time)] = {'id': id, 'totalLapTime': total_lap_time}

    race_order = []
    for key in sorted(ordered_data.iterkeys(), reverse=True):
        id = ordered_data[key]['id']
        laps = race_data[id].get('laps', [])
        numLaps = len(laps)
        race_order.append({'id': id, 'numLaps': numLaps, 'totalTime':race_data[id]['totalTime']})

    print race_data
    print sorted(ordered_data.iterkeys(), reverse=True)
    print race_order


    return race_order


@route('/race', method='GET')
def race():
    global race_data
    for id, data in race_data.items():
        car_data = race_data[id]

        try:
            with open("../test-data/laps-" + id + ".csv", 'r') as lines:
                laps = []
                reader = csv.reader(lines)
                for lap in reader:
                    laps.append(lap[0])
                car_data['laps'] = laps
        except IOError:
            print IOError

    race_data, max_laps = set_formatted_lap_times_and_totals(race_data)
    race_order = calculate_race_orders(race_data)

    return template("templates/race", raceData=race_data, maxLaps=max_laps, raceOrder=race_order)


@route('/css/<filename>')
def server_static(filename):
    return static_file(filename, root='./css/')

@route('/js/<filename>')
def server_static(filename):
    return static_file(filename, root='./js/')

@route('/fonts/<filename>')
def server_static(filename):
    return static_file(filename, root='./fonts/')

## MAIN
if __name__ == '__main__':
    run(host='0.0.0.0', port=8080, debug=True)

