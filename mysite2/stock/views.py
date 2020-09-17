from django.shortcuts import render
from django.shortcuts import render
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pymysql

def get_data(symbol):
    url = 'http://finance.naver.com/item/sise.nhn?code={}'.format(symbol)
    with urlopen(url) as doc:
        soup = BeautifulSoup(doc, "lxml", from_encoding="euc-kr")
        cur_price = soup.find('strong', id='_nowVal')  # ①
        cur_rate = soup.find('strong', id='_rate')  # ②
        stock = soup.find('title')  # ③
        stock_name = stock.text.split(':')[0].strip()  # ④
        return cur_price.text, cur_rate.text.strip(), stock_name


def get_db(symbol, date_):
    try:
        conn = pymysql.connect(host='15.164.163.118', user='ai', passwd='yonsei!', db='stock')
        cur  = conn.cursor()
    except Exception as e:
        print (e)
        return -1

    cur.execute("SELECT st_close FROM stock_day_table WHERE st_id = 'A{}' AND st_day = '{}';".format(symbol, date_))
    rt = cur.fetchall()
    return rt[0][0]

# http://127.0.0.1:8000/stock/?011930=100&011930=20200803
def main_view(request):
    querydict = request.GET.copy()
    mylist = querydict.lists()  # ⑤

    rows = []
    total = 0
    # ('011930', ['100', '20200816'])
    for x in mylist:
        print (x)
        # 2,215 -3.49% 신성이엔지
        cur_price, cur_rate, stock_name = get_data(x[0])  # ⑥
        buy_price = int(get_db(x[0], x[1][1]))
        print(buy_price)
        price = int(cur_price.replace(',', ''))
        stock_count = format(int(x[1][0]), ',')  # ⑦

        sum = (price - buy_price) * int(x[1][0])
        print (sum)
        print (type(sum))
        stock_sum = format(sum, ',')
        # 매수한 날짜
        cur_rate = ((price * int(x[1][0])) / (buy_price * int(x[1][0])) - 1) * 100
        cur_rate = round(cur_rate, 2)
        rows.append([stock_name, x[1][1], cur_price, stock_count, cur_rate,
            stock_sum])  # ⑧
        total = total + int(price) * int(x[1][0])  # ⑨

    total_amount = format(total, ',')
    values = {'rows' : rows, 'total' : total_amount}  # ⑩
    return render(request, 'index.html', values)  # ⑪

# Create your views here.
