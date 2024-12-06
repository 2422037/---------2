import pandas as pd

# CSVファイルを読み込み
df = pd.read_csv('winequality-red.csv')

# 'quality' 列ごとにグループ化し、各グループの平均を計算
grouped_df = df.groupby('quality').mean()

# 結果を表示
print(grouped_df)
