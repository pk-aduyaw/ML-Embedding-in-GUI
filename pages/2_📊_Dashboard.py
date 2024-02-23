import streamlit as st
import numpy as np


# Configure the page
st.set_page_config(
    page_title='Dashboard',
    page_icon='📊',
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
st.title('Dashboard')

# # Create a function to convert True and False values to Yes and No respectively.
# def value_cleaner(data):
#     for column in data.columns:
#         if np.any(data[column].isin(['Yes', 'No'])):
#             data[column] = data[column].replace({True:'Yes', False:'No'})
#     return data