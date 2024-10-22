import requests
import logging
import json
import csv
from datetime import datetime

# Configuración de logging
logging.basicConfig(filename='clima.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Archivo de configuración (config.json)
with open('config.json') as config_file:
    config = json.load(config_file)

API_KEY = config['api_key']
CITIES = config['cities']

# Función para obtener datos de clima de la API
def get_weather_data(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        # Datos en formato JSON
        data = response.json()

        # Extraer los datos relevantes
        weather_data = {
            'city': city,
            'temperature': data['main']['temp'],
            'weather': data['weather'][0]['description'],
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed']
        }
        return weather_data
    except requests.exceptions.RequestException as e:
        logging.error(f"Error obteniendo datos para {city}: {e}")
        return None

# Función para escribir datos en un archivo CSV
def write_to_csv(data, filename='clima_data.csv'):
    try:
        with open(filename, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['city', 'temperature', 'weather', 'humidity', 'wind_speed'])
            writer.writeheader()
            writer.writerows(data)

        logging.info(f"Datos guardados correctamente en {filename}.")
    except Exception as err:
        logging.error(f"Error al escribir los datos en el archivo CSV: {err}")


# Función principal
def main():

    weather_data_list = []

    for city in CITIES:
        weather_data = get_weather_data(city)
        if weather_data:
            weather_data_list.append(weather_data)

    if weather_data_list:
        write_to_csv(weather_data_list)
    else:
        logging.error("No se obtuvieron datos de clima para ninguna ciudad.")


if __name__ == '__main__':
    main()
