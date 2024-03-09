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
    st.markdown('---')
    col1, col2, col3, col4, col5 = st.columns(5)
    st.markdown('---')
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
        average_tenure = df['tenure'].mean()
        st.markdown('###### Average Tenure')
        st.markdown(f'#### {"{:,.2f}".format(average_tenure)}')

    # ------- Churned Customers
    with col4:
        churned = len(df.loc[df['Churn'] == 1])
        st.markdown('###### Churn')
        st.markdown(f'#### {churned}')

    # ------ Total Customers
    with col5:
        total_customers = df['customerID'].count()
        st.markdown('###### Total Customers')
        st.markdown(f'#### {total_customers}')

        
def analytical_ques_viz():
    # ------ Answer Analytical Question 1
    mal_churned_customers = df[(df['gender']=='Male') & (df['Dependents']== 1) & (df['Churn']== 1)]['PaymentMethod'].value_counts()

    values = mal_churned_customers.values
    labels = mal_churned_customers.index

    treemap_df = pd.DataFrame({'labels': labels, 'values': values})

    fig = px.treemap(treemap_df, path=['labels'], values='values', color='values',
                  color_continuous_scale='Blues', title='Q1. How many male customers with dependents churned given their payment method?')
    st.plotly_chart(fig)
    
    
    # ------ Answer Analytical Question 2
    fem_churned_customers = df[(df['gender']=='Female') & (df['Dependents']== 1) & (df['Churn']== 1)]['PaymentMethod'].value_counts()

    values = fem_churned_customers.values
    labels = fem_churned_customers.index

    treemap_df = pd.DataFrame({'labels': labels, 'values': values})

    fig = px.treemap(treemap_df, path=['labels'], values='values', color='values',
                  color_continuous_scale='Blues', title='Q2. How many female customers with dependents churned given their payment method?')
    st.plotly_chart(fig)


    
    # ------ Answer Analytical Question 3
    churned = df[df['Churn'] == 1]

    fig = px.bar(churned, x='MultipleLines', color='gender', barmode='group',
             title='Q3. What is the distribution for the customers who churned given their multiple lines status?',
             labels={'MultipleLines': 'Multiple Lines', 'gender': 'Gender'})

    st.plotly_chart(fig)
    

    # ------ Answer Analytical Question 4
    monthly_charges = df.groupby('gender')['MonthlyCharges'].sum().reset_index()

    fig = px.pie(monthly_charges, names='gender', values='MonthlyCharges',
             title='Q4. What percentage of MonthlyCharges was accumulated given the customer gender?',
             color='gender',
             labels={'gender': 'Gender', 'MonthlyCharges': 'Monthly Charges'})

    # Show the figure in Streamlit
    st.plotly_chart(fig)
    

    # ------ Answer Analytical Question 5
    monthly_charges = df.groupby('Churn')['TotalCharges'].sum().reset_index()

    fig = px.pie(monthly_charges, names='Churn', values='TotalCharges',
             title='Q5. What percentage of TotalCharges was accumulated given customer churn status?',
             color='Churn',
             labels={'Churn': 'Churn', 'TotalCharges': 'Monthly Charges'})

    st.plotly_chart(fig)



if __name__ == '__main__':
    if options == 'EDA':
        eda_viz()
    elif options == 'Analytical Questions':
        kpi_viz()
        analytical_ques_viz()
    else:
        st.markdown('#### No viz display selected yet')