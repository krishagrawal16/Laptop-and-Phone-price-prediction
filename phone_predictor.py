import streamlit as st
import pickle
import numpy as np
import pandas as pd

df = pickle.load(open('df_1.pkl', 'rb'))
model = pickle.load(open('pipe_1.pkl', 'rb'))
X_train = pickle.load(open('X_train_1.pkl', 'rb'))

def run():
    st.title("Mobile Phone Predictor")

    Company = st.selectbox('Brand', df['model_brand'].unique())
    Model = st.selectbox('Model', df['model'].unique())
    RAM = st.number_input('RAM(in GB)')
    Memory = st.number_input('Memory(in GB)')
    rating = st.number_input('Rating')
    Rear_Camera = st.number_input('Rear Camera(in MP)')
    num_rear_cameras = st.number_input('Number of Rear Cameras')
    Front_Camera = st.number_input('Front Camera(in MP)')
    _5G = st.selectbox('5G', ['Yes', 'No'])
    Battery = st.number_input('Battery Capacity')
    Processor = st.selectbox('Processor', df['processor_brand'].unique())
    Processor_speed = st.number_input('Processor Speed')
    fast_charging = st.number_input('Fast Charging')
    screen_size = st.number_input('Screen Size')
    refresh_rate = st.number_input('Refresh Rate')
    os = st.selectbox('OS', df['os'].unique())
    extended_memory_available = st.selectbox('Extended Memory', ['Yes', 'No'])
    Resolution_height = st.number_input('Resolution height')
    Resolution_width = st.number_input('Resolution Width')

    if st.button('Predict Price'):
        query_data = {
            '5G_or_not': 0,
            'avg_rating': 0,
            'processor_brand': 0,
            'processor_speed': 0,
            'battery_capacity': 0,
            'fast_charging': 0,
            'ram_capacity': 0,
            'internal_memory': 0,
            'screen_size': 0,
            'refresh_rate': 0,
            'num_rear_cameras': 0,
            'os': 0,
            'primary_camera_rear': 0,
            'primary_camera_front': 0,
            'extended_memory_available': 0,
            'resolution_height': 0,
            'resolution_width': 0,
            'model_brand': 0,
            'model': 0
        }

        query_data['5G_or_not'] = 1 if _5G == 'Yes' else 0
        query_data['avg_rating'] = rating
        query_data['processor_brand'] = Processor
        query_data['processor_speed'] = Processor_speed
        query_data['battery_capacity'] = Battery
        query_data['fast_charging'] = fast_charging
        query_data['ram_capacity'] = RAM
        query_data['internal_memory'] = Memory
        query_data['screen_size'] = screen_size
        query_data['refresh_rate'] = refresh_rate
        query_data['num_rear_cameras'] = num_rear_cameras
        query_data['os'] = os
        query_data['primary_camera_rear'] = Rear_Camera
        query_data['primary_camera_front'] = Front_Camera
        query_data['extended_memory_available'] = 1 if extended_memory_available == 'Yes' else 0
        query_data['resolution_height'] = Resolution_height
        query_data['resolution_width'] = Resolution_width
        query_data['model_brand'] = Company
        query_data['model'] = Model

        query = pd.DataFrame([query_data])
        query = pd.get_dummies(query, columns=['model_brand', 'processor_brand', 'os', 'model'])
        missing_columns = set(X_train.columns) - set(query.columns)
        for col in missing_columns:
            query[col] = 0
        query = query[X_train.columns]

        p = int(np.exp(model.predict(query)[0]))
        f = "{:,.2f}".format(p)
        st.title("The predicted price of this configuration is " + f)
