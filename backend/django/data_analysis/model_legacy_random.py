import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm
from sklearn.model_selection import GridSearchCV

plt.rc('font', family='malgun gothic')

# CSV 파일 읽기
df1 = pd.read_csv('backend/django/data_analysis/data/datafile/real_final_2020.csv')
df2 = pd.read_csv('backend/django/data_analysis/data/datafile/real_final_2021.csv')
df3 = pd.read_csv('backend/django/data_analysis/data/datafile/real_final_2022.csv')
df = pd.concat([df1, df2, df3], axis=0)

# 데이터 정제
df['대여소ID'] = df['대여소ID'].str[3:].astype(int)
df['월'] = df['월'].apply(lambda x: 0 if x in [11, 12, 1] else (1 if x in [2, 3, 4] else (2 if x in [5, 6, 7] else 3)))


# StandardScaler를 사용하여 정규화
scaler = StandardScaler()
df[['평균기온(°C)', '유동인구(명)']] = scaler.fit_transform(df[['평균기온(°C)', '유동인구(명)']])


features = ['대여소ID', '시간대', '날씨', '평균기온(°C)', '유동인구(명)', '년', '월', '요일']

# 분기별로 범주화
train = df[df['년'] != 2022]
test = df[df['년'] == 2022]

X_train = train[features]
Y_train = train['대여건수']

X_test = test[features]
Y_test = test['대여건수']
print(X_train.shape)
print(Y_train.shape)
print(X_test.shape)
print(Y_test.shape)

# hyperparameter
# Decision Tree 모델을 여러 개 모아서 만든 것 = Random Forest
# n_estimators : 트리 개수
# n_jobs : 사용할 cpu 개수 (-1로 설정하면 가장 많은 cpu 사용 가능)
# max_depth: 모델의 과대 적합 방지를 위한 깊이 설정 변수
# random_state : random 성질을 고정시킴
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [5, 10, 15]
}

grid_search = GridSearchCV(RandomForestRegressor(random_state=0), param_grid, cv=5, scoring='neg_mean_squared_error')
grid_search.fit(X_train, Y_train)

best_model = grid_search.best_estimator_

# 모델 예측
Y_pred = best_model.predict(X_test)

# 모델 평가
mse = mean_squared_error(Y_test, Y_pred)
print(f'Mean Squared Error: {mse}')

# R²
r2 = r2_score(Y_test, Y_pred)
print(f'R-squared: {r2}')

# 특성 중요도 확인
importances = best_model.feature_importances_
feature_importances = dict(zip(features, importances))
print("Feature Importances:")
print(feature_importances)



# # 새로운 데이터로 대여건수 예측
# new_data = pd.DataFrame({'시간대': [15], '날씨': [1], '평균기온(°C)': [5.0], 'Pm2.5': [20.0], '유동인구(명)': [30000.0], '년': [2022], '월':[5], '일':[12]})

# # 데이터 표준화
# scaler = StandardScaler()
# X_scaled = scaler.fit_transform(new_data)

# new_data_scaled = scaler.transform(X_scaled)
# prediction = model.predict(new_data_scaled)
# print(f'예측 대여건수: {prediction}')