# 날씨 데이터
# train(2020) -----------------------------------------------------------------------------
import pandas as pd

# 데이터 불러오기
train_weather1 = pd.read_csv("../data/train_weather/weather_2020.csv")

# '일강수량(mm)' 열의 NaN 값을 '비안옴'으로, 값이 있는 경우 '비옴'으로 변경
train_weather1['일강수량(mm)'] = train_weather1['일강수량(mm)'].fillna('비안옴')
train_weather1.loc[train_weather1['일강수량(mm)'] != '비안옴', '일강수량(mm)'] = '비옴'

print(train_weather1, train_weather1.shape)

try:
    train_weather1.to_csv('2020_weather_processed.csv', index=False)
    print("파일이 성공적으로 저장되었습니다.")
except Exception as e:
    print("파일 저장 중 에러 발생:", e)

# train(2021) -----------------------------------------------------------------------------

# 데이터 불러오기
train_weather2 = pd.read_csv("../data/train_weather/weather_2021.csv")

# '일강수량(mm)' 열의 NaN 값을 '비안옴'으로, 값이 있는 경우 '비옴'으로 변경
train_weather2['일강수량(mm)'] = train_weather2['일강수량(mm)'].fillna('비안옴')
train_weather2.loc[train_weather2['일강수량(mm)'] != '비안옴', '일강수량(mm)'] = '비옴'

print(train_weather2, train_weather2.shape)

try:
    train_weather2.to_csv('2021_weather_processed.csv', index=False)
    print("파일이 성공적으로 저장되었습니다.")
except Exception as e:
    print("파일 저장 중 에러 발생:", e)


# test(2022) -----------------------------------------------------------------------------

# 데이터 불러오기
test_weather = pd.read_csv("../data/test_weather/weather_2022.csv")

# '일강수량(mm)' 열의 NaN 값을 '비안옴'으로, 값이 있는 경우 '비옴'으로 변경
test_weather['일강수량(mm)'] = test_weather['일강수량(mm)'].fillna('비안옴')
test_weather.loc[test_weather['일강수량(mm)'] != '비안옴', '일강수량(mm)'] = '비옴'

print(test_weather, test_weather.shape)

try:
    test_weather.to_csv('2022_weather_processed.csv', index=False)
    print("파일이 성공적으로 저장되었습니다.")
except Exception as e:
    print("파일 저장 중 에러 발생:", e)
