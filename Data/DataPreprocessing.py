import Crawling as dp


df = dp.get_oneroom_info("광진구 화양동")  # 동이름 넣으면 정보 반환하도록 ex. 광진구 화양동

df.to_csv("./Data/광진구_화양동2.csv", index=False)
