import pandas as pd
import streamlit as st
import sqlite3 
from datetime import date
import plotly.graph_objects as go
import plotly.express as px
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder

conn = sqlite3.connect('comment.db',check_same_thread=False)
c = conn.cursor()

# Functions
def create_table():
	c.execute('CREATE TABLE IF NOT EXISTS blogtable(author TEXT,title TEXT,article TEXT,postdate DATE)')
create_table()

def add_data(author,title,article,postdate):
	c.execute('INSERT INTO blogtable(author,title,article,postdate) VALUES (?,?,?,?)',(author,title,article,postdate))
	conn.commit()

def view_all_notes():
	c.execute('SELECT * FROM blogtable')
	data = c.fetchall()
	return data

def view_all_titles():
	c.execute('SELECT DISTINCT title FROM blogtable')
	data = c.fetchall()
	return data


def get_blog_by_title(title):
	c.execute('SELECT * FROM blogtable WHERE title="{}"'.format(title))
	data = c.fetchall()
	return data
def get_blog_by_author(author):
	c.execute('SELECT * FROM blogtable WHERE author="{}"'.format(author))
	data = c.fetchall()
	return data

def delete_data(title):
	c.execute('DELETE FROM blogtable WHERE title="{}"'.format(title))
	conn.commit()
# Layout Templates

html_temp = """
<div style="background-color:{};padding:10px;border-radius:10px">
<h1 style="color:{};text-align:center;">Home of Comments </h1>
</div>
"""
title_temp ="""
<div style="background-color:#464e5f;padding:10px;border-radius:10px;margin:10px;">
<h4 style="color:white;text-align:center;">{}</h1>
<h6>Author:{}</h6>
<br/>
<br/> 
<p style="text-align:justify">{}</p>
</div>
"""
article_temp ="""
<div style="background-color:#464e5f;padding:10px;border-radius:5px;margin:10px;">
<h4 style="color:white;text-align:center;">{}</h1>
<h6>Author:{}</h6> 
<h6>Post Date: {}</h6>
<img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" style="vertical-align: middle;width: 50px;height: 50px;border-radius: 50%;" >
<br/>
<br/>
<p style="text-align:justify">{}</p>
</div>
"""
head_message_temp ="""
<div style="background-color:#464e5f;padding:10px;border-radius:5px;margin:10px;">
<h4 style="color:white;text-align:center;">{}</h1>
<h6 style="color:white;text-align:center;"> Author:{}</h6> 
<h6 style="color:white;text-align:center;"> Post Date: {}</h6> 
</div>
"""
full_message_temp ="""
<div style="background-color:silver;overflow-x: auto; padding:10px;border-radius:5px;margin:10px;">
<p style="text-align:justify;color:black;padding:10px">{}</p>
</div>
"""

news_message_temp= """ 
<div style="background-color:silver;overflow-x: auto; padding:10px;border-radius:5px;margin:10px;">
<p><a href = {} style="color:#000000;text-decoration: none;"target="_blank"> {}</a></p>
</div>
"""
def add_comments():
        st.subheader("Add Comments")
        create_table()
        blog_author =  st.session_state['name']
        blog_title = st.text_input("Enter Comment Title",key = 100)
        blog_article = st.text_area("Write Comment Here",height=200,key = 101)
        blog_post_date = date.today()
        if st.button("Add",key = 103):
            add_data(blog_author,blog_title,blog_article,blog_post_date)
            st.success("Comments:{} saved".format(blog_title))
def comment():
    #st.markdown(html_temp.format('blue','white'),unsafe_allow_html=True)
    
    menu = ["View Comments","Add Comments","Search Comments","Manage Comments"]
    choose = st.sidebar.selectbox("",menu)

    if choose == "View Comments":
        #st.subheader("View Comments")
        all_titles = [i[0] for i in view_all_titles()]
        postlist = st.sidebar.selectbox("View Comments",all_titles)
        post_result = get_blog_by_title(postlist)
        for i in post_result:
            b_author = i[0]
            b_title = i[1]
            b_article = i[2]
            b_post_date = i[3]
            #st.text("Reading Time:{}".format(readingTime(b_article)))
            st.markdown(head_message_temp.format(b_title,b_author,b_post_date),unsafe_allow_html=True)
            st.markdown(full_message_temp.format(b_article),unsafe_allow_html=True)

    elif choose == "Add Comments":
        add_comments()
        
    elif choose == "Search Comments":
        search_term = st.text_input('Enter Search Term')
        search_choice = st.radio("Field to Search By",("Title","Author"))
        
        if st.button("Search"):
            if search_choice == "Title":
                article_result = get_blog_by_title(search_term)	
                if not article_result:
                    st.subheader('Title Not Found!!!')    	
            elif search_choice == "Author":
                article_result = get_blog_by_author(search_term)
                if not article_result:
                    st.subheader('Author Not Found!!!') 
            for i in article_result:
                b_author = i[0]
                b_title = i[1]
                b_article = i[2]
                b_post_date = i[3]
                #st.text("Reading Time:{}".format(readingTime(b_article)))
                st.markdown(head_message_temp.format(b_title,b_author,b_post_date),unsafe_allow_html=True)
                st.markdown(full_message_temp.format(b_article),unsafe_allow_html=True)

    elif choose == "Manage Comments":
        result = view_all_notes()
        clean_db = pd.DataFrame(result,columns=["Author","Title","Articles","Post Date"])


        shows = clean_db.rename(columns ={'Articles':'Comments'})
        gb = GridOptionsBuilder.from_dataframe(shows)

        gb.configure_pagination()
        gb.configure_side_bar()
        gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc="sum", editable=True)
        gridOptions = gb.build()

        AgGrid(shows, gridOptions=gridOptions, enable_enterprise_modules=True)

                
        with st.expander('Delete Comment'):
            unique_titles = [i[0] for i in view_all_titles()]
            delete_blog_by_title = st.selectbox("Title",unique_titles)
            new_df = clean_db
            if st.button("Delete"):
                delete_data(delete_blog_by_title)
                st.warning("Deleted: '{}'".format(delete_blog_by_title))
        if st.checkbox("Metrics"):
            new_df['Length'] = new_df['Articles'].str.len()
            #st.dataframe(new_df)
            st.subheader("Author Stats")
            dg = new_df.groupby('Author').count()
            dg = dg.reset_index()
            dg = dg.rename(columns = {'Title':'Number of Comments'})
            fig = px.bar(dg, x='Author', y='Number of Comments')
            fig.update_layout(
            autosize=True,
            width=1000,
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
    
