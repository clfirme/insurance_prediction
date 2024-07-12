import os
import pickle
import pandas as pd
import streamlit as st

if 'model_loaded' not in st.session_state:
    st.session_state.model_loaded = False
    st.session_state.model = None  # Ensure model key exists

# Page config
st.set_page_config(
    page_title='Insurance Prediction'
)

st.title('Group Medical Insurance Prediction')
st.markdown("Predict medical insurance using a CSV file")

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

data = st.file_uploader('Upload a CSV file')
if data is not None:
    if data.name.endswith('.csv'):
        df_input = pd.read_csv(data)
        if st.session_state.model is not None:  # Check if model is loaded
            insurance_cost = st.session_state.model.predict(df_input)
            df_output = df_input.assign(prediction=insurance_cost)
            st.markdown('Insurance cost prediction:')
            st.write(df_output)  # Display the output DataFrame
            st.download_button(
                label='Download CSV file', data=df_output.to_csv(index=False).encode('utf-8'),
                mime='text/csv', file_name='predicted_insurance.csv'
            )
        else:
            st.error("Model not loaded correctly.")
    else:
        st.error("Only CSV files are accepted. Please upload a CSV file.")
