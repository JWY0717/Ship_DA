from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
from urllib.request import urlopen
import requests

app = Flask(__name__)
CORS(app)

# 모델 불러오기

with open('D:/장우영/LOCALSEARCH/Ship_DA/DA/model/model_latitude.pkl', 'rb') as f:
    model_latitude = pickle.load(f)

with open('D:/장우영/LOCALSEARCH/Ship_DA/DA/model/model_longitude.pkl', 'rb') as f:
    model_longitude = pickle.load(f)
    
with open('D:/장우영/LOCALSEARCH/Ship_DA/DA/model/model_cog.pkl', 'rb') as f:
    model_cog = pickle.load(f)

with open('D:/장우영/LOCALSEARCH/Ship_DA/DA/model/model_sog.pkl', 'rb') as f:
    model_sog = pickle.load(f)

# 기상청 API URL
weather_api_url ='https://apihub.kma.go.kr/api/typ01/url/kma_buoy.php?tm=202306161610&stn=21229&help=1&authKey=cJGQY1PQTnuRkGNT0H57zQ'

@app.route('/api05/predict/', methods=['POST'])
def predict():
    data = request.get_json()
    app.logger.info(data)

    # Extract features to use for prediction
    mmsi = data['mmsi']
    ship_type = data['ship_type']
    latitude = data['latitude']
    longitude = data['longitude']
    cog = data['cog']
    sog = data['sog']

    # Get weather data from the Meteorological Administration API based on latitude and longitude
    weather_data = get_weather_data(latitude, longitude)

    if weather_data is not None:
        # Extract relevant meteorological data
        wind_direction = weather_data.get('wind_direction', '')  # wind direction
        temperatures = weather_data.get('TA', '')  # temperatures
        water_temperature = weather_data.get('TW', '')  # water temperature
        wind_speed = weather_data.get('WS', '')  # wind speed
        atmospheric_pressure = weather_data.get('PA', '')  # atmospheric pressure
        humidity = weather_data.get('HM', '')  # relative humidity

        # Make predictions using the models
        latitude_pred = model_latitude.predict([[mmsi, ship_type, latitude, longitude, cog, sog, wind_direction,
                                                  temperatures, water_temperature, wind_speed,
                                                  atmospheric_pressure, humidity]])[0]
        longitude_pred = model_longitude.predict([[mmsi, ship_type, latitude, longitude, cog, sog, wind_direction,
                                                    temperatures, water_temperature, wind_speed,
                                                    atmospheric_pressure, humidity]])[0]
        cog_pred = model_cog.predict([[mmsi, ship_type, latitude, longitude, cog, sog, wind_direction,
                                        temperatures, water_temperature, wind_speed,
                                        atmospheric_pressure, humidity]])[0]
        sog_pred = model_sog.predict([[mmsi, ship_type, latitude, longitude, cog, sog, wind_direction,
                                        temperatures, water_temperature, wind_speed,
                                        atmospheric_pressure, humidity]])[0]

        # Return prediction result
        result = {'latitude': latitude_pred, 'longitude': longitude_pred, 'cog': cog_pred, 'sog': sog_pred}
        return jsonify(result)
    else:
        # Return error message if weather data could not be fetched
        return jsonify({'error': 'Failed to get weather data'})

def get_weather_data(LAT, LON):
    # Construct the URL
    domain = "https://apihub.kma.go.kr/api/typ01/url/kma_buoy.php?"
    tm = "tm=202306161610&"
    stn_id = "stn=22105&"
    option = "help=0&authKey=cJGQY1PQTnuRkGNT0H57zQ"
    auth = ""
    url = domain + tm + stn_id + option + auth

    # Fetch weather data using requests
    response = requests.get(url)
    if response.status_code == 200:
        data = response.content.strip()

        # Split the data into lines
        lines = data.split(b'\n')

        line = lines[4].split(b' ')[4]
        wind_direction = line.decode('utf-8')

        # Return the weather data as a dictionary
        return {'wind_direction': wind_direction}
    else:
        return None

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
