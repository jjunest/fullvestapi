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


# (코드출처) https://aidalab.tistory.com/29
def get_stock_list_kor():
    print('this is get_stock_list_kor() start')
    # 종목코드는 거래소 파일에서 읽어옴. 네이버주가총액은 etf까지 존재, 거래소파일은 fullvestapi 폴더와 동일위치
    # 운영서버 코드
    stock_list_kospi_csv = pd.read_csv("kospi_list_20210911.csv", encoding='euc-kr')
    stock_list_kosdaq_csv = pd.read_csv("kosdaq_list_20210911.csv", encoding='euc-kr')
    # # 개발서버 PC 코드
    # stock_list_kospi_csv = pd.read_csv("kospi_list_20210911.csv", encoding='euc-kr')
    # stock_list_kosdaq_csv = pd.read_csv("kosdaq_list_20210911.csv", encoding='euc-kr')

    stock_list_kospi_csv = stock_list_kospi_csv.iloc[:,[1,3]]
    stock_list_kospi_csv['type'] = 0
    stock_list_kospi_csv.columns = ['stock_code','stock_name_kr','type']
    stock_list_kospi_csv = stock_list_kospi_csv[['type','stock_code','stock_name_kr']]

    # print(stock_list_kospi_csv)
    stock_list_kosdaq_csv = stock_list_kosdaq_csv.iloc[:,[1,3]]
    stock_list_kosdaq_csv['type'] = 1
    stock_list_kosdaq_csv.columns = ['stock_code','stock_name_kr','type']
    stock_list_kosdaq_csv = stock_list_kosdaq_csv[['type','stock_code','stock_name_kr']]
    # concat을 하면, 앞의 index가 중복이 될 수 있으므로, index를 새롭게 만들어주는 조건을 넣어야 함
    stock_list_kr = pd.concat([stock_list_kospi_csv,stock_list_kosdaq_csv], ignore_index=True)
    stock_list_kr.columns = ['type','stock_code','stock_name_kr']


    # 네이버에서 크롤링하는 방법 : 약간 안됨.
    # 0은 코스피 주소, 1은 코스닥 주소
    # sosoks = ['0', '1']
    # item_code_list = []
    # for sosok in sosoks:
    #     url_templ ='https://finance.naver.com/sise/sise_market_sum.nhn?sosok=%s'
    #     url = url_templ % sosok
    #     #print('this is url' + url)
    #     soup = get_page_content(url)
    #     # class 중에 맨 마지막 페이지 가는 버튼의 클래스는 pgRR
    #     td_class_pgRR = soup.find_all("td", {"class": "pgRR"})
    #     # td_class_pgRR 에 href 내에 page 파라미터 33 및 31을 끌어와야됌
    #     # print(td_class_pgRR)
    #
    #     for page_item in td_class_pgRR :
    #         # td_class_pgRR 에 a태그 내 href 속성을 가져옴
    #         href_addr = page_item.a.get('href')
    #         # re패키지 = 파이썬의 정규식 패키지임
    #         page_info = re.findall("[\d]+", href_addr)
    #         page = page_info[1]
    #         # 캐스팅 후 + 1 (루프가 1번 덜 돈다)
    #         page_loop = int(page)+1
    #     # print("this is",page_loop)
    #     #코스피는 33번 반복, 코스닥은 31번 반복 필요
    #     for i in range(1, 5, 1):
    #     # for i in range(1, page_loop, 1):
    #         sub_url = '{}&page={}'.format(url,i)
    #         # print(sub_url)
    #         page_soup = get_page_content(url)
    #         # print(page_soup)
    #         # (주의) 클래스 이름이 title -> tltle임 ..
    #         stock_item = page_soup.find_all("a",{"class":"tltle"})
    #         # print(stock_item)
    #         for item in stock_item :
    #             item_data = re.search('[\d]+',str(item))
    #             # print(item_data)
    #             if item_data:
    #                 item_code = item_data.group()
    #                 item_name = item.text
    #                 # 코스닥은 0, 코스피는 1로 지정 = sosok
    #                 result = sosok, item_code, item_name
    #                 # print(result)
    #                 item_code_list.append(result)
    # df = pd.DataFrame(item_code_list)
    # df.columns = ['type','stock_code','stock_name_kr']
    # df.to_csv("C:\\list.csv", header=True, index=False, encoding='euc-kr')
    # print(df)
    # return df
    print('this is get_stock_list_kor() end')
    return stock_list_kr


# 출처 : https://aidalab.tistory.com/29
def get_stock_summary_info_kor(stock_list_kor) :
    print("this is get_stock_summary_info_kor() start")
    stock_summary_info_dataframe = pd.DataFrame()
    stock_summary_info_dataframe_csv = pd.DataFrame()
    try:
        #네이버 상세페이지 : https://finance.naver.com/item/main.nhn?code=005930
        stock_detail_url_temp = "https://finance.naver.com/item/main.nhn?code=%s"
        for i in range(len(stock_list_kor)) :
            stock_code = stock_list_kor.loc[i,"stock_code"]
            stock_detail_url = stock_detail_url_temp % stock_code
            print(stock_detail_url)
            stock_detail_soup = get_page_content(stock_detail_url)
            # 가져올 데이터 # (1-1)저장 날짜는 항상 저장하자
            # strptime 는 객체를 -> datetime 오브젝트로 변환, strftime는 string형으로 변환
            bat_time = datetime.now()

            print("this is bat_time",bat_time)
            vesting_type_detail = stock_list_kor.loc[i,"type"]
            # print(bat_time)

            # 샘플로 [한국비엔씨] 정보부터 끌어오자 https://finance.naver.com/item/main.nhn?code=256840
            # 1) (종목시세정보) : 날짜, 종가, 거래량, 현재가, 전일가, 시가, 고가, 상한가, 저가, 하한가, 거래량, 거래대금,
            info_date = stock_detail_soup.find("span", id = "time").get_text().strip().replace(".","-")
            info_date = info_date[0:10]
            dateFormatter = "%Y-%m-%d"
            # infodate 는 정보의 기준날짜를 의미
            info_date = datetime.strptime(info_date,dateFormatter)
            stock_name_kr = stock_list_kor.loc[i,"stock_name_kr"]
            day_info_div = stock_detail_soup.find("div", class_ = "rate_info")
            #현재가 = day_info.div.p.find("span", class_ ="blind").get_text()
            stock_now = remove_comma_string(day_info_div.div.p.find("span", class_ ="blind").get_text())
            day_info_blinds = day_info_div.table.find_all("span", class_="blind")
            if len(day_info_blinds) > 0:
                stock_close = remove_comma_string(day_info_blinds[0].get_text())
            if len(day_info_blinds) > 1:
                stock_high = remove_comma_string(day_info_blinds[1].get_text())
            if len(day_info_blinds) > 3:
                stock_volume_share = remove_comma_string(day_info_blinds[3].get_text())
            if len(day_info_blinds) > 4:
                stock_open = remove_comma_string(day_info_blinds[4].get_text())
            if len(day_info_blinds) > 5:
                stock_low = remove_comma_string(day_info_blinds[5].get_text())
            if len(day_info_blinds) > 6:
                stock_volume_money = remove_comma_string(day_info_blinds[6].get_text())
            # print("this is stock_open",stock_open,stock_low,stock_volume_money)

            # 저장할때는 콤마지우기
            # 2) (투자정보)  시가총액, 시가총액 순위, 52주 최고, 52주 최저, PER, EPS,
            stock_short_info_div = stock_detail_soup.find("div", id ="tab_con1")
            if len(stock_short_info_div.find_all("table")) > 0:
                stock_short_info_table0 = stock_short_info_div.find_all("table")[0]
                stock_short_info_table0_em = stock_short_info_table0.find_all("em")
            if len(stock_short_info_table0_em) > 2:
                stock_share_total_num = remove_comma_string(stock_short_info_table0_em[2].get_text())
            stock_market_sum = int(stock_share_total_num)*int(stock_now)
            if len(stock_short_info_table0_em) > 3:
                stock_first_price = remove_comma_string(stock_short_info_table0_em[3].get_text())
            if len(stock_short_info_div.find_all("table")) > 1:
                stock_short_info_table1 = stock_short_info_div.find_all("table")[1]
                stock_short_info_table1_em = stock_short_info_table1.find_all("em")
            if len(stock_short_info_table1_em) > 0:
                stock_foreign_share_max = remove_comma_string(stock_short_info_table1_em[0].get_text())
            if len(stock_short_info_table1_em) > 1:
                stock_foreign_share_num = remove_comma_string(stock_short_info_table1_em[1].get_text())
            if len(stock_short_info_table1_em) > 2:
                stock_foreign_share_percent = remove_comma_string(stock_short_info_table1_em[2].get_text().strip().replace("%",""))

            if len(stock_short_info_div.find_all("table")) > 2 :
                stock_short_info_table2 = stock_short_info_div.find_all("table")[2]
                stock_short_info_table2_em = stock_short_info_table2.find_all("em")
                stock_maxprice_year = remove_comma_string(stock_short_info_table2_em[2].get_text())
                stock_lowprice_year = remove_comma_string(stock_short_info_table2_em[3].get_text())

            if len(stock_short_info_div.find_all("table")) > 3 :
                stock_short_info_table3 = stock_short_info_div.find_all("table")[3]
                stock_short_info_table3_em = stock_short_info_table3.find_all("em")
                stock_per = remove_comma_string(stock_short_info_table3_em[0].get_text())
                stock_eps = remove_comma_string(stock_short_info_table3_em[1].get_text())
                stock_per_guess = remove_comma_string(stock_short_info_table3_em[2].get_text())
                stock_eps_guess = remove_comma_string(stock_short_info_table3_em[3].get_text())
                stock_pbr = remove_comma_string(stock_short_info_table3_em[4].get_text())
                stock_bps = remove_comma_string(stock_short_info_table3_em[5].get_text())
                stock_allocation_ratio = remove_comma_string(stock_short_info_table3_em[6].get_text())

            if len(stock_short_info_div.find_all("table")) > 4 :
                stock_short_info_table4 = stock_short_info_div.find_all("table")[4]
                stock_short_info_table4_em = stock_short_info_table4.find_all("em")
                stock_similar_ratio = remove_comma_string(stock_short_info_table4_em[0].get_text())


            # 4) (투자자별 매매동향) 매도 상위 TOP 5 / 매수 순위 TOP 5 / 외국인 및 기관 동향 정보
            stock_content_div = stock_detail_soup.find("div", id = "content")
            stock_trend_table = stock_content_div.find("div", class_ ="section invest_trend").find_all("table")
            if len(stock_trend_table)>0 :
                # print(stock_trend_table[0])
                if len(stock_trend_table[0].select("tfoot td em")) != 0 :
                    stock_foreign_buy_today = remove_comma_string(stock_trend_table[0].select("tfoot td em")[0].get_text())
                    stock_foreign_sell_today = remove_comma_string(stock_trend_table[0].select("tfoot td em")[1].get_text())
                    stock_foreign_total_today = remove_comma_string(stock_trend_table[0].select("tfoot td em")[2].get_text())

                else :
                    stock_foreign_buy_today = 0
                    stock_foreign_sell_today = 0
                    stock_foreign_total_today = 0

                # 매도기업 TOP5

                stock_top5_agency_today = stock_trend_table[0].select("tbody .left")
                stock_top5_tvolume_today = stock_trend_table[0].select("tbody em")
            # print("this is top",stock_top5_tvolume_today)
            # 거래 정지 종목은, 거래 내역이 없기 때문에, 매도 / 외국인기관을 끌어올 수 없음
            if len(stock_top5_tvolume_today) != 0:
                for i in range (0, 10, 2) :
                    if i==0 :
                        if(len(stock_top5_agency_today)>0 and len(stock_top5_tvolume_today)>0 ) :
                            stock_agency_sell_top1 = remove_comma_string(stock_top5_agency_today[i].get_text())
                            stock_agency_sell_top1_vol = remove_comma_string(stock_top5_tvolume_today[i].get_text())
                    if i==2 :
                        if(len(stock_top5_agency_today)>2 and len(stock_top5_tvolume_today)>2 ) :
                            stock_agency_sell_top2 = remove_comma_string(stock_top5_agency_today[i].get_text())
                            stock_agency_sell_top2_vol = remove_comma_string(stock_top5_tvolume_today[i].get_text())
                    if i==4 :
                        if(len(stock_top5_agency_today)>4 and len(stock_top5_tvolume_today)>4 ) :
                            stock_agency_sell_top3 = remove_comma_string(stock_top5_agency_today[i].get_text())
                            stock_agency_sell_top3_vol = remove_comma_string(stock_top5_tvolume_today[i].get_text())
                    if i==6 :
                        if(len(stock_top5_agency_today)>6 and len(stock_top5_tvolume_today)>6 ) :
                            stock_agency_sell_top4 = remove_comma_string(stock_top5_agency_today[i].get_text())
                            stock_agency_sell_top4_vol = remove_comma_string(stock_top5_tvolume_today[i].get_text())
                    if i==8 :
                        if(len(stock_top5_agency_today)>8 and len(stock_top5_tvolume_today)>8 ) :
                            stock_agency_sell_top5 = remove_comma_string(stock_top5_agency_today[i].get_text())
                            stock_agency_sell_top5_vol = remove_comma_string(stock_top5_tvolume_today[i].get_text())

                for i in range (1, 11, 2) :
                    if i==1 :
                        if(len(stock_top5_agency_today)>1 and len(stock_top5_tvolume_today)>1 ) :
                            stock_agency_buy_top1 = remove_comma_string(stock_top5_agency_today[i].get_text())
                            stock_agency_buy_top1_vol = remove_comma_string(stock_top5_tvolume_today[i].get_text())
                    if i==3 :
                        if(len(stock_top5_agency_today)>3 and len(stock_top5_tvolume_today)>3 ) :
                            stock_agency_buy_top2 = remove_comma_string(stock_top5_agency_today[i].get_text())
                            stock_agency_buy_top2_vol = remove_comma_string(stock_top5_tvolume_today[i].get_text())
                    if i==5 :
                        if(len(stock_top5_agency_today)>5 and len(stock_top5_tvolume_today)>5 ) :
                            stock_agency_buy_top3 = remove_comma_string(stock_top5_agency_today[i].get_text())
                            stock_agency_buy_top3_vol = remove_comma_string(stock_top5_tvolume_today[i].get_text())
                    if i==7 :
                        if(len(stock_top5_agency_today)>7 and len(stock_top5_tvolume_today)>7 ) :
                            stock_agency_buy_top4 = remove_comma_string(stock_top5_agency_today[i].get_text())
                            stock_agency_buy_top4_vol = remove_comma_string(stock_top5_tvolume_today[i].get_text())
                    if i==9 :
                        if(len(stock_top5_agency_today)>9 and len(stock_top5_tvolume_today)>9 ) :
                            stock_agency_buy_top5 = remove_comma_string(stock_top5_agency_today[i].get_text())
                            stock_agency_buy_top5_vol = remove_comma_string(stock_top5_tvolume_today[i].get_text())
            else :
                print("this is no info _ 거래원 정보")


            # 외국인 기관정보 (날짜, 종가, 전일비, 외국인, 기관)
            if len(stock_trend_table) > 1:
                stock_trend_6days_em = stock_trend_table[1].find_all("em")
                # 거래 정지라도, em이 존재함.
                if len(stock_trend_6days_em) != 0:
                    for i in range (0, 6, 1) :
                        # 날짜가 기준 날짜인 데이터만 밀어넣자.
                        # if ()
                        if len(stock_trend_table[1].find_all(attrs={'scope': 'row'})) > i :
                            stock_trend_6days_datetime = stock_trend_table[1].find_all(attrs={'scope': 'row'})[i].get_text().strip().replace("/","-")
                            # print("this is 6일거래일 기준일: ", stock_trend_6days_datetime)
                            if info_date.strftime("%m-%d") == stock_trend_6days_datetime :
                                # print("this is 6거래일 정보 = 기준일")
                                stock_trading_sum_foreign = remove_comma_string(stock_trend_6days_em[i*4+2].get_text().strip())
                                stock_trading_sum_agency = remove_comma_string(stock_trend_6days_em[i*4+3].get_text().strip())
                                if stock_trading_sum_foreign == '':
                                    print("this is stock_trading_sum_foreign is blank ")
                                if stock_trading_sum_foreign == None:
                                    print("this is sum stock_trading_sum_foreign none")
                                if stock_trading_sum_agency == '':
                                    print("this is stock_trading_sum_agency is blank ")
                                if stock_trading_sum_agency == None:
                                    print("this is stock_trading_sum_agency agency None")
                                if stock_trading_sum_foreign != '' and stock_trading_sum_agency != '' :
                                    stock_trading_sum_ant = - int(stock_trading_sum_foreign) - int(stock_trading_sum_agency)


            # print("this is 전일비(상방/하방/보합)", stock_trend_6days_em[i*4+1]['class'])
            # print("this is 전일비(가격)", stock_trend_6days_em[i*4+1].get_text())
            # print("this is 기준일_외국인", stock_trading_sum_foreign)
            # print("this is 기준일_기관", stock_trading_sum_agency)
            # print("this is 기준일_개인", stock_trading_sum_ant)

            stock_summary_info = {
                                  "bat_time" : bat_time,
                                  "info_date" : info_date,
                                  "stock_code" : stock_code,
                                  "stock_country" : 1,
                                  "vesting_type" : 1,
                                  #   0은 코스닥이고, 1은 코스피
                                  "vesting_type_detail" : vesting_type_detail,
                                  "stock_name" : stock_name_kr,
                                  "stock_market_sum" : stock_market_sum,
                                  "stock_share_total_num" :stock_share_total_num,
                                  "stock_first_price" :stock_first_price,
                                  "stock_foreign_share_max" :stock_foreign_share_max,
                                  "stock_foreign_share_num" :stock_foreign_share_num,
                                  "stock_foreign_share_percent" :stock_foreign_share_percent,
                                  "stock_maxprice_year" :stock_maxprice_year,
                                  "stock_lowprice_year" :stock_lowprice_year,
                                  "stock_per" :stock_per,
                                  "stock_eps" :stock_eps,
                                  "stock_per_guess" :stock_per_guess,
                                  "stock_eps_guess" :stock_eps_guess,
                                  "stock_pbr" : stock_pbr,
                                  "stock_bps" : stock_bps,
                                  "stock_allocation_ratio" :stock_allocation_ratio,
                                  "stock_similar_per" :stock_similar_ratio,
                                  "stock_now" :stock_now,
                                  "stock_close" :stock_close,
                                  "stock_open" :"",
                                  "stock_high" :stock_high,
                                  "stock_low" :stock_low,
                                  "stock_volume_share" :stock_volume_share,
                                  "stock_volume_money" :stock_volume_money,
                                  "stock_trading_sum_foreign" : stock_trading_sum_foreign,
                                  "stock_trading_sum_agency" : stock_trading_sum_agency,
                                  "stock_trading_sum_ant" : stock_trading_sum_ant,
                                  "stock_agency_buy_top1" :stock_agency_buy_top1,
                                  "stock_agency_buy_top1_vol" :stock_agency_buy_top1_vol,
                                  "stock_agency_buy_top2" :stock_agency_buy_top2,
                                  "stock_agency_buy_top2_vol" :stock_agency_buy_top2_vol,
                                  "stock_agency_buy_top3" :stock_agency_buy_top3,
                                  "stock_agency_buy_top3_vol" :stock_agency_buy_top3_vol,
                                  "stock_agency_buy_top4" :stock_agency_buy_top4,
                                  "stock_agency_buy_top4_vol" :stock_agency_buy_top4_vol,
                                  "stock_agency_buy_top5" :stock_agency_buy_top5,
                                  "stock_agency_buy_top5_vol" :stock_agency_buy_top5_vol,
                                  "stock_agency_sell_top1" :stock_agency_sell_top1,
                                  "stock_agency_sell_top1_vol" :stock_agency_sell_top1_vol,
                                  "stock_agency_sell_top2" :stock_agency_sell_top2,
                                  "stock_agency_sell_top2_vol" :stock_agency_sell_top2_vol,
                                  "stock_agency_sell_top3" :stock_agency_sell_top3,
                                  "stock_agency_sell_top3_vol" :stock_agency_sell_top3_vol,
                                  "stock_agency_sell_top4" :stock_agency_sell_top4,
                                  "stock_agency_sell_top4_vol" :stock_agency_sell_top4_vol,
                                  "stock_agency_sell_top5" :stock_agency_sell_top5,
                                  "stock_agency_sell_top5_vol" :stock_agency_sell_top5_vol,
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
            stock_summary_info_dataframe = stock_summary_info_dataframe.append(stock_summary_info, ignore_index=True)
            print("this is summary_info_list len:",len(stock_summary_info_dataframe))
            # 100 개씩 잘라서 넣어주고, dataframe을 초기화 시켜줘야됨
            stock_summary_info_dataframe_csv = stock_summary_info_dataframe_csv.append(stock_summary_info, ignore_index=True)
            print("this is stock_summary_info_dataframe_csv len:",len(stock_summary_info_dataframe_csv))
            if len(stock_summary_info_dataframe) == 100 :
                insert_info_into_db(stock_summary_info_dataframe)
                stock_summary_info_dataframe = stock_summary_info_dataframe.iloc[0:0]

            # 파일명 중복 안되도록 처리 방법
            # filename = 'stock_info'
            # file_ext = '.csv'
            # output_path = 'C:/%s%s' % (filename,file_ext)
            # uniq =1
            # while (os.path.exists(output_path)) :
            #     output_path = 'C:/%s(%d)%s' % (filename,uniq,file_ext)
            #     uniq += 1

            # # print("this is stock_info:",stock_info)
            # stock_summary_info_list_dataframe = pd.DataFrame(stock_summary_info_dataframe)
            # stock_summary_info_list_dataframe.to_csv("C:\\test3.csv", header=True, index=False, encoding='euc-kr')

    except IndexError as e:
        print("this is IndexError:",e.string)
        pass

    except AttributeError as e:
        print("this is AttributeError:", e.string)
        pass

    except TypeError as e :
        print("this is TypeError:", e.string)
        pass

        # 배당성향은 4개밖에없음
        #   배치시간, 기준날짜, stockcode, 주식종목명

        # 6) (테마주 분류) 동일업종명 분류
    print("this is stock_summary_info_dataframe")

    # 100개씩 넣은 후 나머지 데이터가 있으면 넣어주기
    if len(stock_summary_info_dataframe)!=0 :
       insert_info_into_db(stock_summary_info_dataframe)
    # csv파일로 저장하기
    filename = 'backup_stocksummary' + bat_time.strftime("%Y%m%d")
    uniq = 1
    output_path = 'backup_stocksummary/%s(%d).csv' % (filename,uniq)
    while (os.path.exists(output_path)) :
        output_path = 'backup_stocksummary/%s(%d)%s' % (filename,uniq)
        uniq += 1
    print("this is output_path", output_path)
    stock_summary_info_dataframe_csv.to_csv(output_path, header=True, index=False, encoding='euc-kr')
    
    print("this is get_stock_summary_info_kor() end")

# def get_stock_ifrs_info_kor()
 # 5) (기업 실적 분석) 매출액 / 영업이익 / 당기순이익 / 영업이익률/ 순이익률 / ROE / 부채비율 / 유보율 / EPS / PER / BPS / PBR / 주당배당금(원) / 시가배당률 / 배당성향
 #            stock_ifrs_table = stock_content_div.find("table", class_ ="tb_type1 tb_num tb_type1_ifrs")
 #            # print(stock_ifrs_table)
 #            # 앞의 4개는 년도별 데이터, 뒤의 6개 데이터는 분기별데이터
 #            stock_ifrs_date_list = stock_ifrs_table.thead.find_all("tr")[1].find_all("th")
 #            stock_ifrs_trows = stock_ifrs_table.select("tbody tr")
 #            stock_ifrs_revenue_list = stock_ifrs_trows[0].find_all("td")
 #            stock_ifrs_operatingprofit_list = stock_ifrs_trows[1].find_all("td")
 #            stock_ifrs_netincome_list = stock_ifrs_trows[2].find_all("td")
 #            stock_ifrs_operatingmargin_list = stock_ifrs_trows[3].find_all("td")
 #            stock_ifrs_netprofitmargin_list = stock_ifrs_trows[4].find_all("td")
 #            stock_ifrs_roe_list = stock_ifrs_trows[5].find_all("td")
 #            stock_ifrs_debtratio_list = stock_ifrs_trows[6].find_all("td")
 #            stock_ifrs_quickrate_list = stock_ifrs_trows[7].find_all("td")
 #            stock_ifrs_reserveratio_list = stock_ifrs_trows[8].find_all("td")
 #            stock_ifrs_eps_list = stock_ifrs_trows[9].find_all("td")
 #            stock_ifrs_per_list = stock_ifrs_trows[10].find_all("td")
 #            stock_ifrs_bps_list = stock_ifrs_trows[11].find_all("td")
 #            stock_ifrs_pbr_list = stock_ifrs_trows[12].find_all("td")
 #
 #            stock_ifrs_data = [];
 #            for i in range (0, 10, 1) :
 #                print("this is 날짜", stock_ifrs_date_list[i].get_text())
 #                print("this is 매출액", remove_comma_string(stock_ifrs_revenue_list[i].get_text()))
 #                print("this is 영업이익", remove_comma_string(stock_ifrs_operatingprofit_list[i].get_text()))
 #                print("this is 당기순이익", remove_comma_string(stock_ifrs_netincome_list[i].get_text()))
 #                print("this is 영업이익률", remove_comma_string(stock_ifrs_operatingmargin_list[i].get_text()))
 #                print("this is 순이익률", remove_comma_string(stock_ifrs_netprofitmargin_list[i].get_text()))
 #                print("this is ROE", remove_comma_string(stock_ifrs_roe_list[i].get_text()))
 #                print("this is 부채비율", remove_comma_string(stock_ifrs_debtratio_list[i].get_text()))
 #                print("this is 당좌비율", remove_comma_string(stock_ifrs_reserveratio_list[i].get_text()))
 #                print("this is 유보율", remove_comma_string(stock_ifrs_reserveratio_list[i].get_text()))
 #                print("this is EPS", remove_comma_string(stock_ifrs_eps_list[i].get_text()))
 #                print("this is PER", remove_comma_string(stock_ifrs_per_list[i].get_text()))
 #                print("this is BPS", remove_comma_string(stock_ifrs_bps_list[i].get_text()))
 #                print("this is PBR", remove_comma_string(stock_ifrs_pbr_list[i].get_text()))
            #
def check_exist_db() :
    return 0

def insert_info_into_db(stock_summary_info_dataframe) :
    try:
        # DB sqlite 위치 구하기
        # stock_summary_info_dataframe
        # pandas 형식의 데이터 타입 -> 날짜 컬럼의 데이터타입을 바꿔주고 -> list로 변환
        print("this is stock_summary_info_dataframe len",len(stock_summary_info_dataframe))
        stock_summary_info_dataframe['bat_time'] = stock_summary_info_dataframe['bat_time'].apply(str)
        # 데이터프레임 안의 datetime 타입 -> date 타입으로 변경
        stock_summary_info_dataframe['info_date']=stock_summary_info_dataframe['info_date'].dt.date
        stock_summary_info_dataframe['info_date'] = stock_summary_info_dataframe['info_date'].apply(str)
        # stock_summary_info['info_date'].dt.date
        # print("this is bat_time",stock_summary_info['bat_time'])
        # stock_summary_info['info_date'] = stock_summary_info['info_date']
        # stock_summary_info_sample = stock_summary_info_sample['info_date'].apply(str)
        stock_summary_info_tolist = stock_summary_info_dataframe.values.tolist()

        # print("this is tolist()",stock_summary_info_tolist)
        print("this is stock_summary_info_tolist's length:",len(stock_summary_info_tolist))
        # 운영서버용 코드
        sqliteconnection = sqlite3.connect("/home/fullvesting/TheaterWin/db.sqlite3")
        # 개발로컬PC용 코드
        # sqliteconnection = sqlite3.connect("C:\\Users\\jjune\\djangogirls\\TheaterWin\\db.sqlite3")
        print("this is connection")
        cursor = sqliteconnection.cursor()
        # sql = 'SET SESSION max_allowed_packet=100M'
        # cursor.execute(sql)
        # stock_summary_info_sample.to_sql('TheaterWinBook_StockSummaryKr',con=sqliteconnection,if_exists='append',index=False,method='multi')

        # cursor.executemany("INSERT INTO TheaterWinBook_StockSummaryKr("
        #                    "bat_time, info_date, stock_code, stock_country, vesting_type, vesting_type_detail, stock_name"
        #                    ") VALUES"
        #                    "(?,?,?,?,?,?,?) ",stock_summary_info_sample_tolist)

        # executemany 실행 도중 error가 나면, 모두 rollback 이라 삽입이 1개도 되지 않음.
        cursor.executemany("INSERT OR REPLACE INTO TheaterWinBook_StockSummaryKr("
                           "bat_time, info_date, stock_code, stock_country, vesting_type, vesting_type_detail, stock_name,stock_market_sum,stock_share_total_num,stock_first_price,"
                           "stock_foreign_share_max,stock_foreign_share_num,stock_foreign_share_percent,"
                           "stock_maxprice_year,stock_lowprice_year,stock_per,stock_eps,stock_per_guess,"
                           "stock_eps_guess,stock_pbr,stock_bps,stock_allocation_ratio,stock_similar_per,stock_now,"
                           "stock_close, stock_open,stock_high,stock_low,stock_volume_share,stock_volume_money,"
                           "stock_trading_sum_foreign,stock_trading_sum_agency,stock_trading_sum_ant,"
                           "stock_agency_buy_top1,stock_agency_buy_top1_vol,stock_agency_buy_top2,stock_agency_buy_top2_vol,stock_agency_buy_top3,"
                           "stock_agency_buy_top3_vol,stock_agency_buy_top4,stock_agency_buy_top4_vol,stock_agency_buy_top5,stock_agency_buy_top5_vol,"
                           "stock_agency_sell_top1,stock_agency_sell_top1_vol,stock_agency_sell_top2,"
                           "stock_agency_sell_top2_vol,stock_agency_sell_top3,"
                           "stock_agency_sell_top3_vol,stock_agency_sell_top4,"
                           "stock_agency_sell_top4_vol,stock_agency_sell_top5,"
                           "stock_agency_sell_top5_vol, etc1_string, etc2_string, etc3_string,"
                           "etc4_string, etc5_string, etc1_int, etc2_int,etc3_int, etc4_int, etc5_int"
                           ") VALUES"
                           "(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,"
                           "?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,"
                           "?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,"
                           "?,?,?) ", stock_summary_info_tolist)
        # 데이터 프레임의 to_sql함수 : if_exists는 테이블이 존재하면 추가하겠다는 의미.
        # stock_summary_info_dataframe.to_sql('TheaterWinBook_StockSummaryKer3', con = sqliteconnection, if_exists='append', index=False)

        sqliteconnection.commit()

    except sqlite3.Error as error:
        print("Error while connecting to sqlite",error)
        pass

    finally:
        if sqliteconnection :
            sqliteconnection.close()
            print("The Sqlite connection is closed")

def remove_comma_string(integer_withcomma):
    integer_withcomma = integer_withcomma.replace(",","").strip()
    # print("this is integer_withcomma",integer_withcomma)
    return integer_withcomma

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    stockcode_url = "https://finance.naver.com/sise/sise_market_sum.nhn?&page="
    # print('오늘 네이버주가 끌어왓습니다!!! 네이버 주가는 : '+get_price("005930"))
    stock_list_kor = get_stock_list_kor()


    # item_code_list =[]
    # result1 = (0, "035720", "카카오")
    # item_code_list.append(result1)
    # result2 = (0, "005930", "삼성전자")
    # item_code_list.append(result2)
    # stock_list_kor_sample = pd.DataFrame(item_code_list)
    # stock_list_kor_sample.columns = ['type', 'stock_code', 'stock_name_kr']

    get_stock_summary_info_kor(stock_list_kor)
    # get_stock_ifrs_info_kor(stock_list_kor)
    # insert_info_into_db()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
