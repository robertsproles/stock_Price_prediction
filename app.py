import streamlit as st
import pandas as pd
import yfinance as yf
import datetime
from datetime import date
import altair as alt


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
    
with portfolio_chart:
    st.header('', divider='rainbow')
    bar_chart_data = pd.DataFrame()
    line_chart_data = pd.DataFrame()
    for s in range(0, len(df)):
        chart_data = yf.download(df.loc[s,"Ticker"], start_date, end_date)
        line_chart_data.insert(0,df.loc[s,"Ticker"],chart_data.loc[:,'Close'],True)
        chart_data['Close'] = chart_data['Close'].astype(float)
        chart_data.loc[:,'Close'] = (chart_data.loc[:,'Close'] * df.loc[s,'NumShares'])
        bar_chart_data.insert(0,df.loc[s,"Ticker"],chart_data.loc[:,'Close'],True)
    st.write('Individual Performance Over Last', days_to_plot, 'Days ($)')
    st.line_chart(data = line_chart_data)
    st.write('')
    st.write('Portfolio Performance Over Last', days_to_plot, 'Days ($)')
    st.bar_chart(data = bar_chart_data)