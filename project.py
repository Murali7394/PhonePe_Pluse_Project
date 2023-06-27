import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

from pymongo import MongoClient
import sqlite3
import sqlalchemy
from sqlalchemy import text


engine = sqlalchemy.create_engine('sqlite:///D:\Phone pluse project\phonepluse.db')



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


col1, col2 = st.columns([0.6,0.4])

with st.sidebar:
    st.write("This is a phone pe pluse data project")
    dtyp = st.selectbox('Select the type of data', ['Transaction',"User"], index=0)
    year = st.selectbox('Select the year', [2018,2019,2020,2021,2022], index=0)
    quater = st.selectbox('Select the Quater', [1,2,3,4], index=0)

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

        choice = st.radio(label='Top 10 in India', options=['States','Districts','Pincodes'],horizontal=True)

        if choice == 'States':
            query = text(f"""SELECT State, Trans_amount_cf FROM Top_tran_india_state 
                        WHERE Year={year} AND Quater={quater};""")
            df = pd.read_sql(query, con=engine.connect())
            st.table(df)
        if choice == 'Districts':
            query = text(f"""SELECT District_name, Trans_amount_cf FROM Top_tran_india_distric 
                        WHERE Year={year} AND Quater={quater};""")
            df = pd.read_sql(query, con=engine.connect())
            st.table(df)
        if choice == 'Pincodes':
            query = text(f"""SELECT Pincode, Trans_amount_cf FROM Top_tran_india_pincode 
                            WHERE Year={year} AND Quater={quater};""")
            df = pd.read_sql(query, con=engine.connect())
            st.table(df)



