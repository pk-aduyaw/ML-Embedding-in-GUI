# Import necessary libraries
import streamlit as st
import pandas as pd
import numpy as np
import pyodbc


# Configure the page
st.set_page_config(
    page_title='Data Viewer',
    page_icon='👨‍💻',
    layout='wide'
)

# Set header for dataset view
st.header('Dataset View')

# Create selection option
option = st.selectbox('Choose columns to be viewed', ('All Columns','Numeric Columns','Categorical Columns'))

# Set Catch for data
@st.cache_data
def load_data():
    # Connect to database in SQL
    db_config = st.secrets['mssql']

    connection_string = (f"DRIVER={{{db_config['Driver']}}};SERVER={db_config['Server']};DATABASE={db_config['Database']};UID={db_config['Username']};PWD={db_config['Password']}")

    conn = pyodbc.connect(connection_string)

    # Preview the dataset from the MSSQL database
    query = "SELECT * FROM dbo.LP2_Telco_churn_first_3000"
    df = pd.read_sql(query, conn)

    # Close connection
    conn.close()
    return df.head(100)
data = st.dataframe(load_data())


# Select columns based on their data type.































