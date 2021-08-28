# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy
import re
import datetime

from datetime import datetime
import time


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


# (코드출처) https://aidalab.tistory.com/29
def get_stock_list_kor():
    print('this is soup start')
    # 0은 코스피 주소, 1은 코스닥 주소
    sosoks = ['0', '1']
    item_code_list = []

    for sosok in sosoks:
        url_templ ='https://finance.naver.com/sise/sise_market_sum.nhn?sosok=%s'
        url = url_templ % sosok
        #print('this is url' + url)
        soup = get_page_content(url)
        # class 중에 맨 마지막 페이지 가는 버튼의 클래스는 pgRR
        td_class_pgRR = soup.find_all("td", {"class": "pgRR"})
        # td_class_pgRR 에 href 내에 page 파라미터 33 및 31을 끌어와야됌
        # print(td_class_pgRR)

        for page_item in td_class_pgRR :
            # td_class_pgRR 에 a태그 내 href 속성을 가져옴
            href_addr = page_item.a.get('href')
            # re패키지 = 파이썬의 정규식 패키지임
            page_info = re.findall("[\d]+", href_addr)
            page = page_info[1]
            # 캐스팅 후 + 1 (루프가 1번 덜 돈다)
            page_loop = int(page)+1
        # print("this is",page_loop)
        #코스피는 33번 반복, 코스닥은 31번 반복 필요
        for i in range(1, 2, 1):
        # for i in range(1, page_loop, 1):
            sub_url = '{}&page={}'.format(url,i)
            # print(sub_url)
            page_soup = get_page_content(url)
            # print(page_soup)
            # (주의) 클래스 이름이 title -> tltle임 ..
            stock_item = page_soup.find_all("a",{"class":"tltle"})
            # print(stock_item)
            for item in stock_item :
                item_data = re.search('[\d]+',str(item))
                # print(item_data)
                if item_data:
                    item_code = item_data.group()
                    item_name = item.text
                    # 코스닥은 0, 코스피는 1로 지정 = sosok
                    result = sosok, item_code, item_name
                    # print(result)
                    item_code_list.append(result)
    df = pd.DataFrame(item_code_list)
    df.columns = ['type','stock_code_kr','stock_name_kr']
    return df

# 출처 : https://aidalab.tistory.com/29
def get_stock_info_kor(stock_list_kor) :
    #네이버 상세페이지 : https://finance.naver.com/item/main.nhn?code=005930
    stock_code_list = stock_list_kor['stock_code_kr']
    # stock_name_list = stock_list_kor['stock_name_list']

    stock_detail_url_temp = "https://finance.naver.com/item/main.nhn?code=%s"
    data = []
    for stock_code in stock_code_list :
        # print("종목명", stock_list_kor['stock_code'])
        stock_detail_url = stock_detail_url_temp % stock_code
        print(stock_detail_url)
        stock_detail_soup = get_page_content(stock_detail_url)
        # 가져올 데이터 # (1-1)저장 날짜는 항상 저장하자
        now_time = datetime.now()
        print(now_time)
        # 샘플로 [한국비엔씨] 정보부터 끌어오자 https://finance.naver.com/item/main.nhn?code=256840
        # if stock_code == "256840":
        # 1) (종목시세정보) : 날짜, 종가, 거래량, 현재가, 전일가, 시가, 고가, 상한가, 저가, 하한가, 거래량, 거래대금,
        day_info_div = stock_detail_soup.find("div", class_ = "rate_info")
            #현재가 = day_info.div.p.find("span", class_ ="blind").string
        print("this is 현재가(종가) : " , remove_comma_string(day_info_div.div.p.find("span", class_ ="blind").string))
        day_info_blinds = day_info_div.table.find_all("span", class_="blind")
        print("this is 전일종가", remove_comma_string(day_info_blinds[0].string))
        print("this is 고가", remove_comma_string(day_info_blinds[1].string))
        print("this is 거래량", remove_comma_string(day_info_blinds[3].string))
        print("this is 시가", remove_comma_string(day_info_blinds[4].string))
        print("this is 거래대금", remove_comma_string(day_info_blinds[5].string))
            # 거래대금 단위
        print("this is 거래대금 단위: ", day_info_div.table.find("span", class_="sptxt sp_txt11").string)


        # 저장할때는 콤마지우기
        # 2) (투자정보)  시가총액, 시가총액 순위, 52주 최고, 52주 최저, PER, EPS,
        stock_short_info_div = stock_detail_soup.find("div", id ="aside")
        stock_short_info_table = stock_short_info_div.table
        # print(stock_short_info_table)


        # 4) (투자자별 매매동향) 매도 상위 TOP 5 / 매수 순위 TOP 5 / 외국인 및 기관 동향 정보

        # 5) (기업 실적 분석) 매출액 / 영업이익 / 당기순이익 / 영업이익률/ 순이익률 / ROE / 부채비율 / 유보율 / EPS / PER / BPS / PBR / 주당배당금(원) / 시가배당률 / 배당성향

        # 6) (테마주 분류) 동일업종명 분류


def remove_comma_string(integer_withcomma):
    integer_withcomma = integer_withcomma.replace(",","")
    print("this is integer_withcomma",integer_withcomma)
    return integer_withcomma

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    stockcode_url = "https://finance.naver.com/sise/sise_market_sum.nhn?&page="
    # print('오늘 네이버주가 끌어왓습니다!!! 네이버 주가는 : '+get_price("005930"))
    stock_list_kor = get_stock_list_kor()
    get_stock_info_kor(stock_list_kor)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
