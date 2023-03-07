import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np


data = pd.read_csv("data/billionaire_list_20yrs.csv")\
        .dropna()\
        .drop(['last_name', 'last_name', 'name', 'wealth_source_details', 'company', 'industry', 'headquarters', 'age', 'state', 'permanent_country', 'daily_income', 'Unnamed: 0'], axis=1)
data['birth_year'] = pd.to_datetime(data['birth_year'], format='%Y')
data['main_industry'] = data['main_industry'].str.replace('&', 'and')
data.drop_duplicates(keep='first',inplace=True)
data['countries'] = data['countries'].str.split(';',expand=True)[0]

# bilionares
bilionares = data["name_cleaned"].unique().shape[0]
st.write(f"The number of bilionares is {bilionares}")
st.metric('Bilionares', bilionares)

# bilionares by country
df = data[['countries', 'name_cleaned']].drop_duplicates(keep="first").groupby('countries').count().sort_values(by='name_cleaned', ascending=False)
df.rename(columns={'name_cleaned': 'bilionares'}, inplace=True)
st.dataframe(df.T)

# bilionares by gender
df = data[['gender', 'name_cleaned']]\
        .drop_duplicates()\
        .groupby('gender')\
        .count()\
        .reset_index()

bilionares_by_gender_fig = px.pie(df, names=df['gender'], values=df['name_cleaned'], hole=0.4, title="Bilionares by gender")

st.plotly_chart(bilionares_by_gender_fig)

# bilionares by main industry
df = data[['main_industry', 'name_cleaned']].drop_duplicates().groupby('main_industry').count().sort_values(by='name_cleaned')
df.rename(columns={'name_cleaned': 'bilionares'}, inplace=True)
bilionares_by_industry = px.bar(df, title='bilionares by industry', labels={'main_industry': 'main industry', 'value': 'number of bilionares'})
st.plotly_chart(bilionares_by_industry)

# bilionares by age
nownow = datetime.now()
data['age_in_years'] = round((nownow - data['birth_year']) / (365*np.timedelta64(1, 'D')))
df = data[['name_cleaned', 'age_in_years']].drop_duplicates(keep='first').groupby('age_in_years').count()
df.rename(columns={'name_cleaned': 'bilionares'}, inplace=True)
bilionares_by_age = px.line(df, title='Bilionares by age', labels={'age_in_years': 'age', 'value': 'number of bilionares'})
st.plotly_chart(bilionares_by_age)

# data
st.dataframe(data.head(20))