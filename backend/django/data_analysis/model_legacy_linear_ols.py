import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.preprocessing import PolynomialFeatures
from statsmodels.stats.outliers_influence import variance_inflation_factor
from scipy import stats
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

# 데이터 준비
data_2020 = pd.read_csv('backend/django/data_analysis/data/datafile/real_final_2020.csv')
data_2021 = pd.read_csv('backend/django/data_analysis/data/datafile/real_final_2021.csv')
data_2022 = pd.read_csv('backend/django/data_analysis/data/datafile/real_final_2022.csv')
data = pd.concat([data_2020, data_2021, data_2022], axis=0)

# 데이터 정제
data['유동인구(명)'] = data['유동인구(명)'].astype(int)
data['대여소ID'] = data['대여소ID'].str[3:].astype(int)

# 독립변수 및 종속변수 설정
columns_to_keep = [col for col in data.columns if col not in ['대여건수', '반납건수']]
train_x = data[columns_to_keep]
train_y1 = data['대여건수']
train_y2 = data['반납건수']

# 데이터 분할
X_train, X_test, y1_train, y1_test = train_test_split(train_x, train_y1, test_size=0.2, random_state=42)
_, _, y2_train, y2_test = train_test_split(train_x, train_y2, test_size=0.2, random_state=42)

def train_and_evaluate_ols(X_train, y_train, X_test, y_test, degree=2):
    # 다항 특성 생성 (상수항 미포함, 상호 작용만 포함)
    poly = PolynomialFeatures(degree, include_bias=False, interaction_only=True)
    X_train_poly = poly.fit_transform(X_train)
    X_test_poly = poly.transform(X_test)
    
    # OLS 모델을 위해 상수항 추가
    X_train_poly_with_constant = sm.add_constant(X_train_poly)
    
    # OLS 모델 학습
    model = sm.OLS(y_train, X_train_poly_with_constant).fit()
    
    # 학습된 모델 요약 출력
    print(model.summary())
    
    # 예측 및 평가 지표 계산
    X_test_poly_with_constant = sm.add_constant(X_test_poly)
    y_pred = model.predict(X_test_poly_with_constant)
    mse = np.mean((y_test - y_pred) ** 2)
    rmse = np.sqrt(mse)
    
    # 평가 지표 출력
    print("Mean Squared Error:", mse)
    print("Root Mean Squared Error:", rmse)

# 대여건수에 대한 모델 학습 및 평가
print("대여 모델 평가:")
train_and_evaluate_ols(X_train, y1_train, X_test, y1_test, degree=3)  # 예시로 degree를 3으로 설정했습니다. 필요에 따라 조정하세요.

# 반납건수에 대한 모델 학습 및 평가
print("반납 모델 평가:")
train_and_evaluate_ols(X_train, y2_train, X_test, y2_test, degree=3)  # 예시로 degree를 3으로 설정했습니다. 필요에 따라 조정하세요.
