import streamlit as st
import plotly.express as px

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


# ------ Set visualization view page
col1, col2, col3 = st.columns(3)
with col2:
    options = st.selectbox('Choose viz to display', options=['', 'EDA', 'Analytical Quesitons'])

# def eda_viz():
#     # ----- 





# if __name__ == '__main__':
#     eda_viz()
