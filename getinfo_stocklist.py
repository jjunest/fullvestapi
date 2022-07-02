# -*- coding:utf-8,euc-kr -*-

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
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

logging.basicConfig(level=logging.DEBUG)
logging.warning("(logging) get_stock_list_kor() start in loggin")
logging.debug("(logging) get_stock_list_kor() start in loggin")




# 깃헙 업로드 테스트중ㅈ

def get_page_content(url):
    html_text = requests.get(url)
    page_soup = BeautifulSoup(html_text.content.decode('euc-kr', 'replace'), 'html.parser')
    return page_soup


# (코드참고) https://aidalab.tistory.com/29
def get_stock_list_kor():
    # print('this is get_stock_list_kor() start')
    # 종목코드는 거래소 파일에서 읽어옴. 네이버주가총액은 etf까지 존재, 거래소파일은 fullvestapi 폴더와 동일위치
    # 운영서버 코드
    # stock_list_kospi_csv = pd.read_csv("/home/fullvestapi/kospi_list.csv", encoding='euc-kr')
    # stock_list_kosdaq_csv = pd.read_csv("/home/fullvestapi/kosdaq_list.csv", encoding='euc-kr')
    # 개발로컬 PC 코드
    stock_list_kospi_csv = pd.read_csv("kospi_list.csv", encoding='euc-kr')
    stock_list_kosdaq_csv = pd.read_csv("kosdaq_list.csv", encoding='euc-kr')

    stock_list_kospi_csv = stock_list_kospi_csv.iloc[:,[0,1,3]]
    stock_list_kospi_csv['type'] = 0
    stock_list_kospi_csv.columns = ['stock_code_full','stock_code','stock_name_kr','type']
    stock_list_kospi_csv['stock_code'] = stock_list_kospi_csv['stock_code'].astype('str').str.zfill(6)
    stock_list_kospi_csv = stock_list_kospi_csv[['stock_code_full','type','stock_code','stock_name_kr']]

    # print(stock_list_kospi_csv)
    stock_list_kosdaq_csv = stock_list_kosdaq_csv.iloc[ :,[0,1,3]]
    stock_list_kosdaq_csv['type'] = 1
    # print("this is stock_lsit_kosdaq_csv:\n",stock_list_kosdaq_csv)
    stock_list_kosdaq_csv.columns = ['stock_code_full','stock_code','stock_name_kr','type']
    stock_list_kosdaq_csv['stock_code'] = stock_list_kosdaq_csv['stock_code'].astype('str').str.zfill(6)
    stock_list_kosdaq_csv = stock_list_kosdaq_csv[['stock_code_full','type','stock_code','stock_name_kr']]

    # concat을 하면, 앞의 index가 중복이 될 수 있으므로, index를 새롭게 만들어주는 조건을 넣어야 함
    stock_list_kr = pd.concat([stock_list_kospi_csv,stock_list_kosdaq_csv], ignore_index=True)
    stock_list_kr.columns = ['stock_code_full','type','stock_code','stock_name_kr']
    # print("this is stock_list_kr:", stock_list_kr)
    # print('this is get_stock_list_kor() end')

    return stock_list_kr


def get_stock_list_info_kor(stock_list_kor) :
    # print("this is get_stock_list_info_kor() start : ",datetime.now())
    logging.debug("get_stock_list_info_kor() start")
    stock_list_info_dataframe = pd.DataFrame()
    stock_list_info_dataframe_csv = pd.DataFrame()
    try:
        for i in range(len(stock_list_kor)) :
            stock_code_full = stock_list_kor.loc[i,"stock_code_full"]
            stock_code = stock_list_kor.loc[i,"stock_code"]
            # 가져올 데이터 # (1-1)저장 날짜는 항상 저장하자
            # strptime 는 객체를 -> datetime 오브젝트로 변환, strftime는 string형으로 변환
            bat_time = datetime.now()
            # print("this is bat_time",bat_time)
            vesting_type_detail = stock_list_kor.loc[i,"type"]
            stock_name_kr = stock_list_kor.loc[i, "stock_name_kr"]
            # print(bat_time)

            # 샘플로 [한국비엔씨] 정보부터 끌어오자 https://finance.naver.com/item/main.nhn?code=256840
            # 1) (종목시세정보) : 날짜, 종가, 거래량, 현재가, 전일가, 시가, 고가, 상한가, 저가, 하한가, 거래량, 거래대금,

            stock_list_info = {
                                  "stock_code_full" : stock_code_full,
                                  "stock_code" : stock_code,
                                  "stock_country" : 1,
                                  "vesting_type": 1,
                                  #   0은 코스닥이고, 1은 코스피
                                  "vesting_type_detail": vesting_type_detail,
                                  "stock_name" : stock_name_kr,
                                  "etc1_string" : "",
                                  "etc2_string" : "",
                                  "etc3_string" : "",
                                  "etc4_string" : "",
                                  "etc5_string" : "",
                                  "etc1_int" : 0,
                                  "etc2_int" : 0,
                                  "etc3_int" : 0,
                                  "etc4_int" : 0,
                                  "etc5_int" : 0,
            }
            stock_list_info_dataframe = stock_list_info_dataframe.append(stock_list_info, ignore_index=True)
            # print("this is stock_list_info_dataframe:\n",stock_list_info_dataframe)
            # insert_info_into_db(stock_list_info_dataframe)

    except IndexError as e:
        print("this is IndexError:",e.string)
        pass

    except AttributeError as e:
        print("this is AttributeError:", e.string)
        pass

    except TypeError as e :
        print("this is TypeError:", e.string)
        pass

    insert_info_into_db(stock_list_info_dataframe)

def insert_info_into_db(stock_list_info_dataframe) :
    # print("this is insert_info_into_db() start:",datetime.now())
    try:
        # DB sqlite 위치 구하기
        # stock_summary_info_dataframe
        # pandas 형식의 데이터 타입 -> 날짜 컬럼의 데이터타입을 바꿔주고 -> list로 변환
        print("this is stock_summary_info_dataframe len",len(stock_list_info_dataframe))
        # print("this is stock_list_info_dataframe\n",stock_list_info_dataframe)

        stock_list_info_dataframe['stock_code_full'] = stock_list_info_dataframe['stock_code_full'].astype(str)
        stock_list_info_dataframe['stock_code'] = stock_list_info_dataframe['stock_code'].astype(str)
        # stock_list_info_dataframe['stock_country'] = stock_list_info_dataframe['stock_country'].astype(str)
        # stock_list_info_dataframe['vesting_type'] = stock_list_info_dataframe['vesting_type'].astype(str)
        # stock_list_info_dataframe['vesting_type_detail'] = stock_list_info_dataframe['vesting_type_detail'].astype(str)
        stock_list_info_dataframe['stock_name'] = stock_list_info_dataframe['stock_name'].astype(str)


        stock_list_info_tolist = stock_list_info_dataframe.values.tolist()
        print("this is stock_list_info_tolist\n",stock_list_info_tolist)
        # 운영서버용 코드
        # sqliteconnection = sqlite3.connect("/home/TheaterWin/db.sqlite3")
        # 개발로컬PC용 코드
        sqliteconnection = sqlite3.connect("C:/Users/jjune/djangogirls/TheaterWin/db.sqlite3")
        print("this is connection")
        cursor = sqliteconnection.cursor()
        # sql = 'SET SESSION max_allowed_packet=100M'
        # cursor.execute(sql)
        # stock_summary_info_sample.to_sql('TheaterWinBook_StockSummaryKr',con=sqliteconnection,if_exists='append',index=False,method='multi')

        # executemany 실행 도중 error가 나면, 모두 rollback 이라 삽입이 1개도 되지 않음.
        cursor.executemany("INSERT OR REPLACE INTO TheaterWinBook_StockList("
                           "stock_code_full, stock_code, stock_country, vesting_type, vesting_type_detail, stock_name, "
                           "etc1_string, etc2_string, etc3_string, etc4_string, etc5_string, "
                           "etc1_int, etc2_int,etc3_int, etc4_int, etc5_int"
                           ") VALUES"
                           "(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", stock_list_info_tolist)
        # 데이터 프레임의 to_sql함수 : if_exists는 테이블이 존재하면 추가하겠다는 의미.
        # stock_summary_info_dataframe.to_sql('TheaterWinBook_StockSummaryKer3', con = sqliteconnection, if_exists='append', index=False)
        print("this is commit");
        sqliteconnection.commit()

    except sqlite3.Error as error:
        print("Error while connecting to sqlite",error)
        pass

    finally:
        if sqliteconnection :
            sqliteconnection.close()
            print("The Sqlite connection is closed")
        print("this is insert_info_into_db() end")

def remove_comma_string(integer_withcomma):
    integer_withcomma = integer_withcomma.replace(",","").strip()
    # print("this is integer_withcomma",integer_withcomma)
    return integer_withcomma

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("this is getinfo_stocklist.py start:",datetime.now())
    stockcode_url = "https://finance.naver.com/sise/sise_market_sum.nhn?&page="
    # print('오늘 네이버주가 끌어왓습니다!!! 네이버 주가는 : '+get_price("005930"))
    stock_list_kor = get_stock_list_kor()
    get_stock_list_info_kor(stock_list_kor)
    # get_stock_ifrs_info_kor(stock_list_kor)
    print("this is getinfo_summary_everyday.py end:",datetime.now())
    # insert_info_into_db()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
