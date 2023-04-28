import requests
from datetime import datetime, timedelta

# Choose your coordinates, you could use a geolocation API
LAT = '40.7114'
LONG = '-4.0542'

# Temperature, precipitation, cloud cover and uv index thresholds, in that order
TEMP = 15
PREC = 1
CC = 50
UV = 5


# Input: It takes today's date and the first day you want to check the weather
# Output: It outputs the date of the next day that coincides with the first day you want to check the weather
# This function calculates the date of the start day provided by the user
def day_plan(date_now, date_plan):
    first_day = date_plan - date_now.weekday()
    if first_day <= 0:
        first_day += 7
    return date_now + timedelta(first_day)


# Input: It takes a date
# Output: It outputs the day and hour of the date provided in a list
# This function extracts the day of the month and hour of a given date
def extract_date(date):
    result = date.split('-')[2].replace('T', ' ').split(':')[0].split(' ')
    return result


# Input: It takes a list with dates, a list of data (temperatures, cloud cover...) and a threshold
# Output: A list that contains the day in which the data is above the threshold, the start and end hour of the period of time in which the data is above the threshold and the minimum and maximum points in the prior time frame that is above the given threshold
# This function extracts the data from an array of the api
def extract_info(list_calendar, list_data, threshold):
    counter = 0
    message, buffer = [], []
    for item in list_data:
        try:
            if item > threshold:
                date = list_calendar[counter]
                time_split = extract_date(date)
                day = time_split[0]
                hour = time_split[1]

                if buffer:
                    if day != buffer[0]:
                        message.append(buffer)
                        buffer = []
                    else:
                        buffer[2] = hour
                        if item < buffer[3]:
                            buffer[3] = item
                        if item > buffer[4]:
                            buffer[4] = item

                if not buffer:
                    buffer.append(day)
                    buffer.append(hour)
                    buffer.append(hour)
                    buffer.append(item)
                    buffer.append(item)
            counter += 1
        except:
            return message
    return message


# Input: It takes a list given by the function extract_info and a data type like temperature
# Output: It prints the input like this: 'Day' 'Hour'-'Hour'h --> 'minimum data'-'maximum data'
# This function prints all the extracted data in a readable manner
def message(item_list, type_data, units):
    if item_list:
        print(type_data.capitalize())
        for item in item_list:
            print(str(item[0]) + ' ' + str(item[1]) + '-' + str(item[2]) + 'h' + ' --> ' + str(item[3]) + '-' + str(item[4]) + ' ' + units)
    else:
        print(f'No {type_data} above threshold')


today = datetime.now().date()

# Input for which day of the week starts the period in which you want to check the weather
day_week = ['today', 'monday', 'tuesday', 'wednesday', 'thursday', 'wednesday', 'friday', 'saturday', 'sunday']
weekday_input = ''
while weekday_input not in day_week:
    weekday_input = input('What is the first day you want to check the weather?(Day of the week or "today") ')
weekday = day_week.index(weekday_input) - 1

# Input for the amount of additional day to check the weather
days_free = int(input('How many more days do you want to check? ')) + 1

# Calculate the start and end date of the period in which you want to check the weather
if weekday != - 1:
    start_date = day_plan(today, weekday)
else:
    start_date = today
end_date = start_date + timedelta(days_free)

# Access to the weather api data
response = requests.get(
    url=f'https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LONG}&hourly=temperature_2m,precipitation_probability,cloudcover,uv_index&start_date={start_date}&end_date={end_date}&timezone=Europe%2FBerlin')
response.raise_for_status()

# print the url in case you want to look at the JSON info directly
# print(f'https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LONG}&hourly=temperature_2m,precipitation_probability,cloudcover,uv_index&start_date={start_date}&end_date={end_date}&timezone=Europe%2FBerlin')

data = response.json()

# Extraction of all the data in different lists
time = data['hourly']['time']
temperature = data['hourly']['temperature_2m']
precipitation = data['hourly']['precipitation_probability']
cloud_cover = data['hourly']['cloudcover']
uv_index = data['hourly']['uv_index']

message_temperatures = extract_info(time, temperature, TEMP)
message(message_temperatures, 'temperatures', 'ºc')

message_precipitation = extract_info(time, precipitation, PREC)
message(message_precipitation, 'precipitation', '%')

message_cloudcover = extract_info(time, cloud_cover, CC)
message(message_cloudcover, 'cloud cover', '%')

message_uv = extract_info(time, uv_index, UV)
message(message_uv, 'peak uv index', '')
