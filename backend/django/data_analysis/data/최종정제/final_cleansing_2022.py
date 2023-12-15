import pandas as pd 

test_data = pd.read_csv('backend\django\data_analysis\data\datafile\df_final_final2022_.csv')
output_file = pd.read_csv('backend\django\data_analysis\data\datafile\output_file.csv')

# 범주화는 딥러닝 모델 돌릴때 불필요한 과정일거 같아서 뺌 혹시모르니까 일단 주석
# # 범주화 및 약간의 정제
# # '-' 제거
# train_data['날짜'] = train_data['날짜'].str.replace('-', '')
# # 날씨 비옴 : 1, 비안옴 : 0
# train_data['날씨'] = train_data['날씨'].apply(lambda x: 1 if x == '비옴' else 0)
# # 대여소ID와 대여소명을 범주형(categorical) 데이터로 변환
# train_data['대여소ID'] = train_data['대여소ID'].astype('category')
# train_data['대여소명'] = train_data['대여소명'].astype('category')
# train_data['대여소ID'] = train_data['대여소ID'].cat.codes
# train_data['대여소명'] = train_data['대여소명'].cat.codes
# print(train_data.head(3))

# 요일 행 추가 : 월요일 0 ~ 일요일 6
test_data['날짜'] = pd.to_datetime(test_data['날짜'])
test_data['요일'] = test_data['날짜'].dt.dayofweek
# '날짜' 열을 년, 월, 일로 분리 -> 이렇게 하니까 정확도가 더 높게 나옴
test_data['날짜'] = pd.to_datetime(test_data['날짜'], format='%Y-%m-%d')
test_data['년'] = test_data['날짜'].dt.year
test_data['월'] = test_data['날짜'].dt.month
test_data['일'] = test_data['날짜'].dt.day
test_data.drop('날짜', axis=1, inplace=True)

# 날씨 비옴:1, 비안옴:0으로 대체
test_data['날씨'] = test_data['날씨'].apply(lambda x: 1 if x == '비옴' else 0)

# 유동인구에 결측치 제거
nan_in_population = test_data['유동인구(명)'].isnull().any()
if nan_in_population:
    test_data['유동인구(명)'] = test_data.groupby(['시간대','대여소ID'])['유동인구(명)'].transform(lambda x: x.fillna(x.mean()))
    if test_data['유동인구(명)'].isnull().any():
        test_data['유동인구(명)'].fillna(test_data['유동인구(명)'].mean(), inplace=True)
# 결과 확인
print('유동인구(명)에 NaN 값이 있었는가?', nan_in_population)
print('대체 후 유동인구(명)에 NaN 값이 있는가?', test_data['유동인구(명)'].isnull().any())

# ['평균기온(°C)', 'Pm2.5', '유동인구(명)']만 정규화
# from sklearn.preprocessing import MinMaxScaler
# scaler = MinMaxScaler()
# columns_to_normalize = ['평균기온(°C)', 'Pm2.5', '유동인구(명)']
# test_data[columns_to_normalize] = scaler.fit_transform(test_data[columns_to_normalize])
# print(test_data.head(3))

# '대여소명' 컬럼을 사용하여 '400m_지하철' 열을 생성합니다.
test_data['400m_지하철'] = test_data['대여소명'].isin(output_file['대여소']).astype(int)

# 대여소ID와 대여소명은 겹치는 값이기 때문에 대여소ID만 남기기 
test_data = test_data.drop('대여소명', axis=1)

test_data = test_data.drop(columns=['기준_시간대'])

test_data.to_csv('backend/django/data_analysis/data/datafile/real_final_20222.csv', index=False, encoding='utf-8')
