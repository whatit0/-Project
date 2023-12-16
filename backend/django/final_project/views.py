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

"""
def django_view_or_function(request):
    # 모델 경로
    rent_model_path = 'data_analysis/made_model/model_xgboost_rent.json'
    return_model_path = 'data_analysis/made_model/model_xgboost_return.json'

    # 모델 불러오기
    rent_model = load_model(rent_model_path)
    return_model = load_model(return_model_path)

    # 새 데이터 
    new_data = ['STS-818', 20, 0, 29.896258, 23.998998, 41021, 5, 2022, 1, 1, 1]

    # 데이터 준비
    prepared_data = prepare_new_data(new_data)

    # 예측 수행
    rent_predictions = predict_new_data(rent_model, prepared_data)
    return_predictions = predict_new_data(return_model, prepared_data)

    # NumPy 배열을 Python 리스트로 변환
    rent_predictions_list = rent_predictions.tolist()
    return_predictions_list = return_predictions.tolist()

    # JSON 응답 생성
    response_data = {
        'rent_predictions': rent_predictions_list,
        'return_predictions': return_predictions_list,
    }

    return JsonResponse(response_data)

"""