from flask import Flask, request, jsonify
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import pickle

app = Flask(__name__)

# LSTM 모델과 스케일러를 로드합니다.
with open('D:/장우영/LOCALSEARCH/Ship_DA/DA/model/linear_regression_model_Lstm.pkl_0623', 'rb') as f:
    model_LSTRM = pickle.load(f)

with open('D:/장우영/LOCALSEARCH/Ship_DA/DA/model/scaler.pkl_0623', 'rb') as f:
    scaler = pickle.load(f)


@app.route('/api02/predict', methods=['POST'])
def predict():
    # POST 요청에서 데이터를 가져옵니다.
    data = request.json
    
    # 데이터 전처리를 수행합니다.
    df = pd.DataFrame([data])  # 데이터를 리스트로 감싸서 단일 행의 DataFrame을 생성합니다.
    df['minute'] = pd.to_datetime(df['insert_time']).dt.minute + 1
    df['insert_time'] = pd.to_datetime(df['insert_time']) + pd.DateOffset(minutes=1)
    X = df[["mmsi", "ship_type", "latitude", "longitude", "cog", "sog", "year", "month", "day", "hour", "minute", "second", "풍향", "유향", "기온", "수온", "풍속", "유속", "기압", "습도"]]
    X_scaled = scaler.transform(X)
    X_reshaped = X_scaled.reshape((X_scaled.shape[0], 1, X_scaled.shape[1]))
    
    # LSTM 모델을 사용하여 예측을 수행합니다.
    y_pred = model_LSTRM.predict(X_reshaped)
    
    # 예측 결과를 리스트로 변환합니다.
    y_pred_list = y_pred.tolist()
    
    # 응답용 JSON을 생성합니다.
    response = {
        "latitude": y_pred_list[0][0],
        "longitude": y_pred_list[0][1],
        "predicted_cog": y_pred_list[0][2],
        "predicted_sog": y_pred_list[0][3]
    }
    
    # JSON 형태로 응답을 반환합니다.
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    