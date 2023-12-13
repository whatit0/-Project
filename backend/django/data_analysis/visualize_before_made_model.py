import matplotlib.pyplot  as plt
import seaborn as sns
import pandas as pd 
plt.rc('font', family='malgun gothic')

# 상관계수 확인
train_2020 = pd.read_csv('backend/django/data_analysis/data/datafile/real_final_2020.csv')
train_2021 = pd.read_csv('backend/django/data_analysis/data/datafile/real_final_2021.csv')

train_data = pd.concat([train_2020, train_2021], axis=0)
train_data['유동인구(명)'] = train_data['유동인구(명)'].astype(int)
train_data['대여소ID'] = train_data['대여소ID'].str[3:].astype(int)

corr = train_data.corr()
corr.to_csv('backend\django\data_analysis\_visualization\상관계수.csv', encoding='utf-8-sig')

# 히트맵 
plt.figure(figsize=(10, 8))
sns.heatmap(corr, annot=True, fmt=".2f", cmap='coolwarm')
plt.savefig('backend\django\data_analysis\_visualization\상관계수_히트맵.png', dpi=300)
plt.show()

# 시간대 별 대여건수, 반납건수 시각화
grouped_data = train_data.groupby('시간대').agg({'대여건수':'sum', '반납건수':'sum'}).reset_index()

melted_data = pd.melt(grouped_data, id_vars='시간대', var_name='Type', value_name='Count')

plt.figure(figsize=(15, 8))
barplot = sns.barplot(x='시간대', y='Count', hue='Type', data=melted_data, palette=['skyblue', 'pink'])

plt.title('시간대별 대여건수 및 반납건수')
plt.xlabel('시간대')
plt.ylabel('건수')
plt.xticks(range(24)) 
plt.legend(title='Type')
plt.savefig('backend\django\data_analysis\_visualization\시간대별_대여반납건수_그래프.png')
plt.show()


# 왜도, 첨도, 분산 계산
대여건수_왜도 = train_data['대여건수'].skew()
대여건수_첨도 = train_data['대여건수'].kurtosis()
대여건수_분산 = train_data['대여건수'].var()

반납건수_왜도 = train_data['반납건수'].skew()
반납건수_첨도 = train_data['반납건수'].kurtosis()
반납건수_분산 = train_data['반납건수'].var()

print("대여건수 왜도: ", 대여건수_왜도)
print("대여건수 첨도: ", 대여건수_첨도)
print("대여건수 분산: ", 대여건수_분산)

print("반납건수 왜도: ", 반납건수_왜도)
print("반납건수 첨도: ", 반납건수_첨도)
print("반납건수 분산: ", 반납건수_분산)