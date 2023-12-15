from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import pandas as pd

# 데이터 준비
data_2020 = pd.read_csv('backend/django/data_analysis/data/datafile/real_final_2020.csv')
data_2021 = pd.read_csv('backend/django/data_analysis/data/datafile/real_final_2021.csv')
data = pd.concat([data_2020, data_2021], axis=0)

# 데이터 정제
data['유동인구(명)'] = data['유동인구(명)'].astype(int)
data['대여소ID'] = data['대여소ID'].str[3:].astype(int)

# 독립변수와 종속 변수 설정
columns = [col for col in data.columns if col not in ['대여건수', '반납건수']]
train_x = data[columns]
train_y1 = data['대여건수']
train_y2 = data['반납건수']

# 데이터 분할
X_train, X_test, y1_train, y1_test = train_test_split(train_x, train_y1, test_size=0.2, random_state=42)
_, _, y2_train, y2_test = train_test_split(train_x, train_y2, test_size=0.2, random_state=42)

import numpy as np 
# X_train을 3차원으로 재구조화
X_train_np = np.array(X_train)
time_steps = 1  # 각 샘플은 단일 시간 단계를 가짐
features = 11   # 원본 데이터의 특성 수

X_train_reshaped = X_train_np.reshape((-1, time_steps, features))
print("Reshaped shape:", X_train_reshaped.shape)

# X_test도 동일하게 변환
X_test_np = np.array(X_test)
X_test_reshaped = X_test_np.reshape((-1, time_steps, features))
print("Reshaped shape:", X_test_reshaped.shape)

# 모델 평가 함수
def evaluate_model(model, X_test, y_test):
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    return mse

# 모델 생성 함수 업데이트 (인자로 X_train 제거)
def create_model(neurons=50, dropout_rate=0.2):
    model = Sequential([
        LSTM(neurons, return_sequences=True, input_shape=(time_steps, features)),
        Dropout(dropout_rate),
        LSTM(neurons),
        Dropout(dropout_rate),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

# 모델 생성 및 훈련 (X_train 대신 X_train_reshaped 사용)
model_rent = create_model()
model_rent.fit(X_train_reshaped, y1_train, epochs=50, batch_size=32, verbose=2)

model_return = create_model()
model_return.fit(X_train_reshaped, y2_train, epochs=50, batch_size=32, verbose=2)

# 모델 평가 (X_test 대신 X_test_reshaped 사용)
rent_mse = evaluate_model(model_rent, X_test_reshaped, y1_test)
return_mse = evaluate_model(model_return, X_test_reshaped, y2_test)

print("대여건수 모델 MSE:", rent_mse)
print("반납건수 모델 MSE:", return_mse)
