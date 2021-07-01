import streamlit as st 
import pandas as pd 

 

trees_df = pd.read_csv('trees.csv') 
owners = st.sidebar.multiselect('Tree Owner Filter', trees_df['caretaker'].unique()) 

 

st.title('SF Trees') 
st.write('This app analyses trees in San Francisco using' 
         ' a dataset kindly provided by SF DPW. The ' 
         'histogram below is filtered by tree owner.') 
st.write('The current analysis is of trees owned by {}'.format(owners)) 

 

if owners: 
    trees_df = trees_df[trees_df['caretaker'].isin(owners)]  
    df_dbh_grouped = pd.DataFrame(trees_df.groupby(['dbh']).count()['tree_id']) 
    df_dbh_grouped.columns = ['tree_count'] 
    st.line_chart(df_dbh_grouped) 

trees_df = trees_df.dropna(subset=['longitude', 'latitude']) 
trees_df = trees_df.sample(n = 1000, replace=True) 
st.map(trees_df) 