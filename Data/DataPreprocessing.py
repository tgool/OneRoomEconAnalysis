import Crawling as dp
import pandas as pd
import PreprocessingFunc as pf

one_room = pd.read_csv("./Data/one_room_join.csv")
dormitory_df2 = pd.read_csv("./Data/dormitory2.csv", encoding="CP949")
df = pd.DataFrame()
df = pf.crawling_some(df, "성북구 정릉동")
# 월세 데이터 중 투룸, 쓰리룸 제거
df = df[~df["룸_형태"].isin(["투룸", "쓰리룸"])]
print(df)
# 대학 단위 -> 동 단위 그룹화
grouped_df = pf.dormitory_to_dong(dormitory_df2)
# 기숙사 & 원룸 join
merged_df = pd.merge(df, grouped_df, on="주소")
merged_df = pd.concat([one_room, merged_df])
# merged_df.to_csv("./Data/one_room_join.csv", index=False)


def temp():
    dormitory_df = pd.read_csv("./Data/dormitory.csv", encoding="CP949")
    df = pd.DataFrame()
    # 동 list 생성
    list_dormitory = pf.make_crawling_list(dormitory_df)
    # print(list_dormitory)

    # df_temp = dp.get_oneroom_info("서대문구 창천동")  # 동이름 넣으면 정보 반환하도록 ex. 광진구 화양동
    # df = pd.concat([df, df_temp])
    # print(df)
    # df.to_csv("./Data/one_room.csv", index=False)

    # 동 단위 크롤링 & merge
    # df = pf.crawling_all(df, list_dormitory)
