import os
from time import sleep
import requests
import sqlite3
import pprint
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# .envファイルの内容を読み込みます
load_dotenv()

dbname = os.environ['db']
# DBを作成する（既に作成されていたらこのDBに接続する）
conn = sqlite3.connect(dbname)
# SQLiteを操作するためのカーソルを作成
cur = conn.cursor()

# テーブルの作成
# cur.execute(
#     'CREATE TABLE lang(id INTEGER PRIMARY KEY AUTOINCREMENT, name STRING, description STRING, pronounce STRING)'
# )
# cur.execute(
#     'CREATE TABLE log(id INTEGER PRIMARY KEY AUTOINCREMENT, lang_id INTEGER, ok INTEGER)'
# )

# os.environを用いて環境変数を表示させます
site = os.environ['site']

for i in range(1, 21):
    res = requests.get(f"{site}words{i}")
    soup = BeautifulSoup(res.text, "html.parser")
    figure = soup.find('figure', class_='wp-block-table')
    trs = []
    for i, tr in enumerate(figure.find_all('tr')):
        if i == 0:
            continue
        tds = []
        for td in tr.find_all('td'):
            tds.append(td.text)

        trs.append((tds[1], str(tds[2]).replace('"', ''), tds[3]))

    cur.executemany('insert into lang (name, description, pronounce) values (?, ?, ?)', trs)
    sleep(1)

conn.commit()
# DBとの接続を閉じる(必須)
conn.close()