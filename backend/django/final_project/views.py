from django.shortcuts import render
import xgboost as xgb
import pandas as pd
import numpy as np

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

# 장고 뷰 또는 함수에서 사용
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

    # 컨텍스트 생성
    context = {
        'rent_predictions': rent_predictions,
        'return_predictions': return_predictions,
    }

    # 결과와 함께 ex.html로 렌더링
    return render(request, "ex.html", context)
