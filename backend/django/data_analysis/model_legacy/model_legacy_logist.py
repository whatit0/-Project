import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from matplotlib.colors import ListedColormap
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np
import joblib
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler


# 데이터 로딩
pd.options.display.max_columns = None
df1 = pd.read_csv('최종데이터/real_final_2020.csv')
df2 = pd.read_csv('최종데이터/real_final_2021.csv')
df3 = pd.read_csv('최종데이터/real_final_2022.csv')

df = pd.concat([df1, df2, df3], axis=0)

# '-' 제거
# df['날짜'] = df['날짜'].str.replace('-', '')
# 날씨 비옴 : 1, 비안옴 : 0
df['날씨'] = df['날씨'].apply(lambda x: 1 if x == '비옴' else 0)
# 유동인구에 결측치 제거
nan_in_population = df['유동인구(명)'].isnull().any()
if nan_in_population:
    df['유동인구(명)'] = df.groupby(['시간대'])['유동인구(명)'].transform(lambda x: x.fillna(x.mean()))
    if df['유동인구(명)'].isnull().any():
        df['유동인구(명)'].fillna(df['유동인구(명)'].mean(), inplace=True)

df['유동인구(명)'] = df['유동인구(명)'].astype(int)
df['대여소ID'] = df['대여소ID'].str[3:].astype(int)


# 필요한 특성 선택
x = df[['대여소ID', '시간대', '날씨', '평균기온(°C)', 'Pm2.5', '유동인구(명)','년','월','일']]

# 대여건수를 예측할 대상 변수 선택
y = df['반납건수']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=0)
print(x_train.shape, x_test.shape, y_train.shape, y_test.shape)  # (670613, 6) (287406, 6) (670613,) (287406,)

# scaling(크기를 고르게) - feature에 대한 표준화, 정규화 : 최적화 과정에서 안정성, 수련 속도를 향상, 오버피팅 or 언더피팅 방지 기능
print(x_train[:3])
sc = StandardScaler()
sc.fit(x_train)
sc.fit(x_test)
x_train = sc.transform(x_train)
x_test = sc.transform(x_test)
print(x_train[:3])
# 스케일링 값 원복 (똑같지 않을 수 있음 - 근사치로 감)
# 정규화/ 표준화는 feature에 하는거임. label에 하는거 아님(1, 0뿐인데)
# predict할 때 정규화 했으면 정규화 한 값으로 바꿔서 예측치 돌려야됨
# inver_x_train = sc.inverse_transform(x_train)
# print(inver_x_train[:3])

model = LogisticRegression(C=1.0, solver='lbfgs', multi_class='auto', random_state=0, verbose=1)
print(model)


model.fit(x_train, y_train)

# 분류 예측
y_pred = model.predict(x_test)
print('예측값 : ', y_pred)
print('실제값 : ', y_test)
print('총 갯수 : %d, 오류 수 : %d'%(len(y_test), (y_test != y_pred).sum()))
print('분류 정확도 확인 1')
print('%.5f'%accuracy_score(y_test, y_pred))

print('분류 정확도 확인 2')
con_mat = pd.crosstab(y_test, y_pred, rownames=['예측값'], colnames=['관측값'])
print(con_mat)
print((con_mat[0][0] + con_mat[1][1] + con_mat[2][2]) / len(y_test))  # 0.9777

print('분류 정확도 확인 3')
print('test로 정확도는 ', model.score(x_test, y_test))  # 0.977777
print('train으로 정확도는 ', model.score(x_train, y_train))  # 0.97142

# 모델 성능이 만족스러운 경우 모델 저장
# joblib.dump(model, 'logist.sav')

del model
mymodel = joblib.load('logist.sav')
print('새로운 값으로 분류 예측 // 스케일링해서 학습했다면'
      '예측 데이터도 스케일링 해야됨 ')
print(x_test[:2])
new_data = np.array(([[818, 3, 1, 25, 20, 30000, 2022, 3, 5]]))
# 길이가 이거랑 이거일 때 꽃의 종류가 뭐야?  스케일링 된 모델이라면 위의 값도 스케일링 해서 넣어야 됨
new_pred = mymodel.predict(new_data)  # softmax함수가 반환한 결과에 대해 가장 큰 인덱스를 반환
print('예측 결과 : ', new_pred)
# print('softmax 결과(날것) : ', mymodel.predict_proba(new_data))
# 이항분류일 땐 시그모이드 다항분류일 땐 소프트 맥스
