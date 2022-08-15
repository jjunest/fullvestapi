# 인코딩 선언 필수
# -*- coding: utf-8 -*-

import sqlite3
import django

# 개발환경 = local, 운영환경 = real
setting = 'real'
# setting = 'local'

if __name__ == '__main__':
    print("this is apiDBtest")
    testtext = 'testtext'
    if setting in 'real':
        # 운영서버용 코드
        conn = sqlite3.connect("/home/TheaterWin/db.sqlite3")
    if setting in 'local':
        conn = sqlite3.connect('C:\\Users\\jjune\\djangogirls\\TheaterWin\\db.sqlite3')
    cur = conn.cursor()
    query = "INSERT INTO TheaterWinBook_FullvestingApi (fullvesting_text) VALUES (?)"
    cur.execute(query, (testtext,))
    conn.commit()
    cur.close()
    conn.close()
    # get_stock_ifrs_info_kor(stock_list_kor)
    # insert_info_into_db()
