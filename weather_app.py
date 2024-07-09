import requests

def get_weather_data(location, api_key):
    api_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": location,  # Use 'q' for city names and ZIP codes
        "units": "metric",
        "appid": api_key
    }
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        if data.get('cod') != 200:
            return None, data.get('message', 'Unable to fetch weather data')
        return data, None
    except requests.exceptions.RequestException as e:
        return None, f"An error occurred: {e}"

def display_weather(data):
    weather = {
        'temperature': data['main']['temp'],
        'humidity': data['main']['humidity'],
        'description': data['weather'][0]['description'],
        'city': data['name'],
        'country': data['sys']['country']
    }
    print(f"Weather in {weather['city']}, {weather['country']}:")
    print(f"Temperature: {weather['temperature']}°C")
    print(f"Humidity: {weather['humidity']}%")
    print(f"Conditions: {weather['description']}")

def main():
    api_key = "c86432b6f88b243f1a9e5281514eb47b"
    location = input("Enter a city or ZIP code: ")
    data, error = get_weather_data(location, api_key)
    if error:
        print(f"Error: {error}")
    else:
        display_weather(data)

if __name__ == "__main__":
    main()