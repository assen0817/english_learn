import os
from time import sleep
import requests
import sqlite3
import pprint
from dotenv import load_dotenv
from random import randint
from colorama import init
from colorama import Fore, Back

def yes_or_no():
    choice = input("Please respond with 'yes' or 'no' [y/N]: ").lower()
    if choice in ['y', 'ye', 'yes']:
        return True
    elif choice in ['n', 'no']:
        return False
    else:
        return yes_or_no()

#         async_playsound(1, 'https://weblio.hs.llnwd.net/e8/audio/lexicographer.mp3')
# async def async_playsound(time, file):
#     while True:
#         playsound(file)
#         await asyncio.sleep(time)


def check_spell(val):
    ans = input(f"{val}: ")
    if ans == val:
        pass
    else:
        check_spell(val)


# .envファイルの内容を読み込みます
load_dotenv()

dbname = os.environ['db']
weblio = os.environ['weblio']
weblio_sound = os.environ['weblio_sound']
# DBを作成する（既に作成されていたらこのDBに接続する）
conn = sqlite3.connect(dbname)
# SQLiteを操作するためのカーソルを作成
cur = conn.cursor()
cur.execute(
        'SELECT COUNT( * ) FROM lang'
)

count = 0
for c in cur:
    count = c[0]
try:
    while True:
        if count == 0:
            break
        r = randint(1,count)
        cur.execute(f'select * from lang where id={r}')

        id, name, description, pronounce = (0, '', '', '')
        for (id, name, description, pronounce) in cur:
            pass

        print(Fore.WHITE + Back.LIGHTBLUE_EX + f'{id}, {name}: {pronounce}の読み方')
        print(Fore.WHITE + Back.LIGHTBLUE_EX + f'{weblio_sound}{name}.mp3')
        val = input()
        print(Fore.LIGHTWHITE_EX + Back.RESET + f'{description}\n{weblio + name}')
        check_spell(name)
        ans = yes_or_no()
        print(ans)
        cur.execute(f'insert into log (lang_id, ok) values ({id}, {1 if ans else 0})')
        
        conn.commit()
except KeyboardInterrupt:
    print(Back.RESET)
    print(Fore.RED + Back.RESET + f'{name}, {description}, {pronounce}\n{weblio + name}')
    print(Fore.RESET + Back.RESET + '終了します')
    pass
    

# DBとの接続を閉じる(必須)
conn.close()
