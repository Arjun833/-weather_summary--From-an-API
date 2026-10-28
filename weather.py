import requests

WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Fog",
    51: "Light drizzle",
    53: "Drizzle",
    55: "Heavy drizzle",
    61: "Light rain",
    63: "Rain",
    65: "Heavy rain",
    80: "Rain showers",
    95: "Thunderstorm",
}

def describe(code):
    return WEATHER_CODES.get(code, "Unknown conditions")

def get_coordinates(city):
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": city, "count": 1}

    try:
        r = requests.get(url, params=params, timeout=5)
        r.raise_for_status()
        results = r.json().get("results")
    except requests.exceptions.RequestException as e:
        print("Could not look up city:", e)
        return None

    if not results:
        print(f"City '{city}' not found.")
        return None

    place = results[0]
    return place["latitude"], place["longitude"], place["name"], place.get("country", "")

def get_current_weather(lat,lon):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {'latitude':lat , "longitude":lon ,"current_weather": True}
    
    try:
        r = requests.get(url,params=params , timeout= 5)
        r.raise_for_status()
        return r.json()["current_weather"]
    
    except requests.exceptions.RequestException as e :
        print("could not fetch weather " , e)
        return None

def print_summary(city, country, weather):
    print("=" * 35)
    print(f"Weather in {city}, {country}")
    print("=" * 35)
    print(f"Conditions : {describe(weather['weathercode'])}")
    print(f"Temperature: {weather['temperature']} °C")
    print(f"Wind speed : {weather['windspeed']} km/h")
    print(f"Updated at : {weather['time']}")

def main():
    city = input("Enter a city: ").strip()
    if not city:
        print("Please enter a city name.")
        return

    coords = get_coordinates(city)
    if coords is None:
        return
    lat, lon, name, country = coords

    weather = get_current_weather(lat, lon)
    if weather is None:
        return

    print_summary(name, country, weather)

if __name__ == "__main__":
    main()
    
    
    
