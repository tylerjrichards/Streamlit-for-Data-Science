import streamlit as st
import numpy as np
import plotly.express as px

st.title('Deciding Survey Sample Size')
'''
Please use the following app to see how 
representative and expensive a set sample
is for our survey design. 
'''
np.random.seed(1)
num_surveys = 100
num_surveys = st.slider(label='Number of Surveys Sent', 
	min_value=5, max_value=150, value=50)
max_amount = st.number_input(label='What is the max you want to spend?', 
	value=num_surveys*50, step=500)
user_time_spent = np.random.normal(50.5, 10, 1000)
my_sample = np.random.choice(user_time_spent, num_surveys)

#costing section
expected_cost = 50 * num_surveys
percent_change_over = 100 * sum(np.random.binomial(num_surveys, 0.1, 10000) > max_amount/500)/10000
st.write(f'The expected cost of this sample is {expected_cost}')
st.write(f'The percent chance the cost goes over {max_amount} is {percent_change_over}')

fig = px.histogram(user_time_spent, title='Total Time Spent')
fig.update_traces(xbins=dict(start=0,end=100, size=5))
st.plotly_chart(fig)

fig = px.histogram(my_sample, title='Sample Time Spent')
fig.update_traces(xbins=dict(start=0,end=100, size=5))
st.plotly_chart(fig)