import pandas as pd

# ローカルファイルを読み込む
df = pd.read_csv('winequality-red.csv')

# 'quality' が6以上のデータをフィルタリング
filtered_df = df[df['quality'] >= 6]

# 'quality' 列で降順に並べ替え
sorted_df = filtered_df.sort_values(by='quality', ascending=False)

# 結果を表示
print(sorted_df)