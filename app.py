import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup as bs
import yfinance as yf

url = "https://chartink.com/screener/process"

condition_friday = {"scan_clause": "( {cash} ( weekly close >= 30 and latest sma( latest close , 10 ) >= latest sma( latest close , 30 ) and latest sma( latest volume , 5 ) >= 10000 and market cap > 0 and weekly sma( weekly close , 40 ) <= latest close and latest \"\close - 1 candle ago close / 1 candle ago close * 100\"\ >= -4 ) )"}
condition_consolidating = {"scan_clause": "( {cash} ( weekly close >= 30 and latest sma( latest close , 10 ) >= latest sma( latest close , 30 ) and latest sma( latest volume , 5 ) >= 10000 and market cap > 0 and weekly sma( weekly close , 40 ) <= latest close and latest \"\close - 1 candle ago close / 1 candle ago close * 100\"\ >= -4 and( {cash} ( ( abs( latest close - latest sma( latest close , 9 ) ) / latest sma( latest close , 9 ) ) <= .02 or( abs( latest close - latest sma( latest close , 20 ) ) / latest sma( latest close , 20 ) ) <= .02 ) ) ) ) "}

condition = condition_friday

with requests.session() as s:
    r_data = s.get(url)
    soup = bs(r_data.content, "lxml")
    meta = soup.find("meta", {"name" : "csrf-token"})["content"]

    header = {"x-csrf-token" : meta}
    data = s.post(url, headers=header, data=condition).json()

    query_stock_list = pd.DataFrame(data["data"]
                                    
                                    
                                    
                                    
stock_nse_codes = query_stock_list['nsecode'].to_list()
stocks_nse_symbol = [symbol+'.NS' for symbol in stock_nse_codes]
st.write(stocks_nse_symbol)
                                    
from datetime import date ,timedelta
today = date.today()+timedelta(days=1)
start_date = today-timedelta(days=180)
                                    
stock_list = stocks_nse_symbol
filtered_stocks_purple_dots =[]
filtered_darvax =[]
                                    
                                    
