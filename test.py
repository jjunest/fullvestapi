# 네이버 일별 시세에서 모든 페이지 정보 가져오기

import requests
import pandas as pd
from bs4 import BeautifulSoup


if __name__ == '__main__':
    # 네이버 금융
    code = '005930'
    url = 'https://finance.naver.com/item/sise_day.nhn?code={code}'

    # 1. 수집준비
    # 1) user-agent 준비
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' \
                 + 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.62'
    headers = {'User-Agent': user_agent, 'Referer': None}  # 웹브라우저 접속처럼 인식시키기 위해 정보 추가

    # 서버 주소에 종목 코드를 추가하여 get 양식을 완성하고 요청한다
    r = requests.get(url, headers=headers)
    print(r.text)

    # BeautifulSoup으로 추출한 내용을 정리한다
    bs = BeautifulSoup(r.text, 'html.parser')

    # 마지막 페이지 번호 찾기
    # 마지막페이지의 url은 on이라는 클래스의 td 태그내에 ㅇ정의되어있는 것을 확인
    last_page = bs.find('td', class_='on')
    print(type(last_page))

    max_page = 646

    # 일별 시세 추출하기
    page_url = '{}&page={}'.format(url, 1)
    print(page_url)
    df = pd.read_html(requests.get(page_url, headers={'User-Agent': user_agent}).text)[0]

    print(df)

    # 원하는 페이지 수만큼 반복
    for page in range(1, max_page + 1):
        page_url = '{}&page={}'.format(url, page)
        df = df.append(pd.read_html(requests.get(page_url, headers={'User-Agent': user_agent}).text)[0])

    # 추출한 시세의 컬럼명을 수정, 데이터 타입 변경, 컬럼 순서 조정
