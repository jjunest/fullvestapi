#!/home/myvenv/bin/python
# -*- coding:utf-8,euc-kr -*-


import sqlite3
import django
import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy
import re
import datetime
import sqlite3
from datetime import datetime
from datetime import date
import time
import logging

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
    stock_list_info_dataframe = pd.DataFrame()

    stock_list_info = {
        "fullvesting_text" : "test1"
    }
    stock_list_info_dataframe = stock_list_info_dataframe.append(stock_list_info, ignore_index=True)

    stock_list_info = {
        "fullvesting_text" : "test2"
    }
    stock_list_info_dataframe = stock_list_info_dataframe.append(stock_list_info, ignore_index=True)
    stock_list_info_tolist = stock_list_info_dataframe.values.tolist()
    print("this is stock_list_info_tolist:",stock_list_info_tolist)

    cur = conn.cursor()
    # query = "INSERT INTO TheaterWinBook_FullvestingApi (fullvesting_text) VALUES (?)"
    cur.executemany("INSERT INTO TheaterWinBook_FullvestingApi (fullvesting_text) VALUES (?)", stock_list_info_tolist)
    conn.commit()
    cur.close()
    conn.close()
    # get_stock_ifrs_info_kor(stock_list_kor)
    # insert_info_into_db()
