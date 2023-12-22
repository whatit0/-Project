from django.shortcuts import render
import xgboost as xgb
import pandas as pd
import numpy as np
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt  # 추가
from django.views.decorators.http import require_GET # 추가
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
from datetime import datetime, timedelta

data_2020 = pd.read_csv('data_analysis/data/datafile/real_final_2020.csv')
data_2021 = pd.read_csv('data_analysis/data/datafile/real_final_2021.csv')
data_2022 = pd.read_csv('data_analysis/data/datafile/real_final_2022.csv')
data = pd.concat([data_2020, data_2021, data_2022])

# Create your views here.
loaded_models = {}  # 전역 변수로 모델 저장

def load_model(model_path):
    # 모델 경로를 기반으로 이미 로드된 모델이 있는지 확인
    if model_path in loaded_models:
        return loaded_models[model_path]

    # 모델 불러오기
    loaded_model = xgb.XGBRegressor()
    loaded_model.load_model(model_path)
    loaded_models[model_path] = loaded_model  # 모델 저장
    return loaded_model

def prepare_new_data(station_id, selected_date, selected_time):
    # 데이터 필터링 및 평균 계산
    date_obj = datetime.strptime(selected_date, "%Y-%m-%d")
    year = date_obj.year
    month = date_obj.month
    day = date_obj.day
    weekday = date_obj.weekday()
    hours, _ = map(int, selected_time.split(':'))

    filtered_data = data[(data['날짜'] == selected_date) & (data['시간대'] == hours) & (data['대여소ID'] == station_id)]
    average_temperature = filtered_data['평균기온(°C)'].mean()
    average_Pm10 = filtered_data['Pm10'].mean()
    average_people = filtered_data['유동인구(명)'].mean()

    # 400m_지하철 확인
    subway = 1 if data[data['대여소ID'] == station_id]['400m_지하철'].iloc[0] else 0

    # 휴일 및 계절 계산
    holiday = 1 if weekday >= 5 else 0
    season = {1: 4, 2: 4, 3: 1, 4: 1, 5: 1, 6: 2, 7: 2, 8: 2, 9: 3, 10: 3, 11: 3, 12: 4}[month]

    # 데이터 프레임 생성
    new_df = pd.DataFrame({
        '대여소ID': pd.Series([station_id]).astype('category'),
        '시간대': [hours],
        '날씨': pd.Series([0]).astype('category'),  # 임시 날씨 값
        '평균기온(°C)': [average_temperature],
        'Pm10': [average_Pm10],
        '유동인구(명)': [average_people],
        '요일': pd.Series([weekday]).astype('category'),
        '400m_지하철': pd.Series([subway]).astype('category'),
        '년': [year],
        '월': [month],
        '일': [day],
        '휴일':[holiday],
        '계절':[season],
    })

    return new_df


def predict_new_data(model, new_data):
    # 새 데이터 예측
    predictions = model.predict(new_data)
    return predictions

@csrf_exempt
@require_GET
def handle_predictions(request):
    try:
        data = request.GET
        selected_date = data.get('date')
        selected_time = data.get('time')
        station_id = data.get('stationId')
        parkingBike = data.get('parkingBike')
        print(selected_date, selected_time, station_id, parkingBike)
        
        current_datetime = datetime.now()
        selected_datetime = datetime.strptime(f"{selected_date} {selected_time}", "%Y-%m-%d %H:%M")
        cha = selected_datetime - current_datetime 
        t = cha.total_seconds() / 3600

        # 모델 경로
        rent_model_path = 'data_analysis/made_model/model_xgboost_rent.json'
        return_model_path = 'data_analysis/made_model/model_xgboost_return.json'
        
        # 모델 불러오기
        rent_model = load_model(rent_model_path)
        return_model = load_model(return_model_path)
        
        rent_predictions_total = 0
        return_predictions_total =0
        
        # 선택된 시간이 현재 시간보다 2시간 이상 미래인 경우
        if selected_datetime > current_datetime + timedelta(hours=2):
            su = 1
            for hour in range(int(t)):
                new_datetime = current_datetime + timedelta(hours=su)
                date_str = new_datetime.strftime("%Y-%m-%d")
                time_str = new_datetime.strftime("%H:%M")
                
                prepared_data = prepare_new_data(station_id, date_str, time_str)

                rent_predictions = predict_new_data(rent_model, prepared_data)
                return_predictions = predict_new_data(return_model, prepared_data)

                rent_predictions_total += sum(rent_predictions)
                return_predictions_total += sum(return_predictions)
                
                # 잔여대수 구하기
                leftbike = int(parkingBike) - rent_predictions_total + return_predictions_total
                
                su += 1
        else:
            prepared_data = prepare_new_data(station_id, selected_date, selected_time)
            
            rent_predictions = predict_new_data(rent_model, prepared_data)
            return_predictions = predict_new_data(return_model, prepared_data)
            
            # 잔여대수 구하기
            leftbike = int(parkingBike) - rent_predictions + return_predictions
            
        
        print('잔여:',leftbike)
        print(rent_predictions, return_predictions)
        
        rent_predictions = [round(num) for num in rent_predictions.tolist()]
        return_predictions = [round(num) for num in return_predictions.tolist()]
        
        # 잔여대수 계산 후 음수일 경우 0으로 설정
        leftbike = max(0, int(parkingBike) - rent_predictions_total + return_predictions_total)

        # JSON 응답 생성
        response_data = {
            'rent_predictions': rent_predictions,
            'return_predictions': return_predictions,
            'leftbike':round(leftbike),
        }

        # 예측 결과를 클라이언트에게 전송 
        return JsonResponse(response_data)
    except Exception as e:
        # 오류 처리
        return JsonResponse({'error': str(e)}, status=500)
        
@csrf_exempt
@require_GET
def showchart(request):
    try:
        data = request.GET
        station_id = data.get('stationId')
        print('-----------------------',station_id)

        base_url = "http://openapi.seoul.go.kr:8088/"
        api_key = "6d6f7a7258616e6a3130394342466d79"

        # 현재 시간과 24시간 전의 시간 계산
        current_time = datetime.now()
        start_time = current_time - timedelta(hours=24)

        all_data = []

        for i in range(24):
            target_time = start_time + timedelta(hours=i)
            formatted_time = target_time.strftime("%Y%m%d%H")

            # 첫 번째 범위 조회
            url_first_range = f"{base_url}{api_key}/json/bikeListHist/0/999/{formatted_time}"
            response_first_range = requests.get(url_first_range)
            
            if response_first_range.status_code == 200:
                data_first_range = response_first_range.json()
                if 'getStationListHist' in data_first_range and 'row' in data_first_range['getStationListHist']:
                    all_data.extend(data_first_range['getStationListHist']['row'])
            else:
                print(f"Error {response_first_range.status_code}: {response_first_range.text}")

            # 두 번째 범위 조회
            url_second_range = f"{base_url}{api_key}/json/bikeListHist/2500/3035/{formatted_time}"
            response_second_range = requests.get(url_second_range)
            
            if response_second_range.status_code == 200:
                data_second_range = response_second_range.json()
                if 'getStationListHist' in data_second_range and 'row' in data_second_range['getStationListHist']:
                    all_data.extend(data_second_range['getStationListHist']['row'])
            else:
                print(f"Error {response_second_range.status_code}: {response_second_range.text}")

        # 모든 데이터가 담긴 리스트 출력
        print(f"총 {len(all_data)}개의 데이터가 수집되었습니다.")
        print('-----------------------','안녕하세요')

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
                'parkingBikeTotCnt': data['parkingBikeTotCnt'],
                'stationId': data['stationId'],
                'stationDt': data['stationDt']
            }
            for data in all_data
            if data.get('stationId') in included_ids
        ]
        print('-----------------------',station_id)

        # 결과 확인
        print(f"다시 총 {len(filtered_data)}개의 데이터가 추출되었습니다.")
        df=pd.DataFrame(filtered_data)

        # 'ST-814' 대여소의 데이터 추출
        station_814_data = df[df['stationId'] == 'ST-814']

        # stationDt 열을 datetime 형식으로 변환
        station_814_data['stationDt'] = pd.to_datetime(station_814_data['stationDt'], format='%Y%m%d%H')

        # 최근 24시간 데이터 필터링
        current_time = pd.Timestamp.now()
        past_24_hours = current_time - pd.DateOffset(hours=24)
        station_814_data_24h = station_814_data[station_814_data['stationDt'] >= past_24_hours]

        # 필요한 데이터 형태로 가공
        chart_data = {
            'labels': station_814_data_24h['stationDt'].dt.strftime('%H').tolist(),
            'data': station_814_data_24h['parkingBikeTotCnt'].tolist()
        } 
        print(chart_data['labels'],chart_data['data'])

        return JsonResponse(chart_data)
    except Exception as e:
        # 오류 처리
        return JsonResponse({'error': str(e)}, status=500)