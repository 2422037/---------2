import pandas as pd

# CSVファイルを読み込み
df = pd.read_csv('winequality-red.csv')

# 5行目から10行目を表示 (インデックス4から9)
print(df.iloc[4:10])
