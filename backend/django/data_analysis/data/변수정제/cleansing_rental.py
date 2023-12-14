import pandas as pd
import os

df1 = pd.read_csv('공공자전거_대여소_정보(22.12월 기준).csv', usecols=['보관소(대여소)명', '자치구', '위도', '경도'])
df1 = df1.loc[:, ~df1.columns.str.startswith('Unnamed')]

df1 = df1.rename(columns={'보관소(대여소)명': '대여소'})
# '자치구'별로 데이터프레임 분리
rent_by_district = {}
for district, group in df1.groupby('자치구'):
    rent_by_district[district] = group[['대여소', '자치구', '위도', '경도']]

# 결과 확인
for district, df_district in rent_by_district.items():
    print(f"\n자치구: {district}")
    print(df_district.head())

# 각 자치구별로 CSV 파일로 저장
for district, df_district in rent_by_district.items():
    csv_filename = os.path.join('자치구별 대여소 정보', f'{district} 대여소 정보.csv')
    df_district.to_csv(csv_filename, index=False)
    print(f"{csv_filename} 파일이 저장되었습니다.")


rent_gangnam = pd.read_csv('자치구별 대여소 정보/강남구 대여소 정보.csv')
print(rent_by_gangnam.head(5))
print(len(df), '\n', df.isnull().sum())  # 총 169개의 대여소가 있고 결측치는 없음

''' 1년치 이용내역 불러와서 강남구 대여소 정보와 일치하는 것만 저장 ---------------------'''
from glob import glob

# 파일 경로의 패턴을 사용하여 파일들을 찾음
file_pattern = '따릉이 대여이력 정보/공공자전거 대여이력 정보_20*.csv'
file_list = glob(file_pattern)

# 모든 파일을 담을 빈 DataFrame 생성
all_data = pd.DataFrame()

rows_with_errors = 0
# 파일을 순회하면서 DataFrame에 추가
for file in file_list:
    # 파일 읽기
    data = pd.read_csv(file)

    # '대여소'와 '대여 대여소명'이 일치하는 행만 선택
    mg_rent_gangnam = pd.merge(rent_gangnam, data, left_on='대여소', right_on='대여 대여소명', how='inner')

    # 필요한 열만 선택
    gangnam_rent_2020 = mg_rent_gangnam[['대여일시', '대여 대여소명', '반납일시', '반납대여소명', '이용시간', '이용거리']]

    # '대여일시'를 날짜 및 시간 형식으로 변환
    # gangnam_rent_2021['대여일시'] = pd.to_datetime(gangnam_rent_2021['대여일시'])
    gangnam_rent_2020['대여일시'] = pd.to_datetime(gangnam_rent_2020['대여일시'], errors='coerce', format='%Y-%m-%d %H:%M:%S')

    # 오류가 발생한 행 삭제 및 삭제된 행 수 카운트
    before_rows = len(gangnam_rent_2020)
    gangnam_rent_2020 = gangnam_rent_2020.dropna(subset=['대여일시'])
    rows_with_errors += before_rows - len(gangnam_rent_2020)

    # '날짜' 및 '시간대' 열 추가
    gangnam_rent_2020['날짜'] = gangnam_rent_2020['대여일시'].dt.date
    gangnam_rent_2020['시간대'] = gangnam_rent_2020['대여일시'].dt.hour

    # 모든 데이터를 담을 DataFrame에 추가
    all_data = pd.concat([all_data, gangnam_rent_2020])

# '대여일시' 열 삭제
all_data = all_data.drop('대여일시', axis=1)
print(f"삭제된 행 수: {rows_with_errors}")

# 결과 출력
print(all_data.head(5), '\n 길이 : ', len(all_data))
# print(all_data[all_data['대여 대여소명'] == '국립국악중,고교 정문 맞은편'])

unique_count = all_data['대여 대여소명'].nunique()
print(f"'대여 대여소명' 열의 고유값 개수: {unique_count}")




# 파일저장
all_data.to_csv('강남대여소2020.csv', index=False)

all_data = pd.read_csv('강남대여소2020.csv')
print(all_data.isnull().sum(), len(all_data))
# all_data = all_data.dropna()


# 각 일별로 시간대별 데이터 나누기 및 출력
for date, data_by_date in daily_data:
    print(f"\n=== {date}의 시간대별 대여 건수 ===")
    hourly_data = data_by_date.groupby(data_by_date['대여일시'].dt.hour).size()
    print(hourly_data)





# '강남대여소2020.csv' 파일 읽기
df2020 = pd.read_csv('강남대여소2020.csv')

# '강남대여소2021.csv' 파일 읽기
df2021 = pd.read_csv('강남대여소2021.csv')

# 두 데이터프레임을 연결
# merged_df = pd.concat([df2020, df2021])

# 연결된 데이터프레임을 새로운 CSV 파일로 저장
# merged_df.to_csv('강남대여소2020~21.csv', index=False)

df = pd.read_csv('강남대여소2020~21.csv')
# print(len(df), df.isnull().sum())
unique_count = df['대여 대여소명'].nunique()
print(f"'대여 대여소명' 열의 고유값 개수: {unique_count}")
print(len(df2020), len(df2021))




''' 대여소 이름 앞 뒤 공백 제거, 쌍따옴표 제거 -------------------------------'''
import os
import pandas as pd

# 자치구별 대여소 정보가 저장된 폴더 경로
folder_path = '자치구별 대여소 정보'

# 폴더 내의 모든 CSV 파일 불러오기
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        # CSV 파일 읽기
        file_path = os.path.join(folder_path, filename)
        df = pd.read_csv(file_path)

        # '대여소' 열의 맨 앞과 끝의 공백 및 특수문자 제거
        df['대여소'] = df['대여소'].str.replace('"', '')


        # 처리된 데이터를 새로운 CSV 파일로 저장
        processed_file_path = os.path.join(folder_path, f'{filename}')
        df.to_csv(processed_file_path, index=False)

        print(f"{processed_file_path} 파일이 저장되었습니다.")
