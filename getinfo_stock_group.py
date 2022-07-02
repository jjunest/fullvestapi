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
import json

# 깃헙 업로드 테스트중

def get_bs_obj(com_code):
    url = "https://finance.naver.com/item/main.nhn?code=" + com_code
    result = requests.get(url)
    bs_obj = BeautifulSoup(result.content, "html.parser")  # html.parser 로 파이썬에서 쓸 수 있는 형태로 변환
    return bs_obj


def get_price(com_code):
    bs_obj = get_bs_obj(com_code)
    no_today = bs_obj.find("p", {"class": "no_today"})
    blind_now = no_today.find("span", {"class": "blind"})
    return blind_now.text


def get_page_content(url):
    html_text = requests.get(url)
    page_soup = BeautifulSoup(html_text.content.decode('euc-kr', 'replace'), 'html.parser')
    return page_soup


def insert_ifrsinfo_into_db(stock_ifrs_info_dataframe):
    try:
        # DB sqlite 위치 구하기
        # stock_summary_info_dataframe
        # pandas 형식의 데이터 타입 -> 날짜 컬럼의 데이터타입을 바꿔주고 -> list로 변환
        stock_ifrs_info_dataframe['bat_time'] = stock_ifrs_info_dataframe['bat_time'].apply(str)
        # 데이터프레임 안의 datetime 타입 -> date 타입으로 변경
        stock_ifrs_info_dataframe['info_date'] = stock_ifrs_info_dataframe['info_date'].dt.date
        stock_ifrs_info_dataframe['info_date'] = stock_ifrs_info_dataframe['info_date'].apply(str)

        # print("this is stock_ifrs_info_dataframe['ifrs_date']", stock_ifrs_info_dataframe['ifrs_date'])

        stock_ifrs_info_dataframe['ifrs_date'] = stock_ifrs_info_dataframe['ifrs_date'].dt.date
        stock_ifrs_info_dataframe['ifrs_date'] = stock_ifrs_info_dataframe['ifrs_date'].apply(str)
        # stock_summary_info['info_date'].dt.date
        # print("this is bat_time",stock_summary_info['bat_time'])
        # stock_summary_info['info_date'] = stock_summary_info['info_date']
        # stock_summary_info_sample = stock_summary_info_sample['info_date'].apply(str)
        info_intoDB_list = stock_ifrs_info_dataframe.values.tolist()
        # print("this is tolist()",stock_summary_info_tolist)
        print("this is stock_summary_info_tolist's length:", len(info_intoDB_list))
        # 운영서버용 코드
        # sqliteconnection = sqlite3.connect("/home/fullvesting/TheaterWin/db.sqlite3")
        # 개발로컬PC용 코드
        sqliteconnection = sqlite3.connect("C:/Users/jjune/djangogirls/TheaterWin/db.sqlite3")
        print("this is sqlite connection")
        cursor = sqliteconnection.cursor()
        # sql = 'SET SESSION max_allowed_packet=100M'
        # cursor.execute(sql)
        # stock_summary_info_sample.to_sql('TheaterWinBook_StockSummaryKr',con=sqliteconnection,if_exists='append',index=False,method='multi')

        # cursor.executemany("INSERT INTO TheaterWinBook_StockSummaryKr("
        #                    "bat_time, info_date, stock_code, stock_country, vesting_type, vesting_type_detail, stock_name"
        #                    ") VALUES"
        #                    "(?,?,?,?,?,?,?) ",stock_summary_info_sample_tolist)

        # executemany 실행 도중 error가 나면, 모두 rollback 이라 삽입이 1개도 되지 않음.
        cursor.executemany("INSERT OR REPLACE INTO TheaterWinBook_StockIfrsKr("
                           "bat_time, info_date, ifrs_date, stock_code, stock_country, ifrs_type, vesting_type, vesting_type_detail, stock_name,"
                           "stock_revenue,operating_income,net_income,operating_income_ratio,income_ratio,"
                           "roe,debt_ratio,quick_ratio,reserve_ratio,stock_eps,stock_per,stock_bps,stock_pbr,"
                           "dividend_per_share,dividend_yield_ratio,dividend_payout_ratio,"
                           "etc1_string, etc2_string, etc3_string,"
                           "etc1_int, etc2_int,etc3_int"
                           ") VALUES"
                           "(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,"
                           "?,?,?,?,?,?,?,?,?,?,?) ", info_intoDB_list)
        # 데이터 프레임의 to_sql함수 : if_exists는 테이블이 존재하면 추가하겠다는 의미.
        # stock_summary_info_dataframe.to_sql('TheaterWinBook_StockSummaryKer3', con = sqliteconnection, if_exists='append', index=False)

        sqliteconnection.commit()

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
        pass

    finally:
        if sqliteconnection:
            sqliteconnection.close()
            print("The Sqlite connection is closed")


def remove_comma_string(integer_withcomma):
    integer_withcomma = integer_withcomma.replace(",", "").strip()
    # print("this is integer_withcomma",integer_withcomma)
    return integer_withcomma


def getinfo_stock_group():
    info_dataframe = pd.DataFrame()
    info_dataframe_csv = pd.DataFrame()
    print("this is getinfo_stock_group")
    naver_stock_url = 'https://finance.naver.com'
    stock_grouplist_url = "https://finance.naver.com/sise/sise_group.naver?type=upjong"
    stock_detail_soup = get_page_content(stock_grouplist_url)
    bat_time = datetime.now()
    try:
        get_content_area = stock_detail_soup.find("div", id ="contentarea_left")
        get_content_table = get_content_area.find("table", class_ ="type_1")
        # print("get_contetnt",get_content_table)
        get_table_tr = get_content_table.find_all("a")
        # print("this is get_table_tr",get_table_tr)

        # 업종 목록 저장하기
        stock_group_dic = []


        for item in get_table_tr :
            # print("this is item",item.text)
            if item.text :
                stock_group_data = {item.text:item['href']}
                # print("this is group_data",stock_group_data)
                stock_group_dic.append(stock_group_data)

        stock_group_list = list(stock_group_dic)
        # print("this is group_list",stock_group_list)



        # # 업종 목록 모두 방문하기
        for item in stock_group_list :
            try:
                # key 값 및 value 값으로 접근함
                stock_group_name = list(item.keys())
                stock_group_name_withoutbrackets = ', '.join(map(str,stock_group_name))
                stock_group_name_withoutbrackets = str(stock_group_name_withoutbrackets)
                # Dictionary 자료형에서 가로형을 제외하고 string만 저장할 경우

                stock_group_url = list(item.values())
                stock_group_url_withoutbrackets = ', '.join(map(str,stock_group_url))
                stock_group_url_withoutbrackets = str(stock_group_url_withoutbrackets)


                # print(stock_group_url_withoutbrackets)
                naver_group_url = naver_stock_url + stock_group_url_withoutbrackets
                print(naver_group_url)

                # naver_group_url로 들어가서
                group_detail_soup = get_page_content(naver_group_url)
                get_content_area = group_detail_soup.find("div", id ="contentarea")
                get_content_table = get_content_area.find("table", class_="type_5")
                # print(get_content_table)
                get_content_table_tr = get_content_table.select("tbody tr div.name_area a")
                for item in get_content_table_tr :
                    print(item.text)
                    # print(item['href'])
                    stock_name = item.text.strip()
                    stock_code = str(item['href'])[22:]
                    print(stock_code)

                    stock_group_info = {
                        "bat_time": bat_time,
                        "info_date": bat_time,
                        "stock_code": stock_code,
                        "stock_country": 1,
                        "vesting_type": 1,
                        "stock_name" : stock_name,
                        "stock_group" : stock_group_name_withoutbrackets,
                        "stock_theme" : 0

                    }

                    info_dataframe = info_dataframe.append(stock_group_info, ignore_index=True)
                    print("this is info_dataframe len:", len(info_dataframe))
                    # 100 개씩 잘라서 넣어주고, dataframe을 초기화 시켜줘야됨
                    info_dataframe_csv = info_dataframe_csv.append(stock_group_info, ignore_index=True)
                    print("this is info_dataframe_csv len:", len(info_dataframe_csv))
                    if len(info_dataframe) == 100:
                        # insert_ifrsinfo_into_db(info_dataframe)
                        info_dataframe = info_dataframe.iloc[0:0]

            except IndexError as e:
                print("this is IndexError:", e.string)
                pass

            except AttributeError as e:
                print("this is AttributeError:", e.string)
                pass

            except TypeError as e:
                print("this is TypeError:", e.string)
                pass

            # 100개씩 넣은 후 나머지 데이터가 있으면 넣어주기
            # if len(info_dataframe) != 0:
                # insert_ifrsinfo_into_db(info_dataframe)



    except IndexError as e:
        print("this is IndexError:", e.string)
        pass

    except AttributeError as e:
        print("this is AttributeError:", e.string)
        pass

    except TypeError as e:
        print("this is TypeError:", e.string)
        pass

    # csv파일로 저장하기
    filename = 'backup_stock_group_info_' + bat_time.strftime("%Y%m%d")

    uniq = 1
    output_path = 'backup_stockinfo/%s(%d).csv' % (filename, uniq)
    while (os.path.exists(output_path)):
        output_path = 'backup_stockinfo/%s(%d).csv' % (filename, uniq)
        uniq += 1
    print("this is output_path", output_path)
    info_dataframe_csv.to_csv(output_path, header=True, index=False, encoding='euc-kr')

    print("this is get_stock_ifrs_info_kor() end")



    # # 100개씩 넣은 후 나머지 데이터가 있으면 넣어주기
    # if len(info_dataframe) != 0:
    #     insert_ifrsinfo_into_db(info_dataframe)


    # # csv파일로 저장하기
    # filename = 'backup_stock_ifrs_info_' + bat_time.strftime("%Y%m%d")
    # uniq = 1
    # output_path = 'backup_stockinfo/%s(%d).csv' % (filename, uniq)
    # while (os.path.exists(output_path)):
    #     output_path = 'backup_stockinfo/%s(%d)%s' % (filename, uniq)
    #     uniq += 1
    # print("this is output_path", output_path)
    # info_dataframe_csv.to_csv(output_path, header=True, index=False, encoding='euc-kr')
    #
    # print("this is get_stock_ifrs_info_kor() end")
    #
    #
    #



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    getinfo_stock_group()
    # insert_info_into_db()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
