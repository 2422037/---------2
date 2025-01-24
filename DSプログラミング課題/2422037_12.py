import pandas as pd

# ファイルパス
items_file = "items.csv"

# CSVファイルを読み込む
items_df = pd.read_csv(items_file)

# item_id=101 の商品情報を取得
target_item = items_df[items_df['item_id'] == 101].iloc[0]

# 同じ商品を除外し、候補商品を取得
candidates = items_df[items_df['item_id'] != 101].copy()

# ルール1: 小カテゴリが同じ商品を最優先し、大カテゴリが同じ商品を次に優先
candidates['category_rank'] = 2  # デフォルトで最低ランク
candidates.loc[candidates['big_category'] == target_item['big_category'], 'category_rank'] = 1
candidates.loc[candidates['small_category'] == target_item['small_category'], 'category_rank'] = 0

# ルール2: 価格が近い順に並べる（絶対値の差を計算）
candidates['price_diff'] = abs(candidates['item_price'] - target_item['item_price'])

# ルール3: ページ数が近い順に並べる（絶対値の差を計算）
candidates['page_diff'] = abs(candidates['pages'] - target_item['pages'])

# ソート条件: カテゴリ優先 → 価格の近さ → ページ数の近さ
sorted_candidates = candidates.sort_values(by=['category_rank', 'price_diff', 'page_diff'])

# 上位3件を取得
top_3_recommendations = sorted_candidates.head(3)['item_id'].tolist()

# 推薦候補を出力
print(top_3_recommendations)