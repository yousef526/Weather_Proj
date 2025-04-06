import requests
import json

# API credentials
def apiCall():
    api_key = "YOUR_API_HERE"
    country = "EG"
    untis = "metric"

    params = {
    "q": "",
    "units": untis,
    "appid": api_key
    }



    cities_names = []
    with open("/opt/airflow/dags/WeatherScripts/Egypt.citites_used.txt","r",encoding="utf-8") as f:
        for line in f.readlines():
            cities_name = line.split("\n")[0]
            cities_names.append(cities_name)


    measures_per_city = []
    for city in cities_names:
        params["q"] = f"{city},{country}"
        response = requests.get(url=f"https://api.openweathermap.org/data/2.5/weather", params=params)
        measures_per_city.append(response.json())

    with open("/opt/airflow/dags/WeatherScripts/data.json", "w", encoding="utf-8") as file:
        json.dump(measures_per_city, file, indent=4, )

    print("Data successfully written to 'data.json'.")
