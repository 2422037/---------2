import requests
from bs4 import BeautifulSoup
import time
import sqlite3

# SQLiteデータベースの接続
conn = sqlite3.connect('real_estate.db')
cursor = conn.cursor()

# データベースにテーブルを作成（物件名、販売価格、所在地、沿線・駅を格納）
cursor.execute('''
CREATE TABLE IF NOT EXISTS properties (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    property_name TEXT,
    price TEXT,
    location TEXT,
    station TEXT
)
''')

# ベースURL（ページ番号を挿入する部分を含む）
base_url = "https://suumo.jp/jj/bukken/ichiran/JJ010FJ001/?ar=030&bs=020&ta=13&jspIdFlg=patternShikugun&sc=13201&pn={}"

# 1ページ目から180ページ目までスクレイピング
for page_num in range(1, 181):  # 1から180ページ目まで
    url = base_url.format(page_num)
    print(f"スクレイピング中: {url}")

    # URLにアクセスしてHTMLを取得
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 物件情報を全て取得
    property_names = soup.find_all('dt', text="物件名")
    prices = soup.find_all('dt', text="販売価格")
    locations = soup.find_all('dt', text="所在地")
    stations = soup.find_all('dt', text="沿線・駅")

    # 各ページ内で物件ごとにデータを取得してデータベースに格納
    for i in range(len(property_names)):
        property_name = property_names[i].find_next('dd').text.strip() if i < len(property_names) else None
        price = prices[i].find_next('dd').text.strip() if i < len(prices) else None
        location = locations[i].find_next('dd').text.strip() if i < len(locations) else None
        station = stations[i].find_next('dd').text.strip() if i < len(stations) else None

        if property_name and price and location and station:
            # データベースに保存
            cursor.execute('''
            INSERT INTO properties (property_name, price, location, station)
            VALUES (?, ?, ?, ?)
            ''', (property_name, price, location, station))
            conn.commit()  # コミットしてデータを保存

            print(f"物件名: {property_name}")
            print(f"販売価格: {price}")
            print(f"所在地: {location}")
            print(f"沿線・駅: {station}")
            print("-" * 60)

    # 次のページに遷移するために5秒待機
    time.sleep(5)  # 5秒間待機

# データベースを閉じる
conn.close()

import sqlite3
import pandas as pd
import japanize_matplotlib

# SQLiteデータベースに接続
conn = sqlite3.connect('real_estate.db')

# データベースから物件情報を読み込む
query = "SELECT * FROM properties"
df = pd.read_sql(query, conn)

# データベース接続を閉じる
conn.close()

# データの確認
print(df.head())
# 価格を数値に変換する関数
def extract_price(price_str):
    # 価格が「～」または「・」で区切られている場合、最初の価格を返す
    if "～" in price_str or "・" in price_str:
        # 「～」または「・」で分割
        price_range = price_str.split('～') if "～" in price_str else price_str.split('・')  
        # 最小価格を数値に変換
        price_min = price_range[0].replace('万円', '').replace(',', '').strip()
        # '億' or non-numeric characters are present, return NaN
        if not price_min.isdigit() or '億' in price_min:
            return float('nan')  
        price_min = int(price_min) * 10000 
        
        # 最大価格が存在する場合、数値に変換
        if len(price_range) > 1:  
            price_max = price_range[1].replace('万円', '').replace(',', '').strip()
            # '億' or non-numeric characters are present, return NaN
            if not price_max.isdigit() or '億' in price_max:
                return float('nan')  
            price_max = int(price_max) * 10000
            return (price_min + price_max) / 2  # 平均価格を取る
        else:
            return price_min # 最小価格のみを返す

    else:
        # 単一価格の場合
        price = price_str.replace('万円', '').replace(',', '').strip()
        # '億' or non-numeric characters are present, return NaN
        if not price.isdigit() or '億' in price:
            return float('nan')
        return int(price) * 10000
# 所在地から市区町村を抽出（例: 東京都小金井市前原町→小金井市）
df['area'] = df['location'].apply(lambda x: x.split('市')[0] + '市' if '市' in x else x)

# データの確認
print(df[['property_name', 'location', 'area']].head())
import matplotlib.pyplot as plt
import seaborn as sns

# Apply the extract_price function to the 'price' column and create a new 'price_numeric' column
df['price_max'] = df['price'].apply(extract_price)

# Now you can plot the distribution of prices using the new column
plt.figure(figsize=(10, 6))
sns.histplot(df['price_max'], kde=True, bins=30)
plt.title('販売価格の分布')
plt.xlabel('価格（円）')
plt.ylabel('物件数')
plt.show()
# エリアごとに平均価格を計算
area_price = df.groupby('area')['price_max'].mean().sort_values(ascending=False)

# 平均価格を可視化
plt.figure(figsize=(12, 6))
area_price.plot(kind='bar', color='skyblue')
plt.title('エリアごとの平均価格')
plt.xlabel('エリア')
plt.ylabel('平均価格（円）')
plt.xticks(rotation=45)
plt.show()
# 駅名に「徒歩10分以内」が含まれているかをチェック
df['is_near_station'] = df['station'].apply(lambda x: '徒歩' in x and '分' in x and int(x.split('徒歩')[1].split('分')[0]) <= 10)

# 駅近物件の割合
near_station_ratio = df['is_near_station'].value_counts(normalize=True) * 100

# 結果を表示
print("駅近物件の割合:")
print(near_station_ratio)

# 駅近物件の可視化
plt.figure(figsize=(6, 6))
sns.countplot(x='is_near_station', data=df, palette='Set2')
plt.title('駅近物件の分布')
plt.xlabel('駅近物件')
plt.ylabel('物件数')
plt.xticks(ticks=[0, 1], labels=['遠い', '近い'])
plt.show()
# 価格と駅近物件の関係を可視化
plt.figure(figsize=(10, 6))
# Changed 'price_numeric' to 'price_max'
sns.boxplot(x='is_near_station', y='price_max', data=df, palette='Set2') 
plt.title('駅近物件の価格分布')
plt.xlabel('駅近物件')
plt.ylabel('価格（円）')
plt.xticks(ticks=[0, 1], labels=['遠い', '近い'])
plt.show()