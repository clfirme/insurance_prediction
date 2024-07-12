import streamlit as st

# Page config
st.set_page_config(
    page_title='Insurance Prediction',
    page_icon='./img/stethoscope.jpeg'
)

# Handle page navigation based on query parameters
query_params = st.query_params
page = query_params.get('page', [None])[0]

if page == 'individual':
    import pages.individual_prediction as individual
    individual.run_individual_prediction()
elif page == 'group':
    import pages.group_prediction as group
    group.run_group_prediction()
else:
    # Main home content
    st.title('Medical Insurance Prediction')
    st.image('./img/doctor.jpeg', width=200)
    st.markdown(
        """
        This company predicts medical insurance costs based on age, BMI, children count, and smoking status for clients. 
        The model uses these factors to estimate individual insurance expenses.
        By considering these variables, the company offers personalized insurance quotes to clients.
        This approach helps clients make informed decisions regarding their medical insurance coverage.

        There are four important features for the medical insurance prediction:
        1) Age; 
        2) BMI (body mass index); 
        3) Number of children; 
        4) Smoker or not.
        """
    )
