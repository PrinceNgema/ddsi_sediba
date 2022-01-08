from re import L
import pandas as pd
from st_aggrid.shared import GridUpdateMode
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import plotly.graph_objects as go
import streamlit as st
from forecasts import *
import sqlite3 
from datetime import date
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder

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
@st.cache
def get_data():
    data_2015 = pd.read_pickle("2015Economic.pkl")
    data_2016 = pd.read_pickle("2016Economic.pkl")
    data_2017 = pd.read_pickle("2017Economic.pkl")
    data_2018 = pd.read_pickle("2018Economic.pkl")
    data_2019 = pd.read_pickle("2019Economic.pkl")
    data_2020 = pd.read_pickle("2020Economic.pkl")
    graph_data  = pd.read_pickle('Graphs.pkl')
    return (data_2015,data_2016,data_2017,data_2018,data_2019,data_2020,graph_data)
data_2015,data_2016,data_2017,data_2018,data_2019,data_2020,graph_data = get_data()
graph_data = graph_data[graph_data['Country'] != 'Aruba']

def economic():
    #st.sidebar.header('Economics')
    ecos_choice = st.sidebar.selectbox("",["Trends","Maps","Forecasts"])
    if ecos_choice == "Trends":
        #st.sidebar.write("Filter Graphs")
        Country = st.sidebar.selectbox('',graph_data['Country'].unique())
        
        st.subheader(Country)
        c1,c2,c3,c4,c5,c6= st.columns([1,1,1,1,1,1])
        col =  [c1,c2,c3,c4,c5,c6]
        lst = ['GDP','GDP per Capita','GNI','GNI per capita','Inflation, consumer prices (annual %)','Unemployment, total (% of total labor force) (']
        for i in range(len(lst)):
            gdp = graph_data[(graph_data['Country'] == Country) & (graph_data['Indicator'] == lst[i])]
            plot_d = gdp.drop(columns = 'Indicator',axis = 1).set_index('Country')
            try1 = plot_d.T # data to Plot
            try1 = try1.reset_index()
            curr_value = try1[Country].iloc[-1]
            prev_value = try1[Country].iloc[-2]
            fig = go.Figure(go.Indicator(
            mode = "number+delta",
            value =curr_value  ,
            delta = {"reference":prev_value,'relative': True,"valueformat": ".0%"},
            title = {"text": lst[i]},
            number={"font":{"size":50}},))
            fig.update_layout(
            autosize=False,
            width=300,
            height=300)
            with col[i]:
                st.plotly_chart(fig,use_container_width = True)

        a1,a2,a3 = st.columns([5,1,5])
        colors = ['blue','green','red','yellow','brown','orange']
        titles = ['Gross Domest Product','Gross Domestic Product per Capita','Gross National Income','Gross National Income per Capita','Inflation,consumer prices (annual %)','Unemployment, total (% of total labor force)']
        countries = st.sidebar.multiselect('Choose Countries To Compare with',graph_data['Country'].unique())
        comm1 = st.sidebar.checkbox("Add Comment")
        if comm1:
            add_comment()

        with a1:
            for i in range(len(lst)):
                gdp = graph_data[(graph_data['Country'] == Country) & (graph_data['Indicator'] ==lst[i] )]
                plot_d = gdp.drop(columns = 'Indicator',axis = 1).set_index('Country')
                try1 = plot_d.T # data to Plot
                try1 = try1.reset_index()
                fig = go.Figure(data=[go.Scatter(x= try1['index'], y=try1[Country],line_color=colors[i])])
                fig.update_layout(
                updatemenus=[dict(buttons=list([dict(args=["type", "scatter"],
                                label="Line Plot",
                                method="restyle"),
                                dict(args=["type", "bar"],
                                label="Bar Chart",
                                method="restyle")]),
                                direction="down",
                                pad={"r": 10, "t": 10},
                                showactive=True,
                                x= 0.8,
                                xanchor="left",
                                y=1.09,
                                yanchor="top"),],
                    xaxis=dict(showline=True,
                            showgrid=False,
                            showticklabels=True,),
                    yaxis=dict(showgrid=False,zeroline=False,
                            showline=True,
                            showticklabels= True,),
                            showlegend=False,
                            plot_bgcolor= 'rgba(0,0,0,0)',
                            title= titles[i],
                            autosize=False,
                            width=600,
                            height=400)
                st.plotly_chart(fig,use_container_width = True)

        with a3:

            for i in range(len(lst)):
                countries.append(Country)
                df = graph_data[graph_data['Country'].isin(countries)]
                df_gdp = df[df['Indicator']== lst[i]]
                df_gdp= df_gdp[['Country','2020']]
                df_gdp = df_gdp.set_index('Country')
                fig6 = px.bar(df_gdp, x = df_gdp.index , y= df_gdp.columns,title = "Add Countries to Compare Current {}".format(titles[i]),width=600, height=400)
                fig6.update_layout(showlegend=False,yaxis_title= None,xaxis_title = None)
                fig6.update_layout(
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
                st.plotly_chart(fig6,use_container_width = True)

    elif ecos_choice == 'Forecasts':
        forecast()

    elif ecos_choice == 'Maps':
        continent = st.sidebar.selectbox('',['Africa','World','Asia','South America','North America','Europe'])
        indicator = st.sidebar.selectbox("",['GDP','GDP per Capita','GNI','GNI per capita','Inflation','Unemployment'])
        year = st.sidebar.selectbox(" ", ['2015','2016','2017','2018','2019','2020'])
        years = {'2015':data_2015,
                '2016':data_2016,
                '2017':data_2017,
                '2018':data_2018,
                '2019':data_2019,
                '2020':data_2020}

        cont_names = {'Africa':'africa',
                    'Asia':'asia',
                    'North America': 'north america',
                    'South America':'south america',
                    'Europe':'europe',
                    'World':'world'}   

        title = {
        "GDP":" Gross domestic product (GDP US$)," ,
        "GDP per Capita": "Gross domestic product per capita(US$)",
        "GNI": "GNI, Atlas method (current US$)",
        "GNI per capita": "GNI per capita, Atlas method (current US$)",
        "Unemployment":"Unemployment, total (% of total labor force)" ,
        "Official exchange rate":"Official exchange rate (LCU per US$, period average)",
        "Inflation":"Inflation, consumer prices (annual %)"
        }      
        economic_data = years[year]
        region = cont_names[continent]
        if continent == 'World':
            economic_data  = economic_data 
        else:
            economic_data = economic_data[economic_data['continents']== continent]

        data = dict (
            type = 'choropleth',
            locations = economic_data['Countries'],
            locationmode='country names',
            colorscale = 'delta',
            z= economic_data[indicator])
        fig = go.Figure(data=[data])
        fig.update_layout(
                title = title[indicator]+" "+year,
                geo_scope= region,
                width=1300,
                height=700,
                geo = dict(bgcolor = 'rgba(0,0,0,0)')
            )
        col1,col2,col3 = st.columns([1,6,1])
        with col2:
            st.plotly_chart(fig,use_container_width = True)
            
        df = economic_data[['Countries','GDP','GDP per Capita','GNI','GNI per capita','Inflation','Unemployment']]
        if st.checkbox('Show Data'):
            shows = df
            gb = GridOptionsBuilder.from_dataframe(shows)
            gb.configure_pagination()
            gb.configure_side_bar()
            gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc="sum", editable=True)
            gb.configure_selection('multiple',use_checkbox= True,groupSelectsChildren= True)
            gridOptions = gb.build()
            AgGrid(shows, gridOptions=gridOptions, enable_enterprise_modules=True,
                            fit_columns_on_grid_load= False,width ='100%',update_mode = GridUpdateMode.SELECTION_CHANGED)
        st.sidebar.download_button(label = 'Download Data', data = df.to_csv(index = False), mime = 'text/csv')
        comm = st.sidebar.checkbox("Add Comment")
        if comm:
            add_comment()


          
          
          
          

            

                

        
   


