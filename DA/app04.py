from flask import Flask, request, jsonify
import pickle
import pandas as pd

app = Flask(__name__)

# 모델 불러오기

with open('D:/장우영/LOCALSEARCH/DA/DA/notebooks/model_latitude.pkl', 'rb') as f:
    model_latitude = pickle.load(f)

with open('D:/장우영/LOCALSEARCH/DA/DA/notebooks/model_longitude.pkl', 'rb') as f:
    model_longitude = pickle.load(f)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    
  
    # 예측에 사용할 특성 추출
    mmsi = data['mmsi']
    ship_type = data['ship_type']
    latitude = data['latitude']
    longitude = data['longitude']
    cog = data['cog']
    sog = data['sog']
    year = data['year']
    month = data['month']
    day = data['day']
    hour = data['hour']
    minute = data['minute']
    second = data['second']
    풍향 = data['풍향']
    유향 = data['유향']
    기온 = data['기온']
    수온 = data['수온']
    풍속 = data['풍속']
    유속 = data['유속']
    기압 = data['기압']
    습도 = data['습도']

    # 예측 수행
    latitude = model_latitude.predict([[mmsi, ship_type, cog, sog, year, month, day, hour, minute, second, 풍향, 유향, 기온, 수온, 풍속, 유속, 기압, 습도]])
    longitude = model_longitude.predict([[mmsi, ship_type,longitude, cog, sog, year, month, day, hour, minute, second, 풍향, 유향, 기온, 수온, 풍속, 유속, 기압, 습도]])

    # 예측 결과 반환
    result = {'latitude': latitude[0], 'longitude': longitude[0]}
    return jsonify(result)
    

# 플라스크 애플리케이션 실행
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
