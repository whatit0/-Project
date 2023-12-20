'''
차트로 보여주어야 하는 것

- chart.js - 리액트와 함께 웹상에서 필요한 차트를 받아올수 있도록 하기  → 일단은 html로 (준수)
- 차트 : 따릉이 실시간 api 자료 받아서 최근 24시간 데이터로 시간별 잔여대수 그래프 그리기

나중에 된다면 대여소별로 (실시간 api 불러와서 시간별 잔여대수를 그래프로 불러오기 + 대여소별로 나온다면 정말 좋겠다)
'''

import requests
import pandas as pd


# API에서 데이터 가져오기
items_per_page = 1000
total_items = 3000
all_data = []

for page in range(1, total_items // items_per_page + 2):
    start_item = (page - 1) * items_per_page + 1
    end_item = page * items_per_page
    url = f"http://openapi.seoul.go.kr:8088/456852427579656a313035727966656c/json/bikeList/{start_item}/{end_item}"

    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if 'rentBikeStatus' in data and 'row' in data['rentBikeStatus']:
            all_data.extend(data['rentBikeStatus']['row'])
    else:
        print(f"Error {response.status_code}: {response.text}")

# 대여소 ID 리스트
included_ids = [
    'ST-814', 'ST-1181', 'ST-1879', 'ST-1245', 'ST-799', 'ST-1703', 'ST-1680', 'ST-1575', 'ST-1885',
    'ST-777', 'ST-1559', 'ST-1247', 'ST-1897', 'ST-1895', 'ST-960', 'ST-1880', 'ST-966', 'ST-1574', 'ST-1896',
    'ST-953', 'ST-797', 'ST-804', 'ST-1407', 'ST-1560', 'ST-818', 'ST-795', 'ST-787', 'ST-791', 'ST-1888',
    'ST-1578', 'ST-1892', 'ST-812', 'ST-1679', 'ST-807', 'ST-802', 'ST-1364', 'ST-1184', 'ST-1433', 'ST-822',
    'ST-1171', 'ST-1884', 'ST-784', 'ST-798', 'ST-816', 'ST-782', 'ST-794', 'ST-820', 'ST-810', 'ST-1887',
    'ST-821', 'ST-1571', 'ST-1566', 'ST-796', 'ST-1704', 'ST-1365', 'ST-1178', 'ST-956', 'ST-1893', 'ST-1889',
    'ST-937', 'ST-1886', 'ST-790', 'ST-1174', 'ST-783', 'ST-1576', 'ST-811', 'ST-1248', 'ST-1573', 'ST-809',
    'ST-786', 'ST-793', 'ST-959', 'ST-1246', 'ST-954', 'ST-792', 'ST-779', 'ST-1564', 'ST-815', 'ST-963',
    'ST-1177', 'ST-1366', 'ST-1172', 'ST-1180', 'ST-803', 'ST-958', 'ST-806', 'ST-1882', 'ST-1563', 'ST-1894',
    'ST-1182', 'ST-1562', 'ST-1891', 'ST-957', 'ST-1565', 'ST-1185', 'ST-962', 'ST-1179', 'ST-1568', 'ST-1881',
    'ST-1561', 'ST-801', 'ST-817', 'ST-961', 'ST-778',
]

# 필요한 데이터만 추출
filtered_data = [{'parkingBikeTotCnt': data['parkingBikeTotCnt'], 'stationId': data['stationId'],'stationName': data['stationName']} for data in all_data if data.get('stationId') in included_ids]

# 결과 확인
print(f"총 {len(filtered_data)}개의 데이터가 추출되었습니다.")

df=pd.DataFrame(filtered_data)

# 열의 이름 변경 (stationId -> 대여소ID, parkingBikeTotCnt -> 따릉이개수)
df = df.rename(columns={'stationId': '대여소ID', 'parkingBikeTotCnt': '따릉이개수','stationName':'대여소명'})

# 열의 순서 변경 (대여소ID와 따릉이개수의 순서 변경)
df = df[['대여소ID','대여소명','따릉이대여가능건수']]

# 변경된 DataFrame 출력
print(df)
