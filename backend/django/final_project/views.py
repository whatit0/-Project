from django.shortcuts import render
import xgboost as xgb
import pandas as pd
import numpy as np
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt  # 추가
from django.views.decorators.http import require_GET # 추가

from datetime import datetime

# Create your views here.
def index(request):
    return render(request, "hi.html")

def load_model(model_path):
    # 모델 불러오기
    loaded_model = xgb.XGBRegressor()
    loaded_model.load_model(model_path)
    return loaded_model

def prepare_new_data(station_id, selected_date, selected_time):
    
    data_2020 = pd.read_csv('data_analysis/data/datafile/real_final_2020.csv')
    data_2021 = pd.read_csv('data_analysis/data/datafile/real_final_2021.csv')
    data_2022 = pd.read_csv('data_analysis/data/datafile/real_final_2022.csv')
    data = pd.concat([data_2020, data_2021, data_2022])
    
    # 평균기온 불러오기
    filtered_data = data[(data['날짜'] == selected_time) &(data['시간'] == selected_time) & (data['대여소ID'] == station_id)]
    average_temperature = filtered_data['평균기온(°C)'].mean()
    
    # 평균 Pm10 불러오기
    average_Pm10 = filtered_data['Pm10'].mean()
    
    # 평균 유동인구 불러오짜
    average_people = filtered_data['유동인구(명)'].mean()
    
    # 400m_지하철 가져오기 
    matched_rows = data[data['400m_대여소'] == data['대여소ID']]
    subway = matched_rows['400m_지하철']
    
    # ID 정제
    stationID = station_id.replace('ST-', '')
    stationID = pd.Series([station_id]).astype('category')
    
    # 날짜 정제 
    date_obj = datetime.strptime(selected_date, "%Y-%m-%d")
    year = date_obj.year
    month = date_obj.month
    day = date_obj.day
    weekday = date_obj.weekday()
    
    # 휴일, 계절
    holiday = weekday.isin([5, 6]).astype(int)
    season = month.map({1: 4, 2: 4, 3: 1, 4: 1, 5: 1, 6: 2, 7: 2, 8: 2, 9: 3, 10: 3, 11: 3, 12: 4})
    data['휴일'] = data['휴일'].astype('category')
    data['계절'] = data['계절'].astype('category')

    
    # 데이터 프레임 형태로 변환
    new_data = [stationID, selected_time, 0, average_temperature, average_Pm10, average_people, weekday,
                subway, year, month, day, holiday, season]
    columns = ['대여소ID', '시간대', '날씨', '평균기온(°C)', 'Pm10', '유동인구(명)', '요일', 
                '400m_지하철', '년', '월', '일', '휴일', '계절']
    new_df = pd.DataFrame([new_data], columns=columns)


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
        print(selected_date, selected_time, station_id)

        # 모델 경로
        rent_model_path = 'data_analysis/made_model/model_xgboost_rent.json'
        return_model_path = 'data_analysis/made_model/model_xgboost_return.json'
        
        # 모델 불러오기
        rent_model = load_model(rent_model_path)
        return_model = load_model(return_model_path)

        # 데이터 준비
        prepared_data = prepare_new_data(station_id, selected_date, selected_time)
        prepared_data['날씨'] = prepared_data['날씨'].astype('category')
        # 비올때 데이터 준비
        rain_prepared_data = prepared_data.copy()
        rain_prepared_data['날씨'] = 1
        rain_prepared_data['날씨'] = rain_prepared_data['날씨'].astype('category')
        
        # 예측 수행
        rent_predictions = predict_new_data(rent_model, prepared_data)
        return_predictions = predict_new_data(return_model, prepared_data)
        rain_rent_predictions = predict_new_data(rent_model, rain_prepared_data)
        rain_return_predictions = predict_new_data(return_model, rain_prepared_data)

        # NumPy 배열을 Python 리스트로 변환
        rent_predictions_list = rent_predictions.tolist() # toJson
        return_predictions_list = return_predictions.tolist()
        rain_rent_predictions_list = rain_rent_predictions.tolist() # toJson
        rain_return_predictions_list = rain_return_predictions.tolist()

        # JSON 응답 생성
        response_data = {
            'rent_predictions': rent_predictions_list,
            'return_predictions': return_predictions_list,
            'rain_rent_predictions': rain_rent_predictions_list,
            'rain_return_predictions': rain_return_predictions_list,
        }

        # 예측 결과를 클라이언트에게 전송 
        return JsonResponse(response_data)
    except Exception as e:
        # 오류 처리
        return JsonResponse({'error': str(e)}, status=500)