# Import necassary libraries
import streamlit as st
from login import login_user


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




def main():
    login_user()

    if st.session_state["authentication_status"] == True:

        st.write(f'Welcome *{st.session_state["name"]}*')
        st.header('Customer Churn Prediction App.')




if __name__=='__main__':
    main()