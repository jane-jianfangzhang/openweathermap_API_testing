
class DataConstant:

    app_id = 'b6907d289e10d714a6e88b30761fae22' #06ab3d164fe4536fb0ad7feabe13bbc4
    city_id ='2147714'  #Sydney
    zip_code = 2000
    threshold_temp = 20

    web_url = "https://openweathermap.org/"
    base_url = "https://openweathermap.org/data/2.5/forecast?id=%s&appid=%s&units=metric" % (city_id, app_id)
    weather_type = "clear"


class LogConstant:
    all_when = "midnight"
    all_backupCount = 7

    error_when = "midnight"
    error_backupCount = 7
