import plotly.graph_objects as go
import pandas as pd
import wbgapi as wb
import plotly.express as px
import streamlit as st
from prophet import Prophet

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
with st.spinner('Loading data...'):
    gdp = get_data()
country = st.sidebar('Select Country')
sa = gdp[['index','ZAF']]
sa.columns = ['ds','y']
sa['ds'] = pd.to_datetime(sa['ds'])
fig = go.Figure()
fig.add_trace(go.Scatter(x=sa.ds, y=sa.y,
                    mode='lines+markers',
                    name='lines'))
st.plotly_chart(fig)

m = Prophet()
m.fit(sa)
future = m.make_future_dataframe(periods= 10,freq ='Y' ,include_history= False)
forecast = m.predict(future)
st.write(forecast)

fig = go.Figure([
    go.Scatter(
        name='Forecast',
        x=forecast.ds,
        y=forecast.yhat,
        mode='lines+markers',
        line=dict(color='rgb(31, 119, 180)'),
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
    )
])
fig.update_layout(
    yaxis_title='GDP',
    title='South Africa GDP Forecast',
    hovermode="x"
)
#fig.add_trace(go.Scatter(x=sa.ds, y=sa.y,
                    #mode='lines+markers',
                    #name='GDP'))

st.plotly_chart(fig)