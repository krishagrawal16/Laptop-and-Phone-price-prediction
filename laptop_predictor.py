import streamlit as st
import pickle
import numpy as np
import pandas as pd

pipe = pickle.load(open('pipe_final_2.pkl', 'rb'))
df = pickle.load(open('df_final_2.pkl', 'rb'))
df_ohe = pickle.load(open('ohed_2.pkl', 'rb'))

def run():
    st.title("Laptop Predictor")

    laptop_status = st.selectbox('Status', ['New', 'Refurbished'])
    company = st.selectbox('Brand', df['Brand'].unique())
    model = st.selectbox('Model', df['Model'].unique())
    cpu = st.selectbox('CPU Type', df['CPU'].unique())
    ram = st.selectbox('RAM(in GB)', [8, 16, 32, 12, 4, 64, 128])
    storage = st.selectbox('Storage(in GB)', [512, 256, 1000, 64, 128, 2000, 500, 32])
    storage_type = st.selectbox('Storage Type', ['SSD', 'other'])
    gpu = st.selectbox('GPU Type', df['GPU'].unique())
    screen_size = st.number_input('Screen Size')
    touch = st.selectbox('Touch Screen', ['Yes', 'No'])

    if st.button('Predict Price'):
        query_data = {
            'Status(New)': 0,
            'Brand': 0,
            'Model': 0,
            'CPU': 0,
            'RAM': 0,
            'Storage': 0,
            'Storage type(SSD)': 0,
            'GPU': 0,
            'Screen': 0,
            'Touch': 0
        }

        query_data['Status(New)'] = 1 if laptop_status == 'New' else 0
        query_data['Brand'] = company
        query_data['Model'] = model
        query_data['CPU'] = cpu
        query_data['RAM'] = ram
        query_data['Storage'] = storage
        query_data['Storage type(SSD)'] = 1 if storage_type == 'SSD' else 0
        query_data['GPU'] = gpu
        query_data['Screen'] = screen_size
        query_data['Touch'] = 1 if touch == 'Yes' else 0

        query = pd.DataFrame([query_data])
        query = pd.get_dummies(query, columns=['Brand', 'Model', 'CPU', 'GPU'])
        missing_columns = set(df_ohe.columns) - set(query.columns)
        for col in missing_columns:
            query[col] = 0
        query = query[df_ohe.columns]

        p = int(np.exp(pipe.predict(query)[0]))
        f = "{:,.2f}".format(p * 83.5)
        st.title("The predicted price of this configuration is " + f)
