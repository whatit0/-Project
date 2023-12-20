from django.shortcuts import render
import xgboost as xgb
import pandas as pd
import numpy as np
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt  # 추가
from django.views.decorators.http import require_POST  # 추가

# Create your views here.
def index(request):
    return render(request, "hi.html")

def load_model(model_path):
    # 모델 불러오기
    loaded_model = xgb.XGBRegressor()
    loaded_model.load_model(model_path)
    return loaded_model

def prepare_new_data(new_data):
    # 리스트를 DataFrame으로 변환
    columns = ['대여소ID', '시간대', '날씨', '평균기온(°C)', 'Pm2.5', '유동인구(명)', '요일', '년', '월', '일', '400m_지하철']
    new_df = pd.DataFrame([new_data], columns=columns)

    # 필요한 데이터 변환 수행
    new_df['유동인구(명)'] = new_df['유동인구(명)'].astype(int)
    new_df['대여소ID'] = new_df['대여소ID'].str[3:].astype(int)

    return new_df


def predict_new_data(model, new_data):
    # 새 데이터 예측
    predictions = model.predict(new_data)
    return predictions

@csrf_exempt
@require_POST
def handle_predictions(request):
    try:
        data = request.POST
        selected_date = data.get('date')
        selected_time = data.get('time')
        station_id = data.get('stationId')
        print(selected_date, selected_time, station_id)

        # 모델 경로
        rent_model_path = 'data_analysis/made_model/model_xgboost_rent.json'
        return_model_path = 'data_analysis/made_model/model_xgboost_return.json'

        # 모델 불러오기
        rent_model = load_model(rent_model_path)
        return_model = load_model(return_model_path)
        
        # 임시로
        # 새 데이터 
        new_data = ['STS-818', 20, 0, 29.896258, 23.998998, 41021, 5, 2022, 1, 1, 1]

        # 데이터 준비
        prepared_data = prepare_new_data(new_data)
        
        # 예측 수행
        rent_predictions = predict_new_data(rent_model, prepared_data)
        return_predictions = predict_new_data(return_model, prepared_data)

        # NumPy 배열을 Python 리스트로 변환
        rent_predictions_list = rent_predictions.tolist() # toJson
        return_predictions_list = return_predictions.tolist()

        # JSON 응답 생성
        response_data = {
            'rent_predictions': rent_predictions_list,
            'return_predictions': return_predictions_list,
        }

        # 예측 결과를 클라이언트에게 전송 
        return JsonResponse(response_data)
    except Exception as e:
        # 오류 처리
        return JsonResponse({'error': str(e)}, status=500)

import requests
import pandas as pd
from tabulate import tabulate
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
from django.http import HttpResponse
from django.shortcuts import render
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import io
import json

def showchart(request):
    base_url = "http://openapi.seoul.go.kr:8088/"
    api_key = "6d6f7a7258616e6a3130394342466d79"

    # 현재 시간과 24시간 전의 시간 계산
    current_time = datetime.now()
    start_time = current_time - timedelta(hours=24)

    all_data = []

    for i in range(24):
        target_time = start_time + timedelta(hours=i)
        formatted_time = target_time.strftime("%Y%m%d%H")
        
        items_per_page = 1000
        total_items = 3000
        data_per_hour = []  # 각 시간대의 데이터를 임시로 담을 리스트를 생성합니다.

        for page in range(1, total_items // items_per_page + 2):
            start_item = (page - 1) * items_per_page + 1
            end_item = page * items_per_page
            url = f"http://openapi.seoul.go.kr:8088/6d6f7a7258616e6a3130394342466d79/json/bikeListHist/{start_item}/{end_item}/{formatted_time}"

            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                if 'getStationListHist' in data and 'row' in data['getStationListHist']:
                    data_per_hour.extend(data['getStationListHist']['row'])
            else:
                print(f"Error {response.status_code}: {response.text}")

        all_data.extend(data_per_hour)  # 각 시간대의 데이터를 모든 데이터 리스트에 추가합니다.

    # 모든 데이터가 담긴 리스트 출력
    print(f"총 {len(all_data)}개의 데이터가 수집되었습니다.")


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
        'ST-1561', 'ST-801', 'ST-817', 'ST-961', 'ST-778'
    ]

    # 필요한 데이터만 추출
    filtered_data = [
        {
            'rackTotCnt': data['rackTotCnt'],
            'parkingBikeTotCnt': data['parkingBikeTotCnt'],
            'stationId': data['stationId'],
            'stationName': data['stationName'],
            'stationDt': data['stationDt']
        }
        for data in all_data
        if data.get('stationId') in included_ids
    ]

    # 결과 확인
    print(f"다시 총 {len(filtered_data)}개의 데이터가 추출되었습니다.")
    df=pd.DataFrame(filtered_data)

    print(tabulate(df.head(100), headers='keys', tablefmt='psql', showindex=True))

    # 한글 폰트 설정 - 각자의 환경에 맞게 설정해주세요
    font_path = "C:/Windows/Fonts/malgun.ttf"  # 한글 폰트 파일 경로
    font_name = font_manager.FontProperties(fname=font_path).get_name()
    rc('font', family=font_name)

    # 'ST-814' 대여소의 데이터 추출
    station_814_data = df[df['stationId'] == 'ST-777']

    # stationDt 열을 datetime 형식으로 변환
    station_814_data['stationDt'] = pd.to_datetime(station_814_data['stationDt'], format='%Y%m%d%H')

    # 최근 24시간 데이터 필터링
    current_time = pd.Timestamp.now()
    past_24_hours = current_time - pd.DateOffset(hours=24)
    station_814_data_24h = station_814_data[station_814_data['stationDt'] >= past_24_hours]

    # 필요한 데이터 형태로 가공
    chart_data = {
        'labels': station_814_data_24h['stationDt'].dt.strftime('%Y-%m-%d %H:%M:%S').tolist(),
        'data': station_814_data_24h['parkingBikeTotCnt'].tolist()
    }

    return HttpResponse(json.dumps(chart_data), content_type='application/json')