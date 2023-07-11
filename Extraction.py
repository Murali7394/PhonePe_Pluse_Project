import os
import pandas as pd
# import git
import json
import numpy as np

#  cloning the data from Phonephe git hub repository

agg_trans_state_path = fr"C:\Users\LENOVO\Desktop\phonephe\pulse\data\aggregated\transaction\country\india\state/"
agg_user_state_path = fr"C:\Users\LENOVO\Desktop\phonephe\pulse\data\aggregated\user\country\india\state/"
agg_trans_india_path = fr"C:\Users\LENOVO\Desktop\phonephe\pulse\data\aggregated\transaction\country\india"
agg_user_india_path = fr"C:\Users\LENOVO\Desktop\phonephe\pulse\data\aggregated\user\country\india"

def cloning():
    os.system('git clone https://github.com/PhonePe/pulse.git')


def aggregate_transactions_state(save_path):
    path = agg_trans_state_path
    Agg_state_list = os.listdir(path)
    clm = {'State': [], 'Year': [], 'Quater': [], 'Transaction_type': [], 'Transaction_count': [],
           'Transaction_amount': []}
    for i in Agg_state_list:
        p_i = path + i + "/"
        Agg_yr = os.listdir(p_i)
        for j in Agg_yr:
            p_j = p_i + j + "/"
            Agg_yr_list = os.listdir(p_j)
            for k in Agg_yr_list:
                p_k = p_j + k
                Data = open(p_k, 'r')
                D = json.load(Data)
                for z in D['data']['transactionData']:
                    Name = z['name']
                    count = z['paymentInstruments'][0]['count']
                    amount = z['paymentInstruments'][0]['amount']
                    clm['Transaction_type'].append(Name)
                    clm['Transaction_count'].append(count)
                    clm['Transaction_amount'].append(amount)
                    clm['State'].append(i)
                    clm['Year'].append(j)
                    clm['Quater'].append(int(k.strip('.json')))
    # Succesfully created a dataframe
    Agg_Trans = pd.DataFrame(clm)
    Agg_Trans.to_csv(save_path+'Agg_Trans_state.csv', index=False)

def agg_user_state(save_path):
    #  Extracting the users data

    path = agg_user_state_path

    clm = {'State': [], 'Year': [], 'Quater': [], 'User_Brand': [], 'No_of_Users': [], 'Percent': []}

    Agg_state_list = os.listdir(path)
    for state in Agg_state_list:
        p_state = path + state + "/"
        Agg_year_list = os.listdir(p_state)
        for year in Agg_year_list:
            p_state_year = p_state + year + "/"
            Agg_quater_list = os.listdir(p_state_year)
            for quater in Agg_quater_list:
                p_state_year_quater = p_state_year + quater
                #             print(p_state_year_quater)
                Data = open(p_state_year_quater, 'r')
                D = json.load(Data)
                if D['data'].get('usersByDevice', np.nan) == None:
                    continue
                else:
                    for ele in D['data'].get('usersByDevice', np.nan):
                        brand = ele['brand']
                        count = ele['count']
                        percent = ele['percentage']
                        clm['State'].append(state)
                        clm['Year'].append(year)
                        clm['Quater'].append(int(quater.strip('.json')))
                        clm['User_Brand'].append(brand)
                        clm['No_of_Users'].append(count)
                        clm['Percent'].append(percent)

    Agg_user_df = pd.DataFrame(clm)
    Agg_user_df.to_csv(save_path+'Agg_user_state.csv')

def agg_transactions_india(save_path):
    path = agg_trans_india_path
    clm = {'Year': [], 'Quater': [], 'Transaction_type': [], 'Transaction_count': [], 'Transaction_amount': []}
    Agg_tns_India = os.listdir(path)
    for year in Agg_tns_India:
        if year == 'state':
            continue
        else:
            path_year = path + '/' + year
            Agg_tns_India_year_Q = os.listdir(path_year)
            for ele in Agg_tns_India_year_Q:
                #         print(ele)
                path_year_quater = path_year + '/' + ele
                data = open(path_year_quater, 'r')
                D = json.load(data)

                for element in D['data']['transactionData']:
                    name = element['name']
                    count = element['paymentInstruments'][0]['count']
                    amount = element['paymentInstruments'][0]['amount']
                    clm['Transaction_type'].append(name)
                    clm['Transaction_count'].append(count)
                    clm['Transaction_amount'].append(amount)
                    clm['Year'].append(year)
                    clm['Quater'].append(int(ele.strip('.json')))
    Agg_tns_India_df = pd.DataFrame(clm)
    Agg_tns_India_df.to_csv(agg_trans_save_location+'Agg_tns_India.csv')


def agg_user_india(save_path):
    path = agg_user_india_path
    clm = {'Year': [], 'Quater': [], 'User_Brand': [], 'No_of_Users': [], 'Percent': []}
    Agg_user_India = os.listdir(path)
    for year in Agg_user_India:
        if year == 'state':
            continue
        else:
            path_year = path + '\\' + year
            Agg_user_India_year_Q = os.listdir(path_year)
            for quater in Agg_user_India_year_Q:
                #         print(ele)
                path_year_quater = path_year + '\\' + quater
                data = open(path_year_quater, 'r')
                D = json.load(data)
                if D['data'].get('usersByDevice', np.nan) == None:
                    continue
                else:
                    for ele in D['data'].get('usersByDevice', np.nan):
                        brand = ele['brand']
                        count = ele['count']
                        percent = ele['percentage']
                        clm['Year'].append(year)
                        clm['Quater'].append(int(quater.strip('.json')))
                        clm['User_Brand'].append(brand)
                        clm['No_of_Users'].append(count)
                        clm['Percent'].append(percent)
    Agg_user_India_df = pd.DataFrame(clm)
    Agg_user_India_df.to_csv(agg_trans_save_location+'Agg_user_India.csv')

#  The above function contains obtaining information from the aggreate folder of the data

#Below functions we will retrive the data of the Map folder for transactions and users

# path variables for the map folders


map_trans_state_path = fr"C:\Users\LENOVO\Desktop\phonephe\pulse\data\map\transaction\hover\country\india\state"
map_trans_india_path = fr"C:\Users\LENOVO\Desktop\phonephe\pulse\data\map\transaction\hover\country\india"
map_user_state_path = fr"C:\Users\LENOVO\Desktop\phonephe\pulse\data\map\user\hover\country\india\state"
map_user_india_path = fr"C:\Users\LENOVO\Desktop\phonephe\pulse\data\map\user\hover\country\india"
def map_transactions_state(save_path):
    clm = {'State': [], 'Year': [], 'Quater': [], 'District_name': [], 'Transaction_count': [],
           'Transaction_amount': []}
    path = map_trans_state_path
    list_states = os.listdir(path)
    for state in list_states:
        path_state = path + '\\' + state
        list_years = os.listdir(path_state)
        for year in list_years:
            path_state_year = path_state + '\\' + year
            list_quater = os.listdir(path_state_year)
            for quater in list_quater:
                path_state_year_quater = path_state_year + '\\' + quater
                data = open(path_state_year_quater, 'r')
                D = json.load(data)
                for element in D['data']['hoverDataList']:
                    name = element['name']
                    count = element['metric'][0]['count']
                    amount = element['metric'][0]['amount']
                    clm['State'].append(state)
                    clm['Year'].append(year)
                    clm['Quater'].append(int(quater.strip('.json')))
                    clm['District_name'].append(name)
                    clm['Transaction_count'].append(count)
                    clm['Transaction_amount'].append(amount)

    Map_trans_state_df = pd.DataFrame(clm)
    Map_trans_state_df.to_csv(save_path+'map_trans_state.csv')

# map Transaction for India
def map_transactions_india(save_path):
    clm = {'State': [], 'Year': [], 'Quater': [], 'Transaction_count': [], 'Transaction_amount': []}
    path = map_trans_india_path
    list_years = os.listdir(path)
    for year in list_years:
        if year == 'state':
            continue
        else:
            path_year = path + '\\' + year
            list_quater = os.listdir(path_year)
            for quater in list_quater:
                path_year_quater = path_year + '\\' + quater
                data = open(path_year_quater, 'r')
                D = json.load(data)
                for element in D['data']['hoverDataList']:
                    name = element['name']
                    count = element['metric'][0]['count']
                    amount = element['metric'][0]['amount']
                    clm['Year'].append(year)
                    clm['Quater'].append(int(quater.strip('.json')))
                    clm['State'].append(name)
                    clm['Transaction_count'].append(count)
                    clm['Transaction_amount'].append(amount)

    Map_trans_india_df = pd.DataFrame(clm)

    Map_trans_india_df.to_csv(map_trans_save_location+'map_trans_india.csv')


def map_user_state(save_path):
    clm = {'State': [], 'Year': [], 'Quater': [], 'District_name': [], 'User_count': [], 'AppOpens': []}
    path = map_user_state_path
    list_states = os.listdir(path)
    for state in list_states:
        path_state = path + '\\' + state
        #     print(path_state)
        list_state_year = os.listdir(path_state)
        for year in list_state_year:
            path_state_year = path_state + '\\' + year
            #         print(path_state_year)
            list_state_year_quater = os.listdir(path_state_year)
            for quater in list_state_year_quater:
                path_state_year_quater = path_state_year + '\\' + quater
                data = open(path_state_year_quater, 'r')
                Data = json.load(data)
                #             print(Data)
                for i in Data['data']['hoverData']:
                    name = i
                    count = Data['data']['hoverData'][i]['registeredUsers']
                    appopen = Data['data']['hoverData'][i]['appOpens']
                    clm['State'].append(state)
                    clm['Year'].append(year)
                    clm['Quater'].append(quater.strip('.json'))
                    clm['District_name'].append(name)
                    clm['User_count'].append(count)
                    clm['AppOpens'].append(appopen)

    Map_user_state_df = pd.DataFrame(clm)
    Map_user_state_df.to_csv(save_path+'map_user_state.csv')

def map_user_india(save_path):
    clm = {'State': [], 'Year': [], 'Quater': [], 'User_count': [], 'AppOpens': []}
    path = map_user_india_path
    list_year = os.listdir(path)
    for year in list_year:
        if year == 'state':
            continue
        path_year = path + '\\' + year
        list_quaters = os.listdir(path_year)
        for quater in list_quaters:
            path_year_quater = path_year + '\\' + quater
            #         print(path_year_quater)
            data = open(path_year_quater, 'r')
            D = json.load(data)
            #         print(D)
            for i in D['data']['hoverData']:
                name = i
                count = D['data']['hoverData'][i]['registeredUsers']
                appopen = D['data']['hoverData'][i]['appOpens']
                clm['State'].append(name)
                clm['Year'].append(year)
                clm['Quater'].append(quater.strip('.json'))
                clm['User_count'].append(count)
                clm['AppOpens'].append(appopen)

    Map_user_india_df = pd.DataFrame(clm)
    Map_user_india_df.to_csv(save_path+'map_user_india.csv')

# Top data extraction from the repository


top_trans_state_path = fr"C:\Users\LENOVO\Desktop\phonephe\pulse\data\top\transaction\country\india\state"
top_trans_india_path = fr"C:\Users\LENOVO\Desktop\phonephe\pulse\data\top\transaction\country\india"
top_user_state_path = fr"C:\Users\LENOVO\Desktop\phonephe\pulse\data\top\user\country\india\state"
top_user_india_path = fr"C:\Users\LENOVO\Desktop\phonephe\pulse\data\top\user\country\india"
def top_transactions_state(save_path):
    clm_p = {'State': [], 'Year': [], 'Quater': [], "Pincode": [], 'Transaction_count': [], 'Transaction_amount': []}
    clm_d = {'State': [], 'Year': [], 'Quater': [], "District_name": [], 'Transaction_count': [],
             'Transaction_amount': []}
    path = top_trans_state_path
    list_state = os.listdir(path)
    for state in list_state:
        path_state = path + '\\' + state
        list_state_year = os.listdir(path_state)
        for year in list_state_year:
            path_state_year = path_state + '\\' + year
            list_state_year_quater = os.listdir(path_state_year)
            for quater in list_state_year_quater:
                path_state_year_quater = path_state_year + '\\' + quater
                data = open(path_state_year_quater, 'r+')
                Data = json.load(data)
                for each in Data['data']:
                    if each == 'pincodes':
                        for i in range(len(Data['data'][each])):
                            code = Data['data'][each][i]['entityName']
                            count = Data['data'][each][i]['metric']['count']
                            amount = Data['data'][each][i]['metric']['amount']
                            clm_p['State'].append(state)
                            clm_p['Year'].append(year)
                            clm_p['Quater'].append(quater.strip('.json'))
                            clm_p['Pincode'].append(code)
                            clm_p['Transaction_count'].append(count)
                            clm_p['Transaction_amount'].append(amount)
                    if each == 'districts':
                        for i in range(len(Data['data'][each])):
                            name = Data['data'][each][i]['entityName']
                            count = Data['data'][each][i]['metric']['count']
                            amount = Data['data'][each][i]['metric']['amount']
                            clm_d['State'].append(state)
                            clm_d['Year'].append(year)
                            clm_d['Quater'].append(quater.strip('.json'))
                            clm_d['District_name'].append(name)
                            clm_d['Transaction_count'].append(count)
                            clm_d['Transaction_amount'].append(amount)

    Top_trans_state_pincode_df = pd.DataFrame(clm_p)
    Top_trans_state_district_df = pd.DataFrame(clm_d)
    Top_trans_state_pincode_df.to_csv(save_path + 'top_trans_state_pincode_df.csv')
    Top_trans_state_district_df.to_csv(save_path + 'top_trans_state_district_df.csv')


def top_transactions_india(save_path):
    clm_s = {'State': [], 'Year': [], 'Quater': [], 'Transaction_count': [], 'Transaction_amount': []}
    clm_d = {'Year': [], 'Quater': [], "District_name": [], 'Transaction_count': [], 'Transaction_amount': []}
    clm_pc = {'Year': [], 'Quater': [], "Pincode": [], 'Transaction_count': [], 'Transaction_amount': []}
    path = top_trans_india_path
    list_years = os.listdir(path)
    for year in list_years:
        if year == 'state':
            continue
        path_year = path + '\\' + year
        list_years_quater = os.listdir(path_year)
        for quater in list_years_quater:
            path_year_quater = path_year + '\\' + quater
            data = open(path_year_quater, 'r')
            Data = json.load(data)
            for each in Data['data']:
                if each == 'states':
                    for i in range(len(Data['data'][each])):
                        name = Data['data'][each][i]['entityName']
                        count = Data['data'][each][i]['metric']['count']
                        amount = Data['data'][each][i]['metric']['amount']
                        clm_s['State'].append(name)
                        clm_s['Year'].append(year)
                        clm_s['Quater'].append(quater.strip('.json'))
                        clm_s['Transaction_count'].append(count)
                        clm_s['Transaction_amount'].append(amount)
                if each == 'districts':
                    for i in range(len(Data['data'][each])):
                        name = Data['data'][each][i]['entityName']
                        count = Data['data'][each][i]['metric']['count']
                        amount = Data['data'][each][i]['metric']['amount']
                        clm_d['District_name'].append(name)
                        clm_d['Year'].append(year)
                        clm_d['Quater'].append(quater.strip('.json'))
                        clm_d['Transaction_count'].append(count)
                        clm_d['Transaction_amount'].append(amount)
                if each == 'pincodes':
                    for i in range(len(Data['data'][each])):
                        code = Data['data'][each][i]['entityName']
                        count = Data['data'][each][i]['metric']['count']
                        amount = Data['data'][each][i]['metric']['amount']
                        clm_pc['Pincode'].append(code)
                        clm_pc['Year'].append(year)
                        clm_pc['Quater'].append(quater.strip('.json'))
                        clm_pc['Transaction_count'].append(count)
                        clm_pc['Transaction_amount'].append(amount)

    Top_tran_india_state_df = pd.DataFrame(clm_s)
    Top_tran_india_district_df = pd.DataFrame(clm_d)
    Top_tran_india_pincode_df = pd.DataFrame(clm_pc)
    Top_tran_india_state_df.to_csv(save_path + 'top_tran_india_state_df.csv')
    Top_tran_india_district_df.to_csv(save_path + 'top_tran_india_district_df.csv')
    Top_tran_india_pincode_df.to_csv(save_path + 'top_tran_india_pincode_df.csv')


def top_user_state(save_path):
    clm_d = {'State': [], 'Year': [], 'Quater': [], "District_name": [], 'User_count': []}
    clm_pc = {'State': [], 'Year': [], 'Quater': [], "Pincode": [], 'User_count': []}
    path = top_user_state_path
    list_state = os.listdir(path)
    for state in list_state:
        path_state = path + '\\' + state
        list_state_year = os.listdir(path_state)
        for year in list_state_year:
            path_state_year = path_state + '\\' + year
            #         print(path_state_year)
            list_state_year_quater = os.listdir(path_state_year)
            for quater in list_state_year_quater:
                path_state_year_quater = path_state_year + '\\' + quater
                data = open(path_state_year_quater, 'r+')
                Data = json.load(data)
                for each in Data['data']:
                    if each == 'states':
                        continue
                    if each == 'districts':
                        for i in range(len(Data['data'][each])):
                            name = Data['data'][each][i]['name']
                            users = Data['data'][each][i]['registeredUsers']
                            clm_d['State'].append(state)
                            clm_d['Year'].append(year)
                            clm_d['Quater'].append(quater.strip('.json'))
                            clm_d['District_name'].append(name)
                            clm_d['User_count'].append(users)
                            break
                    if each == 'pincodes':
                        for i in range(len(Data['data'][each])):
                            code = Data['data'][each][i]['name']
                            users = Data['data'][each][i]['registeredUsers']
                            clm_pc['State'].append(state)
                            clm_pc['Year'].append(year)
                            clm_pc['Quater'].append(quater.strip('.json'))
                            clm_pc['Pincode'].append(code)
                            clm_pc['User_count'].append(users)
                            break
    Top_users_state_district_df = pd.DataFrame(clm_d)
    Top_users_state_pincodes_df = pd.DataFrame(clm_pc)
    Top_users_state_district_df.to_csv(save_path + 'top_users_state_district_df.csv')
    Top_users_state_pincodes_df.to_csv(save_path + 'top_users_state_pincode_df.csv')

def top_user_inida(save_path):
    clm_s = {'State': [], 'Year': [], 'Quater': [], 'User_count': []}
    clm_d = {'Year': [], 'Quater': [], "District_name": [], 'User_count': []}
    clm_pc = {'Year': [], 'Quater': [], "Pincode": [], 'User_count': []}
    path = top_user_india_path
    list_years = os.listdir(path)
    for year in list_years:
        if year == 'state':
            continue
        path_year = path + '\\' + year
        list_years_quater = os.listdir(path_year)
        for quater in list_years_quater:
            path_year_quater = path_year + '\\' + quater
            data = open(path_year_quater, 'r')
            Data = json.load(data)
            for each in Data['data']:
                if each == 'states':
                    for i in range(len(Data['data'][each])):
                        name = Data['data'][each][i]['name']
                        users = Data['data'][each][i]['registeredUsers']
                        clm_s['State'].append(name)
                        clm_s['Year'].append(year)
                        clm_s['Quater'].append(quater.strip('.json'))
                        clm_s['User_count'].append(users)
                if each == 'districts':
                    for i in range(len(Data['data'][each])):
                        name = Data['data'][each][i]['name']
                        users = Data['data'][each][i]['registeredUsers']
                        clm_d['Year'].append(year)
                        clm_d['Quater'].append(quater.strip('.json'))
                        clm_d['District_name'].append(name)
                        clm_d['User_count'].append(users)
                if each == 'pincodes':
                    for i in range(len(Data['data'][each])):
                        code = Data['data'][each][i]['name']
                        users = Data['data'][each][i]['registeredUsers']
                        clm_pc['Year'].append(year)
                        clm_pc['Quater'].append(quater.strip('.json'))
                        clm_pc['Pincode'].append(code)
                        clm_pc['User_count'].append(users)

    Top_user_india_state_df = pd.DataFrame(clm_s)
    Top_user_india_districts_df = pd.DataFrame(clm_d)
    Top_user_india_pincodes_df = pd.DataFrame(clm_pc)

    Top_user_india_state_df.to_csv(save_path + 'top_user_india_state_df.csv')
    Top_user_india_districts_df.to_csv(save_path + 'top_user_india_districts_df.csv')
    Top_user_india_pincodes_df.to_csv(save_path + 'top_user_india_pincodes_df.csv')


agg_trans_save_location = fr'C:\Users\LENOVO\Desktop\phonephe\Extracted Files\Agg_Transactions/'
map_trans_save_location = fr'C:\Users\LENOVO\Desktop\phonephe\Extracted Files\Map\\'
top_save_location = fr"C:\Users\LENOVO\Desktop\phonephe\Extracted Files\Top\\"
#  Aggregate Transaction Function Implementation part:
# aggregate_transactions_state(agg_trans_save_location)
# agg_user_state(agg_trans_save_location)
# agg_transactions_india(agg_trans_save_location)
# agg_user_india(agg_trans_save_location)

#  Map functions Implementation Part:

# map_transactions_state(map_trans_save_location)
# map_transactions_india(map_trans_save_location)
# map_user_state(map_trans_save_location)
# map_user_india(map_trans_save_location)

#  Top functions implementation part

# top_transactions_state(top_save_location)
# top_transactions_india(top_save_location)
# top_user_state(top_save_location)
top_user_inida(top_save_location)
