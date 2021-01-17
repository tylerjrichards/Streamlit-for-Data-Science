
import streamlit as st
import pandas as pd
import plotly.express as px

st.title('SF Trees')
st.write('This app analyses trees in San Francisco using'
         ' a dataset kindly provided by SF DPW')
st.subheader('Plotly Chart')
trees_df = pd.read_csv('trees.csv')

fig = px.histogram(trees_df['dbh'])
st.plotly_chart(fig)
