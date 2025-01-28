import pandas as pd
import numpy as np
import streamlit as st
#%%
#load data
#data_in = pd.read_excel('liczniki_format.xlsx')
gdrive_url ='https://docs.google.com/spreadsheets/d/12CgLOShxnppvIrDO_1VMuc2v_rGXvmaY/edit?usp=sharing&ouid=117100627735911271600&rtpof=true&sd=true'
file_id=gdrive_url.split('/')[-2]
data_url='https://drive.google.com/uc?id=' + file_id
data_in = pd.read_excel(data_url)
#convert data from dm3 to m3
data_in['GoracaWoda[m3]'] = data_in['GoracaWoda[m3]']/1000
data_in['ZimnaWoda[m3]'] = data_in['ZimnaWoda[m3]']/1000
#%%
def get_lokale_list(data_all):
    
    lokale = data_all['Lokal'].unique()
    lokale = sorted(lokale,key=lambda lokal: int(lokal[6:8]))
    return lokale
#%
def get_lokal(data_all,lokal):
    columns = data_all.columns
    #get subset for given lokal and drop Lokal column
    data_lokal = data_all[data_all["Lokal"] == lokal].drop(["Lokal"],axis='columns')
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
def last_value(data_all):
    #st.write('Im here')
    lokale = get_lokale_list(data_all)
    last_value_list = []
    for lokal in lokale:
        #st.write(lokal)
        df = get_lokal(data_all,lokal)
        #st.write(df)
        if (df is not None):
            period_start = df['Data'].iloc[-2].date()
            period_end = df['Data'].iloc[-1].date()
            goraca = df['Woda Goraca'].iloc[-1]
            zimna = df['Woda Zimna'].iloc[-1]
            last_value_list.append([lokal,period_start,period_end,goraca,zimna])
    df_last_value = pd.DataFrame(data=last_value_list,columns=(['Lokal','Poczatek Okresu','Koniec Okresu','Woda Goraca',
                                                     'Woda Zimna']))
    return df_last_value
def print_lokal(data_all,lokal):
    data_lokal = get_lokal(data_all,lokal)
    st.line_chart(data_lokal,x='Data',y=['Woda Goraca','Woda Zimna'],x_label='Data',y_label='Zuzycie [m3]')

#%%
st.title('Jordanowska 18, zuzycie wody')
# #ostatni okres
dflastvalue = last_value(data_in)
st.write('Ostatni Okres: Srednie zuzycie w ciagu 30 dni')
st.dataframe(dflastvalue,hide_index=True)
st.bar_chart(data=dflastvalue,x='Lokal',y=['Woda Goraca','Woda Zimna'],x_label='Lokal',y_label='Zuzycie [m3]',stack=False)

lokale = get_lokale_list(data_in)

lokal = st.selectbox('Wybierz lokal',lokale)
#st.write('Wybrano lokal: ',select_lokal)
#lokal = select_lokal
st.write('Wykres '+lokal)
print_lokal(data_in,lokal)   