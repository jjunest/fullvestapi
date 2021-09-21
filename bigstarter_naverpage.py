# -*- coding:utf-8 -*-


# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import requests
from bs4 import BeautifulSoup
import pandas as pd



def get_stock_samsung():
    stock_summary_info_dataframe_csv = pd.DataFrame()

    stock_url = "https://finance.naver.com/item/main.naver?code=005930"
    print("this is url", stock_url)
    result = requests.get(stock_url)
    stock_detail_soup = BeautifulSoup(result.content.decode('euc-kr', 'replace'), "html.parser")  # html.parser 로 파이썬에서 쓸 수 있는 형태로 변환

    # 1. 기준일 출력하기
    info_date = stock_detail_soup.find("span", id="time").get_text().strip().replace(".", "-")
    print("this is info_date",info_date)

    # 2. 현재가격 출력하기
    day_info_div = stock_detail_soup.find("div", class_="rate_info")
    stock_now = day_info_div.div.p.find("span", class_="blind").get_text()
    print("this is stock_now", stock_now)

    # 3. 전일종가 출력하기
    day_info_blinds = day_info_div.table.find_all("span", class_="blind")
    stock_close_yesterday = day_info_blinds[0].get_text()
    print("this is stock_close_yesterday",stock_close_yesterday)

    # 4. 고가 출력하기
    stock_high = day_info_blinds[1].get_text()
    print("this is stock_high", stock_high)

    # (문제1) 거래량 읽어서 출력하기


    # (문제2) PER, EPS, 정보 출력하기


    # (문제3) csv 파일로 출력하기

    stock_summary_info = {
        "info_date": info_date,
        "stock_now": stock_now,
        "stock_close_yesterday": stock_close_yesterday,
    }
    stock_summary_info_dataframe_csv = stock_summary_info_dataframe_csv.append(stock_summary_info, ignore_index=True)
    output_path = 'backup_stockinfo/test_210921.csv'
    stock_summary_info_dataframe_csv.to_csv(output_path, header=True, index=False, encoding='euc-kr')

    # (문제4) 다른 주식 종목들도 주소 바꿔서 해보기


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    get_stock_samsung()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
