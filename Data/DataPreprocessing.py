import Crawling as dp
import pandas as pd
import PreprocessingFunc as pf
import statsmodels.api as sm

df = pd.read_csv("./Data/one_room_join_distance_min.csv")
df["룸_층수"] = df["룸_층수"].replace(["반지하", "옥탑방"], -1)
df = df.drop(["item_id"], axis=1)
df = df.drop(["유형"], axis=1)
df = df.drop(["주소"], axis=1)
df = df.drop(["준공년수"], axis=1)
df = df.drop(["대학교"], axis=1)
df_dummy = pd.get_dummies(df, prefix=["건물_형태", "엘레베이터", "룸_형태", "집_방향", "주차_여부"])

X = df_dummy.drop(["월세"], axis=1)
X = sm.add_constant(X)
Y = df_dummy["월세"]
model = sm.OLS(Y, X)
results = model.fit()
print(results.summary())
