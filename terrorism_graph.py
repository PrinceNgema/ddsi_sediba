import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go

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
            blog_post_date = date.today()
            if st.button("Add"):
                add_data(blog_author,blog_title,blog_article,blog_post_date)
                st.success("Comments:{} saved".format(blog_title))

@st.cache(allow_output_mutation=True)
def data():
    df = pd.read_pickle('Terrorism 2000-2019.pkl')
    return df
def graphs():
    df = data()
    lst = sorted(df['Country'].unique().tolist()) 
    lst.insert(0,'Worldwide')
    country = st.sidebar.selectbox('',lst)
    if country == 'Worldwide':
        df = df
    else:
        df = df[df['Country'] == country]
    
   
    with st.container():
        st.header(country)
        col1,col2,col3,col4,col5 = st.columns([2,1,2,1,2])
        with col1:
            att_prev = df[df['Year'] == 2018].shape[0]
            att_curr= df[df['Year'] == 2019].shape[0]
            fig = go.Figure(go.Indicator(
                        mode = "number+delta",
                        value = att_curr  ,
                        delta = {"reference":att_prev,'relative': True,"valueformat": ".0%"},
                        title = {"text": "Number of Attacks" },
                        number={"font":{"size":50}},))
            fig.update_layout(
                        autosize=False,
                        width=300,
                        height=300)
            fig.update_traces(delta_increasing_color='red', selector=dict(type='indicator'))
            fig.update_traces(delta_decreasing_color='green', selector=dict(type='indicator'))
            st.plotly_chart(fig)

        with col3:
            injured_prev = df[df['Year']== 2018]['Number of Injured'].sum()
            injured_curr = df[df['Year']== 2019]['Number of Injured'].sum()
            fig = go.Figure(go.Indicator(
                        mode = "number+delta",
                        value = injured_curr,
                        delta = {"reference":injured_prev ,'relative': True,"valueformat": ".0%"},
                        title = {"text": "Number of Injuries" },
                        number={"font":{"size":50}},))
            fig.update_layout(
                        autosize=False,
                        width=300,
                        height=300)
            fig.update_traces(delta_increasing_color='red', selector=dict(type='indicator'))
            fig.update_traces(delta_decreasing_color='green', selector=dict(type='indicator'))
            st.plotly_chart(fig)

        with col5:
            death_prev = df[df['Year']== 2018]['Deaths'].sum()
            death_curr = df[df['Year']== 2019]['Deaths'].sum()
            fig = go.Figure(go.Indicator(
                        mode = "number+delta",
                        value = death_curr ,
                        delta = {"reference":death_prev ,'relative': True,"valueformat": ".0%"},
                        title = {"text": "Number of Deaths" },
                        number={"font":{"size":50}},))
            fig.update_layout(
                        autosize=False,
                        width=300,
                        height=300)
            fig.update_traces(delta_increasing_color='red', selector=dict(type='indicator'))
            fig.update_traces(delta_decreasing_color='green', selector=dict(type='indicator'))
            st.plotly_chart(fig)

    #Total Terrorist Attacks, Total Deaths and Total Injuries Worldwide by Year 2000-2019
     
    a = df[['Year']]
    a = a.reset_index()
    a  = a.groupby(['Year']).count()
    a = a.reset_index()
    s = df[['Year','Deaths']]
    c = s.groupby('Year').sum()
    c = c.reset_index()
    b = df[['Year','Number of Injured']]
    b = b.groupby('Year').sum()
    b = b.reset_index()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=a.Year, y= a.eventid,
                        mode='lines+markers',
                        name='Terrorists Attack'))
    fig.add_trace(go.Scatter(x=c.Year, y=c.Deaths,
                        mode='lines+markers',
                        name='Deaths'))
    fig.add_trace(go.Scatter(x=b.Year, y=b['Number of Injured'],
                        mode='lines+markers',
                        name='Injuries'))
    fig.update_layout(
                title = "Total Terrorist Attacks, Total Deaths and Total Injuries {} from 2000 to 2019 ".format(country))
    fig.update_layout(
    autosize=True,
    width=1300,
    height=600,)
    fig.update_layout(
            xaxis=dict(
                showline=False,
                showgrid=False,
                showticklabels=True,
                
            ),
            # Turn off everything on y axis
            yaxis=dict(
                showgrid=False,
                showline=False,
                showticklabels= True,
                
            ),
            showlegend=True)
            #plot_bgcolor= 'rgba(0,0,0,0)')
    st.plotly_chart(fig)

### Targeted groups and kills
    targets = df[['Target']]
    targets = targets.reset_index()
    targets =targets.groupby(['Target']).count().sort_values(by = ['eventid'],ascending = False).head(11)
    targets = targets.reset_index()
    target = targets[targets['Target'] != 'Unknown']
    t = target.set_index('Target')
    lst = target['Target'].tolist()
    target_kills = df[df['Target'].isin(lst)]
    tk = target_kills[['Target','Deaths']]
    tk=tk.groupby('Target').sum().sort_values(by = ['Deaths'],ascending= False)
    target_plot = pd.concat([t, tk], axis=1)
    target_plot = target_plot.reset_index()
    
    fig = go.Figure(data=[
    go.Bar(name='Attacks', y=target_plot.eventid, x=target_plot.Target),
    go.Bar(name='Kills', y=target_plot.Deaths, x=target_plot.Target)])
    fig.update_layout(uniformtext_minsize=8,yaxis_title=None, xaxis_title = None)
    fig.update_layout(
            autosize=True,
            width=1300,
            height=700)
    fig.update_layout(
            xaxis=dict(
                showline=True,
                showgrid=False,
                showticklabels=True,
                
                #visible = False  
            ),
            # Turn off everything on y axis
            yaxis=dict(
                showgrid=False,
                zeroline=False,
                showline=False,
                showticklabels= True,
            ),
            showlegend=True,
            plot_bgcolor= 'rgba(0,0,0,0)',
            title = "10 Most Targeted Groups"
        )
    st.plotly_chart(fig)
      #### Method of attacks
    attacks = df[['Attack Type','Deaths']]
    at =attacks.groupby('Attack Type').sum().sort_values(by = ['Deaths'],ascending= False)
    at = at.reset_index()
    at = at[at['Attack Type'] != 'Unknown']
    fig = px.bar(at , y='Attack Type', x='Deaths', text='Deaths', color='Attack Type', title = "Method of Attacks vs Number of Deaths Group 2000-2019")
    fig.update_traces(textposition='outside')
    fig.update_layout(uniformtext_minsize=8,yaxis_title=None, xaxis_title = None)
    fig.update_layout(
            autosize=True,
            width=1300,
            height=600)
    fig.update_layout(
            xaxis=dict(
                showline=True,
                showgrid=False,
                showticklabels=True,
                
                #visible = False  
            ),
            # Turn off everything on y axis
            yaxis=dict(
                showgrid=False,
                zeroline=False,
                showline=False,
                showticklabels= True,
            ),
            showlegend=False,
            #xaxis_tickangle=-45,
            plot_bgcolor= 'rgba(0,0,0,0)'
        )
    st.plotly_chart(fig)

    #Most used method of attack and kills
    sun_burst = target_kills[['Target','Attack Type','Weapon Type','Weapon Sub Type','Deaths']]
    burst = sun_burst.groupby(['Target','Attack Type','Weapon Type','Weapon Sub Type']).sum().sort_values(by = ['Deaths'],ascending = False)
    burst = burst.reset_index()
    burst = burst[burst['Deaths'] > 10]
    fig = px.sunburst(burst, path=['Target','Attack Type','Weapon Type','Weapon Sub Type'], values='Deaths',title = 'Top 10 Attacked Groups and Methods of Attacks')
    fig.update_layout(
    autosize=True,
    width=1300,
    height=700,)
    fig.update_layout(
            xaxis=dict(
                showline=False,
                showgrid=False,
                showticklabels=True,
                
            ),
            # Turn off everything on y axis
            yaxis=dict(
                showgrid=False,
                showline=False,
                showticklabels= True,
                
            ),
            showlegend=True)
            #plot_bgcolor= 'rgba(0,0,0,0)')
    st.plotly_chart(fig)

    ### 10 Most Suicidal Terrorist Groups
    suicidal = df[df['Weapon Sub Type'] == 'Suicide (carried bodily by human being)']
    d_suicidal = suicidal[['Perpetrator Name']].reset_index()
    sui  = d_suicidal .groupby(['Perpetrator Name']).count().sort_values(by = ['eventid'],ascending= False).head(10)
    sui = sui.reset_index()
    sui = sui[sui['Perpetrator Name'] != 'Unknown']

    fig1 = px.bar(sui , y='eventid', x='Perpetrator Name', text='eventid', color='Perpetrator Name', title = "Top 10 Most Suicidal Terrorist Group 2000-2019")
    fig1.update_traces(textposition='outside')
    fig1.update_layout(uniformtext_minsize=8,yaxis_title=None, xaxis_title = None)
    fig1.update_layout(
            autosize=True,
            width=1300,
            height=600)
    fig1.update_layout(
            xaxis=dict(
                showline=True,
                showgrid=False,
                showticklabels=True,
                
                #visible = False  
            ),
            # Turn off everything on y axis
            yaxis=dict(
                showgrid=False,
                zeroline=False,
                showline=False,
                showticklabels= True,
            ),
            showlegend=False,
            xaxis_tickangle=-45,
            plot_bgcolor= 'rgba(0,0,0,0)'
        )
    st.plotly_chart(fig1)


    dg = df[['Perpetrator Name','Deaths']]
    dg =dg.groupby('Perpetrator Name').sum().sort_values(by = ['Deaths'],ascending= False).head(10)
    dg = dg.reset_index()
    dg = dg[dg['Perpetrator Name'] != 'Unknown']
    fig = px.bar(dg , y='Deaths', x='Perpetrator Name', text='Deaths', color='Perpetrator Name', title = "Top 10 Most Deadliest Group 2000-2019")
    fig.update_traces(textposition='outside')
    fig.update_layout(uniformtext_minsize=8,yaxis_title=None, xaxis_title = None)
    fig.update_layout(
            autosize=True,
            width=1300,
            height=600)
    fig.update_layout(
            xaxis=dict(
                showline=True,
                showgrid=False,
                showticklabels=True,
                
                #visible = False  
            ),
            # Turn off everything on y axis
            yaxis=dict(
                showgrid=False,
                zeroline=False,
                showline=False,
                showticklabels= True,
            ),
            showlegend=False,
            xaxis_tickangle=-45,
            plot_bgcolor= 'rgba(0,0,0,0)'
        )
    st.plotly_chart(fig)
    comm = st.sidebar.checkbox("Add Comment")
    if comm:
            add_comment()



    
