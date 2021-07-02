import streamlit as st 

import pandas as pd 

import seaborn as sns 

import datetime as dt 

import matplotlib.pyplot as plt 

 

st.title('SF Trees') 

st.write('This app analyses trees in San Francisco using' 

         ' a dataset kindly provided by SF DPW. The ' 

         'histogram below is filtered by tree owner.') 

 

#load trees dataset, add age column in days 

trees_df = pd.read_csv('trees.csv') 

trees_df['age'] = (pd.to_datetime('today') - 

                   pd.to_datetime(trees_df['date'])).dt.days 

#add tree owner filter to sidebar, then filter, get color  

owners = st.sidebar.multiselect('Tree Owner Filter', trees_df['caretaker'].unique()) 

graph_color = st.sidebar.color_picker('Graph Colors') 

if owners: 
    trees_df = trees_df[trees_df['caretaker'].isin(owners)]  

 

#group by dbh for leftmost graph 

df_dbh_grouped = pd.DataFrame(trees_df.groupby(['dbh']).count()['tree_id']) 

df_dbh_grouped.columns = ['tree_count'] 

col1, col2 = st.beta_columns(2) 

with col1: 

    st.write('Trees by Width') 

    fig_1, ax_1 = plt.subplots() 

    ax_1 = sns.histplot(trees_df['dbh'],  

    color=graph_color) 

    plt.xlabel('Tree Width') 

    st.pyplot(fig_1) 

with col2: 

    st.write('Trees by Age') 

    fig_2, ax_2 = plt.subplots() 

    ax_2 = sns.histplot(trees_df['age'], 

    color=graph_color) 

    plt.xlabel('Age (Days)') 

    st.pyplot(fig_2) 

 

st.write('Trees by Location') 

trees_df = trees_df.dropna(subset=['longitude', 'latitude']) 

trees_df = trees_df.sample(n = 1000, replace=True) 

st.map(trees_df) 