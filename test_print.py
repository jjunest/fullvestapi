import requests
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt


url= 'https://finance.naver.com/item/sise_day.nhn?code=005930'
user_agent= 'Mozilla/5.0'
headers = {'User-Agent':user_agent, 'Referer':None}
request=requests.get(url)
BeautifulSoup= BeautifulSoup(request.text, 'html.parser')
last=BeautifulSoup.find('td',class_='on')
df=pd.read_html(requests.get(url, headers={'User-Agent':user_agent}).text)[0]


print(df)

for i in range(1, 647):
    url='{}&page={}'.format(url, i)
    df=df.append(pd.read_html(requests.get(url, headers={'User-Agent':user_agent}).text)[0])

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['font.size'] = 15
plt.rcParams['figure.figsize'] = (10, 5)
plt.rcParams['axes.unicode_minus'] = False
df['종가'].plot(color = 'red')
plt.grid()
plt.xlabel("날짜(거래일)")
plt.ylabel("종가")
plt.title("삼성전자 주식가격")
plt.legend()
plt.show()