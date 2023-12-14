import pandas as pd
from glob import glob

# CSV 파일 불러오기
file_pattern = '5분데이터21년/tpss_bcycl_od_statnhm_2021*.csv'
file_list = glob(file_pattern)

for file in file_list:
    # 파일 읽기
    df = pd.read_csv(file, encoding='ANSI')

    # 파일 저장 (UTF-8 인코딩)
    df.to_csv(file, index=False, encoding='utf-8')