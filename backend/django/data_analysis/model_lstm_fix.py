import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
from keras.callbacks import EarlyStopping
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
from sklearn.inspection import permutation_importance

df1 = pd.read_csv('backend/django/data_analysis/data/datafile/real_final_2020.csv')
df2 = pd.read_csv('backend/django/data_analysis/data/datafile/real_final_2021.csv')
df3 = pd.read_csv('backend/django/data_analysis/data/datafile/real_final_2022.csv')
data = pd.concat([df1, df2, df3], axis=0)

# 정규화
scaler = MinMaxScaler(feature_range=(0, 1))
selected_columns = data[['평균기온(°C)', 'Pm2.5', '유동인구(명)']]
scaled_data = scaler.fit_transform(selected_columns)

# 날짜 열을 datetime로 변환
data['datetime'] = pd.to_datetime(data[['기준_날짜', '시간대']].astype(str).agg('-'.join, axis=1), format='%Y-%m-%d-%H')

def create_sequences(data, target, time_steps=1):
    X, y = [], []
    
    for i in range(len(data) - time_steps):
        X.append(data[i:(i + time_steps)])
        y.append(target[i + time_steps])
        
    return np.array(X), np.array(y)

def build_model(X_train_shape, n_neurons=100):
    model = Sequential()
    model.add(LSTM(n_neurons, return_sequences=True, input_shape=(X_train_shape[1], X_train_shape[2])))
    model.add(Dropout(0.2))
    model.add(LSTM(n_neurons, return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(50))
    model.add(Dense(1))
    
    return model


def train_and_evaluate_model(X_train, y_train, X_test, y_test):

    early_stopping = EarlyStopping(monitor='val_loss', patience=10)
    model = build_model(X_train.shape)
    model.compile(optimizer='adam', loss='mean_squared_error')

    history = model.fit(
        X_train, y_train, 
        epochs=100, batch_size=32, validation_data=(X_test, y_test), callbacks=[early_stopping])

    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)

    return model, history, mse, r2


def plot_and_save_history(history, filename_loss):
    plt.figure()
    plt.plot(history.history['loss'], label='train_loss')
    plt.plot(history.history['val_loss'], label='val_loss')
    plt.title('Model Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.savefig(filename_loss)

def save_model(model, model_filename):
    model.save(model_filename)
    
# 대여건수 ---------------------------------------------------------------------------------

# 데이터 준비
target=data['대여건수']
X, y = create_sequences(scaled_data, target, time_steps=24)
print(X)
print(y)
X_train, X_test, y1_train, y1_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 모델 학습 및 평가
model_rent, history, mse, r2 = train_and_evaluate_model(X_train, y1_train, X_test, y1_test)
print(f"Rent Mean Squared Error: {mse}")
print(f'Rent R-squared: {r2}')

# 시각화 및 저장
plot_and_save_history(history, 'model_rent_loss.png')

# 모델 저장
save_model(model_rent, 'lstm_model_rent.h5')
# 반납건수 ---------------------------------------------------------------------------------

# 데이터 준비
target2=data['반납건수']
X, y = create_sequences(scaled_data, target2, time_steps=24)
X_train, X_test, y2_train, y2_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 모델 학습 및 평가
model_return, history, mse, r2 = train_and_evaluate_model(X_train, y2_train, X_test, y2_test)
print(f"Return Mean Squared Error: {mse}")
print(f'Return R-squared: {r2}')

# 시각화 및 저장
plot_and_save_history(history, 'model_return_loss.png')

# 모델 저장
save_model(model_return, 'lstm_model_return.h5')

# 대여건수 ----
# 특성 중요도 계산
results = permutation_importance(model_rent, X_test, y1_test, n_repeats=10, random_state=42, scoring='neg_mean_squared_error')

# 중요도 출력
importance = results.importances_mean
for i, imp in enumerate(importance):
    print(f'Feature {i}: Importance: {imp}')

# 반납건수 ----
# 특성 중요도 계산
results = permutation_importance(model_return, X_test, y2_test, n_repeats=10, random_state=42, scoring='neg_mean_squared_error')

# 중요도 출력
importance = results.importances_mean
for i, imp in enumerate(importance):
    print(f'Feature {i}: Importance: {imp}')
