import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
plt.rc('font', family='malgun gothic')

df1 = pd.read_csv('backend/django/data_analysis/data/datafile/real_final_2020.csv')
df2 = pd.read_csv('backend/django/data_analysis/data/datafile/real_final_2021.csv')
df3 = pd.read_csv('backend/django/data_analysis/data/datafile/real_final_2022.csv')
df = pd.concat([df1, df2, df3], axis=0)

# 선택한 열만 추출
selected_columns = ['평균기온(°C)', '유동인구(명)']
df_selected = df[selected_columns]

# StandardScaler를 사용하여 정규화
scaler = StandardScaler()
df_normalized = scaler.fit_transform(df_selected)
df_normalized = pd.DataFrame(df_normalized, columns=selected_columns)


# 평균기온과 유동인구 확인하는 히스토그램 그리기
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
sns.histplot(df_normalized['평균기온(°C)'], kde=True)
plt.title('평균기온(°C) - 정규분포 확인')

plt.subplot(1, 2, 2)
sns.histplot(df_normalized['유동인구(명)'], kde=True)
plt.title('유동인구(명) - 정규분포 확인')

plt.tight_layout()
# plt.savefig('backend\django\data_analysis\_visualization\정규분포_기온_유동인구.png')
plt.show()