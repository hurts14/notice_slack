### web scraping 
import gspread
import requests
import datetime
from bs4 import BeautifulSoup
from oauth2client.service_account import ServiceAccountCredentials

#2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
SCOPE = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
#認証情報設定
#ダウンロードしたjsonファイル名をクレデンシャル変数に設定（秘密鍵、Pythonファイルから読み込みしやすい位置に置く）
CREDENTIALS = ServiceAccountCredentials.from_json_keyfile_name('receive-vix-c7b393541993.json', SCOPE)

NOW = datetime.datetime.now().strftime("%Y-%m-%d")

def get_google_spread(date):
    #OAuth2の資格情報を使用してGoogle APIにログインします。
    gc = gspread.authorize(CREDENTIALS)

    #共有設定したスプレッドシートキーを変数[SPREADSHEET_KEY]に格納する。
    SPREADSHEET_KEY = '14kv6zXOJUoGJev7UzRekhKO0wuvLQR6vlsS0n9x42m4'

    #共有設定したスプレッドシートのシート1を開く
    worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1

    #A1セルの値を受け取る
    import_value = int(worksheet.acell('A1').value)

    #A1セルの値に100加算した値をB1セルに表示させる
    export_value = import_value+100
    worksheet.update_cell(1,2, export_value)
    #dateのvixとnikkeiの値を受け取る
    vix = ''
    nikkei = ''

    return vix, nikkei

def set_vix(vix, nikkei):

    gc = gspread.authorize(CREDENTIALS)
    SPREADSHEET_KEY = '14kv6zXOJUoGJev7UzRekhKO0wuvLQR6vlsS0n9x42m4'
    worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1
    
    #A1セルの値を受け取る
    import_value = int(worksheet.acell('A1').value)

    #A1セルの値に100加算した値をB1セルに表示させる
    export_value = import_value+100
    worksheet.update_cell(1,2, export_value)
    #dateセルにvixとnikkeiのを表示させる



def request_nikkei():
    nikkei_url = 'https://indexes.nikkei.co.jp/nkave/historical/nikkei_stock_average_daily_jp.csv'
    r = requests.get(nikkei_url)
    print('nikkei')
    return r

def request_vix():
    vix_url = 'https://indexes.nikkei.co.jp/nkave/historical/nikkei_stock_average_vi_daily_jp.csv'
    r = requests.get(vix_url)
    print('vix')
    return r

def main():
    print('hello')

if __name__ == "__main__":
    main()