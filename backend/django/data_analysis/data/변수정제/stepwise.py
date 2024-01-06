import pandas as pd
import statsmodels.api as sm
import seaborn as sns
import matplotlib.pyplot as plt
plt.rc('font', family='malgun gothic')


# 데이터 로딩
pd.options.display.max_columns = None
df1 = pd.read_csv('backend\django\data_analysis\data\datafile/real_final_2020.csv')
df2 = pd.read_csv('backend\django\data_analysis\data\datafile/real_final_2021.csv')
df3 = pd.read_csv('backend\django\data_analysis\data\datafile/real_final_2022.csv')

df = pd.concat([df1, df2, df3], axis=0)

# 독립 변수 선택 (모든 변수를 사용하거나 특정 변수를 선택)
# independent_vars = ['시간대', '날씨', '평균기온(°C)', 'Pm2.5', '유동인구(명)', '년', '월', '요일', '일']
independent_vars = ['시간대', '날씨', '평균기온(°C)', '유동인구(명)', '년', '월', '요일']

# 종속 변수
dependent_vars = ['대여건수', '반납건수']

# 선택된 변수를 담을 리스트 초기화
selected_vars_dict = {}


# forward 방식의 단계적 선택법
for dependent_var in dependent_vars:
    selected_vars = []
    remaining_vars = set(independent_vars)

    while remaining_vars:
        # 선택되지 않은 변수들 중에서 가장 설명력 있는 변수 선택
        model = sm.OLS(df[dependent_var], sm.add_constant(df[selected_vars + list(remaining_vars)])).fit()
        pvalues = model.pvalues.iloc[1:]
        best_var = pvalues.idxmin()

        # 유의수준 0.05를 만족하면 선택된 변수에 추가 (중복 방지)
        if (pvalues[best_var] < 0.05).any() and best_var not in selected_vars:
            selected_vars.append(best_var)
        else:
            break

    selected_vars_dict[dependent_var] = selected_vars

# 선택된 변수 출력
for dependent_var, selected_vars in selected_vars_dict.items():
    print(f"Selected Variables for '{dependent_var}':", selected_vars)

    # 선택된 변수를 이용하여 다시 회귀 모델 적합
    final_model = sm.OLS(df[dependent_var], sm.add_constant(df[selected_vars])).fit()

    # 회귀 모델 결과 출력
    print(final_model.summary())



# 후진 제거법을 위한 함수 정의
def backward_elimination(df, dependent_var, independent_vars):
    while True:
        model = sm.OLS(df[dependent_var], sm.add_constant(df[independent_vars])).fit()
        max_pvalue = model.pvalues.drop('const').max()  # 가장 큰 p-value
        if max_pvalue > 0.05:
            remove_var = model.pvalues.drop('const').idxmax()  # 가장 큰 p-value를 가진 변수 제거
            independent_vars.remove(remove_var)
        else:
            break
    return model, independent_vars

# 후진 제거법 적용
selected_vars_backward = {}
for dependent_var in dependent_vars:
    _, selected_vars_backward[dependent_var] = backward_elimination(df, dependent_var, independent_vars)

# 선택된 변수 출력
print("Selected Variables (Backward Elimination):", selected_vars_backward)

# 선택된 변수를 이용하여 다시 회귀 모델 적합
final_model_backward = {}
for dependent_var in dependent_vars:
    final_model_backward[dependent_var] = sm.OLS(df[dependent_var], sm.add_constant(df[selected_vars_backward[dependent_var]])).fit()

# 회귀 모델 결과 출력
for dependent_var in dependent_vars:
    print(f"\nResults for '{dependent_var}':")
    print(final_model_backward[dependent_var].summary())



'''히트맵'''
'''
# 대여소ID 열 제외
df = df.drop(columns=['대여소ID'])

# 상관 행렬 계산
correlation_matrix = df.corr()

# 히트맵 그리기
plt.figure(figsize=(12, 10))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
plt.title('Correlation Heatmap')
plt.show()
'''