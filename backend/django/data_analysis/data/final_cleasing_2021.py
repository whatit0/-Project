import pandas as pd 

train_data = pd.read_csv('backend\django\data_analysis\data\datafile\df_final_final2021_.csv')

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

# 유동인구에 결측치 제거
nan_in_population = train_data['유동인구(명)'].isnull().any()
if nan_in_population:
    train_data['유동인구(명)'] = train_data.groupby(['시간대'])['유동인구(명)'].transform(lambda x: x.fillna(x.mean()))
    if train_data['유동인구(명)'].isnull().any():
        train_data['유동인구(명)'].fillna(train_data['유동인구(명)'].mean(), inplace=True)
# 결과 확인
print('유동인구(명)에 NaN 값이 있었는가?', nan_in_population)
print('대체 후 유동인구(명)에 NaN 값이 있는가?', train_data['유동인구(명)'].isnull().any())

# ['평균기온(°C)', 'Pm2.5', '유동인구(명)']만 정규화
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
columns_to_normalize = ['평균기온(°C)', 'Pm2.5', '유동인구(명)']
train_data[columns_to_normalize] = scaler.fit_transform(train_data[columns_to_normalize])
print(train_data.head(3))

train_data.to_csv('backend/django/data_analysis/data/datafile/real_final_2021.csv', index=False, encoding='utf-8')
