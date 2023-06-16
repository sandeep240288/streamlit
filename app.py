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




    # Get Clicked Item 
    # Get the clicked element
    # Create a function to load data from Yahoo Finance
def load_data(symbol):
    data = yf.Ticker(symbol).history(period="180d")
    return data

    # Create a button to load data from Yahoo Finance
    load_data_button = st.button("Load Data")

    # If the button is clicked
    if load_data_button:
        # Get the symbol from the user
        symbol = st.selectbox("Select a symbol:", friday_scan_list_2pct["nsecode"])
        # Load the data from Yahoo Finance
        data = load_data(symbol)
        # Display the data
        st.dataframe(data)

# from datetime import date ,timedelta
# today = date.today()+timedelta(days=1)
# start_date = today-timedelta(days=180)
                                    
# stock_list = stocks_nse_symbol
# filtered_stocks_purple_dots =[]
# filtered_darvax =[]
                                    
                                    
tabs = st.tabs(["Weekly Scan Full List", "Within 2pct of SMA10", "Tab 3"])

# Add content to each tab
with tabs[0]:
  st.header("Weekly Scan on Friday: Full List")
  friday_scan_list = getChartinkSymbols(condition_friday)
  friday_stock_nse_codes = friday_scan_list['nsecode'].to_list()
  stocks_nse_symbol = [symbol+'.NS' for symbol in friday_stock_nse_codes]
  st.write(f'Chartink Stocks Weekly Scan on Friday {len(friday_stock_nse_codes)}')
  st.dataframe(friday_scan_list)


with tabs[1]:
  st.header("Within 2pct of 10SMA Friday scan")
  friday_scan_list_2pct = getChartinkSymbols(condition_consolidating)
  friday_scan_list_2pct["nsecode"] = friday_scan_list_2pct["nsecode"]+'.NS'
  friday_stock_nse_codes_2pct = friday_scan_list['nsecode'].to_list()
  stocks_nse_symbol_2pct = [symbol+'.NS' for symbol in friday_stock_nse_codes]
  st.write(f'Chartink Stocks Weekly Scan on Friday {len(friday_scan_list_2pct)}')
  st.dataframe(friday_scan_list_2pct)



with tabs[2]:
  st.header("Tab 3")
  st.write("This is the content for Tab 3.")



from datetime import date ,timedelta
today = date.today()+timedelta(days=1)
start_date = today-timedelta(days=180)



import multiprocessing as mp
def get_stock_history(symbol):
  """Gets the stock history for the given symbol."""
  ticker = yf.Ticker(symbol)
  if ticker:
    stock_history = ticker.history(start=start_date, end=today, interval="1d")
    stock_history["return"] = stock_history["Close"].pct_change() * 100
    stock_history["is_1M"] = stock_history["Volume"] >= 1000000
    stock_history["gt_5pct"] = stock_history["return"] >= 5
    stock_history["match"] = stock_history["is_1M"] & stock_history["gt_5pct"]
    total = stock_history["match"].sum()
    stock_history["total"] = total
    stock_history["sma10"] = stock_history["Close"].rolling(10).mean()
    stock_history["sma10_distance"] =abs((stock_history["sma10"]/stock_history["Close"])-1)*100
    zerodha_symbol = symbol.split(".", 1)[0]
    return stock_history, total, zerodha_symbol
  else:
    return None, None, None



def main(stock_list):
  """The main function."""
  # Create a pool of workers.
  pool = mp.Pool()
  # Get the stock histories for all of the symbols.
  results = pool.map(get_stock_history, stock_list)

  # Filter the results.
  filtered_stocks_purple_dots = []
  stocks_at_10_ma = []
  stock_match_dates = {}
  for result in results:
    if result is not None and  result[1] >= 2:
        if result[0].iloc[-1]['sma10_distance']<=2:
          stocks_at_10_ma.append(result[2])

        filtered_stocks_purple_dots.append({
            "symbol": result[2],
            "total": result[1]
        })

        index_values = result[result['match'] == True].index
        stock_match_dates[result[2]] = index_values


  # Print the filtered results.
  return filtered_stocks_purple_dots,stocks_at_10_ma,stock_match_dates

stock_list = stocks_nse_symbol_2pct
filtered_stocks_purple_dots,stocks_at_10_ma, stock_match_dates = main(stock_list)

st.table(filtered_stocks_purple_dots)
st.table(stock_match_dates)
