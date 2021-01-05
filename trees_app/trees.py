import streamlit as st
import pandas as pd

trees_df = pd.read_csv('trees.csv')
st.write(trees_df.head())