from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import pandas as pd

app = Flask(__name__)
CORS(app)

# 모델 불러오기
# D:\장우영\LOCALSEARCH\Ship_DA\DA\model\model_latitude.pkl

with open('D:/장우영/LOCALSEARCH/Ship_DA/DA/model/model_latitude.pkl', 'rb') as f:
    model_latitude = pickle.load(f)

with open('D:/장우영/LOCALSEARCH/Ship_DA/DA/model/model_longitude.pkl', 'rb') as f:
    model_longitude = pickle.load(f)
    
with open('D:/장우영/LOCALSEARCH/Ship_DA/DA/model/model_cog.pkl', 'rb') as f:
    model_cog = pickle.load(f)

with open('D:/장우영/LOCALSEARCH/Ship_DA/DA/model/model_sog.pkl', 'rb') as f:
    model_sog = pickle.load(f)

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
    # year = data['year']
    # month = data['month']
    # day = data['day']
    # hour = data['hour']
    # minute = data['minute'] + 1 
    # second = data['second']
    # wind_direction = data['풍향']
    # direct = data['유향']
    # temperatures = data['기온']
    # water_temperature = data['수온']
    # wind_speed = data['풍속']
    # current_speed = data['유속']
    # atmospheric_pressure = data['기압']
    # humidity = data['습도']

    
    # 예측 수행
    
    latitude = model_latitude.predict([[mmsi, ship_type, latitude,longitude,cog, sog, year, month, day, hour, minute, second, wind_direction, direct, temperatures, water_temperature, wind_speed, current_speed, atmospheric_pressure, humidity]])
    longitude = model_longitude.predict([[mmsi, ship_type,latitude,longitude, cog, sog, year, month, day, hour, minute, second, wind_direction, direct, temperatures, water_temperature, wind_speed, current_speed, atmospheric_pressure, humidity]])
    cog = model_cog.predict([[mmsi, ship_type, latitude,longitude,cog, sog, year, month, day, hour, minute, second, wind_direction, direct, temperatures, water_temperature, wind_speed, current_speed, atmospheric_pressure, humidity]])
    sog = model_sog.predict([[mmsi, ship_type, latitude,longitude,cog, sog, year, month, day, hour, minute, second, wind_direction, direct, temperatures, water_temperature, wind_speed, current_speed, atmospheric_pressure, humidity]])


    # 예측 결과 반환
    result = {'latitude': latitude[0], 'longitude': longitude[0],'cog': cog[0],'sog': sog[0]}
    return jsonify(result)
    

# 플라스크 애플리케이션 실행
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    
    
    
# Flask                        2.3.2  
# Flask-Cors                   3.0.10  
# pandas                       2.0.1
# pickleshare                  0.7.5