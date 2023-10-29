import Crawling as dp
import pandas as pd


def make_crawling_list(dormitory_df):
    # 리스트 생성
    list_dormitory = []

    # '동1', '동2', '동3' 열의 값들을 리스트에 추가
    for row in dormitory_df.itertuples():
        list_dormitory.append(row.동1)
        list_dormitory.append(row.동2)
        list_dormitory.append(row.동3)
    # 'nan' 값 제거
    list_dormitory = [x for x in list_dormitory if pd.notna(x)]
    # 중복 제거
    list_dormitory = list(set(list_dormitory))
    return list_dormitory


def crawling_some(df, name):
    df_temp = dp.get_oneroom_info(name)  # 동이름 넣으면 정보 반환하도록 ex. 광진구 화양동
    df = pd.concat([df, df_temp])
    print(df)
    return df


def crawling_all(df, list_dormitory):
    for i in list_dormitory:
        df_temp = dp.get_oneroom_info(i)
        if df_temp is None:
            continue
        df = pd.concat([df, df_temp])
        df.to_csv("./Data/one_room.csv", index=False)
    return df


def dormitory_to_dong(dormitory_df2):
    # '동1', '동2', '동3' 열을 '주소' 열로 합치기
    melted_df = pd.melt(
        dormitory_df2,
        id_vars=["대학교", "외국인_학생_수", "연평균_등록금", "기숙사비", "재학생_수", "수용가능인원", "지원자_수"],
        value_vars=["동1", "동2", "동3"],
        value_name="주소",
    )

    # '주소' 열을 새로운 인덱스로 설정
    melted_df.set_index("주소", inplace=True)

    # '주소' 열을 기준으로 그룹화하고, "외국인_학생_수", "연평균_등록금", "기숙사비", "재학생_수", "수용가능인원", "지원자_수" 열의 값을 합산
    grouped_df = melted_df.groupby("주소").agg(
        {
            "대학교": ",".join,
            "외국인_학생_수": "sum",
            "재학생_수": "sum",
            "수용가능인원": "sum",
            "지원자_수": "sum",
            "연평균_등록금": "mean",
            "기숙사비": "mean",
        }
    )
    # print(grouped_df)
    return grouped_df
