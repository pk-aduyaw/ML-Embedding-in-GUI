# Import necassary libraries
import streamlit as st
from streamlit_option_menu import option_menu
import login




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

    login.login_user()
    
    if st.sidebar == 'Home':
        # After successful login, render other pages
        st.title('Customer Churn Prediction App')



if __name__=='__main__':
    main()