import pandas as pd
import streamlit as st
import wbgapi as wb
from newsapi import NewsApiClient
from pandas.io.json import json_normalize
#import pycountry
import plotly.express as px
#import world_bank_data as wb1
import plotly.graph_objects as go
import altair as alt
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, CustomJS, formatters
from bokeh.models import DataTable, TableColumn, HTMLTemplateFormatter
import requests
import re
import plotly.graph_objects as go
import datetime

def news():

    news_message_temp= """ 
    <div style="background-color:lightblue;overflow-x: auto; padding:10px;border-radius:20px;margin:15px;">
    <p><a href = {} style="color:#000000;text-decoration: none;"target="_blank"> {}</a></p>
    </div>
    """
    temp="""                
            <p style="color:black;font-size: 10px">;
            <%= value %>
            </p>
            """
    formatter =  HTMLTemplateFormatter(template=temp)

    def top_headlines(country,category):
        top_headlines =newsapi.get_top_headlines(category = category,language='en',country=country)     
        top_headlines=pd.json_normalize(top_headlines['articles'])   
        df=top_headlines[["url","publishedAt","source.name","author","title"]]        

        n1,n2 = st.columns([5,5])
        with n1:
            st.markdown(news_message_temp.format(df['url'][0],df['title'][0]),unsafe_allow_html=True)
            st.markdown(news_message_temp.format(df['url'][1],df['title'][1]),unsafe_allow_html=True)
            st.markdown(news_message_temp.format(df['url'][2],df['title'][2]),unsafe_allow_html=True)
            st.markdown(news_message_temp.format(df['url'][3],df['title'][3]),unsafe_allow_html=True)
				
        with n2:
            st.markdown(news_message_temp.format(df['url'][4],df['title'][4]),unsafe_allow_html=True)
            st.markdown(news_message_temp.format(df['url'][5],df['title'][5]),unsafe_allow_html=True)
            st.markdown(news_message_temp.format(df['url'][6],df['title'][6]),unsafe_allow_html=True)
            st.markdown(news_message_temp.format(df['url'][7],df['title'][7]),unsafe_allow_html=True)


        formatter =  HTMLTemplateFormatter(template=temp)
        cds = ColumnDataSource(df)
        columns = [TableColumn(field= 'title', title='Article Title', width=600,formatter =formatter),
						#TableColumn(field ='author',title = 'Author',width = 100),
						#TableColumn(field ='source.name',title = 'Source',width = 100),
						#TableColumn(field= 'publishedAt', title='Published At', width=100),
						TableColumn(field='url',title='Url Link',formatter=HTMLTemplateFormatter(template='<a href="<%= url%>"target="_blank"><%= value %></a>'),width=400)]
        p = DataTable(source=cds, columns=columns, css_classes=["my_table"],width= 1000)
			#st.bokeh_chart(p)
        show_data = st.checkbox("See more Stories")
        if show_data:
            st.bokeh_chart(p)


    def text_from_urls(query,start_date,end_date):
        while True:
            try:
                all_articles = newsapi.get_everything(q=query,language='en',sort_by='relevancy',from_param= start_date,to= end_date)
                break
            except ValueError:
                print("Oops!  That was no valid number.  Try again...")  
        d= pd.json_normalize(all_articles['articles'])
        n1,n2 = st.columns([5,5])
        if d.shape[0] > 1: 
            df =d[["url","publishedAt","source.name","author","title"]]
            with n1:
                st.markdown(news_message_temp.format(df['url'][0],df['title'][0]),unsafe_allow_html=True)
                st.markdown(news_message_temp.format(df['url'][1],df['title'][1]),unsafe_allow_html=True)
                st.markdown(news_message_temp.format(df['url'][2],df['title'][2]),unsafe_allow_html=True)
                st.markdown(news_message_temp.format(df['url'][3],df['title'][3]),unsafe_allow_html=True)
					
            with n2:
                st.markdown(news_message_temp.format(df['url'][4],df['title'][4]),unsafe_allow_html=True)
                st.markdown(news_message_temp.format(df['url'][5],df['title'][5]),unsafe_allow_html=True)
                st.markdown(news_message_temp.format(df['url'][6],df['title'][6]),unsafe_allow_html=True)
                st.markdown(news_message_temp.format(df['url'][7],df['title'][7]),unsafe_allow_html=True)
            cds = ColumnDataSource(df)
            columns = [TableColumn(field= 'title', title='Article Title', width=600,formatter =formatter),
					#TableColumn(field ='author',title = 'Author',width = 100),
					#TableColumn(field ='source.name',title = 'Source',width = 100),
					#TableColumn(field= 'publishedAt', title='Published At', width=100),
					TableColumn(field='url',title='Url Link',formatter=HTMLTemplateFormatter(template='<a href="<%= url%>"target="_blank"><%= value %></a>'),width=400)]
            p = DataTable(source=cds, columns=columns, css_classes=["my_table"],width= 1000)
            shows_data = st.checkbox("See more Stories")
            if shows_data:
                st.bokeh_chart(p)
        else:
                st.write("Oops!  There is no stories available at the moment.  Try another search word...")

    
    newsapi = NewsApiClient(api_key='5515e5abf50847d191cb32618e9597c1')
    page = st.sidebar.selectbox("", ["Today's Stories", "Search for Stories"],key = 21)
    if page == "Today's Stories":
        st.header("Today's Stories")
        country = st.sidebar.selectbox("", ("South Africa","USA","France","Germany"))
        countries = {"South Africa":"za","USA":"us","France":"fr","Germany":"gb"} 
        st.subheader(country)
        category= st.sidebar.selectbox("",["Business","Entertainment","Sports","General","Science","Technology"])
        cat = {"Business":"business","Entertainment":"entertainment","Sports":"sports","General":"general","Science":"science","Technology":"technology" }
        top_headlines(countries[country],cat[category])
    elif page == "Search for Stories":
        st.header("Search for Stories")
        query = st.sidebar.text_input("Enter Topic of choice",'Army')
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        start_date = st.sidebar.date_input('Start date', today)
        end_date = st.sidebar.date_input('End date', tomorrow)
        text_from_urls(query,start_date,end_date)
				  
		