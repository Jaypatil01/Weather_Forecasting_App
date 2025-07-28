import requests

def get_weather(city):
    api_key = "35b99b622b8f22ce01d723b5f4390fd4"
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if response.status_code == 200:
        city_name = data['name']
        temp = data['main']['temp']

        print(f" City: {city_name}")
        print(f" Temperature: {temp} °C")
    else:
        print("\n City not found. Please try again.\n")

city_name = input("Enter a city name: ")
get_weather(city_name)