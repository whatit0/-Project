import pandas as pd
from glob import glob

# 데이터 불러오기
pd.options.display.max_columns = None
df1 = pd.read_csv('자치구별 대여소 정보/최종강남대여소.csv')

# 파일 경로의 패턴을 사용하여 파일들을 찾음
file_pattern = '5분데이터21년/tpss_bcycl_od_statnhm_2021*.csv'
file_list = glob(file_pattern)

# 결과를 저장할 빈 리스트
result_dfs = []

for file in file_list:
    # 파일 읽기
    df = pd.read_csv(file)

    # df1에 존재하는 대여대여소ID만 필터링
    valid_ids = df1['대여대여소ID']
    filtered_df = df[df['시작_대여소ID'].isin(valid_ids) | df['종료_대여소ID'].isin(valid_ids)]

    filtered_df['시간대'] = filtered_df['기준_시간'] // 100  # 시간대를 100으로 나눈 몫으로 계산

    # 대여대여소ID에 대한 반복문
    for rental_id in valid_ids:
        # '시작_대여소'가 해당 ID인 경우 대여건수, '종료_대여소'가 해당 ID인 경우 반납건수 추출
        rental_counts = filtered_df[filtered_df['시작_대여소ID'] == rental_id].groupby(['기준_날짜', '시간대'])['전체건수'].sum()
        return_counts = filtered_df[filtered_df['종료_대여소ID'] == rental_id].groupby(['기준_날짜', '시간대'])['전체건수'].sum()

        # 대여건수와 반납건수를 합침
        result_df = pd.DataFrame({'대여건수': rental_counts, '반납건수': return_counts}).reset_index()

        # 시간대 순으로 정렬
        result_df = result_df.sort_values(by=['기준_날짜', '시간대']).reset_index(drop=True)

        # '시간대'를 0~23의 정수로 바꿈
        result_df['시간대'] = result_df['시간대'].astype(int)

        # NaN값을 0으로 대체
        result_df = result_df.fillna(0).astype({'대여건수': int, '반납건수': int})

        # '대여대여소ID'와 '대여 대여소명'을 모두 나타내기
        rental_station_info = df1[df1['대여대여소ID'] == rental_id][['대여대여소ID', '대여 대여소명']].squeeze()
        result_df['대여소ID'] = rental_station_info['대여대여소ID']
        result_df['대여소명'] = rental_station_info['대여 대여소명']

        result_dfs.append(result_df)

        print(f"대여소명: {rental_station_info['대여 대여소명']} (대여소ID: {rental_station_info['대여대여소ID']})")
        print(result_df)
        print("\n")

# 모든 결과를 하나의 DataFrame으로 결합
final_result = pd.concat(result_dfs, ignore_index=True)

# 결과를 CSV 파일로 저장
final_result.to_csv('21년5분데이터.csv', index=False)
