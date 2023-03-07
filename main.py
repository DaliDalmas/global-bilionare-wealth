import streamlit as st
import pandas as pd

data = pd.read_csv('data/billionaire_list_20yrs.csv')
st.dataframe(data.head(20))