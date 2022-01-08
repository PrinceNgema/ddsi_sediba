import pandas as pd
import numpy as np
import streamlit  as st
import plotly.express as px
import plotly.graph_objects as go
import datetime
from datetime import date
px.set_mapbox_access_token("pk.eyJ1IjoicHJpbmNlbiIsImEiOiJja3d3NDR4amowMDFxMm5ucjI4cWFqemUyIn0.Ge2IPq5WzgR1kATkwBOjIQ")

@st.cache
def get_acled():
    df = pd.read_csv('acled_2014-2021.csv')
    return df

def summaries():
    df = get_acled()
    A_country = st.sidebar.selectbox("",df['COUNTRY'].unique())
    df_country = df[df['COUNTRY'] == A_country]
    today = datetime.date.today()
    #st.sidebar.markdown('Select Event dates:')
    ys = [2021,2014,2015,2016,2017,2018,2019,2020]
    get_year = st.sidebar.selectbox('',ys)
    data = df[['COUNTRY','YEAR','FATALITIES','LOCATION']]
    data1 = data
    data = data[data['YEAR'] == get_year]
    scatter  = data1.groupby(['COUNTRY','YEAR']).sum().sort_values(by = ['FATALITIES'],ascending= False)
    top_10_F  = data.groupby(['COUNTRY','YEAR']).sum().sort_values(by = ['FATALITIES'],ascending= False).head(10)
    top_10_F = top_10_F.reset_index()
    fig = px.bar(top_10_F , y='FATALITIES', x='COUNTRY', text='FATALITIES', color='COUNTRY', title = "Top 10 Countries Fatalaties in Africa "+ str(get_year))
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
    df_country = df[df['COUNTRY'] == A_country]
    df_country = df_country[df_country['YEAR']== get_year]
    actors = df_country[['LOCATION','ACTOR1','FATALITIES']]
    top_5  = actors.groupby(['LOCATION']).sum().sort_values(by = ['FATALITIES'],ascending= False).head(5)                                                                                                   
    top_5 = top_5.reset_index()
    cities = top_5['LOCATION'].values
    df_actors = actors[actors['LOCATION'].isin(cities)]
    fig1 = px.bar(df_actors, x="LOCATION", y="FATALITIES", color="LOCATION",title = 'Main Group Responsible for Fatalities in '+ A_country,
    animation_frame="ACTOR1", animation_group="ACTOR1", range_y=[0,50])
    fig1.update_layout(uniformtext_minsize=8,yaxis_title=None, xaxis_title = None)
    fig1.update_traces(textposition='outside')
    fig1.update_layout(
        autosize=True,
        width=800,
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
            showline=True,
            showticklabels= True,

        ),
        showlegend=True,
        #xaxis_tickangle=-45,
        plot_bgcolor= 'rgba(0,0,0,0)'
    )
    fig1.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1000
    st.header(A_country)
    

    my_data = df.set_index('EVENT_DATE')
    df_trend = my_data[my_data['COUNTRY'] == A_country]
    fatalities = df_trend[['FATALITIES']]
    format = '%Y-%m-%d'
    fatalities.index = pd.to_datetime(fatalities.index,format = format)
    fatalities = fatalities.resample(rule = 'M').sum()

    #Final Graph 
    fig3 = go.Figure()

    fig3.add_trace(
        go.Scatter(x=list(fatalities.index), y=list(fatalities.FATALITIES)))


    fig3.update_layout(
        title_text="Fatalities Trend in  " +A_country,
        autosize=True,
        width=800,
        height=600
    )

    # Add range slider
    fig3.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label="1m",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6m",
                        step="month",
                        stepmode="backward"),
                    dict(count=1,
                        label="YTD",
                        step="year",
                        stepmode="todate"),
                    dict(count=1,
                        label="1y",
                        step="year",
                        stepmode="backward"),
                    dict(step="all")
                ]),
                font = dict(
                    color = 'black'

                )

                
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
    a1,a2 = st.columns([5,5])

    st.plotly_chart(fig)
    st.plotly_chart(fig3)
    st.plotly_chart(fig1)
    st.plotly_chart(fig1)

    m1,m3 = st.columns([5,1])
    data = df[['YEAR','COUNTRY','ACTOR1','LONGITUDE','LATITUDE','FATALITIES','ADMIN2']]
    da = data[data['COUNTRY'] ==  A_country ]
    #Actors = st.sidebar.multiselect('Add Actors',da['ACTOR1'].unique(),default = da['ACTOR1'].values[0])
    #zoom = st.sidebar.slider('select zoom level', 0, 15, 4)
    with m1:
        Actors = st.multiselect('Add Actors to map',da['ACTOR1'].unique(),default = da['ACTOR1'].values[0])
        actor_data = da[da['ACTOR1'].isin(Actors)]
        fig4 = px.scatter_mapbox(actor_data ,
              lat="LATITUDE" ,
              lon="LONGITUDE",
              #hoverinfo = "FATALITIES",
              color="ACTOR1",
              animation_frame='YEAR',
              mapbox_style='carto-positron',
              size_max=100,width =1200, height = 600,hover_data= {
              'LATITUDE':False,
              'LONGITUDE':False,
              'FATALITIES':True
              },
              hover_name = 'ADMIN2',
              zoom=4)
#fig.update_traces(mode="markers", hovertemplate=None)
  
        fig4.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1000

        fig4.update_layout(
            plot_bgcolor= 'rgba(0,0,0,0)',
            title='Violence Instigators in '+A_country,
            legend_title_text='Instigators'
        )
        st.plotly_chart(fig4)

    


        
        
        
    
        
    
 


    
    

