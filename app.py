import streamlit as st
import pandas as pd
import yfinance as yf
import datetime
from datetime import date
import altair as alt
import plotly.express as px


header = st.container()
user_sidebar = st.sidebar.container()
portfolio_chart = st.container()
df = pd.read_csv("portfolio.csv")

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
    df.loc[i,"Price"] = stock.info['currentPrice']
    df.loc[i,"Value"] = df.loc[i,"Number of Shares"] * df.loc[i,"Price"]
    df.to_csv('portfolio.csv', index=False)
    chart_data = yf.download(df.loc[i,"Ticker"], start_date, end_date)

with header:
    st.title('Portfolio Value Chart')
    st.write('Enter the stock (ticker symbols) and number of shares in the sidebar to update the portfolio.')
    st.write(df[['Ticker','Number of Shares']])
    
with portfolio_chart:
    st.header('Performance Chart')
    st.write(chart_data)
    st.line_chart(chart_data, y=["Low", "Close", "High"])
    st.plotly_chart(px.pie(df, values="Value", names="Ticker", title='Portfolio Balance'))