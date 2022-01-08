import pandas as pd
import streamlit as st
import wbgapi as wb
from newsapi import NewsApiClient
from pandas.io.json import json_normalize
from bs4 import BeautifulSoup
import pycountry
import plotly.express as px
import world_bank_data as wb1
import plotly.graph_objects as go
import altair as alt
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, CustomJS, formatters
from bokeh.models import DataTable, TableColumn, HTMLTemplateFormatter
from newsapi import NewsApiClient
import requests
import re
import plotly.graph_objects as go
import string
import io
import re
import nltk
import lxml
#from acledd import *

@st.cache
def get_data():
    df = pd.read_csv('Africa_2010-2021.csv')
    names = {'EVENT_DATE': 'Date', 'YEAR':'Year','COUNTRY':'Country','LOCATION':'Location','SUB_EVENT_TYPE': 'Event', 'ACTOR1':'Perpetrator', "ACTOR2": 'Actor Two',"FATALITIES":'Fatalities','NOTES':'Event Desc'}
    df.rename(columns=names,inplace=True)
    return df
df = get_data()
Perpetrator = st.sidebar.selectbox("Select Perpetrator:", df['Perpetrator'].unique())
year = st.sidebar.selectbox("Select Year:", df['Year'].unique())
Boko_haram = df[df['Perpetrator']== Perpetrator]
Boko_haram_year = Boko_haram[Boko_haram ['Year']== year]
fig = go.Figure(go.Scattermapbox(
    mode = "markers",
    lon = Boko_haram_year['LONGITUDE'],
    lat = Boko_haram_year['LATITUDE'],
    marker = {'size': 10}))
fig.update_layout(
    margin ={'l':0,'t':0,'b':0,'r':0},
    mapbox = {
        'center': {'lon': 10, 'lat': 10},
        'style': "carto-positron",
        'center': {'lon': Boko_haram['LONGITUDE'].iloc[0], 'lat': Boko_haram['LATITUDE'].iloc[0]},
        'zoom': 3})
st.plotly_chart(fig)


