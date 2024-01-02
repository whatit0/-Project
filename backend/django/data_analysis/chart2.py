import requests
from datetime import datetime, timedelta

base_url = "http://openapi.seoul.go.kr:8088/"
api_key = "6d6f7a7258616e6a3130394342466d79"

station_id = 'ST-777'
all_data = []

current_time = datetime.now()
start_time = current_time - timedelta(hours=24)

for i in range(24):
    target_time = start_time + timedelta(hours=i)
    formatted_time = target_time.strftime("%Y%m%d%H")
    
    url = f"{base_url}{api_key}/json/bikeListHist/1/1000/{formatted_time}?stationId={station_id}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if 'getStationListHist' in data and 'row' in data['getStationListHist'] and len(data['getStationListHist']['row']) > 0:
            # 각 시간별로 첫 번째 데이터만 가져와서 추가
            all_data.append(data['getStationListHist']['row'][0])
    else:
        print(f"Error {response.status_code}: {response.text}")

print(f"총 {len(all_data)}개의 데이터가 수집되었습니다.")
print(all_data)

import pandas as pd
all_data=pd.DataFrame(all_data)
from tabulate import tabulate
print(tabulate(all_data, headers='keys', tablefmt='psql', showindex=True))
