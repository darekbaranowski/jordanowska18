import streamlit as st
import numpy as np
import pandas as pd
import datetime


dt = pd.date_range("2024-01-01", "2024-01-30", freq="1h")

np.random.seed(0) # fix the random numbers so they are consistent
randoms = np.random.rand((len(dt)))
uptime_1 = np.ones(len(dt))
uptime_1[randoms<0.05] = 0

randoms_2 = np.random.rand((len(dt)))
uptime_2= np.ones(len(dt))
uptime_2[randoms_2<0.02] = 0

df = pd.DataFrame({"station 1 uptime": uptime_1,
                  "station 2 uptime": uptime_2},
                 index=dt)

st.line_chart(df)

temp_1 = 20 + 5 * np.sin(1 * 0.25 * np.arange(len(dt))) - randoms * 3
temp_2 = 15 + 5 * np.sin(0.25 * np.arange(len(dt))) + randoms_2 * 5
temp_1[uptime_1==0] = np.nan
temp_2[uptime_2==0] = np.nan

df_temp = pd.DataFrame({"station 1 temp (C)": temp_1,
                  "station 2 temp (C)": temp_2},
                 index=dt)



st.line_chart(df_temp)

@st.cache_data
def convert_df(df):
    return df.to_csv().encode("utf-8")

csv = convert_df(df_temp)

st.download_button(
    label="Download temperature data as CSV",
    data=csv,
    file_name="temperature.csv",
    mime="text/csv",
)
