import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import altair as alt

st.title("NBA Top Shot Data Visualization")

st.subheader("Top 10 Transaction Value as of 1/15/2021")

@st.cache(persist = True)
def load_data(csv, nrows):
    data = pd.read_csv(csv, nrows = nrows)
    return data

raw = load_data('topshot_115.csv', 200000)
new = raw.drop(columns = ['Unnamed: 0', 'Unnamed: 0.1'])

data = new[new['Set'].notnull()]
data['USD'] = data['USD'].map(lambda x: x.replace('$', ''))
data['USD'] = data['USD'].map(lambda x: x.replace(',', ''))
data['USD'] = data['USD'].map(lambda x: float(x))

data.columns = ['Month', 'Player', 'Set', 'Team', 'Category', 'Price', 'USD', 'Serial', 'Seller', 'Buyer']

display_1 = data.sort_values('USD', ascending = False)[['Player', 'Set','Team','Category','Price']].head(10).set_index('Player')

st.table(display_1)

st.subheader("Number of Transactions by Sets - Top 10")

display_2 = data.groupby('Set').count().reset_index()[['Set','Buyer']]
display_2.sort_values('Buyer',  ascending = False, inplace = True)

display_2 = display_2.head(10)

st.write(alt.Chart(display_2).mark_bar().encode(
    x=alt.X('Set', sort=None),
    y='Buyer',
).properties(
    width=900,
    height=600
))

st.subheader("Average price of Transactions by Sets - Top 10")

display_3 = data.groupby('Set').agg({
    'USD': 'mean'
}).reset_index()
display_3.sort_values('USD',  ascending = False, inplace = True)
display_3 = display_3.head(10)

st.write(alt.Chart(display_3).mark_bar().encode(
    x=alt.X('Set', sort=None),
    y='USD',
).properties(
    width=900,
    height=600
))

st.subheader("Average price of Transactions by Month")

group = data.groupby(['Month', 'Category']).agg({
    'USD':'mean'
}).reset_index()

st.write(alt.Chart(group).mark_line().encode(
    x=alt.X('Month', sort=['Current Month', '1 month ago', '2 months ago', '3 months ago', '4 months ago', '5 months ago']),
    y='USD',
    color='Category',
    strokeDash='Category'
).properties(
    width=900,
    height=600
))

st.subheader("Max price of Transactions by Month")

group_2 = data.groupby(['Month', 'Category']).agg({
    'USD':'max'
}).reset_index()

st.write(alt.Chart(group_2).mark_line().encode(
    x=alt.X('Month', sort=['Current Month', '1 month ago', '2 months ago', '3 months ago', '4 months ago', '5 months ago']),
    y='USD',
    color='Category',
    strokeDash='Category'
).properties(
    width=900,
    height=600
))

st.subheader("Price change for most traded cards - Last 100 Transactions")

display_3_pre = data.groupby(['Player', 'Set', 'Team', 'Category']).agg({
    'Buyer':'count'
}).reset_index().sort_values('Buyer', ascending = False)

lft = display_3_pre.head(10)
merge = pd.merge(data, lft, on = ['Player', 'Set', 'Team', 'Category'], how = 'left')
display_3 = merge[merge['Buyer_y'].notnull()]
display_3['Player'] = display_3['Player'].map(lambda x: x.replace("\xa0", " "))
display_3['unique'] = display_3['Player'] + ': ' + display_3['Set']
lst = display_3['unique'].unique()

option = st.selectbox('Choose Moment',(lst[0], lst[1], lst[2], lst[3], lst[4], lst[5], lst[6], lst[7], lst[8], lst[9]))

d_3 = display_3[(display_3['Player'] == option.split(':')[0]) & (display_3['Set'] == option.split(': ')[1])]

dis_3 = d_3.reindex(index=d_3.index[::-1])

displ_3 = dis_3[-100:].reset_index().reset_index().rename(columns = {'level_0': 'tranx'})
displ_3['tranx'] = displ_3['tranx'] + 1

st.write(alt.Chart(displ_3).mark_circle(size=60).encode(
    x='tranx',
    y='USD',
    color='Set',
    tooltip=['Player', 'Set', 'Category', 'tranx', 'USD']
).interactive().properties(
    width=900,
    height=600
))

st.subheader("Price change for Biggest Delta in value cards - Last 100 Transactions")

display_4_pre = data.groupby(['Player', 'Set', 'Team', 'Category']).agg({
    'USD':['min', 'max']
}).reset_index()

display_4_pre.columns = ['Player', 'Set', 'Team', 'Category', 'min', 'max']

display_4_pre['diff'] = display_4_pre['max'] - display_4_pre['min']
rgt = display_4_pre.sort_values('diff', ascending = False).head(10)
merge_2 = pd.merge(data, rgt, on = ['Player', 'Set', 'Team', 'Category'], how = 'left')

display_4 = merge_2[merge_2['diff'].notnull()]
display_4['Player'] = display_4['Player'].map(lambda x: x.replace("\xa0", " "))
display_4['unique'] = display_4['Player'] + ': ' + display_4['Set']
lst_2 = display_4['unique'].unique()

option_2 = st.selectbox('Choose Moment ',(lst_2[0], lst_2[1], lst_2[2], lst_2[3], lst_2[4], lst_2[5], lst_2[6], lst_2[7], lst_2[8], lst_2[9]))

d_4 = display_4[(display_4['Player'] == option_2.split(':')[0]) & (display_4['Set'] == option_2.split(': ')[1])]

dis_4 = d_4.reindex(index=d_4.index[::-1])

displ_4 = dis_4[-100:].reset_index().reset_index().rename(columns = {'level_0': 'tranx'})
displ_4['tranx'] = displ_4['tranx'] + 1

st.write(alt.Chart(displ_4).mark_circle(size=60).encode(
    x='tranx',
    y='USD',
    color='Set',
    tooltip=['Player', 'Set', 'Category', 'tranx', 'USD']
).interactive().properties(
    width=900,
    height=600
))
