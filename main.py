import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np


data = pd.read_csv("data/billionaire_list_20yrs.csv")\
        .dropna()\
        .drop(['last_name', 'last_name', 'name', 'wealth_source_details',
               'company', 'industry', 'headquarters', 'age', 'state',
               'permanent_country', 'daily_income', 'Unnamed: 0'], axis=1)
data['birth_year'] = pd.to_datetime(data['birth_year'], format='%Y')
data['main_industry'] = data['main_industry'].str.replace('&', 'and')
data.drop_duplicates(keep='first',inplace=True)
data['countries'] = data['countries'].str.split(';',expand=True)[0]

st.title("GLOBAL BILIONARES DASHBOARD")

# side bar components
with st.sidebar:
    # select
    industries = [str(y) for y in data['main_industry'].unique()]
    industries.sort()
    all_industries = ['all industries']+industries
    industries_selected = st.selectbox('Select industries', all_industries)
    if industries_selected!='all industries':
        data = data[data['main_industry']==industries_selected]
    # slider
    years_time = [int(y) for y in data['time'].unique()]
    years_slider = st.sidebar.slider(
        'Select a range of years',
        min(years_time), max(years_time), (min(years_time), max(years_time))
    )

data['time'] = data['time'].apply(lambda t: int(t))
data = data[(data['time']>=years_slider[0]) & (data['time']<=years_slider[-1])]

with st.container():
    col1, col2, col3 = st.columns(3)
    with col1:
        # bilionares
        bilionares = data["name_cleaned"].unique().shape[0]
        st.metric('Bilionares', bilionares)

    with col2:
        # maximum annual income
        max_annual_income = data["annual_income"].max()
        st.metric('max annual income', max_annual_income)

    with col3:
        # minimum annual income
        min_annual_income = data["annual_income"].min()
        st.metric('min annual income', min_annual_income)

# bilionares by country
st.write('Bilionares by country table')
df = data[['countries', 'name_cleaned']].drop_duplicates(keep="first").groupby('countries').count().sort_values(by='name_cleaned', ascending=False)
df.rename(columns={'name_cleaned': 'bilionares'}, inplace=True)
st.dataframe(df.T.style.highlight_max(axis=0), width=2000)

col1, col2 = st.columns(2)
with col1:
    # bilionares by gender
    df = data[['gender', 'name_cleaned']]\
            .drop_duplicates()\
            .groupby('gender')\
            .count()\
            .reset_index()
    bilionares_by_gender_fig = px.pie(df, names=df['gender'], values=df['name_cleaned'], hole=0.4, title="Bilionares by gender", width=300)
    st.plotly_chart(bilionares_by_gender_fig)



with col2:
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
bilionares_by_age = px.line(df, title='Bilionares by age', labels={'age_in_years': 'age', 'value': 'number of bilionares'},  width=1000)
st.plotly_chart(bilionares_by_age)

# main industry by average annual income
df = data[['main_industry', 'annual_income']].groupby('main_industry').mean().sort_values(by='annual_income')
df.rename(columns={'main_industry': 'main industry', 'annual_income': 'average annual income'}, inplace=True)
average_annual_income = px.bar(df, title='average annual income of bilionares by main industry', orientation='h',  width=1000)
st.plotly_chart(average_annual_income)


