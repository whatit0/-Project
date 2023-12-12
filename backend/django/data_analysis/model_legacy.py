# 독립변수와 종속변수로 나누기
columns_to_keep = [col for col in train_data.columns if col not in ['대여건수', '반납건수']]
train_x = train_data[columns_to_keep]
train_y1 = train_data['대여건수']
train_y2 = train_data['반납건수']