# 날씨 데이터
# ------ train -----------------------------------------------------------------------------
import pandas as pd
import glob

# 파일 목록 가져오기
file_list = glob.glob("../data/train_weather/weather_*.csv")

# 빈 데이터프레임 생성
train_weather = pd.DataFrame()

# 각 파일에 대해 반복 처리
for file in file_list:
    # CSV 파일 읽기
    people_data = pd.read_csv(file)
    
    # 결과를 all_data에 추가
    train_weather = pd.concat([train_weather, people_data])

# '일강수량(mm)' 열의 NaN 값을 '비안옴'으로, 값이 있는 경우 '비옴'으로 변경
train_weather['일강수량(mm)'] = train_weather['일강수량(mm)'].fillna('비안옴')
train_weather.loc[train_weather['일강수량(mm)'] != '비안옴', '일강수량(mm)'] = '비옴'

print(train_weather, train_weather.shape)

try:
    train_weather.to_csv('train_weather_processed.csv', index=False)
    print("파일이 성공적으로 저장되었습니다.")
except Exception as e:
    print("파일 저장 중 에러 발생:", e)
    

# ---------- test -----------------------------------------------------------------------------

# 파일 목록 가져오기
file_list = glob.glob("../data/test_weather/weather_*.csv")

# 빈 데이터프레임 생성
test_weather = pd.DataFrame()

# 각 파일에 대해 반복 처리
for file in file_list:
    # CSV 파일 읽기
    people_data = pd.read_csv(file)
    
    # 결과를 all_data에 추가
    test_weather = pd.concat([test_weather, people_data])

# '일강수량(mm)' 열의 NaN 값을 '비안옴'으로, 값이 있는 경우 '비옴'으로 변경
test_weather['일강수량(mm)'] = test_weather['일강수량(mm)'].fillna('비안옴')
test_weather.loc[test_weather['일강수량(mm)'] != '비안옴', '일강수량(mm)'] = '비옴'

print(test_weather, test_weather.shape)

try:
    test_weather.to_csv('test_weather_processed.csv', index=False)
    print("파일이 성공적으로 저장되었습니다.")
except Exception as e:
    print("파일 저장 중 에러 발생:", e)