from django.shortcuts import render
import xgboost as xgb
import pandas as pd
import numpy as np
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt  # 추가
from django.views.decorators.http import require_GET # 추가

from datetime import datetime, timedelta

data_2020 = pd.read_csv('data_analysis/data/datafile/real_final_2020.csv')
data_2021 = pd.read_csv('data_analysis/data/datafile/real_final_2021.csv')
data_2022 = pd.read_csv('data_analysis/data/datafile/real_final_2022.csv')
data = pd.concat([data_2020, data_2021, data_2022])

# Create your views here.
def index(request):
    return render(request, "hi.html")

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