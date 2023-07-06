import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import sqlalchemy
import streamlit as st
from sqlalchemy import text
import sqlite3
import plotly.express as px

engine = sqlalchemy.create_engine(r"sqlite:///D:\Phone pluse project\phonepluse.db")

st.header("Valuable Insights From the Phone Transactions and Users Data")
st.subheader("Trend of Transaction amount and Transaction count")

query = text(r"""SELECT Year, sum(Transaction_count) Total_count, sum(Transaction_amount) 
                Total_amount FROM Agg_tns_India GROUP BY Year;""")

year_on_year_df = pd.read_sql(query, con= engine.connect())
# year_on_year_df

fig,(ax1,ax2) = plt.subplots(1,2)
fig.suptitle("Year on Year count and amount")
ax1.plot(year_on_year_df['Year'], year_on_year_df['Total_amount'], label='tns_amount', c = '#FF5733',
         marker='o')
ax1.legend()
ax2.plot(year_on_year_df['Year'], year_on_year_df['Total_count'], label='tns_count', c = '#FFBD33',
         marker='o')
ax2.legend()
plt.show()
st.pyplot(fig)
st.subheader('Observations')
st.write('The trend line has shown exponential growth in transaction amount and count from the year 2020'
         'From covid the digital transactions are in high use and phone has benefited from it.'
         'After covid the growth is exponential means many users like phone and not shifting to other'
         'platforms')


st.subheader("Analyse which Transaction type is performing over the years")
query = text(fr"SELECT * FROM Agg_tns_India")
trans_df = pd.read_sql(query, con=engine.connect())
# trans_df
plt.figure(figsize=(10,6))
fig = px.area(trans_df, x='Transaction_type', y='Transaction_amount', color='Quater', facet_col='Year')
st.plotly_chart(fig)

st.write("It is clear that Peer to Peer Payments, Merchant Payments and Recharge and Bill Payments is"
         "performing way better than the other instruments, working on the other instruments will boost "
         "the growth even further and good maintenance of the good performing ones")
