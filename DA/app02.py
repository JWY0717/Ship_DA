from flask import Flask, request, jsonify
import pickle
import pandas as pd

app = Flask(__name__)


# 훈련된 모델 불러오기
# linear_regression_model23
#D:\장우영\LOCALSEARCH\Ship_DA\DA\model\model_latitude.pkl
model = pickle.load(open('D:/장우영/LOCALSEARCH/Ship_DA/DA/model/linear_regression_model_Lstm.pkl', 'rb'))
loaded_scaler = pickle.load(open('D:/장우영/LOCALSEARCH/Ship_DA/DA/model/scaler.pkl', 'rb'))
# 예측 끝점 정의    
@app.route('/api02/predict', methods=['POST'])
def predict():
    # 들어오는 요청에서 데이터 가져오기
    data = request.json
    
    # 풍향	유향	기온	수온	풍속	유속	기압	습도

    # Preprocess input data
    df = pd.DataFrame(data)
    df['minute'] = pd.to_datetime(df['insert_time']).dt.minute + 1
    X = df[["mmsi", "ship_type", "latitude", "longitude", "cog", "sog", "year", "month", "day", "hour", "minute", "second", "wind direction", "direction", "temperature", "water temperature", "wind speed", "flow speed", "atmospheric pressure", "humidity"]]
    
    # Scale input features
    X_scaled = loaded_scaler.transform(X)
    
    # Reshape input data for LSTM model
    X_reshaped = X_scaled.reshape((X_scaled.shape[0], 1, X_scaled.shape[1]))
    
    # Make predictions using the LSTM model
    y_pred = model.predict(X_reshaped)
    
    # Convert predictions to a list
    y_pred_list = y_pred.tolist()
    
    # Prepare response JSON
    response = {
        "latitude": y_pred_list[0][0],
        "longitude": y_pred_list[0][1],
        "predicted_cog": y_pred_list[0][2],
        "predicted_sog": y_pred_list[0][3]
    }
    
    return jsonify(response)

if __name__ == '__main__':
        app.run(debug=True, host='0.0.0.0', port=5000)