# import libraries
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter


# load data
df = pd.read_csv("C:/Users/u/Ngee Ann/Project/Documents/HDB resale/resale-flat-prices-based-on-registration-date-from-jan-2017-onwards.csv")
# to split month column into year and month
df['yr'] = df['month'].str.split('-').str[0]
df['mth'] = df['month'].str.split('-').str[1]
# combine yr and mth column and convert into datetime
df['period'] = pd.to_datetime(df['yr'].astype(str) + df['mth'], format='%Y%m')
# remove 'month' 'yr' and 'mth' columns
df = df.drop(['month', 'yr', 'mth'], axis=1)

# shift column 'period' to first position
first_column = df.pop('period')
df.insert(0, 'period', first_column)

data = df.groupby('period', as_index=False)['resale_price'].mean()

# st.set_page_config(page_title="HDB resale price", page_icon="C:/Users/u/Ngee Ann/Project/HDB_icon.png")
image = Image.open("C:/Users/u/Ngee Ann/Project/HDB_icon.png").resize((200, 40))

st.image(image)

# set the page title
now = df['period'].iloc[-1].strftime("%B %Y")
title = 'HDB resale from January 2017 to ' + now
#title = 'HDB resale from January 2017 to April 2022'
st.title(title)
st.markdown('[Source](https://data.gov.sg/dataset/resale-flat-prices)')
st.write('updated as at 2 August 2022')


# chart 1
# plots the graph
st.header("Overall average resale price")
fig = px.line(data, x='period', y='resale_price')
st.plotly_chart(fig, use_container_width=True)

#data_df = df.groupby('period', as_index=False).agg(no_of_unit=('resale_price','count'), Avg_resale_price =('resale_price','mean'))
#fig, ax = plt.subplots(figsize=(10, 5))
#ax1 = sns.lineplot(data=data_df, color="g")
#ax2 = plt.twinx()
#sns.barplot(data=data_df, y="no_of_unit", x="period", ax=ax2)
#st.pyplot(ax)

#data_df = df.groupby('period', as_index=False).agg(no_of_unit=('resale_price','count'))
#fig = px.bar(x=data_df['period'], y=data_df['no_of_unit'])

#fig, ax = plt.subplots(figsize=(10, 5))
#ax1 = sns.lineplot(data=data_df, color="g")
#ax2 = plt.twinx()
#sns.barplot(data=data_df, y="no_of_unit", x="period", ax=ax2)
#st.pyplot(ax)

# chart 2
# plot the graph
st.header("Number of resale flat sold")
data_flat_q = df.groupby(['period', 'flat_type'], as_index=False)['resale_price'].count()
data_flat_q = data_flat_q.rename(columns = {'resale_price':'no_of_unit'})
fig1 = px.bar(data_frame=data_flat_q,x='period',y='no_of_unit', color='flat_type')
st.plotly_chart(fig1)

# Chart 3
#st.title("Average resale price for town and/or flat_type")
#st.write("Please select town and/or flat_type for average selling price from Jan 2017 to ", now)

# chart 4
# plots the graph
#st.write("Average resale price by town")
#town_selected = st.multiselect("Town: ", df['town'].unique().tolist())
#data_town = df.groupby(['period', 'town'], as_index=False)['resale_price'].mean()
#data_town_selected = data_town.loc[data_town['town'].isin(town_selected)]

#if len(town_selected) == 0:
#    pass
#else:
#    fig = px.line(data_town_selected, x='period', y='resale_price', color='town')
#    st.plotly_chart(fig, use_container_width=True)


# Chart 5
# plots the graph
st.header("Average resale price by flat type and town")
st.subheader('Note')
st.write('1. Please select the flat type and the town area for resale price analysis')
st.write('2. You are only allow to select ONE flat type. Multiple selection for town are allowed')
flat_type = st.radio("Flat type: ", df['flat_type'].unique().tolist(), index=False)
town_area = st.multiselect("Town area: ", df['town'].unique().tolist())

data_flat_town = df.groupby(['period', 'flat_type','town'], as_index=False)['resale_price'].mean()
data_flat_town_selected = data_flat_town.loc[data_flat_town['town'].isin(town_area) & data_flat_town['flat_type'].isin([flat_type])]

if len(town_area) == 0 or len(flat_type) == 0:
    pass
else:
    fig = px.line(data_flat_town_selected, x='period', y='resale_price', color='town')
    st.plotly_chart(fig, use_container_width=True)



# streamlit run HDB_resaleprice.py --server.port 5992

# map
# source: https://stackoverflow.com/questions/69854674/python-generate-lat-long-points-from-address
#address = st.text_input("Address")
#if len(address) == 0:
#    pass
#else:
#    geolocator = Nominatim(user_agent="myApp")
#    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
#    location = geolocator.geocode(address)
#    lat, lon = location.latitude, location.longitude
#    data_of_map = pd.DataFrame({'lat': [location.latitude], 'lon': [location.longitude]})
#    st.map(data_of_map, zoom=12)

# street = st.sidebar.text_input("Street", "75 Bay Street")
# city = st.sidebar.text_input("City", "Toronto")
# province = st.sidebar.text_input("Province", "Ontario")
# country = st.sidebar.text_input("Country", "Canada")
# geolocator = Nominatim(user_agent="GTA Lookup")
# geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
# location = geolocator.geocode(street+", "+city+", "+province+", "+country)
# lat = location.latitude
# lon = location.longitude
# map_data = pd.DataFrame({'lat': [lat], 'lon': [lon]})
# st.map(map_data,zoom=10)


# source: https://www.vantage-ai.com/en/blog/how-to-build-and-host-beautiful-web-based-python-apps-using-streamlit
# source: https://www.datacamp.com/tutorial/streamlit#how-to-run-your-streamlit-code

# source: https://datatofish.com/install-package-python-using-pip/

# go to venn environment
# cd venv/Scripts
# then press Enter
# activate.bat
# source: https://stackoverflow.com/questions/22288569/how-do-i-activate-a-virtualenv-inside-pycharms-terminal
# go back to orginal folder
# cd..


# streamlit run resale_price.py --server.port 5992
