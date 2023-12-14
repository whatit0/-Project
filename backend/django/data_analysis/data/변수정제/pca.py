from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import pandas as pd

# 데이터 로드
data_2020 = pd.read_csv('backend/django/data_analysis/data/datafile/real_final_2020.csv')
data_2021 = pd.read_csv('backend/django/data_analysis/data/datafile/real_final_2021.csv')
data_2022 = pd.read_csv('backend/django/data_analysis/data/datafile/real_final_2022.csv')
df = pd.concat([data_2020, data_2021, data_2022], axis=0)

df['대여소ID'] = df['대여소ID'].str[3:].astype(int)

# features (독립 변수), (종속 변수) 정의
features = [col for col in df.columns if col not in ['대여건수', '반납건수']]
X = df[features]  
y = df[['대여건수', '반납건수']]  

# 표준화
X_standardized = StandardScaler().fit_transform(X)

# PCA 수행
pca = PCA()
principal_components = pca.fit_transform(X_standardized)

# 주성분으로 데이터프레임 만들기
principal_df = pd.DataFrame(data=principal_components, columns=['PC' + str(i) for i in range(1, len(features)+1)])

# 설명 분산
explained_variance_ratio = pca.explained_variance_ratio_

# 결과 출력
print("Principal components:")
print(principal_df.head())
print("\nExplained variance ratio:")
print(explained_variance_ratio)

# Interpret the results
# Extracting the PCA component details
components = pca.components_
# Pairing the feature names with the corresponding PCA weights
weights = dict(zip(features, components[0]))  # Only for the first principal component

# Sorting the features based on absolute weight in descending order
sorted_weights = sorted(weights.items(), key=lambda kv: abs(kv[1]), reverse=True)

# Interpretation of the first principal component
print("\nInterpretation of the first principal component:")
for feature, weight in sorted_weights:
    print(f"{feature}: {weight:.4f}")
    
# How much variance the first two principal components explain
variance_explained_first_two = explained_variance_ratio[0] + explained_variance_ratio[1]
print(f"\nThe first two principal components explain {variance_explained_first_two:.2%} of the variance.")


# 평균기온(°C): -0.6837의 가중치를 가지며, 이는 첫 번째 주성분이 주로 낮은 평균 기온과 관련이 있음을 나타냅니다.
# 월: -0.5245의 가중치를 가지며, 첫 번째 주성분이 연중 월에 따른 변동을 반영한다고 볼 수 있습니다.
# 날씨: -0.4783의 가중치로, 날씨의 변화가 첫 번째 주성분에 큰 영향을 미칩니다.
# 시간대: 0.1579의 가중치로, 낮은 가중치임에도 불구하고 시간대가 첫 번째 주성분에 어느 정도 기여하고 있음을 보여줍니다.
# 유동인구(명): 0.0451의 가중치로, 이 변수는 첫 번째 주성분에 비교적 적은 기여를 하고 있습니다.
# 요일: -0.0291의 가중치로, 요일별 변동성이 첫 번째 주성분에 약간의 영향을 끼치고 있음을 보여줍니다.
# 일: -0.0258의 가중치로, 달의 일자가 첫 번째 주성분에 미미한 영향을 줍니다.
# Pm2.5: 0.0163의 가중치로, 대기 질은 첫 번째 주성분에 거의 영향을 주지 않습니다.
# 년: 0.0000의 가중치로, 이 분석에서 연도는 첫 번째 주성분에 영향을 주지 않습니다.