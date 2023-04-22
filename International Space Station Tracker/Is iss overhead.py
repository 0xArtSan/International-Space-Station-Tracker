import requests
from datetime import datetime
import smtplib

# email and password so this file can send you and email when the iss is overhead and is nighttime
MY_EMAIL = 'example@email.com'
MY_PASSWORD = 'example'

# latitude and longitude of Puerta del Sol in Madrid
MY_LAT = 40.4169
MY_LONG = -3.7035

def is_iss_overhead():
    response = requests.get(url='http://api.open-notify.org/iss-now.json')
    response.raise_for_status()

    data = response.json()

    iss_longitude = float(data.json()['iss_position']['longitude'])
    iss_latitude = float(data.json()['iss_position']['latitude'])

    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
        return True

def is_night():
    parameters = {
        'lat': MY_LAT,
        'lng': MY_LONG,
        'formatted': 0,
    }
    response = requests.get('https://api.sunrise-sunset.org/json', params=parameters)
    response.raise_for_status()
    data = response.json()

    sunrise = int(data['response']['sunrise'].split('T')[1].split(':')[0])
    sunset = int(data['response']['sunset'].split('T')[1].split(':')[0])

    time_now = datetime.now().hour
    if time_now >= sunset or time_now <= sunrise:
        return True

if is_night() and is_iss_overhead():
    connection = smtplib.SMTP('smtp.gmail.com')
    connection.starttls()
    connection.login(MY_EMAIL, MY_PASSWORD)
    connection.sendmail(
        from_addr=MY_EMAIL,
        to_addrs=MY_EMAIL,
        msg='Subject:Look Up\n\nThe Iss is above you'
    )
