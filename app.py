import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup as bs
import yfinance as yf
import streamlit as st
url = "https://chartink.com/screener/process"

condition_friday = {"scan_clause": "( {cash} ( weekly close >= 30 and latest sma( latest close , 10 ) >= latest sma( latest close , 30 ) and latest sma( latest volume , 5 ) >= 10000 and market cap > 0 and weekly sma( weekly close , 40 ) <= latest close and latest \"\close - 1 candle ago close / 1 candle ago close * 100\"\ >= -4 ) )"}
condition_consolidating = {"scan_clause": "( {cash} ( weekly close >= 30 and latest sma( latest close , 10 ) >= latest sma( latest close , 30 ) and latest sma( latest volume , 5 ) >= 10000 and market cap > 0 and weekly sma( weekly close , 40 ) <= latest close and latest \"\close - 1 candle ago close / 1 candle ago close * 100\"\ >= -4 and( {cash} ( ( abs( latest close - latest sma( latest close , 9 ) ) / latest sma( latest close , 9 ) ) <= .02 or( abs( latest close - latest sma( latest close , 20 ) ) / latest sma( latest close , 20 ) ) <= .02 ) ) ) ) "}

condition = condition_friday

                              
def getChartinkSymbols(condition):
    with requests.session() as s:
        r_data = s.get(url)
        soup = bs(r_data.content, "lxml")
        meta = soup.find("meta", {"name" : "csrf-token"})["content"]

        header = {"x-csrf-token" : meta}
        data = s.post(url, headers=header, data=condition).json()

        query_stock_list = pd.DataFrame(data["data"])
        return query_stock_list
                                    
friday_scan_list = getChartinkSymbols(condition_friday)

friday_stock_nse_codes = friday_scan_list['nsecode'].to_list()
stocks_nse_symbol = [symbol+'.NS' for symbol in friday_stock_nse_codes]
st.write(f'Chartink Stocks Weekly Scan on Friday {len(friday_stock_nse_codes)}')
st.write(friday_scan_list)



friday_scan_list_2pct = getChartinkSymbols(condition_consolidating)
friday_stock_nse_codes_2pct = friday_scan_list['nsecode'].to_list()
stocks_nse_symbol_2pct = [symbol+'.NS' for symbol in friday_stock_nse_codes]
st.write(f'Chartink Stocks Weekly Scan on Friday {len(friday_scan_list_2pct)}')
st.write(friday_scan_list_2pct)


# Get Clicked Item 
# Get the clicked element
clicked_element = st.session_state.clicked_element

# If an element was clicked
if clicked_element is not None:

    # Get the row and column of the clicked element
    row, column = clicked_element

    # Get the value of the cell at the clicked row and column
    value = friday_scan_list_2pct.iloc[row, column]

    # Display the value
    st.write("The value of the cell at row {} and column {} is {}".format(row, column, value))



from datetime import date ,timedelta
today = date.today()+timedelta(days=1)
start_date = today-timedelta(days=180)
                                    
stock_list = stocks_nse_symbol
filtered_stocks_purple_dots =[]
filtered_darvax =[]
                                    
                                    
