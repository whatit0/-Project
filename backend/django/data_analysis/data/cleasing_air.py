# 대기 오염 데이터
# 일반적으로 PM2.5가 많은 관심을 받고 있는 대기오염 요인 중 하나입니다.
# PM2.5는 지름이 2.5 마이크로미터 이하인 미세먼지 입자로, 대기 중에 떠다니는 작은 입자로 인해 호흡기에 침투하여 건강에 악영향을 미칠 수 있습니다. 
# 이러한 미세먼지는 건강에 해로울 뿐만 아니라 대기오염으로 인해 시야가 흐리게 만들 수도 있고, 황사와 같은 특정한 기상 현상에도 연관되어 있습니다.
# 따라서, PM2.5는 다른 대기오염 요소들과 마찬가지로 대기질을 평가하고 건강에 미치는 영향을 이해하는 데 중요한 요소 중 하나입니다. 
# => 측정항목은 PM2.5 (9)을 사용
# ---------------train ---------------------------------------------------------------------------
import pandas as pd
import glob

# 파일 목록 가져오기
file_list = glob.glob("../data/train_air/AIR_HOUR_*")

# 빈 데이터프레임 생성
train_air = pd.DataFrame()

# 각 파일에 대해 반복 처리
for file in file_list:
    # CSV 파일 읽기
    data = pd.read_csv(file)
    
    # 측정소 코드가 123인 행 필터링하여 추출
    station_123 = data[data['측정소 코드'] == 123].copy()  # 복사본 생성
    
    # 필요한 열만 선택
    selected_columns = station_123[['측정일시', '측정소 코드', '측정항목', '평균값']]
    
    # 측정항목이 9인 행 추출
    measurement_9 = selected_columns[selected_columns['측정항목'] == 9].copy()  # 복사본 생성
    
    # 데이터 타입 확인과 결측값 처리
    measurement_9['측정일시'] = measurement_9['측정일시'].astype(str)  # 문자열로 변환
    
    # '측정일시' 열에서 날짜와 시간 분리하여 새로운 열로 추가
    measurement_9['측정일'] = measurement_9['측정일시'].apply(lambda x: x[:8] if len(x) >= 8 else None)  # 날짜
    
    # '측정시간' 열의 '00'에서 '09'를 '0'에서 '9'로 변경하고, 공백을 0으로 대체
    measurement_9['측정시간'] = measurement_9['측정일시'].apply(lambda x: x[8:].lstrip('0') if len(x) >= 8 else '0' if x == '' else x)  # 시간

    # train_air에 추출된 데이터 추가
    train_air = pd.concat([train_air, measurement_9])

print(train_air, train_air.shape)

print(train_air.isnull().sum())

try:
    train_air.to_csv('train_air_processed.csv', index=False)
    print("파일이 성공적으로 저장되었습니다.")
except Exception as e:
    print("파일 저장 중 에러 발생:", e)

# ------------test ------------------------------------------------------------------------------
# 파일 목록 가져오기
file_list = glob.glob("../data/test_air/AIR_HOUR_*")

# 빈 데이터프레임 생성
test_air = pd.DataFrame()

# 각 파일에 대해 반복 처리
for file in file_list:
    # CSV 파일 읽기
    data = pd.read_csv(file)
    
    # 측정소 코드가 123인 행 필터링하여 추출
    station_123 = data[data['측정소 코드'] == 123].copy()  # 복사본 생성
    
    # 필요한 열만 선택
    selected_columns = station_123[['측정일시', '측정소 코드', '측정항목', '평균값']]
    
    # 측정항목이 9인 행 추출
    measurement_9 = selected_columns[selected_columns['측정항목'] == 9].copy()  # 복사본 생성
    
    # 데이터 타입 확인과 결측값 처리
    measurement_9['측정일시'] = measurement_9['측정일시'].astype(str)  # 문자열로 변환
    
    # '측정일시' 열에서 날짜와 시간 분리하여 새로운 열로 추가
    measurement_9['측정일'] = measurement_9['측정일시'].apply(lambda x: x[:8] if len(x) >= 8 else None)  # 날짜
    
    # '측정시간' 열의 '00'에서 '09'를 '0'에서 '9'로 변경하고, 공백을 0으로 대체
    measurement_9['측정시간'] = measurement_9['측정일시'].apply(lambda x: x[8:].lstrip('0') if len(x) >= 8 else '0' if x == '' else x)  # 시간

    # train_air에 추출된 데이터 추가
    test_air = pd.concat([test_air, measurement_9])

print(test_air, test_air.shape)

print(test_air.isnull().sum())

try:
    test_air.to_csv('test_air_processed.csv', index=False)
    print("파일이 성공적으로 저장되었습니다.")
except Exception as e:
    print("파일 저장 중 에러 발생:", e)