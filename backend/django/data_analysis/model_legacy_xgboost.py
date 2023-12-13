import pandas as pd
import xgboost as xgb

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

# 대여건수에 대한 XGBoost 모델 생성
xgb_classifier1 = xgb.XGBClassifier(n_estimators=100, random_state=42)
xgb_classifier1.fit(train_x, train_y1)

# 예측 및 정확도 계산
# predictions = xgb_classifier1.predict(test_x)
# accuracy = accuracy_score(train_y1, predictions)
# print(f"모델의 정확도: {accuracy}")

# 반납건수에 대한 XGBoost 모델 생성
xgb_classifier2 = xgb.XGBClassifier(n_estimators=100, random_state=42)
xgb_classifier2.fit(train_x, train_y2)

# 예측 및 정확도 계산
# predictions = xgb_classifier2.predict(test_x)
# accuracy = accuracy_score(train_y2, predictions)

# print(f"모델의 정확도: {accuracy}")
