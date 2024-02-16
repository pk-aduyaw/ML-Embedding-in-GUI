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
    df = pd.read_sql(query, conn).head(100)

    # Close connection
    conn.close()
    return df

df = load_data().head(100)

# Display based on selection
if option == 'Numeric Columns':
    st.subheader('Numeric Data')
    st.write(df.select_dtypes(include='number'))

elif option == 'Categorical Columns':
    st.subheader('Categorical Data')
    st.write(df.select_dtypes(include='object'))

else:
    st.subheader('Entire Dataset')
    st.write(df)





























