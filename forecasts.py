from numpy import complex128
import plotly.graph_objects as go
import pandas as pd
import wbgapi as wb
import plotly.express as px
import streamlit as st
from prophet import Prophet
from streamlit import caching
from create_forecasts import *
from datetime import date
import sqlite3

conn = sqlite3.connect('comment.db')
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

def forecast():
    @st.cache
    def get_data():
        gdp = wb.data.DataFrame('NY.GDP.MKTP.CD')
        gdp = gdp.T
        gdp = gdp.reset_index()
        dic = {}
        for i in gdp['index']:
            dic[i] = i[-4:]
        gdp['index'].replace(dic,inplace = True)
        return gdp
    #with st.spinner('Loading data...'):
    gdp = get_data()

    @st.cache
    def fit(data):
        m = Prophet()
        m.fit(data)
        return m

    tabs = ["View Forecasts","Create forecasts","About"]
    with st.sidebar:
        page = st.selectbox("",tabs)
    if page == "View Forecasts":
        st.title('Forecasts Model')
        st.write('This app enables you to generate time series forecast withouth any dependencies.')
        st.markdown("""The forecasting library used is **[Prophet](https://facebook.github.io/prophet/)**.""")
        country = ['South Africa','Egypt','Zimbabwe','Malawi']
        ind = ['Gross Domestic Product','Inflation','Gross National Income','Unemployement','I will add more']
        
        col1,col2,col3,col4 = st.columns([1,5,5,1])

        with col3:
            indicators = st.selectbox("Select Indicator to Forecast",ind)
        with col2:
            countries = st.selectbox('Select Country',country)
        sa = gdp[['index','ZAF']]
        sa.columns = ['ds','y']
        sa['ds'] = pd.to_datetime(sa['ds'])
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=sa.ds, y=sa.y,
                    mode='lines+markers',
                    name='lines'))
        fig.update_layout(xaxis=dict(
						  showline=True,
						  showgrid= False,
						  showticklabels=True),
                        
                          yaxis=dict(
						  showgrid= False,
						  zeroline=False,
						  showline=True,
						  showticklabels= True,),
                          showlegend=False,
						  xaxis_tickangle=-45,
						  plot_bgcolor= 'rgba(0,0,0,0)',
                          autosize=False,
                          width=1100,
                          height=700,
                          title = 'Gross domestic Product Trend of South Africa 1960 - 2020')

        st.plotly_chart(fig)
        ####Predictions
        with st.form("Predict"):
            with st.container():
                st.write('Forecasts')
                with st.expander("Horizon"):
                    periods_input = st.number_input('Select how many future periods (Years) to forecast.',
                    min_value = 1, max_value = 10,value=5)
            predict = st.form_submit_button("Forecasts")
            m = fit(sa)
            if isinstance(periods_input,int)==True:
                future = m.make_future_dataframe(periods= periods_input,freq ='Y' ,include_history= False)
            else:
                 future = m.make_future_dataframe(periods= 5,freq ='Y' ,include_history= False)
                
            forecast = m.predict(future)
            if predict:
                fig = go.Figure([
                go.Scatter(
                    name='Forecast',
                    x=forecast.ds,
                    y=forecast.yhat,
                    mode='lines+markers',
                    marker=dict(color="red"),
                    line=dict(color='red'),
                ),
                go.Scatter(
                    name='Upper Bound',
                    x= forecast.ds,
                    y=forecast.yhat_upper,
                    mode='lines',
                    marker=dict(color="#444"),
                    line=dict(width=0),
                    showlegend=False
                ),
                go.Scatter(
                    name='Lower Bound',
                    x=forecast.ds,
                    y=forecast.yhat_lower,
                    marker=dict(color="#444"),
                    line=dict(width=0),
                    mode='lines',
                    fillcolor='rgba(68, 68, 68, 0.3)',
                    fill='tonexty',
                    showlegend=False
                )])
                fig.update_layout(
                    yaxis_title='GDP',
                    title='South Africa GDP Forecast',
                    hovermode="x"
                )
                fig.add_trace(go.Scatter(x=sa.ds, y=sa.y,
                                    mode='lines+markers',
                                    name='GDP'))
                fig.update_layout(
                    autosize=False,
                    width=1100,
                    height=700,)
                fig.update_layout(
				                            xaxis=dict(
											showline=True,
											showgrid= False,
											showticklabels=True,
											
											#visible = False  
										),
										# Turn off everything on y axis
										yaxis=dict(
											showgrid= False,
											zeroline=False,
											showline=True,
											showticklabels= True,
										),
										showlegend=False,
										xaxis_tickangle=-45,
										plot_bgcolor= 'rgba(0,0,0,0)'
									)


                st.plotly_chart(fig)
        comm3 = st.sidebar.checkbox("Add Comment")
        if comm3:
            add_comment()

                
    elif page == 'About':
        st.image("prophet.png")
        st.header("About")
        st.markdown("Official documentation of **[Facebook Prophet](https://facebook.github.io/prophet/)**")
        st.markdown("Official documentation of **[Streamlit](https://docs.streamlit.io/en/stable/getting_started.html)**")
        st.write("")
        st.write("Author:")
        st.markdown(""" **[Prince Ngema](https://www.linkedin.com/public-profile/settings?trk=d_flagship3_profile_self_view_public_profile&lipi=urn%3Ali%3Apage%3Ad_flagship3_profile_self_edit_contact_info%3BjZsKf1G2TyCk%2Bbr6GKw0KA%3D%3D)**""")
        st.write("Created on 01/01/2022")
        #st.write("Last updated: **29/04/2021**")

    elif page == "Create forecasts":
        create()
