import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

def login_user():
    with open('./config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)
    col1, col2, col3 = st.columns([.3,.4,.3])
    with col2:
        authenticator = stauth.Authenticate(
            config['credentials'],
            config['cookie']['name'],
            config['cookie']['key'],
            config['cookie']['expiry_days']
        )

        authenticator.login()

        if st.session_state["authentication_status"]:
            with st.sidebar:
                authenticator.logout()
            st.write(f'Welcome *{st.session_state["name"]}*')
        elif st.session_state["authentication_status"] is False:
            st.error('Username/password is incorrect')
        elif st.session_state["authentication_status"] is None:
            st.warning('Please enter your username and password')
    