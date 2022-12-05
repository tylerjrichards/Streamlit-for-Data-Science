import datetime as dt

import pandas as pd
import streamlit as st

st.title("SF Trees")
st.write(
    """
    This app analyses trees in San Francisco using
    a dataset kindly provided by SF DPW. The dataset
    is filtered by the owner of the tree as selected
    in the sidebar!
    """
)
trees_df = pd.read_csv("trees.csv")
owners = st.sidebar.multiselect("Tree Owner Filter", trees_df["caretaker"].unique())
if owners:
    trees_df = trees_df[trees_df["caretaker"].isin(owners)]
df_dbh_grouped = pd.DataFrame(trees_df.groupby(["dbh"]).count()["tree_id"])
df_dbh_grouped.columns = ["tree_count"]
st.line_chart(df_dbh_grouped)

trees_df = trees_df.dropna(subset=["longitude", "latitude"])
trees_df = trees_df.sample(n=1000, replace=True)
st.map(trees_df)

st.stop()
