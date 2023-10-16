import streamlit as st
import pandas as pd
import yfinance as yf
import datetime
from datetime import date
import altair as alt

header = st.container()
user_list = st.container()
portfolio_chart = st.container()


with header:
    st.title('Portfolio Value Chart')
    st.write('Enter the stock (ticker symbols) and number of shares in the section below to generate a chart of portfolio value as a function of stock value over time.')

with user_list:
    st.header('Use the input form to add stocks to your portfolio.')
    df = pd.DataFrame(
        [
            {"Ticker": "TSLA", "Number of Shares": 1.000, "Price": 1.00}
        ]
    )
    edited_df = st.data_editor(df, num_rows="dynamic")
    
with portfolio_chart:
    st.write("Here you go...")
    for i in range(0, len(edited_df)):
        stock = yf.Ticker(edited_df.loc[i].at["Ticker"])
        st.write(stock.info['currentPrice'])
        st.write(edited_df.loc[i].at["Price"])
        edited_df.loc[i].at["Price"] = stock.info['currentPrice']

    st.write("After YF...")
    st.write(edited_df)













st.title('Stock Portfolio Visualizer')
st.sidebar.info('Welcome to the Stock Portfolio Visualizer App. Update your portfolio using the options below.')

def main():
    single_ticker_chart()

@st.cache_resource
def download_data(option, start_date, end_date):
    df = yf.download(option, start=start_date, end=end_date, progress=False)
    return df



def add_stock_ticker(stocks, ticker):
    st.sidebar.write("Start")
    st.sidebar.write(stocks)
    st.sidebar.write(ticker)
    st.sidebar.write("End")
    stocks.append(ticker)  # Add the ticker to the list
    st.sidebar.write('Stocks in List')
    st.sidebar.write(stocks)
    return stocks


#sideboard
stocks = []
st.sidebar.write('Stocks in List')
st.sidebar.write(stocks)
ticker = st.sidebar.text_input('Enter a Stock Symbol to Add', value='TSLA')
if st.sidebar.button('Add Ticker'):
    stocks = add_stock_ticker(stocks, ticker)

option = st.sidebar.text_input('Enter a Stock Symbol', value='TSLA')
option = option.upper()
today = datetime.date.today()
duration = st.sidebar.number_input('Days to chart', value=90)
end_date = today
start_date = today - datetime.timedelta(days=duration)
data = download_data(option, start_date, end_date)

def single_ticker_chart():
    st.header('Single Ticker Chart')
    st.write(option)
    st.write(data.Close[-1])
    st.line_chart(data.Close)   
    alt.Chart(options).mark_bar().encode(
        x='Date',
        y='sum(close)',
        color='site'
    )

if __name__ == '__main__':
    main()
