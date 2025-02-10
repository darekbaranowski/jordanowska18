import pandas as pd
import numpy as np
import streamlit as st

def load_data():
    #loads data from google drive; url passed using st.secrets method
#data_in = pd.read_excel('liczniki_format.xlsx')
#gdrive_url ='https://docs.google.com/spreadsheets/d/12CgLOShxnppvIrDO_1VMuc2v_rGXvmaY/edit?usp=sharing&ouid=117100627735911271600&rtpof=true&sd=true'
    gdrive_url = st.secrets["gdrive_url"]
    file_id=gdrive_url.split('/')[-2]
    data_url='https://drive.google.com/uc?id=' + file_id
    data_in = pd.read_excel(data_url,sheet_name=1)
    columns = data_in.columns
    #sort the data by date
    data_in.sort_values(by=columns[0]).reset_index(drop=True,inplace=True)
    #cast data into float
    data_in=data_in.astype({columns[2]:'float64',columns[3]:'float64'})
    
    #convert data from dm3 to m3
    data_in[columns[2]] = data_in[columns[2]]/1000
    data_in[columns[3]] = data_in[columns[3]]/1000
    return data_in
#
def get_lokale_list(data_all):
    #get get list of lokals in an order
    columns = data_all.columns
    lokale = data_all[columns[1]].unique()
    lokale = sorted(lokale,key=lambda lokal: int(lokal[6:8]))
    return lokale
#
def get_lokal(data_all,lokal):
    #get df with data corresponding to a single lokal
    #if number of records is 1 then returns None
    columns = data_all.columns
    #get subset for given lokal and drop Lokal column
    data_lokal = data_all[data_all[columns[1]] == lokal].drop([columns[1]],axis='columns')
    if (len(data_lokal)>1):
        data_lokal_index = data_lokal.index
        #differentiate the data
        diff_data_lokal = data_lokal.diff()
        #drop the first row cause it is all NaN
        diff_data_lokal.drop(index=diff_data_lokal.index[0],axis=0,inplace=True)
        list_lokal = []
        for index in diff_data_lokal.index: #for each row
            #normalize Odczyty to match 30 days
            goraca_zuzycie = np.round(diff_data_lokal[columns[2]].loc[index]/diff_data_lokal[columns[0]].loc[index].days*30,decimals=2) #in m3
            zimna_zuzycie = np.round(diff_data_lokal[columns[3]].loc[index]/diff_data_lokal[columns[0]].loc[index].days*30,decimals=2) #in m3
            #e
            date_end = data_lokal[columns[0]].loc[index]
            #find previous index in subset dataframe
            idata_lokal_index = np.where(data_lokal_index == index)[0][0]
            date_start = data_lokal[columns[0]].loc[data_lokal_index[idata_lokal_index-1]]
            list_lokal.append([date_start,goraca_zuzycie,zimna_zuzycie])
            list_lokal.append([date_end,goraca_zuzycie,zimna_zuzycie])
        dflokal = pd.DataFrame(data=list_lokal,columns=['Data','Woda Goraca','Woda Zimna'])
        return dflokal
    else:
        return None
#
def get_period_value(data_all,idx = 1):
    #get df with data for all lokals for a given period. 
    #by default it gets last period (idx = 1) but can be any period (e.g. one before last, idx = 2) ect as long as record exists!
    lokale = get_lokale_list(data_all)
    period_value_list = []
    for lokal in lokale:
        df = get_lokal(data_all,lokal)
        if (df is not None):
            period_start = df['Data'].iloc[-idx-1].date()
            period_end = df['Data'].iloc[-idx].date()
            goraca = df['Woda Goraca'].iloc[-idx]
            zimna = df['Woda Zimna'].iloc[-idx]
            period_value_list.append([lokal,period_start,period_end,goraca,zimna])
    df_last_value = pd.DataFrame(data=period_value_list,columns=(['Lokal','Poczatek Okresu','Koniec Okresu','Woda Goraca',
                                                     'Woda Zimna']))
    return df_last_value
#
def print_lokal(data_all,lokal):
    #prints all data for a given lokal as a line chart
    data_lokal = get_lokal(data_all,lokal)
    st.line_chart(data_lokal,x='Data',y=['Woda Goraca','Woda Zimna'],x_label='Data',y_label='Zuzycie [m3]')