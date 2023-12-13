from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import pandas as pd

# 데이터셋을 로드합니다.
data_2020 = pd.read_csv('backend/django/data_analysis/data/datafile/real_final_2020.csv')
data_2021 = pd.read_csv('backend/django/data_analysis/data/datafile/real_final_2021.csv')
data_2022 = pd.read_csv('backend/django/data_analysis/data/datafile/real_final_2022.csv')
df = pd.concat([data_2020, data_2021, data_2022], axis=0)

# PCA에 사용할 수치형 특성들을 선택합니다.
features = ['시간대', '날씨','평균기온(°C)','Pm2.5','유동인구(명)','요일','년','월', '일']
# 특성들을 분리합니다.
x = df.loc[:, features].values

# PCA를 수행합니다.
pca = PCA(n_components=2)  # 시각화를 위해 2개의 주성분으로 축소합니다.
principal_components = pca.fit_transform(x)

# 주성분으로 이루어진 데이터프레임을 생성합니다.
principal_df = pd.DataFrame(data=principal_components)

# 설명된 분산 비율을 확인합니다.
explained_variance = pca.explained_variance_ratio_

print(principal_df.head())
print(explained_variance)

# 주성분의 원래 특성들에 대한 가중치 확인
components = pca.components_

# 각 주성분에 대한 가중치와 원래 특성 이름을 함께 출력
for i, (component, variance) in enumerate(zip(components, explained_variance)):
    component_details = dict(zip(features, component))
    print(f"주성분 {i+1}: 설명된 분산 = {variance:.2f}, 가중치: {component_details}")

# 주성분 분석의 목적 : 변수의 개수를 줄이는 것, 즉 자료의 차원축약

# 해석 
# 주성분 1: 설명된 분산이 거의 1.00으로, 이 주성분이 데이터 변동성의 대부분을 포착합니다. 
# 가장 큰 가중치를 가진 특성은 '유동인구(명)'으로, 거의 모든 변동성이 이 변수에 의해 설명됩니다. 
# 이는 '유동인구(명)'이 데이터 세트에서 가장 중요한 변동 요인이라는 것을 의미합니다. 
# 다른 모든 특성들의 가중치는 매우 작아서 이 주성분에서는 거의 영향을 미치지 않습니다.

# 주성분 2: 설명된 분산이 0에 가깝고, 가장 큰 가중치를 가진 특성은 'Pm2.5'입니다. 
# 그러나 이 주성분의 분산 설명력이 매우 낮기 때문에 이 주성분은 데이터의 변동성을 거의 설명하지 않는 것으로 보입니다. 
# '월'과 '일', 그리고 '요일'의 가중치도 상대적으로 높지만, 전체적인 데이터 변동성에서 차지하는 비중은 미미할 것으로 예상됩니다.

# 이 분석에서 주목할 점은 첫 번째 주성분이 데이터 변동성의 대부분을 설명하고 있으며, '유동인구(명)'이 이 주성분의 구성에 결정적인 역할을 한다는 것입니다. 
# 두 번째 주성분은 추가적인 변동성을 거의 설명하지 못하기 때문에, 데이터를 잘 설명하는 데에는 크게 기여하지 않는 것으로 보입니다.

# 설명된 분산(Explained Variance)은 주성분 분석(PCA)에서 각 주성분이 원본 데이터에서 얼마나 많은 정보(변동성)를 포착하고 있는지를 나타내는 지표입니다. 
# 데이터의 분산은 데이터가 얼마나 퍼져 있는지를 나타내는 척도이며, PCA에서는 이 분산을 최대한 보존하면서 차원을 축소합니다.

# 주성분 1의 설명된 분산은 첫 번째 주성분이 데이터 전체 분산 중 얼마나 많은 부분을 설명하는지를 나타냅니다. 
# 만약 이 값이 1에 가까우면, 첫 번째 주성분 하나로 데이터의 대부분의 변동성을 설명할 수 있다는 의미이며, 
# 이는 데이터의 대부분이 그 주성분에 의해 설명될 수 있음을 의미합니다.

# 주성분 2의 설명된 분산은 두 번째 주성분이 추가로 얼마나 많은 데이터 변동성을 설명하는지를 나타냅니다. 
# 이 값이 매우 낮다면, 두 번째 주성분이 추가하는 정보는 매우 적다는 것을 의미합니다.

# 설명된 분산의 합은 모델이 데이터의 전체 변동성 중 얼마나 많은 부분을 포착할 수 있는지를 나타냅니다. 
# 일반적으로, 몇 개의 주성분으로도 대부분의 분산을 설명할 수 있다면, 
# 그 데이터는 높은 차원에서 낮은 차원으로 효과적으로 축소될 수 있다고 볼 수 있습니다.