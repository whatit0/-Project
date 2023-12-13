import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error, explained_variance_score, mean_absolute_error
import lightgbm as lgb 
import xgboost as xgb

# 데이터 준비
train_2020 = pd.read_csv('backend/django/data_analysis/data/datafile/real_final_2020.csv')
train_2021 = pd.read_csv('backend/django/data_analysis/data/datafile/real_final_2021.csv')
train_data = pd.concat([train_2020, train_2021], axis=0)

# 데이터 정제
train_data['날씨'] = train_data['날씨'].apply(lambda x: 1 if x == '비옴' else 0)
train_data['대여소ID'] = train_data['대여소ID'].astype('category')
train_data['대여소명'] = train_data['대여소명'].astype('category')
train_data['대여소ID'] = train_data['대여소ID'].cat.codes
train_data['대여소명'] = train_data['대여소명'].cat.codes
# '날짜' 열을 datetime 형식으로 변환
train_data['날짜'] = pd.to_datetime(train_data['날짜'], format='%Y-%m-%d')
train_data['년'] = train_data['날짜'].dt.year
train_data['월'] = train_data['날짜'].dt.month
train_data['일'] = train_data['날짜'].dt.day
train_data.drop('날짜', axis=1, inplace=True)


# 독립변수 및 종속변수 설정
columns_to_keep = [col for col in train_data.columns if col not in ['대여건수', '반납건수']]
train_x = train_data[columns_to_keep]
train_y1 = train_data['대여건수']
train_y2 = train_data['반납건수']

# 데이터 분할
X_train, X_test, y1_train, y1_test = train_test_split(train_x, train_y1, test_size=0.2, random_state=42)
_, _, y2_train, y2_test = train_test_split(train_x, train_y2, test_size=0.2, random_state=42)

# LGBM 모델
lgbm_model_rent = lgb.LGBMRegressor()
lgbm_model_return = lgb.LGBMRegressor()
lgbm_model_rent.fit(X_train, y1_train)
lgbm_model_return.fit(X_train, y2_train)

# XGBoost 모델
xgb_model_rent = xgb.XGBRegressor()
xgb_model_return = xgb.XGBRegressor()
xgb_model_rent.fit(X_train, y1_train)
xgb_model_return.fit(X_train, y2_train)

# 정확도 평가
def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    return r2, mse, mae

# LGBM 및 XGBoost 모델 평가
lgbm_rent_metrics = evaluate_model(lgbm_model_rent, X_test, y1_test)
lgbm_return_metrics = evaluate_model(lgbm_model_return, X_test, y2_test)
xgb_rent_metrics = evaluate_model(xgb_model_rent, X_test, y1_test)
xgb_return_metrics = evaluate_model(xgb_model_return, X_test, y2_test)

# 결과 출력
print("LGBM Rent Metrics:")
print("R2 Score:", lgbm_rent_metrics[0])
print("Mean Squared Error:", lgbm_rent_metrics[1])
print("Mean Absolute Error:", lgbm_rent_metrics[2])

print("LGBM Return Metrics:")
print("R2 Score:", lgbm_return_metrics[0])
print("Mean Squared Error:", lgbm_return_metrics[1])
print("Mean Absolute Error:", lgbm_return_metrics[2])

print("XGBoost Rent Metrics:")
print("R2 Score:", xgb_rent_metrics[0])
print("Mean Squared Error:", xgb_rent_metrics[1])
print("Mean Absolute Error:", xgb_rent_metrics[2])

print("XGBoost Return Metrics:")
print("R2 Score:", xgb_return_metrics[0])
print("Mean Squared Error:", xgb_return_metrics[1])
print("Mean Absolute Error:", xgb_return_metrics[2])

