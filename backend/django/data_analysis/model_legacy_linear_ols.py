import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.preprocessing import PolynomialFeatures
from statsmodels.stats.outliers_influence import variance_inflation_factor
from scipy import stats
import matplotlib.pyplot as plt

# 데이터 로드
train_2020 = pd.read_csv('backend/django/data_analysis/data/datafile/real_final_2020.csv')
train_2021 = pd.read_csv('backend/django/data_analysis/data/datafile/real_final_2021.csv')
train_data = pd.concat([train_2020, train_2021], axis=0)

# 데이터 전처리
train_data['날짜'] = train_data['날짜'].str.replace('-', '')
train_data['날씨'] = train_data['날씨'].apply(lambda x: 1 if x == '비옴' else 0)
train_data['대여소ID'] = train_data['대여소ID'].astype('category').cat.codes
train_data['대여소명'] = train_data['대여소명'].astype('category').cat.codes

# 독립변수와 종속변수 분리
columns_to_keep = [col for col in train_data.columns if col not in ['대여건수', '반납건수']]
train_x = train_data[columns_to_keep]
train_y1 = train_data['대여건수']
train_y2 = train_data['반납건수']

# 다항 특성 생성
poly = PolynomialFeatures(degree=2, include_bias=False)
X_poly = poly.fit_transform(train_x)

# 상수항 추가
X_poly_with_constant = sm.add_constant(X_poly)

# 대여건수
# OLS 모델 학습
model1 = sm.OLS(train_y1, X_poly_with_constant).fit()

# 모델 요약 출력
print(model1.summary())

# 다중 공선성 검정 (상수항 제외)
vif_data = pd.DataFrame()
vif_data["feature"] = ['const'] + list(poly.get_feature_names_out())
vif_data["VIF"] = [variance_inflation_factor(X_poly_with_constant, i) for i in range(X_poly_with_constant.shape[1])]
print(vif_data)

# 정규성 검정
_, p_value_for_normality = stats.shapiro(model1.resid)
print(f'P-value for normality: {p_value_for_normality}')

# 잔차의 선형성, 등분산성 검사
plt.scatter(model1.predict(), model1.resid)
plt.xlabel('Predicted')
plt.ylabel('Residuals')
plt.axhline(y=0, color='red', linestyle='--')
plt.show()

# 평가 지표 계산
predictions = model1.predict()
r2 = model1.rsquared
mse = model1.mse_resid
rmse = np.sqrt(mse)
mae = np.mean(np.abs(model1.resid))
explained_variance = model1.rsquared_adj

print(f'R^2 Score: {r2}')
print(f'Mean Squared Error: {mse}')
print(f'Root Mean Squared Error: {rmse}')
print(f'Mean Absolute Error: {mae}')
print(f'Explained Variance Score: {explained_variance}')

# 반납건수
# OLS 모델 학습
model2 = sm.OLS(train_y2, X_poly_with_constant).fit()

# 모델 요약 출력
print(model2.summary())

# 다중 공선성 검정 (상수항 제외)
vif_data = pd.DataFrame()
vif_data["feature"] = ['const'] + list(poly.get_feature_names_out())
vif_data["VIF"] = [variance_inflation_factor(X_poly_with_constant, i) for i in range(X_poly_with_constant.shape[1])]
print(vif_data)

# 정규성 검정
_, p_value_for_normality = stats.shapiro(model2.resid)
print(f'P-value for normality: {p_value_for_normality}')

# 잔차의 선형성, 등분산성 검사
plt.scatter(model2.predict(), model2.resid)
plt.xlabel('Predicted')
plt.ylabel('Residuals')
plt.axhline(y=0, color='red', linestyle='--')
plt.show()

# 평가 지표 계산
predictions = model2.predict()
r2 = model2.rsquared
mse = model2.mse_resid
rmse = np.sqrt(mse)
mae = np.mean(np.abs(model2.resid))
explained_variance = model2.rsquared_adj

print(f'R^2 Score: {r2}')
print(f'Mean Squared Error: {mse}')
print(f'Root Mean Squared Error: {rmse}')
print(f'Mean Absolute Error: {mae}')
print(f'Explained Variance Score: {explained_variance}')