import matplotlib.pyplot  as plt
import seaborn as sns
import pandas as pd 
plt.rc('font', family='malgun gothic')

# 상관계수 확인
train_2020 = pd.read_csv('backend\django\data_analysis\data\datafile\df_final_final2020_.csv')
train_2021 = pd.read_csv('backend\django\data_analysis\data\datafile\df_final_final2021_.csv')

train_data = pd.concat([train_2020, train_2021], axis=0)
print(train_data)

# '-' 제거
train_data['날짜'] = train_data['날짜'].str.replace('-', '')
# 날씨 비옴 : 1, 비안옴 : 0
train_data['날씨'] = train_data['날씨'].apply(lambda x: 1 if x == '비옴' else 0)
print(train_data.head(3))

corr = train_data[['대여건수','반납건수','날짜','시간대','날씨','평균기온(°C)','Pm2.5','유동인구(명)']].corr()
corr.to_csv('backend\django\data_analysis\visualization\상관계수.csv', encoding='utf-8-sig')

# 히트맵 
plt.figure(figsize=(10, 8))
sns.heatmap(corr, annot=True, fmt=".2f", cmap='coolwarm')
plt.savefig('backend\django\data_analysis\visualization\상관계수_히트맵.png', dpi=300)
plt.show()

# 독립변수와 종속변수로 나누기
# columns_to_keep = [col for col in train_data.columns if col not in ['대여건수', '반납건수']]
# train_x = train_data[columns_to_keep]
# train_y1 = train_data['대여건수']
# train_y2 = train_data['반납건수']