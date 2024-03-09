import streamlit as st
import plotly.express as px
import pandas as pd

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
    options = st.selectbox('Choose viz to display', options=['', 'EDA', 'Analytical Questions'])

# ------ Load Dataset from remote location
@st.cache_data(show_spinner='Loading data')
def load_data():
    df = pd.read_csv('./data/dataset.csv')
    return df

df = load_data()

def eda_viz():
    st.subheader('Exploratory Data Analysis')
    column1, column2 = st.columns(2)
    with column1:
        fig = px.histogram(df, x='tenure', title='Distribution of Tenure')
        st.plotly_chart(fig)
    with column1:
        fig = px.histogram(df, x='MonthlyCharges', title='Distribution of MonthlyCharges')
        st.plotly_chart(fig)
    with column1:
        fig = px.histogram(df, x='TotalCharges', title='Distribution of TotalCharges')
        st.plotly_chart(fig)
    
    with column2:
        fig = px.bar(df, x='Churn', title='Churn Distribution')
        st.plotly_chart(fig)
    with column2:
        fig = px.box(df, x='gender', y='TotalCharges', title='Total Charges Distribution across Gender')
        st.plotly_chart(fig)
    

def kpi_viz():
    st.subheader('Analytical Questions')
    col1, col2, col3, col4, col5 = st.columns(5)

    # ------- Grand Total Charges
    with col1:
        grand_tc = df['TotalCharges'].sum()
        st.markdown('###### Grand TotalCharges')
        st.markdown(f'#### {"{:,.2f}".format(grand_tc)}')

    # ------- Grand Monthly Charges
    with col2:
        grand_mc = df['MonthlyCharges'].sum()
        st.markdown('###### Grand MonthlyCharges')
        st.markdown(f'#### {"{:,.2f}".format(grand_mc)}')

    # ------- Average Customer Tenure
    with col3:
        average_tenure = df['tenure'].sum()
        st.markdown('###### Average Tenure')
        st.markdown(f'#### {"{:,.2f}".format(average_tenure)}')

    # ------- Churned Customers
    with col4:
        churned = len(df.loc[df['Churn']==1])
        st.markdown('###### Churn')
        st.markdown(f'#### {churned}')

    # ------ Total Customers
    with col5:
        total_customers = df['customerID'].count()
        st.markdown('###### Total Customers')
        st.markdown(f'#### {total_customers}')

        



if __name__ == '__main__':
    if options == 'EDA':
        eda_viz()
    elif options == 'Analytical Questions':
        kpi_viz()
