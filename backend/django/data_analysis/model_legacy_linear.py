import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error, explained_variance_score, mean_absolute_error
from sklearn.preprocessing import PolynomialFeatures
from statsmodels.stats.outliers_influence import variance_inflation_factor
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

# LinearRegression 

train_2020 = pd.read_csv('backend/django/data_analysis/data/datafile/real_final_2020.csv')
train_2021 = pd.read_csv('backend/django/data_analysis/data/datafile/real_final_2021.csv')
train_data = pd.concat([train_2020, train_2021], axis=0)

# 범주화 및 약간의 정제
# '-' 제거
train_data['날짜'] = train_data['날짜'].str.replace('-', '')
# 날씨 비옴 : 1, 비안옴 : 0
train_data['날씨'] = train_data['날씨'].apply(lambda x: 1 if x == '비옴' else 0)
# 대여소ID와 대여소명을 범주형(categorical) 데이터로 변환
train_data['대여소ID'] = train_data['대여소ID'].astype('category')
train_data['대여소명'] = train_data['대여소명'].astype('category')
train_data['대여소ID'] = train_data['대여소ID'].cat.codes
train_data['대여소명'] = train_data['대여소명'].cat.codes
print(train_data.head(3))

# 독립변수, 종속변수 나누기
columns_to_keep = [col for col in train_data.columns if col not in ['대여건수', '반납건수']]
train_x = train_data[columns_to_keep]
train_y1 = train_data['대여건수']
train_y2 = train_data['반납건수']

# 대여건수
poly = PolynomialFeatures(degree=2, include_bias=False)
X_poly = poly.fit_transform(train_x)

model1 = LinearRegression()
model1.fit(X_poly, train_y1)
y_pred = model1.predict(X_poly)

# 평가 지표 계산
r2 = r2_score(train_y1, y_pred)
mse = mean_squared_error(train_y1, y_pred)
rmse = np.sqrt(mse)
mae = mean_absolute_error(train_y1, y_pred)
explained_variance = explained_variance_score(train_y1, y_pred)

print(f'R^2 Score: {r2}')
print(f'Mean Squared Error: {mse}')
print(f'Root Mean Squared Error: {rmse}')
print(f'Mean Absolute Error: {mae}')
print(f'Explained Variance Score: {explained_variance}')

# 다중 공선성 검정
vif_data = pd.DataFrame()
vif_data["feature"] = poly.get_feature_names_out()
vif_data["VIF"] = [variance_inflation_factor(X_poly, i) for i in range(X_poly.shape[1])]
print(vif_data)

# 잔차 계산
residuals = train_y1 - y_pred
# 정규성 검정
_, p_value_for_normality = stats.shapiro(residuals)
print(f'P-value for normality: {p_value_for_normality}')

# 시각화로 선형성, 등분산성 확인
plt.scatter(y_pred, residuals)
plt.xlabel('Predicted')
plt.ylabel('Residuals')
plt.axhline(y=0, color='red', linestyle='--')
plt.show()

# 반납 건수 
model2 = LinearRegression()
model2.fit(X_poly, train_y2)
y_pred = model2.predict(model2)

# 평가 지표 계산
r2 = r2_score(train_y2, y_pred)
mse = mean_squared_error(train_y2, y_pred)
rmse = np.sqrt(mse)
mae = mean_absolute_error(train_y2, y_pred)
explained_variance = explained_variance_score(train_y2, y_pred)

print(f'R^2 Score: {r2}')
print(f'Mean Squared Error: {mse}')
print(f'Root Mean Squared Error: {rmse}')
print(f'Mean Absolute Error: {mae}')
print(f'Explained Variance Score: {explained_variance}')

# 다중 공선성 검정
vif_data = pd.DataFrame()
vif_data["feature"] = poly.get_feature_names_out()
vif_data["VIF"] = [variance_inflation_factor(X_poly, i) for i in range(X_poly.shape[1])]
print(vif_data)

# 잔차 계산
residuals2 = train_y2 - y_pred
# 정규성 검정
_, p_value_for_normality = stats.shapiro(residuals2)
print(f'P-value for normality: {p_value_for_normality}')

# 시각화로 선형성, 등분산성 확인
plt.scatter(y_pred, residuals2)
plt.xlabel('Predicted')
plt.ylabel('Residuals')
plt.axhline(y=0, color='red', linestyle='--')
plt.show()
