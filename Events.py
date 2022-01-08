import pandas as pd
import streamlit as st
import wbgapi as wb
from pandas.io.json import json_normalize
import plotly.express as px
import plotly.graph_objects as go
import plotly.graph_objects as go
from acledd_summaries import *
import datetime
import sqlite3 
from datetime import date

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


def track_events():
    track = st.sidebar.selectbox('',['Conflict Events'])
    if track == "Conflict Events":
        @st.cache
        def get_data():
            df = pd.read_csv('Africa_2010-2021.csv')
            names = {'EVENT_DATE': 'Date', 'YEAR':'Year','COUNTRY':'Country','LOCATION':'Location','SUB_EVENT_TYPE': 'Event', 'ACTOR1':'Perpetrator', "ACTOR2": 'Actor Two',"FATALITIES":'Fatalities','NOTES':'Event Desc'}
            df.rename(columns=names,inplace=True)
            return df
        stratejic_dev = """ACLED defines 'Strategic developments' as contextually important events which may 
        contribute to a state's political disorder and/or may trigger future events. It includes 
        arrests of key political figures, mass arrests, rallies, peace talks, mass hunger strikes, 
        other strikes (e.g. 'dead city'), recruitment drives, looting, destruction of property, etc. It 
        can also include instances in which bombs are diffused prior to an attack, or when a bomb 
        is accidentally detonated earlier than intended. While it is rare for fatalities to be reported 
        as a result of such events, they can occur in certain cases, such as the suspicious death of
        a high-ranking official, accidental detonation of a bomb resulting in the bomber being 
        killed, etc."""
        battles = """ACLED defines a battle as “a violent interaction between two politically organized 
        armed groups at a particular time and location.” Typically these interactions occur 
        between government militaries/militias and rebel groups/factions within the context of 
        a civil war. However, these interactions also include militia violence, rebel on rebel 
        violence and military on military violence. There is no causality minimum necessary 
        for inclusion.
        """

        explosions_or_remote_violence = """This refers to events where an explosion, bomb  or other	
        explosive device was used to engage	in conflict. They include one-sided violent events in	
        which the tool for engaging in conflict creates asymmetry by taking away the ability of
        the target to engage or	defend	themselves and their location"""

        violence_against_citizens = """ ACLED defines 'Violence against civilians' as violent events where
        an organised armed group deliberately inflicts violence upon unarmed non-combatants.
        By definition, civilians are unarmed and cannot engage in political violence
        """
        riots =""" ACLED defines 'Riots" as a public demonstration by a spontaneously organized group that uses
        violence"""

        protests = """Acled defines 'Protests' as a  public demonstration in which the participants do not engage in violence, though violence may be used against them """

        df = get_data()
        countries = df['Country'].unique().tolist()
        countries.append('Africa')
        default_ix = countries.index('Africa')
        country = st.sidebar.selectbox("", countries,index= default_ix)
        #categories = st.sidebar.selectbox("", df['EVENT_TYPE'].unique())
        if country == 'Africa':
            events_data = df[df['Country'].isin(df['Country'].unique().tolist())]
            zoom = 2
        else:
            events_data = df[df['Country'] == country]
            zoom = 4
        #strategic_development = events_data[events_data['EVENT_TYPE']==categories]
        #strategic_data = strategic_development[['EVENT_DATE','YEAR','COUNTRY','ADMIN1','LOCATION','ADMIN2','SUB_EVENT_TYPE', 'ACTOR1','ACTOR2','NOTES','FATALITIES','LATITUDE','LONGITUDE']]
        #strategic_development['Number of Occurences'] = strategic_development.groupby(['Location','Event'])['Event'].transform('count')
        # KPIS
        st.header(country)
        c1,c2,c3,c4,c5,c6= st.columns([1,1,1,1,1,1])
        col =  [c1,c2,c3,c4,c5,c6]
        current_year = events_data['Year'].max()
        previous_year = events_data['Year'].max()-1
        a = events_data['EVENT_TYPE'].unique().tolist()
        for i in range(len(a)):
            strategic_dev = events_data[events_data['EVENT_TYPE'] == a[i]]
            strategic_dev_cur = strategic_dev[strategic_dev['Year'] == current_year].shape[0]
            strategic_dev_prev = strategic_dev[strategic_dev['Year'] == previous_year].shape[0]
            fig = go.Figure(go.Indicator(
            mode = "number+delta",
            value =strategic_dev_cur  ,
            delta = {"reference":strategic_dev_prev,'relative': True,"valueformat": ".0%"},
            title = {"text": a[i] },
            number={"font":{"size":50}},))
            fig.update_layout(
            autosize=False,
            width=300,
            height=300)
            fig.update_traces(delta_increasing_color='red', selector=dict(type='indicator'))
            fig.update_traces(delta_decreasing_color='green', selector=dict(type='indicator'))
            #fig.update_traces(number_valueformat=<VALUE>, selector=dict(type='indicator'))
            with col[i]:
                st.plotly_chart(fig)
        #######
        events_data1 = events_data
        events_data1['Number of Occurences'] = events_data1['Number of Occurences'] = events_data1.groupby(['Year','EVENT_TYPE'])['EVENT_TYPE'].transform('count')
        main_event = events_data1.groupby(['Year','EVENT_TYPE']).count()
        main_event = main_event.reset_index()
        fig3 = px.line(main_event,x='Year', y='Number of Occurences', color='EVENT_TYPE', markers=True,title = "Conflict Events Occuraring Per Year")
        fig3.update_layout(
            autosize=True,
            width=1300,
            height=500)
        fig3.update_layout(
            xaxis=dict(
                showline=True,
                showgrid=False,
                showticklabels=True,
                ),
            yaxis=dict(
                showgrid= False,
                zeroline=False,
                showline=True,
                showticklabels= True,
            ),
            showlegend=True,
            legend_title="Events",
            #xaxis_tickangle=-45,
            plot_bgcolor= 'rgba(0,0,0,0)'
        )
        st.plotly_chart(fig3)

        # Map box
        col1,col2 = st.columns([5,5])
        
        explanations = {"Strategic developments":stratejic_dev,"Riots":riots,"Battles":battles,
        "Explosions/Remote violence":explosions_or_remote_violence, "Violence against civilians":violence_against_citizens,"Protests":protests}
        with col1:
            st.subheader('Choose Event')
            categories = st.selectbox("", df['EVENT_TYPE'].unique())
            with st.expander('Defination'):
                st.write(explanations[categories])

        
        strategic_development = events_data[events_data['EVENT_TYPE']==categories]
        #strategic_data = strategic_development[['EVENT_DATE','YEAR','COUNTRY','ADMIN1','LOCATION','ADMIN2','SUB_EVENT_TYPE', 'ACTOR1','ACTOR2','NOTES','FATALITIES','LATITUDE','LONGITUDE']]
        strategic_development['Number of Occurences'] = strategic_development.groupby(['Location','Event'])['Event'].transform('count')
        fig = px.scatter_mapbox(strategic_development,
                    lat="LATITUDE" ,
                    lon="LONGITUDE",
                    size= 'Number of Occurences',
                    color="Event",
                    animation_frame='Year',
                    mapbox_style='carto-positron',
                    size_max=20,width =1100, height = 600,
                    hover_data= {
                    "Location": True,
                    "Event Desc": True,
                    "Perpetrator": True,
                    "Actor Two": True,
                    'LATITUDE':False,
                    'LONGITUDE':False,
                    'Fatalities':True,
                    'Event': False
                    },
                    hover_name = 'Event',
                    zoom = zoom)
            #fig.update_traces(mode="markers", hovertemplate=None)
        #fig.update_layout(mapbox_style = "open-street-map")
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1000
        fig.update_layout(
                autosize=True,
                width=1300,
                height=700)
        
        

        a2,a3 = st.columns([5,1])
        with a2:
            st.plotly_chart(fig)

        sub_event_plot = strategic_development[['Year','Event','Number of Occurences']]
        sub_event_plot = sub_event_plot.groupby(['Year','Event']).count()
        sub_event_plot = sub_event_plot.reset_index()
        fig1 = px.line(sub_event_plot,x='Year', y='Number of Occurences', color='Event', markers=True,title = "Number of Sub Events Per Year")
        fig1.update_layout(
                autosize=True,
                width=1300,
                height=500)
        fig1.update_layout(
                xaxis=dict(
                    showline=True,
                    showgrid=False,
                    showticklabels=True,
                    ),
                yaxis=dict(
                    showgrid= False,
                    zeroline=False,
                    showline=True,
                    showticklabels= True,
                ),
                showlegend=True,
                legend_title="Sub Event Types",
                xaxis_tickangle=-45,
                plot_bgcolor= 'rgba(0,0,0,0)'
            )
        event_plot = strategic_development[['Year','EVENT_TYPE','Number of Occurences']]
        event_plot = event_plot.groupby(['Year','EVENT_TYPE']).count()
        event_plot = event_plot.reset_index()
        fig2 = px.line(event_plot,x='Year', y='Number of Occurences', color='EVENT_TYPE', markers=True,title = "Number of {} Occurances Per Year".format(categories))
        fig2.update_layout(
                autosize=True,
                width=1300,
                height=500)
        fig2.update_layout(
                xaxis=dict(
                    showline=True,
                    showgrid=False,
                    showticklabels=True,
                    ),
                yaxis=dict(
                    showgrid= False,
                    zeroline=False,
                    showline=True,
                    showticklabels= True,
                ),
                showlegend=False,
                legend_title="Sub Event Types",
                xaxis_tickangle=-45,
                plot_bgcolor= 'rgba(0,0,0,0)'
            )
       
        st.plotly_chart(fig2)
        st.plotly_chart(fig1)
        comm4 = st.sidebar.checkbox("Add Comment")
        if comm4:
            add_comment()
   


        



    