import streamlit as st
import pandas as pd


# Configure the page
st.set_page_config(
    page_title='History',
    page_icon='🕰️',
    layout='wide'
)


# --------- Add custom CSS to adjust the width of the sidebar
st.markdown( """ <style> 
            section[data-testid="stSidebar"]
            { width: 200px !important;
            }
            </style> """,
            unsafe_allow_html=True,
)


# Set header for page
st.title('History')

data = pd.read_csv('./data/history.csv')
st.dataframe(data)