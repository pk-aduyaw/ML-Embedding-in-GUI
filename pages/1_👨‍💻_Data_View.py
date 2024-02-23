# Import necessary libraries
import streamlit as st
import pandas as pd
import pyodbc


# Configure the page
st.set_page_config(
    page_title='Data Viewer',
    page_icon='👨‍💻',
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

# Set header for dataset view
st.title('Dataset View')

# Create selection option
column1, column2 = st.columns(2)
with column2:
        option = st.selectbox('Choose columns to be viewed',
                              ('All Columns','Numeric Columns','Categorical Columns'))


# Set Catch for data
@st.cache_data(experimental_allow_widgets=True)
def load_data():

    
    # Connect to database in SQL
    db_config = st.secrets['mssql']

    connection_string = (f"DRIVER={{{db_config['Driver']}}};SERVER={db_config['Server']};DATABASE={db_config['Database']};UID={db_config['Username']};PWD={db_config['Password']}")

    conn = pyodbc.connect(connection_string)

    # Preview the dataset from the MSSQL database
    query = "SELECT * FROM dbo.LP2_Telco_churn_first_3000"
    df = pd.read_sql(query, conn).head(100)
    
    conn.close()

    return df

df = load_data()

# Display based on selection
if option == 'Numeric Columns':
    st.subheader('Numeric Columns')
    st.write(df.select_dtypes(include='number'))

elif option == 'Categorical Columns':
    st.subheader('Categorical Columns')
    st.write(df.select_dtypes(include='object'))

else:
    st.subheader('Entire Dataset')
    st.write(df)


with st.expander('**Expand to view data description**'):
    st.markdown('''
    :gray[**The following describes the columns present in the data.**]

**Gender** -- Whether the customer is a male or a female

**SeniorCitizen** -- Whether a customer is a senior citizen or not

**Partner** -- Whether the customer has a partner or not (Yes, No)

**Dependents** -- Whether the customer has dependents or not (Yes, No)

**Tenure** -- Number of months the customer has stayed with the company

**Phone Service** -- Whether the customer has a phone service or not (Yes, No)

**MultipleLines** -- Whether the customer has multiple lines or not

**InternetService** -- Customer's internet service provider (DSL, Fiber Optic, No)

**OnlineSecurity** -- Whether the customer has online security or not (Yes, No, No Internet)

**OnlineBackup** -- Whether the customer has online backup or not (Yes, No, No Internet)

**DeviceProtection** -- Whether the customer has device protection or not (Yes, No, No internet service)

**TechSupport** -- Whether the customer has tech support or not (Yes, No, No internet)

**StreamingTV** -- Whether the customer has streaming TV or not (Yes, No, No internet service)

**StreamingMovies** -- Whether the customer has streaming movies or not (Yes, No, No Internet service)

**Contract** -- The contract term of the customer (Month-to-Month, One year, Two year)

**PaperlessBilling** -- Whether the customer has paperless billing or not (Yes, No)

**Payment Method** -- The customer's payment method (Electronic check, mailed check, Bank transfer(automatic), Credit card(automatic))

**MonthlyCharges** -- The amount charged to the customer monthly

**TotalCharges** -- The total amount charged to the customer

**Churn** -- Whether the customer churned or not (Yes or No)
''')
             
