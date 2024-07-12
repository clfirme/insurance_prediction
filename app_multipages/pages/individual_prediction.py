import os
import pickle
import pandas as pd
import streamlit as st

# Initialize session state variables
if 'bmi' not in st.session_state:
    st.session_state.bmi = None

if 'model_loaded' not in st.session_state:
    st.session_state.model_loaded = False

# Page config
st.set_page_config(
    page_title='Insurance Prediction'
)

st.title('Individual Medical Insurance Prediction')

# Input fields for age, height, and weight
age = st.number_input(label='Enter your age', min_value=18, max_value=120, step=1, format='%d')
height = st.number_input(label='Enter height in meters', min_value=0.0, step=0.01)
weight = st.number_input(label='Enter weight in kg', min_value=0.0, step=0.1)

def calculate_bmi():
    if height > 0 and weight > 0:
        st.session_state.bmi = weight / (height ** 2)
    else:
        st.warning("Please enter both height and weight.")

# Button to calculate BMI
if st.button('Calculate BMI'):
    calculate_bmi()
    if st.session_state.bmi:
        st.write(f'Body Mass Index (BMI): {st.session_state.bmi:.2f}')

children = st.slider(label='Children', min_value=0, max_value=5)
smoker = st.selectbox(label='Smoker', options=['no', 'yes'])

# Load model if not already loaded
if not st.session_state.model_loaded:
    # Get the directory where the current script is located
    current_script_dir = os.path.dirname(__file__)

    # Construct the absolute path to the model file
    model_path = os.path.abspath(os.path.join(current_script_dir, '..', '..', 'model', 'model.pkl'))

    # Load the model file
    try:
        with open(model_path, 'rb') as model_file:
            st.session_state.model = pickle.load(model_file)
        st.session_state.model_loaded = True
        st.write("Model loaded successfully.")
    except Exception as e:
        st.error(f"Error loading model: {e}")

# Prediction function
def prediction():
    df_input = pd.DataFrame([{
        'age': age,
        'bmi': st.session_state.bmi,
        'children': children,
        'smoker': smoker
    }])
    st.write("Data passed to model for prediction:", df_input)  # Debug: show input data
    prediction = st.session_state.model.predict(df_input)[0]
    return prediction

# Button to predict insurance cost
if st.button('Predict'):
    if st.session_state.bmi is not None:
        try:
            insurance_cost = prediction()
            st.success(f'**Prediction insurance price:** ${insurance_cost:,.2f}')
        except Exception as error:
            st.error(f"Couldn't predict the input data. The following error occurred: \n\n{error}")
    else:
        st.warning("Please calculate the BMI first.")
