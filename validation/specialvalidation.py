import json
import time
from calendar import timegm
from config import DataConstant as dc
import copy

logging = None
days_counter = 0
temp_days_counter = 0


class DayTemperature:
    date = ""
    time = ""
    temperature = None
    epoch_time = ""
    weather_type = ""
    is_sunny_day = False
    sunrise = ""
    sunset = ""

    def __str__(self):
        return "{%s, %s, %d, %d, %s, %r, %d, %d }" % (self.date, self.time, self.temperature, self.epoch_time,
                                                      self.weather_type, self.is_sunny_day, self.sunrise, self.sunset)


def special_validation(response, logger):
    global logging
    logging = logger
    temp_list = get_all_datetime_templist(response)
    sunnyDayList = get_weather_type_list(temp_list)
    highest_day_temp_list = getHighestTempForEachDay(temp_list)

    print_day_temp_list(temp_list, "List of all forecasts greater than 20 degrees in the next 5 days(hour / hour).")

    print_day_temp_list(highest_day_temp_list, "List of all above 20 degrees in the next 5 days(day to day). "
                                         "Total days is : %s"  % temp_days_counter)

    print_day_temp_list(sunnyDayList, "List all days that are considered \'Sunny\'. "
                                 "Total days is : %s" % days_counter)

def get_all_datetime_templist(response):
    """
    Returns a list of all date and temperature data as DateTemperature objects
    """
    json_list = json.loads(response.text)
    city_data = json_list['city']
    temp_list = json_list['list']
    new_list = []

    for dayData in temp_list:
        # pdb.set_trace()
        day_temp = DayTemperature()
        day_temp.date = dayData['dt_txt'].split()[0]
        day_temp.time = dayData['dt_txt'].split()[1]
        day_temp.epoch_time = datetime_to_epoch(dayData['dt_txt'])
        day_temp.temperature = dayData['main']['temp']
        day_temp.sunset = city_data['sunset']
        day_temp.sunrise = city_data['sunrise']
        day_temp.weather_type = dayData['weather'][0]['main']

        if day_temp.temperature > dc.threshold_temp:
            new_list.append(day_temp)
        #print_day_temp_list(new_list, "TESTING!!!!")

    return new_list


def date_exists_inlist(in_list, date):
    exists = False
    for tempObj in in_list:
        if tempObj.date == date:
            return True

    return False


def getHighestTempForEachDay(temp_list):
    """"
        This function takes in a list of DateTemperature (DT) objects
        and will return a new list where if multiple DT objects of the
        same date are found, then only the date with the highest temperature
        will included in the returned new list of DT objects.
    """
    new_list=[]
    new_list.append(copy.copy(temp_list[0]))
    global temp_days_counter

    for index1 in range(len(temp_list)):
        # get DT object from orig list to see if it's date exists in the new list
        if not date_exists_inlist(new_list, temp_list[index1].date):
            new_list.append(copy.copy(temp_list[index1]))
            continue
        # if date already exists, check to see if its temperature is higher
        for index2 in range(len(new_list)):
            if new_list[index2].date == temp_list[index1].date and temp_list[index1].temperature > new_list[index2].temperature:
                new_list[index2].temperature = temp_list[index1].temperature
                new_list[index2].time = temp_list[index1].time
                temp_days_counter += 1
    return new_list


def epoch_to_datetime(epoch_time):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epoch_time))


def datetime_to_epoch(date_time):
    # "2019-12-18 03:00:00"
    in_time = time.strptime(date_time, "%Y-%m-%d %H:%M:%S")
    epoch_time = timegm(in_time)
    return epoch_time


def get_weather_type_list(weather_list):
    new_list = []
    new_list.append(weather_list[0])
    global days_counter

    for i in range(len(weather_list)):
        if date_exists_inlist(new_list, weather_list[i].date):
            if weather_list[i].sunrise <= weather_list[i].epoch_time <= \
                    weather_list[i].sunset and weather_list[i].weather_type.lower() == dc.weather_type:
                for weather_list[i].date in new_list[i].date:
                    if new_list[i].date == weather_list[i].date:
                        new_list.append(weather_list[i])

    days_counter += 1

    return new_list

def print_day_temp_list(temp_list, message):
    logging.info("-------------------------------------------------------------------------------------------")
    logging.info(message)
    for i in temp_list:
        print_day_temp(i)


def print_day_temp(tempObj):
    #log_message = "%s : %s : %d : %d" % (i.date, i.time, i.temperature, i.epoch_time)
    log_message = tempObj.__str__()
    logging.info(log_message)

# def get_city_info(response):
#     response = json.loads(response.text)
#     return response['city']