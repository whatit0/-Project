import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import matplotlib.pyplot as plt

plt.rc('font', family='malgun gothic')

# 데이터 준비
df1 = pd.read_csv('backend/django/data_analysis/data/datafile/real_final_2020.csv')
df2 = pd.read_csv('backend/django/data_analysis/data/datafile/real_final_2021.csv')
df3 = pd.read_csv('backend/django/data_analysis/data/datafile/real_final_2022.csv')
data = pd.concat([df1, df2, df3], axis=0)

# 데이터 정제
data['날짜'] = pd.to_datetime(data['날짜'], format='%Y-%m-%d')
data['년'] = data['날짜'].dt.year
data['월'] = data['날짜'].dt.month
data['일'] = data['날짜'].dt.day
data.drop(['날짜','행정동'], axis=1, inplace=True)
data['대여소ID'] = data['대여소ID'].str.replace('ST-', '')
data['대여소ID'] = data['대여소ID'].astype('category')
data['날씨'] = data['날씨'].astype('category')
data['400m_지하철'] = data['400m_지하철'].astype('category')
data['휴일'] = data['요일'].isin([5, 6]).astype(int)
data['계절'] = data['월'].map({1: 4, 2: 4, 3: 1, 4: 1, 5: 1, 6: 2, 7: 2, 8: 2, 9: 3, 10: 3, 11: 3, 12: 4})
data['휴일'] = data['휴일'].astype('category')
data['계절'] = data['계절'].astype('category')

# 정규화 
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
columns_to_scale = ['평균기온(°C)', 'Pm10', '유동인구(명)']
data[columns_to_scale] = scaler.fit_transform(data[columns_to_scale])

# 독립변수 및 종속변수 설정
columns_to_keep = [col for col in data.columns if col not in ['대여건수', '반납건수']]
train_x = data[columns_to_keep]
train_y1 = data['대여건수']
train_y2 = data['반납건수']

# 데이터 분할
X_train, X_test, y1_train, y1_test = train_test_split(train_x, train_y1, test_size=0.2, random_state=42)
_, _, y2_train, y2_test = train_test_split(train_x, train_y2, test_size=0.2, random_state=42)

# 모델 생성 및 학습
rent_params = {
    'colsample_bytree': 0.8925879806965068,
    'learning_rate': 0.12980426929501584,
    'max_depth': 9,
    'n_estimators': 343,
    'subsample': 0.7962072844310213,
    'enable_categorical': True
}
return_params = {
    'colsample_bytree': 0.8925879806965068,
    'learning_rate': 0.12980426929501584,
    'max_depth': 9,
    'n_estimators': 343,
    'subsample': 0.7962072844310213,
    'enable_categorical': True
}

xgb_model_rent = xgb.XGBRegressor(**rent_params)
xgb_model_return = xgb.XGBRegressor(**return_params)
xgb_model_rent.fit(X_train, y1_train)
xgb_model_return.fit(X_train, y2_train)

# 모델 평가 함수
def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    return r2, mse, mae

# XGBoost 모델 평가
xgb_rent_metrics = evaluate_model(xgb_model_rent, X_test, y1_test)
xgb_return_metrics = evaluate_model(xgb_model_return, X_test, y2_test)

# 결과 출력
print("XGBoost Rent Metrics:")
print("R2 Score:", xgb_rent_metrics[0])
print("Mean Squared Error:", xgb_rent_metrics[1])
print("Mean Absolute Error:", xgb_rent_metrics[2])

print("XGBoost Return Metrics:")
print("R2 Score:", xgb_return_metrics[0])
print("Mean Squared Error:", xgb_return_metrics[1])
print("Mean Absolute Error:", xgb_return_metrics[2])

# 피쳐 중요도 시각화 및 저장 함수
def plot_and_save_feature_importance(model, columns, title, filename):
    feature_importance = model.feature_importances_
    sorted_idx = feature_importance.argsort()
    plt.figure(figsize=(10, 6))
    plt.barh(range(len(sorted_idx)), feature_importance[sorted_idx], align='center')
    plt.yticks(range(len(sorted_idx)), [columns[i] for i in sorted_idx])
    plt.title(title)
    plt.xlabel('Feature Importance')
    plt.ylabel('Feature')
    plt.savefig(filename)  # 그래프 저장
    plt.show()

# 피쳐 중요도 시각화 및 저장 실행
plot_and_save_feature_importance(xgb_model_rent, X_train.columns, "Feature Importance for Bike Renting", "backend/django/data_analysis/_visualization/rent_feature_importance.png")
plot_and_save_feature_importance(xgb_model_return, X_train.columns, "Feature Importance for Bike Returning", "backend/django/data_analysis/_visualization/return_feature_importance.png")

xgb_model_rent.save_model('backend/django/data_analysis/made_model/model_xgboost_rent.json')
xgb_model_return.save_model('backend/django/data_analysis/made_model/model_xgboost_return.json')
