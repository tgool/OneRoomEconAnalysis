import Crawling as dp
import pandas as pd
import PreprocessingFunc as pf

dormitory_df = pd.read_csv("./Data/dormitory.csv", encoding="CP949")
dormitory_df2 = pd.read_csv("./Data/dormitory2.csv", encoding="CP949")
df = pd.DataFrame()
# 동 list 생성
list_dormitory = pf.make_crawling_list(dormitory_df)
# one_room = pd.read_csv("./Data/one_room_join.csv")

# 동 단위 크롤링 & merge
df = pf.crawling_all(df, list_dormitory)
# 월세 데이터 중 투룸, 쓰리룸 제거
df = df[~df["룸_형태"].isin(["투룸", "쓰리룸"])]
# 대학 단위 -> 동 단위 그룹화
grouped_df = pf.dormitory_to_dong(dormitory_df2)
# 기숙사 & 원룸 join
merged_df = pd.merge(df, grouped_df, on="주소")
# merged_df = pd.concat([one_room, merged_df])
merged_df.to_csv("./Data/one_room_join_gpt.csv", index=False)
# one_room.to_excel("./Data/one_room_join.xlsx", index=False)
df = pd.read_csv("./Data/one_room_join_gpt.csv", encoding="CP949")
# df = pf.gpt_edit_date_list(gpt_df)
df = pf.distance_min(df)
df.to_excel("./Data/one_room_join_distance_min.xlsx", index=False)
df.to_csv("./Data/one_room_join_distance_min.csv", index=False)
