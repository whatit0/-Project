import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler

# CSV 파일 읽기
df1 = pd.read_csv('backend/django/data_analysis/data/datafile/real_final_2020.csv')
df2 = pd.read_csv('backend/django/data_analysis/data/datafile/real_final_2021.csv')
df3 = pd.read_csv('backend/django/data_analysis/data/datafile/real_final_2022.csv')
df = pd.concat([df1, df2, df3], axis=0)


# 대여건수를 예측하기 위한 데이터 준비
# 필요한 특성 선택
features = ['시간대', '날씨', '평균기온(°C)', 'Pm2.5', '유동인구(명)', '년', '월', '일']

X = df[features]
y = df['대여건수']


# 훈련 데이터와 테스트 데이터로 분리
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 랜덤 포레스트 모델 생성 및 훈련
model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)

# 테스트 데이터에 대한 예측
y_pred = model.predict(X_test)

# 모델 평가
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

# 새로운 데이터로 대여건수 예측
new_data = pd.DataFrame({'시간대': [15], '날씨': [1], '평균기온(°C)': [5.0], 'Pm2.5': [20.0], '유동인구(명)': [30000.0], '년': [2022], '월':[5], '일':[12]})

# 데이터 표준화
scaler = StandardScaler()
X_scaled = scaler.fit_transform(new_data)

new_data_scaled = scaler.transform(X_scaled)
prediction = model.predict(new_data_scaled)
print(f'예측 대여건수: {prediction}')