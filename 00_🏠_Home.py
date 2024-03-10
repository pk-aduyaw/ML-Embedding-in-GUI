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

        cols = st.columns(2)
        # Churn Prediction Status
        with cols[0]:
            st.subheader('Churn Prediction Status')
            st.write("This application provides a platform for predicting the churn status of customers by leveraging historical data encompassing customer demographics, subscription details, account information, and their corresponding churn status.")

        # Application Features
        with cols[0]:
            st.subheader('Application Features')
            st.markdown("""                
            * Data View - View proprietory data
            * Dashboard - Shows EDA and KPIs with other analytical questions
            * Predict - Allows user to predict churn status from two available models
            * History - Displays all previous predictions made using the app
            """)

        # Key Advantages
        with cols[0]:
            st.subheader('Key Advantages')
            st.markdown("""
                        Discover the advantages of using this Churn Prediction App, such as;
                        * Accurate predictions
                        * User-friendly interface
                        """)

        # How to run the app
        with cols[1]:
            st.subheader('How to Run the App')
            st.write("Follow the steps to run the Customer Churn Prediction App and make accurate predictions for customer churn.")
            st.code("""
                    #activate virtual environment
                    venv/Scripts/activate

                    streamlit run 00_🏠_Home.py
                    """, language="python")

        # Machine Learning Integration
        with cols[1]:
            st.subheader('Machine Learning Integration')
            st.write("Learn about the machine learning models integrated into the app, including Gradient Boosting and Support Vector models.")

        # Need Assistance
        with cols[1]:
            st.subheader('Need Assistance?')
            st.write("If you need any assistance or have questions, feel free to reach out. Email: princeekow4@gmail.com")
            cols = st.columns(4)
            with cols[0]:
                st.link_button(":red[GitHub]", "https://github.com/pk-aduyaw/ML-Embedding-in-GUI",)
            with cols[1]:
                st.link_button(":red[Medium]", "https://medium.com/@pkaduyaw/enhancing-customer-retention-a-machine-learning-solution-f58abb4b77c5")
            with cols[2]:
                st.link_button(":red[LinkedIn]", "https://www.linkedin.com/in/prince-kwabena-aduyaw")
            with cols[3]:
                st.link_button(":red[X]", "https://twitter.com/pk_aduyaw")





if __name__=='__main__':
    main()