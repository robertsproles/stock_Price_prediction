import streamlit as st
import pandas as pd
import yfinance as yf
import datetime
from datetime import date
import altair as alt
import matplotlib.pyplot as plt


header = st.container()
user_sidebar = st.sidebar.container()
portfolio_chart = st.container()
df = pd.read_csv("portfolio.csv")

def build_historic_prices(Ticker,NumShares):
    st.write('')

with user_sidebar:
    st.header('Use the form to add stocks to your portfolio.')
    edited_df = st.data_editor(df, num_rows="dynamic")
    if st.button('Refresh'):
        edited_df.to_csv('portfolio.csv', index=False)
        st.rerun()
    else:
        st.write('')
    st.write('')
    today = datetime.date.today()
    days_to_plot = st.sidebar.number_input('Days to chart', value=90)
    end_date = today
    start_date = today - datetime.timedelta(days=days_to_plot)
    
for i in range(0, len(df)):
    stock = yf.Ticker(df.loc[i,"Ticker"])
#    stock.info
    df.loc[i,"Price"] = stock.info['previousClose']
    df.loc[i,"Value"] = df.loc[i,"NumShares"] * df.loc[i,"Price"]
    df.to_csv('portfolio.csv', index=False)

with header:
    st.title('Portfolio Value Chart')
    st.write('Enter the stock (ticker symbols) and number of shares in the sidebar to update the portfolio.')
#    st.write(df[['Ticker','NumShares']])
    
with portfolio_chart:
    st.header('Performance Chart')
#    st.write(chart_data)
    for s in range(0, len(df)):
        chart_data = yf.download(df.loc[s,"Ticker"], start_date, end_date)
        st.line_chart(chart_data, y=["Close"])