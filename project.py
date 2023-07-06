import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
import numpy as np
from pymongo import MongoClient
import sqlite3
import sqlalchemy
from sqlalchemy import text
import json

engine = sqlalchemy.create_engine('sqlite:///D:\Phone pluse project\phonepluse.db')
# filling up to remove the
# error

def formatINR(number):
    s, *d = str(number).partition(".")
    r = ",".join([s[x-2:x] for x in range(-3, -len(s), -2)][::-1] + [s[-3:]])
    return "".join([r] + d)


def format_cash(amount):
    def truncate_float(number, places):
        return int(number * (10 ** places)) / 10 ** places

    if amount < 1e3:
        return amount

    if 1e3 <= amount < 1e5:
        return str(truncate_float((amount / 1e5) * 100, 2)) + " K"

    if 1e5 <= amount < 1e7:
        return str(truncate_float((amount / 1e7) * 100, 2)) + " L"

    if amount > 1e7:
        return str(truncate_float(amount / 1e7, 2)) + " Cr"


def final_format(amount):
    x = format_cash(amount)
    n,d,v = str(x).partition('.')
    value = formatINR(int(n))
    final = value + d + v
    return final


col1, col2 = st.columns([3,1])

with st.sidebar:
    st.write("This is a phone pe pluse data project")
    dtyp = st.selectbox('Select the type of data', ['Transaction',"Users"], index=1)
    year = st.selectbox('Select the year', [2018,2019,2020,2021,2022], index=0)
    quater = st.selectbox('Select the Quater', [1,2,3,4], index=0)

# if the transaction is selected these are the options or details that should be displyed in the application
if dtyp == 'Transaction':
    with col2:
        st.header("Transactions")

        st.write("All PhonePe Transactions")
        query = text(f"""SELECT sum(Transaction_count) FROM Agg_tns_India 
                    WHERE Year = {year} and quater = {quater} GROUP BY Year,Quater ;""")
        all_trans = pd.read_sql(query, con=engine.connect())
        tc = all_trans.iloc[0]['sum(Transaction_count)']
        st.subheader(formatINR(tc))

        st.write("Total Amount")
        query = text(f"""SELECT sum(Transaction_amount) FROM Agg_tns_India 
                    WHERE Year = {year} and quater = {quater} GROUP BY Year,Quater ;""")
        all_trans = pd.read_sql(query, con=engine.connect())
        ta = all_trans.iloc[0]['sum(Transaction_amount)']
        st.subheader(final_format(ta))

        atv = ta//tc
        st.write("Average Transaction Value")
        st.subheader(formatINR(atv))
        st.subheader('____________________________')
        st.subheader('Categories')

        query = text(f"""SELECT Trans_count_cf FROM Agg_tns_India WHERE Year = {year} and Quater = {quater} AND 
                     Transaction_type = 'Recharge & bill payments'GROUP BY Year,Quater, Transaction_type;""")
        all_trans = pd.read_sql(query, con=engine.connect())
        vrb = all_trans.iloc[0]['Trans_count_cf']

        query = text(f"""SELECT Trans_count_cf FROM Agg_tns_India WHERE Year = {year} and Quater = {quater} AND 
                             Transaction_type = 'Peer-to-peer payments'GROUP BY Year,Quater, Transaction_type;""")
        all_trans = pd.read_sql(query, con=engine.connect())
        vpp = all_trans.iloc[0]['Trans_count_cf']

        query = text(f"""SELECT Trans_count_cf FROM Agg_tns_India WHERE Year = {year} and Quater = {quater} AND 
                                     Transaction_type = 'Merchant payments' GROUP BY Year,Quater, Transaction_type;""")
        all_trans = pd.read_sql(query, con=engine.connect())
        vmp = all_trans.iloc[0]['Trans_count_cf']

        query = text(f"""SELECT Trans_count_cf FROM Agg_tns_India WHERE Year = {year} and Quater = {quater} AND 
                                             Transaction_type = 'Financial Services' GROUP BY Year,Quater, Transaction_type;""")
        all_trans = pd.read_sql(query, con=engine.connect())
        vfp = all_trans.iloc[0]['Trans_count_cf']

        query = text(f"""SELECT Trans_count_cf FROM Agg_tns_India WHERE Year = {year} and Quater = {quater} AND 
                                                     Transaction_type = 'Others' GROUP BY Year,Quater, Transaction_type;""")
        all_trans = pd.read_sql(query, con=engine.connect())
        vop = all_trans.iloc[0]['Trans_count_cf']
        st.write("Recharge & bill payments:",vrb)
        st.write("Peer-to-peer payments   :", vpp)
        st.write("Merchant payments   :", vmp)
        st.write("Financial Services   :", vfp)
        st.write("Others   :", vop)

        choice = st.radio(label = '', options=['States','Districts','Pincodes'],horizontal=True)

        if choice == 'States':
            st.subheader("Top 10 States")
            query = text(f"""SELECT State, Trans_amount_cf FROM Top_tran_india_state 
                        WHERE Year={year} AND Quater={quater};""")
            df = pd.read_sql(query, con=engine.connect())
            df['State'] = df['State'].apply(lambda x: x.title())
            st.table(df)
        if choice == 'Districts':
            st.subheader("Top 10 Districts")
            query = text(f"""SELECT District_name, Trans_amount_cf FROM Top_tran_india_distric 
                        WHERE Year={year} AND Quater={quater};""")
            df = pd.read_sql(query, con=engine.connect())
            df['District_name'] = df['District_name'].apply(lambda x: x.title())
            st.table(df)
        if choice == 'Pincodes':
            st.subheader("Top 10 Pincodes")
            query = text(f"""SELECT Pincode, Trans_amount_cf FROM Top_tran_india_pincode 
                            WHERE Year={year} AND Quater={quater};""")
            df = pd.read_sql(query, con=engine.connect())
            st.table(df)
    with col1:
        indian_states = json.load(open('states_india.geojson', 'r'))
        # creating id key in the feature with the statecode
        # creating the state_id_map for mapping with the dataframe that is to be used in the map

        state_id_map = {}
        for feature in indian_states['features']:
            feature['id'] = feature['properties']['state_code']
            state_id_map[feature['properties']['st_nm']] = feature['id']
        #  connecting to sqlite server to retrive the table using query
        engine = sqlalchemy.create_engine(r'sqlite:///D:\Phone pluse project\phonepluse.db')
        query = text(f"""SELECT * FROM Map_trans_india WHERE Year = {year} AND Quater = {quater} GROUP BY Year,Quater, State;""")
        data_df = pd.read_sql(query, con=engine.connect())

        #  Preprocessing the dataframe created form sqlite to map with the geojson file(the state name where
        #  not same so changing the state names accordingly to map both the files)
        data_df['State'] = data_df['State'].apply(lambda x: x.title())

        data_df['State'][0] = 'Andaman & Nicobar Island'
        data_df['State'][2] = 'Arunanchal Pradesh'
        data_df['State'][7] = 'Daman & Diu'
        data_df['State'][8] = 'NCT of Delhi'

        #  mapping the geojson file with the df and using apply lambda function by creating an id column to merge
        data_df['id'] = data_df['State'].apply(lambda x: state_id_map[x] if x != 'Ladakh' else np.nan)
        data_df.dropna(inplace=True)  # removing the null values

        # plotting the choropleth map for the dataframe
        fig = px.choropleth(data_df,
                            locations='id',
                            geojson=indian_states,
                            color='Transaction_amount',
                            scope='asia',
                            hover_name='State',
                            hover_data=['Trans_count_cf', "Trans_amount_cf"],
                            title="Transactions Map",
                            center={'lat': 24, 'lon': 78},
                            color_continuous_scale="PuRd",
                            height=700,
                            width=700
                            )
        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(coloraxis_showscale=False)

        # st.write("This the choropleth map that is to be shown in the col1 of the phonepe project")
        st.plotly_chart(fig)


# If the user selects the users option in the selectbox then these should be displayed and the default selection
# transactions

if dtyp == 'Users':
    with col2:
        #  just getting the reg_users and app_opens data from sql and displaying in the  application
        # this section is for registers users
        st.header("Users")
        st.write(f'Registered PhonePe users till Quater{quater} {year} :')
        query = text(f"""SELECT Reg_users_cf FROM AUI_RU_AO WHERE Year = {year} AND Quater = {quater};""")
        df = pd.read_sql(query, con=engine.connect())
        ru = df.iloc[0]['Reg_users_cf']
        st.subheader(ru)
        # this section is for app opens
        st.write(f'PhonePe app opens in Quater{quater} {year} :')
        query = text(f"""SELECT App_Opens_cf FROM AUI_RU_AO WHERE Year = {year} AND Quater = {quater};""")
        df = pd.read_sql(query, con=engine.connect())
        ao = df.iloc[0]['App_opens_cf']
        st.subheader(ao)
        st.subheader('____________________________')
#       this section is to display the top india users tables such as
        u_choice = st.radio(label='', options=['States', 'Districts', 'Pincodes'], horizontal=True)

        if u_choice == 'States':
            query = text(f"""SELECT State, User_count_cf FROM Top_user_india_state WHERE Year={year} 
                         AND Quater={quater};""")
            st.subheader('Top 10 States')
            sdf = pd.read_sql(query, con=engine.connect())
            sdf['State'] = sdf['State'].apply(lambda x: x.title())
            st.table(sdf)
        if u_choice == 'Districts':
            query = text(f"""SELECT District_name, User_count_cf FROM Top_user_india_district WHERE Year={year} 
                         AND Quater={quater};""")
            st.subheader('Top 10 Districts')
            ddf = pd.read_sql(query, con=engine.connect())
            ddf['District_name'] = ddf['District_name'].apply(lambda x: x.title())
            st.table(ddf)
        if u_choice == 'Pincodes':
            query = text(f"""SELECT Pincode, User_count_cf FROM Top_user_india_pincode WHERE Year={year} 
                         AND Quater={quater};""")
            st.subheader('Top 10 Pincodes')
            pdf = pd.read_sql(query, con=engine.connect())
            st.table(pdf)

    with col1:
        indian_states = json.load(open('states_india.geojson', 'r'))
        # creating id key in the feature with the statecode
        # creating the state_id_map for mapping with the dataframe that is to be used in the map

        state_id_map = {}
        for feature in indian_states['features']:
            feature['id'] = feature['properties']['state_code']
            state_id_map[feature['properties']['st_nm']] = feature['id']
        #  connecting to sqlite server to retrive the table using query
        engine = sqlalchemy.create_engine(r'sqlite:///D:\Phone pluse project\phonepluse.db')
        query = text(f"""SELECT * FROM Map_user_india WHERE Year = {year} AND Quater = {quater} GROUP BY Year,Quater, State;""")
        data_df = pd.read_sql(query, con=engine.connect())
        # preprocessing the dataframe to fit with geojson file so that we can map it
        data_df['State'] = data_df['State'].apply(lambda x: x.title())
        data_df['State'][0] = 'Andaman & Nicobar Island'
        data_df['State'][2] = 'Arunanchal Pradesh'
        data_df['State'][7] = 'Daman & Diu'
        data_df['State'][8] = 'NCT of Delhi'

        #  mapping the geojson file with the df and using apply lambda function by creating an id column to merge
        data_df['id'] = data_df['State'].apply(lambda x: state_id_map[x] if x != 'Ladakh' else np.nan)
        data_df.dropna(inplace=True)
        fig = px.choropleth(data_df,
                            locations='id',
                            geojson=indian_states,
                            color='User_count',
                            hover_name='State',
                            hover_data=['User_count_cf', "AppOpens_cf"],
                            title="Users Map",
                            center={'lat': 24, 'lon': 78},
                            color_continuous_scale="Bluyl",
                            height=700,
                            width=700
                            )
        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig)


#



