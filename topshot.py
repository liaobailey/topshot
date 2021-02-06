import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import altair as alt
import unidecode

st.title("NBA Top Shot Data Visualization, Updated Daily")

st.subheader("Top 10 Transaction Value as of 2/6/2021")

@st.cache(persist = True)
def load_data(csv, nrows):
    data = pd.read_csv(csv, nrows = nrows)
    return data

raw = load_data('master.csv', 900000)
new = raw.drop(columns = ['Unnamed: 0'])

data = new[new['Set'].notnull()]
data['USD'] = data['USD'].map(lambda x: x.replace('$', ''))
data['USD'] = data['USD'].map(lambda x: x.replace(',', ''))
data['USD'] = data['USD'].map(lambda x: float(x))

data.columns = ['Sold', 'Player', 'Set', 'Team', 'Category', 'Price', 'USD', 'Serial', 'Seller', 'Buyer', 'Month']

data['Player'] = data['Player'].map(lambda x: x.replace("\xa0", " "))
data['Player'] = data['Player'].map(lambda x: unidecode.unidecode(x))


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
    x=alt.X('Month', sort = ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May','Jun']),
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
    x=alt.X('Month', sort = ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May','Jun']),
    y='USD',
    color='Category',
    strokeDash='Category'
).properties(
    width=900,
    height=600
))

st.subheader("Price change for most traded cards - Last 500 Transactions")

display_3_pre = data.groupby(['Player', 'Set', 'Team', 'Category']).agg({
    'Buyer':'count'
}).reset_index().sort_values('Buyer', ascending = False)

lft = display_3_pre.head(10)
merge = pd.merge(data, lft, on = ['Player', 'Set', 'Team', 'Category'], how = 'left')
display_3 = merge[merge['Buyer_y'].notnull()]
display_3['unique'] = display_3['Player'] + ': ' + display_3['Set'] + ' - ' + display_3['Category']
lst = display_3['unique'].unique()

option = st.selectbox('Choose Moment',(lst[0], lst[1], lst[2], lst[3], lst[4], lst[5], lst[6], lst[7], lst[8], lst[9]))

d_3 = display_3[(display_3['Player'] == option.split(':')[0]) & (display_3['Set'] == option.split(': ')[1].split(' -')[0]) & (display_3['Category'] == option.split('- ')[1])]
dis_3 = d_3.reindex(index=d_3.index[::-1])

displ_3 = dis_3[-500:].reset_index().reset_index().rename(columns = {'level_0': 'tranx'})
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

st.subheader("Price change for Biggest Delta in value cards - Last 500 Transactions")

display_4_pre = data.groupby(['Player', 'Set', 'Team', 'Category']).agg({
    'USD':['min', 'max']
}).reset_index()

display_4_pre.columns = ['Player', 'Set', 'Team', 'Category', 'min', 'max']

display_4_pre['diff'] = display_4_pre['max'] - display_4_pre['min']
rgt = display_4_pre.sort_values('diff', ascending = False).head(10)
merge_2 = pd.merge(data, rgt, on = ['Player', 'Set', 'Team', 'Category'], how = 'left')

display_4 = merge_2[merge_2['diff'].notnull()]
display_4['unique'] = display_4['Player'] + ': ' + display_4['Set'] + ' - ' + display_4['Category']
lst_2 = display_4['unique'].unique()

option_2 = st.selectbox('Choose Moment ',(lst_2[0], lst_2[1], lst_2[2], lst_2[3], lst_2[4], lst_2[5], lst_2[6], lst_2[7], lst_2[8], lst_2[9]))

d_4 = display_4[(display_4['Player'] == option_2.split(':')[0]) & (display_4['Set'] == option_2.split(': ')[1].split(' -')[0]) & (display_4['Category'] == option_2.split('- ')[1])]
dis_4 = d_4.reindex(index=d_4.index[::-1])

displ_4 = dis_4[-500:].reset_index().reset_index().rename(columns = {'level_0': 'tranx'})
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

st.subheader("Find Last 500 Tranx from any play")

player = st.text_input('Input full player name:', 'Luka Doncic')
pack = st.selectbox('Choose Pack', list(data['Set'].unique()))
cat = st.selectbox('Choose Play', list(data['Category'].unique()))
year = st.text_input('Choose Year (format 2020-21):', '2019-20')

d_5 = data[(data['Player'].str.lower().str.contains(player.lower())) & (data['Set'] == pack) & (data['Category'] == cat) & (data['Player'].str.contains(year))]
dis_5 = d_5.reindex(index=d_5.index[::-1])
displ_5 = dis_5[-500:].reset_index().reset_index().rename(columns = {'level_0': 'tranx'})
displ_5['tranx'] = displ_5['tranx'] + 1

st.write(alt.Chart(displ_5).mark_circle(size=60).encode(
    x='tranx',
    y='USD',
    color='Set',
    tooltip=['Player', 'Set', 'Category', 'tranx', 'USD']
).interactive().properties(
    width=900,
    height=600
))
