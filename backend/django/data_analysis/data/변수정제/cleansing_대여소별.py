import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
plt.rc('font', family='malgun gothic')

data_2020 = pd.read_csv('backend/django/data_analysis/data/datafile/df_final_final2020_.csv')
data_2021 = pd.read_csv('backend/django/data_analysis/data/datafile/df_final_final2021_.csv')
data_2022 = pd.read_csv('backend/django/data_analysis/data/datafile/df_final_final2022_.csv')
data = pd.concat([data_2020, data_2021, data_2022], axis=0)

# 특정 대여소만 하나 뽑아 보겠음
data['대여소ID'] = data['대여소ID'].str[3:].astype(int)
data = data[data['대여소ID'] == 1181]

# '날짜' 열을 년, 월, 일로 분리 -> 이렇게 하니까 정확도가 더 높게 나옴
data['날짜'] = pd.to_datetime(data['날짜'], format='%Y-%m-%d')
data['년'] = data['날짜'].dt.year
data['월'] = data['날짜'].dt.month
data['일'] = data['날짜'].dt.day
# 요일 행 추가 : 월요일 0 ~ 일요일 6
data['날짜'] = pd.to_datetime(data['날짜'])
data['요일'] = data['날짜'].dt.dayofweek
data.drop('날짜', axis=1, inplace=True)

# 대여소ID와 대여소명은 겹치는 값이기 때문에 대여소ID만 남기기 
data = data.drop('대여소명', axis=1)

# 날씨 비옴:1, 비안옴:0으로 대체
data['날씨'] = data['날씨'].apply(lambda x: 1 if x == '비옴' else 0)

# 유동인구에 결측치 제거
nan_in_population = data['유동인구(명)'].isnull().any()
if nan_in_population:
    data['유동인구(명)'] = data.groupby(['시간대','대여소ID'])['유동인구(명)'].transform(lambda x: x.fillna(x.mean()))
    if data['유동인구(명)'].isnull().any():
        data['유동인구(명)'].fillna(data['유동인구(명)'].mean(), inplace=True)
# 결과 확인
print('유동인구(명)에 NaN 값이 있었는가?', nan_in_population)
print('대체 후 유동인구(명)에 NaN 값이 있는가?', data['유동인구(명)'].isnull().any())

# data.to_csv('backend/django/data_analysis/data/datafile/대여소별정제데이터.csv', index=False, encoding='utf-8')

corr = data.corr()
# corr.to_csv('backend\django\data_analysis\_visualization\상관계수.csv', encoding='utf-8-sig')

# 히트맵 
plt.figure(figsize=(10, 8))
sns.heatmap(corr, annot=True, fmt=".2f", cmap='coolwarm')
plt.savefig('backend\django\data_analysis\_visualization\상관계수_히트맵_대여소별2.png', dpi=300)
plt.show()