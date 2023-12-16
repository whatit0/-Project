import pandas as pd

df = pd.read_csv('backend\django\data_analysis\data\datafile\df_final_final2020_.csv')
df['날짜'] = pd.to_datetime(df['날짜'])

# 대여소ID와 날짜, 시간대 별로 데이터 생성
date_range = pd.date_range(start='2020-01-01', end='2020-01-02', freq='H')
id_list = df['대여소ID'].unique()

# 모든 대여소ID, 날짜, 시간대의 가능한 조합 생성
date_id_combinations = pd.MultiIndex.from_product([date_range, id_list, range(24)], names=['날짜', '대여소ID', '시간대'])

# 빈 데이터프레임 생성
result_df = pd.DataFrame(index=date_id_combinations).reset_index()

# 결과 출력
print(result_df.head(50))

# df와 result_df를 머지
merged_df = pd.merge(result_df, df, on=['대여소ID', '날짜', '시간대'], how='outer')

# 결과 출력
print(merged_df.head())



