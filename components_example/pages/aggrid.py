import pandas as pd
import streamlit as st
from st_aggrid import AgGrid

st.title("Streamlit AgGrid Example: Penguins")
penguins_df = pd.read_csv("penguins.csv")
st.write("AgGrid DataFrame:")
response = AgGrid(penguins_df, height=500, editable=True)
df_edited = response["data"]
st.write("Edited DataFrame:")
st.dataframe(df_edited)

st.stop()
st.write(response["data"])
st.stop()
selected_rows = response["selected_rows"]
st.write(response)
st.write(selected_rows)
