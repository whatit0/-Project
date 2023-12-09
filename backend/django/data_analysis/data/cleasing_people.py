# 유동인구 데이터
import pandas as pd
import glob


# -------------------------------train(2020) -----------------------------------------------------------------------------

# 파일 목록 가져오기
file_list = glob.glob("../data/train_people/LOCAL_PEOPLE_DONG_2020*.csv")
print(file_list)

# 빈 데이터프레임 생성
train_people = pd.DataFrame()

# 각 파일에 대해 반복 처리
for file in file_list:
    # CSV 파일 읽기
    people_data = pd.read_csv(file)
    
    # 특정 행정동코드로 시작하는 행만 선택
    people_data = people_data[people_data['행정동코드'].astype(str).str.startswith('1168')]
    
    # 결과를 all_data에 추가
    train_people = pd.concat([train_people, people_data])

print(train_people, train_people.shape)

# 행정동 코드를 행정동 이름으로 변환
dong = pd.read_csv('../data/dong.CSV')
dong = dong.drop(0)
print(dong)

# 행정동 코드를 행정동 이름으로 변환하여 train_people에 추가
train_people['행정동'] = train_people['행정동코드'].astype(str).map(dong.set_index('행자부행정동코드')['행정동명'])

print(train_people)
print(train_people.isnull().sum())

# 거치대 자료 도로명주소를 엑셀 메크로를 사용해서 행정동으로 변환함. 그 파일을 이용해서 거치대이름과 매핑 
df = pd.read_csv('../data/대여소동정보.csv')
# print(df)

# train_people와 df에서 행정동 이름을 기준으로 대여소명을 추가하는 코드
train_people = train_people.merge(df, how='left', left_on='행정동', right_on='행정동 명칭')

# 필요없는 열 삭제
columns_to_drop = ['행정동코드', '행정동', '자치구', '상세주소', '행정동 명칭']
train_people.drop(columns=columns_to_drop, inplace=True)
print(train_people)

# try:
#     train_people.to_csv('2020_people_processed.csv', index=False)
#     print("파일이 성공적으로 저장되었습니다.")
# except Exception as e:
#     print("파일 저장 중 에러 발생:", e)
    
# -------------------------------train(2021) -----------------------------------------------------------------------------

# 파일 목록 가져오기
file_list = glob.glob("../data/train_people/LOCAL_PEOPLE_DONG_2021*.csv")
print(file_list)

# 빈 데이터프레임 생성
train_people = pd.DataFrame()

# 각 파일에 대해 반복 처리
for file in file_list:
    # CSV 파일 읽기
    people_data = pd.read_csv(file)
    
    # 특정 행정동코드로 시작하는 행만 선택
    people_data = people_data[people_data['행정동코드'].astype(str).str.startswith('1168')]
    
    # 결과를 all_data에 추가
    train_people = pd.concat([train_people, people_data])

print(train_people, train_people.shape)

# 행정동 코드를 행정동 이름으로 변환
dong = pd.read_csv('../data/dong.CSV')
dong = dong.drop(0)
print(dong)

# 행정동 코드를 행정동 이름으로 변환하여 train_people에 추가
train_people['행정동'] = train_people['행정동코드'].astype(str).map(dong.set_index('행자부행정동코드')['행정동명'])

print(train_people)
print(train_people.isnull().sum())

# 거치대 자료 도로명주소를 엑셀 메크로를 사용해서 행정동으로 변환함. 그 파일을 이용해서 거치대이름과 매핑 
df = pd.read_csv('../data/대여소동정보.csv')
# print(df)

# train_people와 df에서 행정동 이름을 기준으로 대여소명을 추가하는 코드
train_people = train_people.merge(df, how='left', left_on='행정동', right_on='행정동 명칭')

# 필요없는 열 삭제
columns_to_drop = ['행정동코드', '행정동', '자치구', '상세주소', '행정동 명칭']
train_people.drop(columns=columns_to_drop, inplace=True)
print(train_people)

# try:
#     train_people.to_csv('2021_people_processed.csv', index=False)
#     print("파일이 성공적으로 저장되었습니다.")
# except Exception as e:
#     print("파일 저장 중 에러 발생:", e)


# -------------------------------test(2022) -----------------------------------------------------------------------------
# 파일 목록 가져오기
file_list2 = glob.glob("../data/test_people/LOCAL_PEOPLE_DONG_2022*.csv")
print(file_list2)

# 빈 데이터프레임 생성
test_people = pd.DataFrame()

# 각 파일에 대해 반복 처리
for file in file_list2:
    # CSV 파일 읽기
    people_data = pd.read_csv(file)
    
    # 특정 행정동코드로 시작하는 행만 선택
    people_data = people_data[people_data['행정동코드'].astype(str).str.startswith('1168')]
    
    # 결과를 all_data에 추가
    test_people = pd.concat([test_people, people_data])
print(test_people, test_people.shape)

# 행정동 코드를 행정동 이름으로 변환
dong = pd.read_csv('../data/dong.CSV')
dong = dong.drop(0)
# print(dong)

# 행정동 코드를 행정동 이름으로 변환하여 train_people에 추가
test_people['행정동'] = test_people['행정동코드'].astype(str).map(dong.set_index('행자부행정동코드')['행정동명'])

print(test_people)
print(test_people.isnull().sum())

# 거치대 자료 도로명주소를 엑셀 메크로를 사용해서 행정동으로 변환함. 그 파일을 이용해서 거치대이름과 매핑 
df = pd.read_csv('../data/대여소동정보.csv')
# print(df)

# test_people와 df에서 행정동 이름을 기준으로 대여소명을 추가하는 코드
test_people = test_people.merge(df, how='left', left_on='행정동', right_on='행정동 명칭')

# 필요없는 열 삭제
columns_to_drop = ['행정동코드', '자치구', '상세주소', '행정동 명칭']
test_people.drop(columns=columns_to_drop, inplace=True)
print(test_people)

try:
    test_people.to_csv('2022_people_processed.csv', index=False)
    print("파일이 성공적으로 저장되었습니다.")
except Exception as e:
    print("파일 저장 중 에러 발생:", e)

