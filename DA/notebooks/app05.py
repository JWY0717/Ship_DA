from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import pandas as pd
from urllib.request import urlopen
from datetime import datetime
    
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
 

    # 예측에 사용할 특성 추출
    mmsi = data['mmsi']
    ship_type = data['ship_type']
    latitude = data['latitude']
    longitude = data['longitude']
    cog = data['cog']
    sog = data['sog']
    
    # Get current datetime
    now = datetime.now()

    # Extract year, month, date, hour, minute, and second
    year = now.year
    month = now.month
    day = now.day
    hour = now.hour
    minute = now.minute + 1 
    second = now.second
          
    # 위도와 경도를 기반으로 기상 데이터를 기상청 API에서 가져옴
    weather_data = get_weather_data(latitude, longitude)
    

    if weather_data is not None:
        
        # 관련 기상 데이터 추출
        wind_direction = weather_data.get('WD', 100)             # 풍향
        temperatures = weather_data.get('TA', 15)                # 기온
        water_temperature = weather_data.get('TW', 10)           # 수온
        wind_speed = weather_data.get('WS', 100)                 # 풍속
        atmospheric_pressure = weather_data.get('PA', 10)        # 기압
        humidity = weather_data.get('HM', 10)                    # 상대습도
        direct = weather_data.get('CD', 10)                      # 유향
        current_speed = weather_data.get('CS', 10)               # 유속
        
        #X = data                       [["mmsi", "ship_type", "latitude","longitude", "cog", "sog", "year", "month", "day", "hour", "minute", "second", "풍향", "기온", "수온", "풍속", "유속", "기압", "습도"]]
        # = data[["mmsi", "ship_type", "latitude","longitude", "cog", "sog", "year", "month", "day", "hour", "minute", "second", "풍향", "유향", "기온", "수온", "풍속", "유속", "기압", "습도"]]

        
        # 모델을 사용하여 예측 수행
        latitude = model_latitude.predict([[mmsi, ship_type, latitude,longitude,cog, sog, year, month, day, hour, minute, second,  wind_direction,direct, temperatures, water_temperature, wind_speed, current_speed,atmospheric_pressure, humidity]])
        longitude = model_longitude.predict([[mmsi, ship_type,latitude,longitude, cog, sog, year, month, day, hour, minute, second,wind_direction,direct, temperatures, water_temperature, wind_speed, current_speed,atmospheric_pressure, humidity]])
        cog = model_cog.predict([[mmsi, ship_type, latitude,longitude,cog, sog,year, month, day, hour, minute, second, wind_direction,direct,temperatures, water_temperature, wind_speed,  current_speed,atmospheric_pressure, humidity]])
        sog = model_sog.predict([[mmsi, ship_type, latitude,longitude,cog, sog, year, month, day, hour, minute, second,wind_direction,direct, temperatures, water_temperature, wind_speed,  current_speed,atmospheric_pressure, humidity]])

        # 예측 결과 반환
        result = {'latitude': latitude[0], 'longitude': longitude[0], 'cog': cog[0], 'sog': sog[0]}
        return jsonify(result)
    else:
        # 기상 데이터를 가져오지 못한 경우 에러 메시지 반환
        return jsonify({'error': '기상 데이터 가져오기 실패'})

def get_weather_data(LAT, LON):
    # Construct the URL
    domain = "https://apihub.kma.go.kr/api/typ01/url/kma_buoy.php?"
    tm = "tm=202306161610&"
    stn_id = "stn=22105&"
    option = "help=0&authKey=cJGQY1PQTnuRkGNT0H57zQ"
    auth = ""
    url = domain + tm + stn_id + option + auth
    
    # Fetch weather data using urlopen
    with urlopen(url) as f:
        response = f.read()
    
    print(response)
    data = response.strip()

    # Split the data into lines
    lines = data.split(b'\n')
    
    print("파싱")

    print(lines[4])
    line = lines[4].split(b' ')[4]
    wind_direction = line.decode('utf-8')
    print(line)
    # Return the weather data as a dictionary
    return {'wind_direction': wind_direction}

# Flask 애플리케이션 실행
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
