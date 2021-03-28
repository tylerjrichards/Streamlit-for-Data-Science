import streamlit as st 
import pandas as pd 
import numpy as np 
 
st.title('SF Trees') 
st.write('This app analyses trees in San Francisco using a dataset kindly provided by SF DPW') 
trees_df = pd.read_csv('trees.csv') 
df_dbh_grouped = pd.DataFrame(trees_df.groupby(['dbh']).count()['tree_id']) 
df_dbh_grouped.columns = ['tree_count']
st.line_chart(df_dbh_grouped) 
df_dbh_grouped['new_col'] = np.random.randn(len(df_dbh_grouped)) * 500 
st.line_chart(df_dbh_grouped) 
