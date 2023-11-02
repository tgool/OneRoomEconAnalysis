import requests
import pandas as pd
import geohash2
from GPT_model import GPTModel as gpt_model


def get_oneroom_info(addr):  # 동이름 넣으면 정보 반환하도록 ex. 광진구 화양동
    # GPT = gpt_model()
    # 동이름으로 원룸의 위도와 경도을 받기(1번째 request)
    url = f"https://apis.zigbang.com/v2/search?leaseYn=N&q={addr}&serviceType=원룸"
    response = requests.get(url)
    data = response.json()["items"][0]
    lat, lng = data["lat"], data["lng"]
    geohash = geohash2.encode(lat, lng, precision=5)

    # 범위 값으로 원룸 매물 아이디 값을 수집한다(2번째 request)
    # url = f"https://apis.zigbang.com/v2/items?deposit_gteq=0&domain=zigbang\&geohash={geohash}&needHasNoFiltered=true&rent_gteq=0&sales_type_in=월세&service_type_eq=원룸"
    url = f"https://apis.zigbang.com/v2/items/oneroom?geohash={geohash}&depositMin=0&rentMin=0&salesTypes[0]=월세&domain=zigbang&checkAnyItemWithoutFilter=true"
    response = requests.get(url)
    items = response.json()["items"]
    ids = [item["itemId"] for item in items]

    # 아이디 값으로 원룸 매물 정보를 추출한다(3번째 request)
    url = "https://apis.zigbang.com/v2/items/list"
    params = {"domain": "zigbang", "item_ids": ids[:900]}
    response = requests.post(url, params)
    if "items" not in response.json():
        return
    items = response.json()["items"]
    colums = [
        "item_id",
        "sales_type",
        "deposit",
        "rent",
        "address1",
        "manage_cost",
        # "floor",
        "size_m2",
        "service_type",
        # "room_type",
    ]
    df = pd.DataFrame(items)[colums]
    df = df[df["address1"].str.contains(addr)].reset_index(drop=True)
    df = df.rename(
        columns={
            "address1": "주소",
            "sales_type": "유형",
            "deposit": "보증금",
            "rent": "월세",
            "manage_cost": "관리비",
            # "floor": "층수",
            "size_m2": "평수",
            "service_type": "건물_형태",
            # "room_type": "분리형",  # 1 오픈형 2 분리형 3 투룸 4 쓰리룸+
        }
    )
    # 아이디 값으로 원룸 etc 정보를 추출한다(4번째 request)
    id_list = df["item_id"].tolist()
    for i in id_list:
        url = f"https://apis.zigbang.com/v3/items/{i}?version=&domain=zigbang"
        response = requests.get(url)
        data = response.json()["item"]
        df.loc[df["item_id"] == i, "엘레베이터"] = data["elevator"]
        df.loc[df["item_id"] == i, "룸_형태"] = data["roomType"]
        df.loc[df["item_id"] == i, "룸_층수"] = data["floor"]["floor"]
        df.loc[df["item_id"] == i, "건물_층수"] = data["floor"]["allFloors"]
        df.loc[df["item_id"] == i, "집_방향"] = data["roomDirection"]  # se
        df.loc[df["item_id"] == i, "옵션_수"] = len(data["options"])
        df.loc[df["item_id"] == i, "지하철역_수"] = len(response.json()["subways"])
        # print("loading..")
        # gpt_date = GPT.edit_date(data["approveDate"])
        # print("done")
        df.loc[df["item_id"] == i, "준공년수"] = data["approveDate"]
        df.loc[df["item_id"] == i, "주차여부"] = data["parkingAvailableText"]
        for poi in data["neighborhoods"]["nearbyPois"]:
            df.loc[df["item_id"] == i, poi["poiType"]] = poi["distance"]
        # pnu 정보 없는 데이터도 있어서 PASS
        # 추가 건물 정보 수집
        # pnu = data["pnu"]
        # url = f"https://apis.zigbang.com/v2/bls/{pnu}"
        # response = requests.get(url)
        # data = response.json()
        # print(data)
        # df.loc[df["item_id"] == i, "건물_연식"] = data["준공시기"]
        # df.loc[df["item_id"] == i, "건물_총세대수"] = data["세대수"]
        # df.loc[df["item_id"] == i, "건물_주차대수"] = data["주차대수"]

    # if "룸_형태" in df.columns:
    #    if df["룸_형태"].isin(["투룸", "쓰리룸"]).any():
    #        df = df[~df["룸_형태"].isin(["투룸", "쓰리룸"])]
    return df


def univ(name):
    lat, lng = None, None
    url = f"https://apis.zigbang.com/v2/search?leaseYn=N&q={name}&serviceType=원룸"
    response = requests.get(url)
    data = response.json()
    print(data)
    for item in data["items"]:
        if item["hint"] == "본교":
            lat, lng = (
                item["lat"],
                item["lng"],
            )
    return lat, lng


def distance(id):
    url = f"https://apis.zigbang.com/v3/items/{id}?version=&domain=zigbang"
    response = requests.get(url)
    data = response.json()["item"]
    lat = data["randomLocation"]["lat"]
    lng = data["randomLocation"]["lng"]
    return lat, lng
