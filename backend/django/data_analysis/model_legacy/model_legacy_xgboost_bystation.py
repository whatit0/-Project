import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error, explained_variance_score, mean_absolute_error
import matplotlib.pyplot as plt

# 데이터 준비
data = pd.read_csv('backend\django\data_analysis\data\datafile\대여소별정제데이터.csv')

# 데이터 정제
data['유동인구(명)'] = data['유동인구(명)'].astype(int)
data = data.drop('대여소ID', axis=1)

# 독립변수 및 종속변수 설정
columns_to_keep = [col for col in data.columns if col not in ['대여건수', '반납건수']]
train_x = data[columns_to_keep]
train_y1 = data['대여건수']
train_y2 = data['반납건수']

# 데이터 분할
X_train, X_test, y1_train, y1_test = train_test_split(train_x, train_y1, test_size=0.2, random_state=42)
_, _, y2_train, y2_test = train_test_split(train_x, train_y2, test_size=0.2, random_state=42)

# 모델 작성
xgb_model_rent = xgb.XGBRegressor()
xgb_model_return = xgb.XGBRegressor()
xgb_model_rent.fit(X_train, y1_train)
xgb_model_return.fit(X_train, y2_train)

# 모델 학습 및 평가
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

# # 피쳐 중요도 시각화
# def plot_feature_importance(model, columns, title):
#     feature_importance = model.feature_importances_
#     sorted_idx = feature_importance.argsort()
#     plt.figure(figsize=(10, 6))
#     plt.barh(range(len(sorted_idx)), feature_importance[sorted_idx], align='center')
#     plt.yticks(range(len(sorted_idx)), [columns[i] for i in sorted_idx])
#     plt.title(title)
#     plt.xlabel('Feature Importance')
#     plt.ylabel('Feature')
#     plt.show()

# # 피쳐 중요도 시각화 실행
# plot_feature_importance(xgb_model_rent, X_train.columns, "Feature Importance for Bike Renting")
# plot_feature_importance(xgb_model_return, X_train.columns, "Feature Importance for Bike Returning")