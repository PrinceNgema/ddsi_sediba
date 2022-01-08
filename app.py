
import streamlit as st
st.set_page_config(page_title="Sediba", page_icon=":open_file_folder:", layout="wide")
import streamlit_authenticator as stauth
from Sediba import *

hide_st_style = """
            <style>
            footer {visibility: hidden;}
            </style>""" 
            
st.markdown(hide_st_style, unsafe_allow_html=True)

st.sidebar.title("Sediba 1.0")
st.sidebar.image('index.jpg', width = 250)
#st.sidebar.write(" **tel:** 01392 451192 **| website:** https://www.swast.nhs.uk **| email:** mailto:data.science@swast.nhs.uk")


names = ['Prince Ngema','Tsholo Moleleko','Peter Manda','Joseph Mukupe']
usernames = ['princen','tsholom','peterm','jmukupe']
passwords = ['2468','2468','2468','2468']

hashed_passwords = stauth.hasher(passwords).generate()
authenticator = stauth.authenticate(names,usernames,hashed_passwords,
    'some_cookie_name','some_signature_key',cookie_expiry_days=30)
name, authentication_status = authenticator.login('Login','sidebar')
if st.session_state['authentication_status']:
    st.sidebar.write('Welcome *%s*' % (st.session_state['name']))
    main()
elif st.session_state['authentication_status'] == False:
    st.sidebar.error('Username/password is incorrect')
elif st.session_state['authentication_status'] == None:
    st.sidebar.warning('Please enter your username and password')