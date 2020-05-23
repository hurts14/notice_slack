### web scraping 
import gspread
import requests
import datetime
import pandas as pd
import numpy as np
import io
from bs4 import BeautifulSoup
from oauth2client.service_account import ServiceAccountCredentials

#2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
SCOPE = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
#認証情報設定
#ダウンロードしたjsonファイル名をクレデンシャル変数に設定（秘密鍵、Pythonファイルから読み込みしやすい位置に置く）
json_path = 'receive-vix-c7b393541993.json'
CREDENTIALS = ServiceAccountCredentials.from_json_keyfile_name(json_path, SCOPE)

NOW = datetime.datetime.now().strftime('%Y/%m/%d')


def get_google_spread(date):
    #OAuth2の資格情報を使用してGoogle APIにログインします。
    gc = gspread.authorize(CREDENTIALS)

    #共有設定したスプレッドシートキーを変数[SPREADSHEET_KEY]に格納する。
    SPREADSHEET_KEY = '14kv6zXOJUoGJev7UzRekhKO0wuvLQR6vlsS0n9x42m4'

    #共有設定したスプレッドシートのシートopen_225viを開く
    worksheet = gc.open_by_key(SPREADSHEET_KEY).worksheet('open_225vi')
    #import_value = int(worksheet.acell('A1').value)
    #dateの行の値を受け取る
    #指定した文字列を検索してマッチした全てのセルを取得 
    cell = worksheet.find(str(date))
    value_list = worksheet.row_values(cell.row)

    #dateのvixとnikkeiの値を受け取る
    vix = float(value_list[2])
    nikkei = float(value_list[1])

    return vix, nikkei


def set_vix(vix, nikkei):

    gc = gspread.authorize(CREDENTIALS)
    SPREADSHEET_KEY = '14kv6zXOJUoGJev7UzRekhKO0wuvLQR6vlsS0n9x42m4'
    worksheet = gc.open_by_key(SPREADSHEET_KEY).worksheet('open_225vi')
    
    #行数を取得=最終行
    #all_len = len(worksheet.get_all_values())
    update_list = [NOW, nikkei, vix]

    #spreadの一番最後の行にdateとvixとnikkeiの値を表示させる
    worksheet.append_row(update_list)
    #worksheet.update_cell(1,2, export_value)


def request_nikkei():
    #Nikkei_OHLCを取得
    nikkei_url = 'https://indexes.nikkei.co.jp/nkave/historical/nikkei_stock_average_daily_jp.csv'
    r = requests.get(nikkei_url).content
    print('nikkei')
    df = pd.read_csv(io.StringIO(r.decode('shift-jis')), header=0, skipfooter=1, engine='python')
    col = ['Date', 'Close', 'Open', 'High', 'Low']
    df.columns = col
    df['Date'] = pd.to_datetime(df['Date'])
    return df


def request_vix():
    #VIX_OHLCを取得
    vix_url = 'https://indexes.nikkei.co.jp/nkave/historical/nikkei_stock_average_vi_daily_jp.csv'
    r = requests.get(vix_url).content
    df = pd.read_csv(io.StringIO(r.decode('shift-jis')), header=0, skipfooter=1, engine='python')
    col = ['Date', 'Close', 'Open', 'High', 'Low']
    df.columns = col
    df['Date'] = pd.to_datetime(df['Date'])
    return df


def main():
    print('hello')
    #set_vix(5,10)
    #v, n = get_google_spread(NOW)
    #print('{},{}'.format(v,n))
    #request_vix()
    

if __name__ == "__main__":
    main()