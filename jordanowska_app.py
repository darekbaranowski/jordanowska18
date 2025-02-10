# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 11:10:53 2025

@author: dbaranowski
"""

import streamlit as st
from utils.utils import *

def main():
    data_in = load_data()
    st.title('Jordanowska 18, zuzycie wody')
#    #ostatni okres
    df_period_value = get_period_value(data_in)
    st.write('Ostatni Okres: Srednie zuzycie w ciagu 30 dni')
    st.write('Tabela: Szacowane zuzycie wody na lokal w casie 30 dni')
    st.dataframe(df_period_value,hide_index=True)
    st.write('Histogram: Szacowane zuzycie wody na lokal w czasie 30 dni')
    st.bar_chart(data=df_period_value,x='Lokal',y=['Woda Goraca','Woda Zimna'],x_label='Lokal',y_label='Zuzycie [m3]',stack=False)
    #
    lokale = get_lokale_list(data_in)
    #
    lokal = st.selectbox('Wybierz lokal',lokale)
    st.write('Wykres zuzycia wody w czasie w '+lokal)
    print_lokal(data_in,lokal)
#
if __name__ == '__main__':
    main()
