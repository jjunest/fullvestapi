import sqlite3
import django



if __name__ == '__main__':
    print("this is apiDBtest")
    testtext = 'testtext'
    conn = sqlite3.connect('C:\\Users\\jjune\\djangogirls\\TheaterWin\\db.sqlite3')
    cur = conn.cursor()
    query = "INSERT INTO TheaterWinBook_FullvestingApi (fullvesting_text) VALUES (?)"
    cur.execute(query, (testtext,))
    conn.commit()
    cur.close()
    conn.close()
    # get_stock_ifrs_info_kor(stock_list_kor)
    # insert_info_into_db()
