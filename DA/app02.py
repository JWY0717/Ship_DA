from flask import Flask, request, jsonify
import pickle
import pandas as pd

app = Flask(__name__)

# 훈련된 모델 불러오기
# linear_regression_model23
model = pickle.load(open('D:/장우영/LOCALSEARCH/DA/DA/notebooks/linear_regression_model_Lstm.pkl', 'rb'))

# 예측 끝점 정의    
@app.route('/api02/predict', methods=['POST'])
def predict():
    # 들어오는 요청에서 데이터 가져오기
    data = request.json
    
    # 풍향	유향	기온	수온	풍속	유속	기압	습도

    # 데이터 전처리
    mmsi = data["mmsi"]
    ship_type = data["ship_type"]
    latitude = data["latitude"]
    longitude = data["longitude"]
    cog = data["cog"]
    sog = data["sog"]
    insert_time = pd.Timestamp(data["insert_time"]).strftime('%Y-%m-%d %H:%M:%S') # Convert to Unix timestamp
    wind_direction = data["풍향"]
    direction = data["유향"]
    temperature = data["기온"]
    water_temperature = data["수온"]
    wind_speed = data["풍속"]
    flow_speed = data["유속"]
    air_pressure = data["기압"]
    humidity = data["습도"]
    
    # 입력 데이터로 DataFrame 생성  
    input_data = pd.DataFrame({
        "mmsi": [float(mmsi)],
        "latitude": [float(latitude)],
        "longitude": [float(longitude)],
        "cog": [float(cog)],
        "sog": [float(sog)],
        "ship_type": [float(ship_type)],
        "year": (pd.to_datetime(insert_time).year),
        "month": (pd.to_datetime(insert_time).month),
        "day": (pd.to_datetime(insert_time).day),
        "hour": (pd.to_datetime(insert_time).hour),
        "minute": (pd.to_datetime(insert_time).minute),
        "second": (pd.to_datetime(insert_time).second),
        "풍향": [float(wind_direction)],
        "유향": [float(direction)],
        "기온": [float(temperature)],
        "수온": [float(water_temperature)],
        "풍속": [float(wind_speed)],
        "유속": [float(flow_speed)],
        "기압": [float(air_pressure)],
        "습도": [float(humidity)]
    })
    
    
    # Convert input data shape to fit LSTM
    #input_data_reshaped = input_data.values.reshape((input_data.shape[0], 1, input_data.shape[1]))
    input_data_reshaped = input_data.values.reshape((input_data.shape[0], 1, input_data.shape[1]))

    # 훈련된 모델을 사용하여 예측하기
    prediction = model.predict(input_data_reshaped)
    
    # float type
    prediction = prediction.astype(float)
    
    # 응답 JSON 생성
    response = {
        "latitude": prediction[0][0], # 위도
        "longitude": prediction[0][1],
        "predicted_cog": prediction[0][2],
        "predicted_sog": prediction[0][3]
    }
    
    # 응답을 JSON으로 반환
    return jsonify(response)

# 플라스크 애플리케이션 실행
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
