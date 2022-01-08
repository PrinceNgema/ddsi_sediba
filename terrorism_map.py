import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
from terrorism_graph import *
import sqlite3 
import datetime

conn = sqlite3.connect('comment.db',check_same_thread=False)
c = conn.cursor()
def add_data(author,title,article,postdate):
        c.execute('INSERT INTO blogtable(author,title,article,postdate) VALUES (?,?,?,?)',(author,title,article,postdate))
        conn.commit()
def add_comment():
        #st.subheader("Add Comments")
        #create_table()
        with st.sidebar.container():
            blog_author = st.session_state['name']
            blog_title = st.text_input("Enter Comment Title")
            blog_article = st.text_area("Write Comment Here",height=200)
            now  = datetime.datetime.now()
            blog_post_date = now.strftime("%Y-%m-%d %H:%M:%S")
            if st.button("Add"):
                add_data(blog_author,blog_title,blog_article,blog_post_date)
                st.success("Comments:{} saved".format(blog_title))

@st.cache(allow_output_mutation=True)
def terrorism_data():
    df = pd.read_pickle('Terrorism 2000-2019.pkl')
    return df

def terror_map():
    df = terrorism_data()
    #with st.sidebar.container():
        #st.sidebar.subheader('GLOBAL TERRORISM ANALYSIS')
        #st.sidebar.image('terror.jpg', width = 300)
        #page = st.sidebar.selectbox(' ',['Home','About'])
    #if page == 'Home':
    tab = st.sidebar.selectbox("",["Analytics","Map","Forecasting"])
    if tab == "Map":
        st.subheader('Global Terrorism Deaths Per Year')
        lst = sorted(df['Country'].unique().tolist()) 
        lst.insert(0,'Worldwide')
        country = st.sidebar.selectbox('',lst,key = 1)
        if country == "Worldwide":
            data = df
            zoom = 1.5
            
        else:
            data = df[df['Country'] == country]
            zoom = 4
        st.write(country)
        deaths = data.groupby(['Year','City'])['Deaths'].transform('sum')
        data['deaths'] = deaths
        data['deaths'].fillna(0,inplace = True)
        fig = px.scatter_mapbox(data,
                    lat="Latitude" ,
                    lon="Longitude",
                    size = 'deaths',
                    animation_frame='Year',
                    color_continuous_scale=px.colors.sequential.Rainbow,
                    mapbox_style='carto-positron',
                    size_max=50,width =1100, height = 600,
                    hover_data= {
                        "Year": True,
                        'Perpetrator Name': True,
                        'Latitude':False,
                        'Longitude':False,
                        'Deaths':False,
                        },
                        hover_name = 'City',
                    zoom = zoom)
            #fig.update_traces(mode="markers", hovertemplate=None)
        #fig.update_layout(mapbox_style = "open-street-map")
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
        showlegend = False)
        fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1000
        st.plotly_chart(fig)
        comm6 = st.sidebar.checkbox("Add Comment")
        if comm6:
            add_comment()
    if tab == "Analytics":
        graphs()

        

    
    


    
    