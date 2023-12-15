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
    # 새 데이터 정제 및 변환 (필요한 경우)
    # 예: '대여소ID'와 '유동인구(명)' 컬럼 처리
    new_data['유동인구(명)'] = new_data['유동인구(명)'].astype(int)
    new_data['대여소ID'] = new_data['대여소ID'].str[3:].astype(int)
    return new_data

def predict_new_data(model, new_data):
    # 새 데이터 예측
    predictions = model.predict(new_data)
    return predictions

# 장고 뷰 또는 함수에서 사용
def django_view_or_function(request):
    import codecs

    # 모델 파일의 인코딩 변환 (예: CP1252 -> UTF-8)
    with codecs.open('backend/django/data_analysis/made_model/model_xgboost_rent.json', 'r', encoding='cp1252') as file:
        model_data = file.read()
    with codecs.open('backend/django/data_analysis/made_model/model_xgboost_rent.json', 'w', encoding='utf-8') as file:
        file.write(model_data)

    with codecs.open('backend/django/data_analysis/made_model/model_xgboost_return.json', 'r', encoding='cp1252') as file:
        model_data = file.read()
    with codecs.open('backend/django/data_analysis/made_model/model_xgboost_return.json', 'w', encoding='utf-8') as file:
        file.write(model_data)

    # 모델 경로
    rent_model_path = 'backend/django/data_analysis/made_model/model_xgboost_rent.json'
    return_model_path = 'backend/django/data_analysis/made_model/model_xgboost_return.json'

    # 모델 불러오기
    rent_model = load_model(rent_model_path)
    return_model = load_model(return_model_path)

    # 한 행의 새로운 데이터만 생성
    data = pd.read_csv('backend/django/data_analysis/data/datafile/real_final2022.csv', encoding='utf-8')
    new_single_row_data = data.iloc[0:1].copy()  # 기존 데이터의 첫 번째 행을 복사
    new_single_row_data['시간대'] = np.random.choice(range(0, 24))
    new_single_row_data['평균기온(°C)'] = np.random.uniform(-10, 30)
    new_single_row_data['Pm2.5'] = np.random.uniform(5, 50)
    new_single_row_data['유동인구(명)'] = int(np.random.uniform(10000, 50000))  # 정수로 변환

    # 새로 생성된 한 행의 데이터 확인
    new_single_row_data

    # 새 데이터 
    new_data = new_single_row_data

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
