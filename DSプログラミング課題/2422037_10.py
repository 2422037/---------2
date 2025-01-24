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

# 最大の購入金額の注文を特定
max_order = merged_df.loc[merged_df['total_price'].idxmax(), ['order_id', 'total_price']]

# 結果を出力
print([max_order['order_id'], max_order['total_price']])