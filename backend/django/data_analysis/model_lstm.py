import pandas as pd

# Load the dataset
df1 = pd.read_csv('backend/django/data_analysis/data/datafile/real_final_2020.csv')
df2 = pd.read_csv('backend/django/data_analysis/data/datafile/real_final_2021.csv')
df3 = pd.read_csv('backend/django/data_analysis/data/datafile/real_final_2022.csv')
data = pd.concat([df1, df2, df3], axis=0)


# Combine year, month, day, and time columns to create a datetime object
data['datetime'] = pd.to_datetime(data[['년', '월', '일', '시간대']].astype(str).agg('-'.join, axis=1), format='%Y-%m-%d-%H')

# Set this new datetime column as the index
data.set_index('datetime', inplace=True)

# Display the first few rows of the modified dataset
print(data.head(3))

from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import numpy as np

# Assuming 'data' is your DataFrame and you are predicting '대여건수'
target_column = '대여건수'

# Normalize features
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data.drop(columns=['대여소ID', '년', '월', '일', '시간대', '요일']))

# Create sequences
def create_sequences(data, target, time_steps=1):
    X, y = [], []
    for i in range(len(data) - time_steps):
        X.append(data[i:(i + time_steps)])
        y.append(target[i + time_steps])
    return np.array(X), np.array(y)

# 하이퍼파라미터 튜닝
time_steps = 24  # 시간 단계 조정
n_neurons = 100  # LSTM 뉴런 수 증가
X, y = create_sequences(scaled_data, data[target_column].values, time_steps)
print(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

from keras.models import Sequential
from keras.layers import Dense, LSTM
from keras.layers import Dropout
from keras.callbacks import EarlyStopping
# 모델 구축
model = Sequential()
model.add(LSTM(n_neurons, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])))
model.add(Dropout(0.2))  # 드롭아웃 추가
model.add(LSTM(n_neurons, return_sequences=False))
model.add(Dropout(0.2))  # 드롭아웃 추가
model.add(Dense(50))  # Dense 층 추가
model.add(Dense(1))

# 조기 종료 콜백 설정
early_stopping = EarlyStopping(monitor='val_loss', patience=10)

# 모델 컴파일 및 훈련
model.compile(optimizer='adam', loss='mean_squared_error')
history = model.fit(X_train, y_train, epochs=100, batch_size=32, validation_data=(X_test, y_test), callbacks=[early_stopping])

history = model.fit(X_train, y_train, epochs=100, batch_size=32, validation_data=(X_test, y_test))

# Make predictions
predictions = model.predict(X_test)

# Evaluate predictions
from sklearn.metrics import mean_squared_error, r2_score
mse = mean_squared_error(y_test, predictions)
print(f"Mean Squared Error: {mse}")

# R² 계산
r2 = r2_score(y_test, predictions)
print(f'R-squared: {r2}')

# Loss와 Accuracy 그래프 출력
import matplotlib.pyplot as plt

# 훈련 및 검증 손실 그래프
plt.plot(history.history['loss'], label='train_loss')
plt.plot(history.history['val_loss'], label='val_loss')
plt.title('Model Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.show()

# 훈련 및 검증 정확도 그래프
plt.plot(history.history['r2'], label='train_r2')
plt.plot(history.history['val_r2'], label='val_r2')
plt.title('Model R-squared')
plt.xlabel('Epoch')
plt.ylabel('R-squared')
plt.legend()
plt.show()

model.save('lstm_rent_model.h5')