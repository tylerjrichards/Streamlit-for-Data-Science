import streamlit as st
import pandas as pd
import pydeck as pdk 

st.title('SF Trees')
st.write('This app analyses trees in San Francisco using'
         ' a dataset kindly provided by SF DPW')

trees_df = pd.read_csv('trees.csv')
trees_df.dropna(how='any', inplace=True)

sf_initial_view = pdk.ViewState(
    latitude=37.77,
    longitude=-122.4,
    zoom=11
    )

sp_layer = pdk.Layer(
    'ScatterplotLayer',
    data = trees_df,
    get_position = ['longitude', 'latitude'],
    get_radius=30)

st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=sf_initial_view,
    layers = [sp_layer]
    ))