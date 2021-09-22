import streamlit as st
import numpy as np
import pickle

## title
st.title("Should This Loan be Approved or Denied?")


## information needed to make a prediction
NAICS = st.selectbox("Industry of the business", 
         ["11 Agriculture, forestry, fishing and hunting", "21	Mining, quarrying, and oil and gas extraction",
          "22 Utilities", "23 Construction", "31–33	Manufacturing", "42	Wholesale trade",
          "44–45 Retail trade", "48–49 Transportation and warehousing", "51	Information", "52	Finance and insurance",
          "53 Real estate and rental and leasing", "54	Professional, scientific, and technical services",
          "55 Management of companies and enterprises", "56	Administrative and support and waste management and remediation services",
          "61 Educational services", "62 Health care and social assistance", "71 Arts, entertainment, and recreation",
          "72 Accommodation and food services", "81	Other services (except public administration)", "92 Public administration"])
GrAppv = st.text_input("Gross Amount of loan Approved by Bank", 'Type Here ...')
SBA_Appv = st.text_input("SBA’s Guaranteed Amount of Loan", 'Type Here ...')
Term = st.slider("Loan Term (Months)", 0, 360)
UrbanRural = st.radio("Select location:", ("Rural", "Urban"))
RevLineCr = st.radio("Revolving Line of Credit:",("Yes","No"))
LowDoc = st.radio("LowDoc Loan Program:",("Yes","No"))
NoEmp = st.text_input("Number of Employees", 'Type Here ...')
CreateJob = st.text_input("Number of Jobs Created", 'Type Here ...')
RetainedJob = st.text_input("Number of Jobs Retained", 'Type Here ...')


## encode inputs
NAICS_dict = {
    "21 Mining, quarrying, and oil and gas extraction": [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "22 Utilities": [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    "23 Construction": [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    "31–33	Manufacturing": [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    "42	Wholesale trade": [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "44–45 Retail trade": [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    "48–49 Transportation and warehousing": [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    "51	Information": [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    "52	Finance and insurance": [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "53 Real estate and rental and leasing": [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    "54	Professional, scientific, and technical services": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    "55 Management of companies and enterprises": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], 
    "56	Administrative and support and waste management and remediation services": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    "61 Educational services": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], 
    "62 Health care and social assistance": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0], 
    "71 Arts, entertainment, and recreation": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    "72 Accommodation and food services": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], 
    "81	Other services (except public administration)": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0], 
    "92 Public administration": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
}

UrbanRural_dict = {
    "Urban": 1,
    "Rural": 2
}

RevLineCr_dict = {
    "Yes": 1,
    "No": 0
}

LowDoc_dict = {
    "Yes": 1,
    "No": 0
}

def return_val(dict_name, user_inp):
    for key, val in dict_name.items():
        if user_inp == key:
            return val


new_NAICS = return_val(NAICS_dict, NAICS)
new_UrbanRural = return_val(UrbanRural_dict, UrbanRural)
new_RevLineCr = return_val(RevLineCr_dict, RevLineCr)
new_LowDoc = return_val(LowDoc_dict, LowDoc)


## input to use
inp_data = [1.0, Term, int(NoEmp), int(CreateJob), int(RetainedJob), new_UrbanRural, float(GrAppv), float(SBA_Appv)]
inp_data += new_NAICS
add_info = [new_RevLineCr, new_LowDoc]
inp_data = inp_data + add_info
inp_data = np.array(inp_data).reshape(1, -1)

## Make a prediction
if st.button("Predict the Result!"):
    model = pickle.load(open("rf_smote_enn.pkl", 'rb'))
    pred = model.predict(inp_data)
    likelihood = model.predict_proba(inp_data)[:,1]
    
    st.header("Probability of Default: " + str((np.around(likelihood[0], 3))))
    if likelihood > 0.5:
        st.subheader("Unfortunately, it is risky to approve the loan.")
    else:
        st.subheader(st.subheader("It is safe to approve the loan!"))