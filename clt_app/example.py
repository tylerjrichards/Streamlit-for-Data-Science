import streamlit as st   
import numpy as np   
import matplotlib.pyplot as plt  

with st.form('first form'):
	perc_heads = st.number_input(label='Chance of Coins Landing on Heads', min_value=0.0, 	max_value=1.0, value=.5)  
	graph_title = st.text_input(label='Graph Title') 
	my_submit_button = st.form_submit_button()

binom_dist = np.random.binomial(1, perc_heads, 1000)  
list_of_means = []  
for i in range(0, 1000):
	list_of_means.append(np.random.choice(binom_dist, 100, replace=True).mean())  

fig, ax = plt.subplots()  
plt.hist(list_of_means, range=[0,1]) 
plt.title(graph_title) 
st.pyplot(fig) 