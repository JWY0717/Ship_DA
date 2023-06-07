from flask import Flask, request, jsonify
import pickle

app = Flask(__name__)

# 모델 불러오기
with open('D:/장우영/LOCALSEARCH/Ship_DA/DA/model_latitude02.pkl', 'rb') as f:
    model_latitude = pickle.load(f)

with open('D:/장우영/LOCALSEARCH/Ship_DA/DA/model_longitude02.pkl', 'rb') as f:
    model_longitude = pickle.load(f)

with open('D:/장우영/LOCALSEARCH/Ship_DA/DA/model_cog02.pkl', 'rb') as f:
    model_cog = pickle.load(f)

with open('D:/장우영/LOCALSEARCH/Ship_DA/DA/    model_sog02.pkl', 'rb') as f:
    model_sog = pickle.load(f)

@app.route('/api03/predict', methods=['POST'])
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
    predicted_latitude = model_latitude.predict([[mmsi, ship_type, latitude, longitude, cog, sog, year, month, day, hour, minute, second, 풍향, 유향, 기온, 수온, 풍속, 유속, 기압, 습도]])
    predicted_longitude = model_longitude.predict([[mmsi, ship_type, latitude, longitude, cog, sog, year, month, day, hour, minute, second, 풍향, 유향, 기온, 수온, 풍속, 유속, 기압, 습도]])
    predicted_cog = model_cog.predict([[mmsi, ship_type, latitude, longitude, cog, sog, year, month, day, hour, minute, second, 풍향, 유향, 기온, 수온, 풍속, 유속, 기압, 습도]])
    predicted_sog = model_sog.predict([[mmsi, ship_type, latitude, longitude, cog, sog, year, month, day, hour, minute, second, 풍향, 유향, 기온, 수온, 풍속, 유속, 기압, 습도]])

    # 예측 결과를 리스트로 변환
    predicted_latitude = predicted_latitude.tolist()
    predicted_longitude = predicted_longitude.tolist()
    predicted_cog = predicted_cog.tolist()
    predicted_sog = predicted_sog.tolist()

    # 예측 결과 반환
    result = {
        'predicted_latitude': predicted_latitude[0],
        'predicted_longitude': predicted_longitude[0],
        'predicted_cog': predicted_cog[0],
        'predicted_sog': predicted_sog[0]
    }
    return jsonify(result)

# 플라스크 애플리케이션 실행
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
