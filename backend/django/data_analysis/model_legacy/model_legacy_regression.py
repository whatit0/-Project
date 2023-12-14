import pandas as pd
import xgboost as xgb
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
import lightgbm as lgb 
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error, explained_variance_score, mean_absolute_error

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

# 모델 작성
xgb_model = xgb.XGBRegressor()
linear_model = LinearRegression()
# linear_ols_model = sm.OLS()
lgbm_model = lgb.LGBMRegressor()

# 모델 학습 및 평가
def evaluate_model(model, X_train, y_train ,X_test, y_test):
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    print('r2 score : ',r2)
    print('mse : ',mse)
    print('mae : ',mae)
    return r2, mse, mae

# 함수 활용
print('xgb 대여건수')
evaluate_model(xgb_model, X_train, y1_train, X_test, y1_test)
print('xgb 반납건수')
evaluate_model(xgb_model, X_train, y2_train, X_test, y2_test)
print('LinearRegression 대여건수')
evaluate_model(linear_model, X_train, y1_train, X_test, y1_test)
print('LinearRegression 반납건수')
evaluate_model(linear_model, X_train, y2_train, X_test, y2_test)
# print('OLS 대여건수')
# evaluate_model(linear_ols_model, X_train, y1_train, X_test, y1_test)
# print('OLS 반납건수')
# evaluate_model(linear_ols_model, X_train, y2_train, X_test, y2_test)
print('lgbm 대여건수')
evaluate_model(lgbm_model, X_train, y1_train, X_test, y1_test)
print('lgbm 반납건수')
evaluate_model(lgbm_model, X_train, y2_train, X_test, y2_test)