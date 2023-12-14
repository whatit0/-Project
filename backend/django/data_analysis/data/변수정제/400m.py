import geopandas as gpd
import pandas as pd

df_bike = pd.read_csv('backend\django\data_analysis\data\datafile\강남구 대여소 정보.csv')
df_station = pd.read_csv('backend\django\data_analysis\data\datafile\서울시 역사마스터 정보.csv')

# 역사명이 리스트에 포함되어 있는지 확인하는 코드 수정
stations = ['학동', '도곡', '일원', '선릉', '대치', '언주', '학여울', '봉은사', '청담', '수서', '압구정로데오', '대모산입구', '언주', '삼성중앙', '개포동', '매봉', '대청', '선정릉', '구룡', '한티', '구룡', '강남', '신논현', '삼성', '신사', '역삼', '압구정', '논현', '강남구청', '선정릉', '삼성', '양재']

df_station = df_station[df_station['역사명'].isin(stations)]

geom_bike = gpd.points_from_xy(df_bike['경도'], df_bike['위도'])
gdf_bike4326 = gpd.GeoDataFrame(df_bike, geometry=geom_bike, crs=4326)
gdf_bike3857 = gdf_bike4326.to_crs(epsg=3857)
# print(gdf_bike3857.head())

geom_station = gpd.points_from_xy(df_station['경도'], df_station['위도'])
gdf_station4326 = gpd.GeoDataFrame(df_station, geometry=geom_station, crs=4326)
gdf_station3857 = gdf_station4326.to_crs(epsg=3857)
# print(gdf_station3857.head())

gdf02 = gpd.sjoin_nearest(gdf_bike3857, gdf_station3857, max_distance=400)
gdf02.to_csv('output_file.csv', index=False)
print(gdf02.head(10))
