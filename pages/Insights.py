import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import sqlalchemy
import streamlit as st
from sqlalchemy import text
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu

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
st.write('The above graph shows an exponential growth in transaction amount and count from the year 2020.'
         'The year in which there is a onset of pandemic, many people switched to digital mode payment.'
         ' Digital Transactions become higher in use and their volume increased exponentially '
         'as clearly seen from the graph. Pandemic set fire to digital transactions and it sky rocketted.'
         'After covid the growth rate as slow down a bit but there is are high transactions in amount and count.'
         'To maintain or to increase the growth rate  we have work on some features lets explore the data further')

st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

st.subheader("Analyse which Transaction type is performing over the years")
query = text(fr"SELECT * FROM Agg_tns_India")
trans_df = pd.read_sql(query, con=engine.connect())
# trans_df
plt.figure(figsize=(10,6))
fig = px.area(trans_df, x='Transaction_type', y='Transaction_amount', color='Quater', facet_col='Year',
              title='Performance of Transaction Insutruments')
st.plotly_chart(fig)

st.write("It is clear that Peer to Peer Payments, Merchant Payments and Recharge and Bill Payments is"
         " performing way better than the other instruments, working on the other instruments"
         " and maintenance of the good performing ones will boost "
         "the growth even further.")

st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

st.subheader("Users Trend Analysis")
query = text(fr"SELECT * FROM AUI_RU_AO")
users_df = pd.read_sql(query, con=engine.connect())
# users_df
plt.figure(figsize=(10,6))
registered_Users = px.area(data_frame=users_df, x='Year', y='Registered_Users', color='Quater',
                           title = 'Registered Users Growth Over Years')
st.plotly_chart(registered_Users)
plt.figure(figsize=(10,6))
user = px.area(data_frame=users_df, x='Year', y='App_Opens', color='Quater',
               title='App Opens Growth Over Years')
st.plotly_chart(user)
st.subheader('Observations')
st.write("The growth of the number of users and app opens has increased significantly but not like Transactions"
         " here the growth is constant from the year 2018 and linearly increasing till now ")

st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)


# Brand wise distribution of users of phonephe
st.subheader("No of Users distribution based on the brand of the device they use")
query = text(fr"SELECT * FROM Agg_user_india")
brand_users_df = pd.read_sql(query, con=engine.connect())
brand_users_df['Quater'] = brand_users_df['Quater'].astype('str')

brand_graph = px.bar(data_frame=brand_users_df, x='User_Brand', y='No_of_Users',facet_col='Year', color='Quater',
             title='Users distribution per Brand of Device')
st.plotly_chart(brand_graph)
st.subheader("Observations")
st.write('From the above Graph it is evident that Xiaomi and Vivo brands are the top two brands '
         'that has high phonephe users in the India on all the quaters and they are increasing in '
         ' good number')

st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)


# state wise analysis of the users and the transactions
st.subheader("Visualization of Transaction Instruments and Users")
states_list = ['andaman-&-nicobar-islands', 'andhra-pradesh',
               'arunachal-pradesh', 'assam', 'bihar', 'chandigarh', 'chhattisgarh', 'dadra-&-nagar-haveli-&-daman-&-diu'
               , 'delhi', 'goa', 'gujarat', 'haryana', 'himachal-pradesh',  'jammu-&-kashmir', 'jharkhand', 'karnataka',
               'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram',
               'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim', 'tamil-nadu', 'telangana', 'tripura'
               , 'uttar-pradesh', 'uttarakhand', 'west-bengal']
state = st.selectbox(label='Select The State and Year', options=states_list, index=0)
year = st.selectbox(label='Year', options=[2018, 2019, 2020, 2021, 2022], index=0)
quater = st.selectbox(label='Quater', options=[1,2,3,4])
# st.write(type(state), type(year))

query = text(f'SELECT * FROM Agg_tns_India WHERE Year = {year} AND Quater = {quater};')
vz_trans_df = pd.read_sql(query, con=engine.connect())
fig = px.bar(data_frame=vz_trans_df, x='Transaction_type', y='Transaction_count', color='Transaction_type',
             title='Transactions in India')
st.plotly_chart(fig)

st.subheader("Observations on Transaction in India")
st.write("On observing all the Transaction Type Over the years. Top three payment instruments in India"
         " are Peer-Peer Payments, Recharge and Bill Payments, Merchant Payments")

st.write("Merchant Payments is very low when at the intial stages of digitisation. This shows at the starting"
         " the merchants we reluctant for the digital mode of transactions")
st.write("But afterwards slowly merchants started to incorporate the digital mode of transaction this has reflected"
         " in the data that the Merchant Payments have moved from the 3rd lowest to the top instrument in the the later"
         " years and Merchant payments will stay at the top as India is Developing country with many MSME business ")
st.write('Financial services and Other payments mode very low in count and amount.This shows that these has '
         'less scope in the people of india or proper streamlining of the sector should be done')


query = text(f"""SELECT * FROM Agg_tns_state WHERE State = '{state}' AND Year = {year} AND Quater = {quater};
""")
state_tns_df = pd.read_sql(query, con=engine.connect())
# st.table(state_tns_df)
fig = px.bar(data_frame=state_tns_df, x='Transaction_type', y='Transaction_amount', color='Transaction_type',
             facet_col='Year', title=f'Performance of Transaction Instruments in {state} in the year {year} '
                                     f'quater {quater}')
st.plotly_chart(fig)

st.subheader("Observations on Transaction in State")
st.write('Though Merchant Payments have topped in India as a whole. In many states still merchant payments'
         ' is a low performing. Merchants in the towns and villages have not fully accepted the digital mode'
         ' of payment ')
st.write('The State that are top contributor to the GDP of India has more transaction amount and count')



# top charts visualization:

#
selected = option_menu(menu_title="Top 10",
                       options=['States', 'Districts', 'Pincodes'],
                       orientation='horizontal',
                       default_index=0
                       )

if selected == 'States':
    st.subheader("Top 10 States")
    query = text(f"""SELECT * FROM Top_tran_india_state
                WHERE Year={year} AND Quater={quater} ORDER BY Transaction_amount DESC;""")
    df = pd.read_sql(query, con=engine.connect())
    df['State'] = df['State'].apply(lambda x: x.title())
    fig = px.bar(data_frame=df, x='State', y='Transaction_amount', color='State')
    st.plotly_chart(fig)
    # fig = plt.figure(figsize=(10,6))
    # sns.barplot(df, x='State', y='Transaction_amount', hue='State')
    # st.pyplot(fig)
    # st.table(df)
if selected == 'Districts':
    st.subheader("Top 10 Districts")
    query = text(f"""SELECT * FROM Top_tran_india_distric
                WHERE Year={year} AND Quater={quater} ORDER BY Transaction_amount DESC;""")
    df = pd.read_sql(query, con=engine.connect())
    df['District_name'] = df['District_name'].apply(lambda x: x.title())
    fig = px.bar(data_frame=df, x='District_name', y='Transaction_amount', color='District_name')
    st.plotly_chart(fig)
    # st.table(df)
if selected == 'Pincodes':
    st.subheader("Top 10 Pincodes")
    query = text(f"""SELECT * FROM Top_tran_india_pincode
                    WHERE Year={year} AND Quater={quater} ORDER BY Transaction_amount DESC;""")
    df = pd.read_sql(query, con=engine.connect())
    df['Pincode'] = df['Pincode'].astype('str')
    fig = px.bar(data_frame=df, x='Pincode', y='Transaction_amount', color='Pincode')
    st.plotly_chart(fig)
    # st.table(df)

st.subheader("Observations")
st.write('Electronic city of Inida Bengaluru tops the district table shows that many people in bengaluru'
         ' are exposed to new technology. They are aware of the tech make use of it. ')
st.write('Awareness about the digital mode of payment among the people who are in the rural side is very low'
         ' that is why other districts are behind Bengaluru ')
st.write("Fear of Fradulant links and hacking also impacts the thought of people who are thinking to change to "
         " digital")








