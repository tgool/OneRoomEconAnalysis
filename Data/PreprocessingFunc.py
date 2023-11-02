import Crawling as dp
import pandas as pd
from GPT_model import GPTModel as gpt_model
import ast
import time
from haversine import haversine


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
        df.to_csv("./Data/one_room_gpt.csv", index=False)
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


def gpt_edit_date(df):
    GPT = gpt_model()
    print("loading..")
    for index, row in df.iterrows():
        # 원하는 조건 없이 값을 변경합니다.
        modified_value = GPT.edit_date(row["준공년수"])  # 예시: 원래 값에 10을 곱함
        df.at[index, "준공년수"] = modified_value
    print("done")
    return df


def gpt_edit_date_list(df):
    GPT = gpt_model()

    B_column_list = df["준공년수"].tolist()
    # 리스트를 10분의 1로 나누기 위한 크기를 계산합니다.
    chunk_size = len(B_column_list) // 100

    # 리스트를 10분의 1씩 나누어서 각 부분을 처리합니다.
    for i in range(0, len(B_column_list), chunk_size):
        # 현재 부분의 끝 인덱스를 계산합니다.
        end = (
            i + chunk_size
            if (i + chunk_size) < len(B_column_list)
            else len(B_column_list)
        )
        print("loading..")
        # 현재 부분의 리스트를 GPT 모델에게 전달하고 결과를 받아옵니다.
        results = GPT.edit_date(str(B_column_list[i:end]))
        print("done")
        # 결과를 이용하여 원래 리스트의 해당 부분을 대체합니다.
        B_column_list[i:end] = ast.literal_eval(results)
        time.sleep(10)

    # 변경된 리스트를 데이터프레임에 반영합니다.
    df["준공년수"] = B_column_list

    return df


def distance_avg(df):
    dis = 0
    for index, row in df.iterrows():
        item_id = row["item_id"]
        lat1, lng1 = dp.distance(item_id)
        room = (float(lat1), float(lng1))
        name = row["대학교"]
        universities = name.split(",")  # 쉼표를 기준으로 문자열 분리
        if len(universities) > 1:
            for university in universities:
                lat2, lng2 = dp.univ(university)
                univ = (float(lat2), float(lng2))
                dis += haversine(room, univ, unit="km")
            df.at[index, "대학교_거리"] = dis / len(
                universities
            )  # 대학교가 많을 경우 각 거리 평균 내서 넣어줌
        else:
            lat2, lng2 = dp.univ(name)
            univ = (float(lat2), float(lng2))
            df.at[index, "대학교_거리"] = haversine(room, univ, unit="km")
        # lat lng 순 (위도 경도)
    return df


def distance_min(df):
    dis = []
    for index, row in df.iterrows():
        item_id = row["item_id"]
        lat1, lng1 = dp.distance(item_id)
        room = (float(lat1), float(lng1))
        name = row["대학교"]
        universities = name.split(",")  # 쉼표를 기준으로 문자열 분리
        if len(universities) > 1:
            for university in universities:
                lat2, lng2 = dp.univ(university)
                univ = (float(lat2), float(lng2))
                dis.append(haversine(room, univ, unit="km"))
            df.at[index, "대학교_거리"] = min(dis)  # 대학교가 많을 경우 최소 거리
        else:
            lat2, lng2 = dp.univ(name)
            univ = (float(lat2), float(lng2))
            df.at[index, "대학교_거리"] = haversine(room, univ, unit="km")
        # lat lng 순 (위도 경도)
    return df
