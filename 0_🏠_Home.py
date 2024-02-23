# Import necassary libraries
import streamlit as st
import streamlit_authenticator as stauth



# Configure the page
st.set_page_config(
    page_title='Home Page',
    page_icon='👨‍💻',
    layout='wide',
    initial_sidebar_state='auto'
)

# --------- Add custom CSS to adjust the width of the sidebar

st.markdown( """ <style> 
            section[data-testid="stSidebar"]
            { width: 200px !important;
            }
            </style> """,
            unsafe_allow_html=True,
)

# Set page title
st.title('Customer Churn Prediction App')