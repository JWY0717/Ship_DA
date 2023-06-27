# Data Analysis

```shell
$ python -venv venv
$ .\venv\Scripts\activate
$ (venv) pip install -r .\requirements.txt
```

## Flask 실행
> app.py


### 폴더 설명
- notebooks = flask사용 notebook으로 모델 생성 코드를 pickle 이용해서 가져오는 코드 
- report.ipynb = 선박 항해 경로 예측 데이터셋 및 모델 분석 보고서
- model.ipynb = 모델 생성 풀코드

### 코드 설명
- 01_linear model.py = 선형 회귀 모델 코드
- 02_LSTMmodel.py = LSTM모델 코드
- 03_CNN,LSTM..py = LSTM+CNN모델 코드 및 시각화 
- 04_GradientBoostingRegressor.py = radientBoostingRegressor 모델  코드 및 시각화

### ToDo

- [x] step 0. 모델 학습을 위한 이미지 전처리하기
- [x] step 1. CNN, LSTM, 선형을 활용해 간단한 항로 예측 모델 만들어보기
- [x] step 2. 더 큰 모델로 수정하는 과정과 더 정교한 데이터 전처리 과정을 수행하여 정확도 높히기
- [x] step 3. 3가지의 모델 중 정확도와 속도가 정확하고 빠른 커스텀 모델 만들어보기


