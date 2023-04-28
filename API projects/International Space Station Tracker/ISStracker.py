import requests
import webbrowser

response = requests.get(url='http://api.open-notify.org/iss-now.json')
response.raise_for_status()

longitude = response.json()['iss_position']['longitude']
latitude = response.json()['iss_position']['latitude']

iss_position = (latitude, longitude)

webbrowser.open(f"https://www.google.com/maps/place/{iss_position[0]},{iss_position[1]}")
