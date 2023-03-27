import pandas as pd
import streamlit as st

st.title("SF Trees Data Quality App")

st.write(
    """This app is a data quality tool for the SF trees dataset. Edit the data and save to a new file!"""
)

trees_df = pd.read_csv("trees.csv")
trees_df = trees_df.dropna(subset=["longitude", "latitude"])
trees_df_filtered = trees_df[trees_df["legal_status"] == "Private"]


edited_df = st.experimental_data_editor(trees_df_filtered)
trees_df.loc[edited_df.index] = edited_df

if st.button("Save data and overwrite:"):
    trees_df.to_csv("trees.csv", index=False)
    st.write("Saved!")
