import pandas as pd

# ファイルパス
orders_file = "orders.csv"
items_file = "items.csv"

# CSVファイルを読み込む
orders_df = pd.read_csv(orders_file)
items_df = pd.read_csv(items_file)

# orders_df と items_df を item_id で結合
merged_df = orders_df.merge(items_df[['item_id', 'item_price']], on='item_id', how='left')

# 購入金額を計算（購入個数 * 商品単価）
merged_df['total_price'] = merged_df['order_num'] * merged_df['item_price']

# 各ユーザーごとの平均購入金額を計算
user_avg_price = merged_df.groupby('user_id')['total_price'].mean()

# 最大の平均購入金額を持つユーザーを特定
max_user = user_avg_price.idxmax()
max_avg_price = user_avg_price.max()

# 結果を出力
print([max_user, max_avg_price])