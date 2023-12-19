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
    # '대여소ID', '시간대', '날씨', '평균기온(°C)', 'Pm10', '유동인구(명)', '요일', '년', '월', '일', '400m_지하철'
    # ID 정제
    station_id = station_id.replace('ST-', '')
    station_id = pd.Series([station_id]).astype('category')
    
    # 날짜 정제 
    date_obj = datetime.strptime(selected_date, "%Y-%m-%d")
    year = date_obj.year
    month = date_obj.month
    day = date_obj.day
    
    

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