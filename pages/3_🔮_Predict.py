import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
import requests
from sklearn.base import BaseEstimator, TransformerMixin
import joblib
import imblearn

# Configure the page
st.set_page_config(
    page_title='Predictions',
    page_icon='🔮',
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

# ------ Set header for page
st.title('Predict Churn Status')

column1, column2 = st.columns([.6, .4])
with column1:
    model_option = st.selectbox('Choose which model to use for prediction', options=['Gradient Boosting', 'Support Vector'])


# Load trained machine learning model and encoder from GitHub
github_model1_url = 'https://raw.githubusercontent.com/pk-aduyaw/Customer_Churn_Classification_Project/master/model/GradientBoosting.joblib'
github_model2_url = 'https://raw.githubusercontent.com/pk-aduyaw/Customer_Churn_Classification_Project/master/model/SupportVector.joblib'
encoder_url = 'https://raw.githubusercontent.com/pk-aduyaw/Customer_Churn_Classification_Project/master/model/label_encoder.joblib'


# -------- Function to load the model from GitHub
@st.cache_resource(show_spinner=True, experimental_allow_widgets=True)
def gb_pipeline():
    response = requests.get(github_model1_url)
    model_bytes = BytesIO(response.content)
    pipeline = joblib.load(model_bytes)
    return pipeline

@st.cache_resource(show_spinner=False, experimental_allow_widgets=True)
def sv_pipeline():
    response = requests.get(github_model2_url)
    model_bytes = BytesIO(response.content)
    pipeline = joblib.load(model_bytes)
    return pipeline

# --------- Function to load encoder from GitHub
def load_encoder():
    response = requests.get(encoder_url)
    encoder_bytes = BytesIO(response.content)
    encoder = joblib.load(encoder_bytes)
    return encoder

# --------- Create a function for model selection
def select_model():
    # ------- Option for first model
    if model_option == 'Gradient Boosting':
        model = gb_pipeline()
        encoder = load_encoder()
    # ------- Option for second model
    if model_option == 'Support Vector':
        model = sv_pipeline()
        encoder = load_encoder()
    return model, encoder


# Custom function to deal with cleaning the total charges column
class TotalCharges_cleaner(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        # Replace empty string with NA
        X['TotalCharges'].replace(' ', np.nan, inplace=True)

        # Convert the values in the Totalcharges column to a float
        X['TotalCharges'] = X['TotalCharges'].transform(lambda x: float(x))
        return X
    
    # Serialization methods
    def __getstate__(self):
        # Return state to be serialized
        return {}

    def __setstate__(self, state):
        # Restore state from serialized data
        pass
    
    # Since this transformer doesn't remove or alter features, return the input features
    def get_feature_names_out(self, input_features=None):
        return input_features


# Create a class to deal with dropping Customer ID from the dataset
class columnDropper(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        # Drop the specified column
        return X.drop('customerID', axis=1)
    
    def get_feature_names_out(self, input_features=None):
        # If input_features is None or not provided, return None
        if input_features is None:
            return None
        # Return feature names after dropping the specified column
        return [feature for feature in input_features if feature != 'customerID']


# ------- Create a function to make prediction
def make_prediction(model, encoder):
    df = st.session_state['df']
    # -------- Get the value for predicted
    prediction = model.predict(df)
    prediction = encoder.inverse_transform(prediction)
    st.session_state['prediction'] = prediction

    # -------- Get the value for prediction probability
    prediction_proba = model.predict_proba(df)
    st.session_state['prediction_proba'] = prediction_proba

    return prediction, prediction_proba

# ------- Prediction page creation
def input_features():

    with st.form('features'):

        model, encoder = select_model()
        col1, col2, col3 = st.columns(3)
        # ------ Collect customer information
        with col1:
            st.subheader('Demographics')
            customer_id = st.text_input('Customer ID', placeholder='eg. 1234-ABCD', key='customer_id')
            gender = st.radio('Gender', options=['Male', 'Female'],horizontal=True, key='gender')
            partners = st.radio('Partners', options=['Yes', 'No'],horizontal=True, key='partners')
            dependents = st.radio('Dependents', options=['Yes', 'No'],horizontal=True, key='dependents')
            senior_citizen = st.radio("Senior Citizen ('Yes-1, No-0')", options=[1, 0],horizontal=True, key='senior_citizen')
        
        # ------ Collect customer account information
        with col2:
            st.subheader('Customer Account Info.')
            tenure = st.number_input('Tenure', min_value=0, max_value=70, key='tenure')
            contract = st.selectbox('Contract', options=['Month-to-month', 'One year', 'Two year'], key='contract')
            payment_method = st.selectbox('Payment Method',
                                        options=['Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)'],
                                        key='payment_method')
            paperless_billing = st.radio('Paperless Billing', ['Yes', 'No'], horizontal=True, key='paperless_billing')
            monthly_charges = st.number_input('Monthly Charges', placeholder='Enter amount...', key='monthly_charges')
            total_charges = st.number_input('Total Charges', placeholder='Enter amount...', key='total_charges')
            

        # ------ Collect customer subscription information
        with col3:
            st.subheader('Subscription')
            phone_service = st.radio('Phone Service', ['Yes', 'No'], horizontal=True, key='phone_service')
            multiple_lines = st.selectbox('Multiple Lines', ['Yes', 'No', 'No internet servie'], key='multiple_lines')
            internet_service = st.selectbox('Internet Service', ['DSL','Fiber optic', 'No'], key='internet_service')
            online_security = st.selectbox('Online Security', ['Yes', 'No', 'No internet servie'], key='online_security')
            online_backup = st.selectbox('Online Backup', ['Yes', 'No', 'No internet servie'], key='online_backup')
            device_protection = st.selectbox('Device Protection', ['Yes', 'No', 'No internet servie'], key='device_protection')
            tech_support = st.selectbox('Tech Support', ['Yes', 'No', 'No internet servie'], key='tech_support')
            streaming_tv = st.selectbox('Streaming TV', ['Yes', 'No', 'No internet servie'], key='streaming_tv')
            streaming_movies = st.selectbox('Streaming Movies', ['Yes', 'No', 'No internet servie'], key='streaming_movies')



        # Create a DataFrame with the input features
        input_data = pd.DataFrame({
                'customerID': [customer_id],
                'gender': [gender],
                'SeniorCitizen': [senior_citizen],
                'Partner': [partners],
                'Dependents': [dependents],
                'tenure': [tenure],
                'PhoneService': [phone_service],
                'MultipleLines': [multiple_lines],
                'InternetService': [internet_service],
                'OnlineSecurity': [online_security],
                'OnlineBackup': [online_backup],
                'DeviceProtection': [device_protection],
                'TechSupport': [tech_support],
                'StreamingTV': [streaming_tv],
                'StreamingMovies': [streaming_movies],
                'Contract': [contract],
                'PaperlessBilling': [paperless_billing],
                'PaymentMethod': [payment_method],
                'MonthlyCharges': [monthly_charges],
                'TotalCharges': [total_charges]
            })
        st.session_state['df'] = input_data
        st.form_submit_button('Submit', on_click=make_prediction, kwargs=dict(model=model, encoder=encoder))
    return input_data

if __name__ == '__main__':
    columnDropper()
    TotalCharges_cleaner()
    input_features()

if 'prediction' not in st.session_state:
    st.session_state['prediction'] = None

else:
    value = st.session_state['prediction']
    st.write(value)
