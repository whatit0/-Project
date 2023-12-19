import pandas as pd
from tabulate import tabulate
from sklearn import svm, metrics
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import seaborn as sns
from sklearn import metrics
from sklearn.metrics import r2_score

# 데이터 불러오기
df = pd.read_csv('backend/django/data_analysis/data/datafile/real_final_2020.csv')
# data_2021 = pd.read_csv('backend/django/data_analysis/data/datafile/real_final_2021.csv')
# data_2022 = pd.read_csv('backend/django/data_analysis/data/datafile/real_final_2022.csv')

# df = pd.concat([data_2020, data_2021, data_2022], axis=0)

# 데이터 정제
df['유동인구(명)'] = df['유동인구(명)'].astype(int)
df['대여소ID'] = df['대여소ID'].str[3:].astype(int)

# 데이터 전처리
# 필요한 특성 선택 및 가공
features = ['시간대', '날씨', '평균기온(°C)', 'Pm2.5', '유동인구(명)', '년', '월', '일','400m_지하철']

X = df[features]
y = df['대여건수']

# 훈련 데이터와 테스트 데이터로 분리
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# SVM 회귀 모델 생성 및 학습
model = svm.SVR(C=1.0, epsilon=0.2) # Support Vector Regression 모델
model.fit(X_train, y_train)

# 테스트 데이터에 대한 예측
predictions = model.predict(X_test)
print('예측값 : ', predictions[:10])
print('실제값 : ', y_test[:10].values)

# 모델 평가
mse = metrics.mean_squared_error(y_test, predictions)
print('평균 제곱 오차(MSE) : ', mse)

# R² 계산
r2 = r2_score(y_test, predictions)
print(f'R-squared: {r2}')



#---------------------------------------반납건수--------------------------------------

# 데이터 전처리
# 필요한 특성 선택 및 가공
features = ['시간대', '날씨', '평균기온(°C)', 'Pm2.5', '유동인구(명)', '년', '월', '일']

X = df[features]
y = df['반납건수']

# 훈련 데이터와 테스트 데이터로 분리
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# SVM 회귀 모델 생성 및 학습
model = svm.SVR(C=0.1,shrinking=False)  # Support Vector Regression 모델
model.fit(X_train, y_train)

# 테스트 데이터에 대한 예측
predictions = model.predict(X_test)
print('예측값 : ', predictions[:10])
print('실제값 : ', y_test[:10].values)

# 모델 평가
mse = metrics.mean_squared_error(y_test, predictions)
print('평균 제곱 오차(MSE) : ', mse)

# R² 계산
r2 = r2_score(y_test, predictions)
print(f'R-squared: {r2}')
