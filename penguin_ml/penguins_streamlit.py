import streamlit as st
st.title('Penguin Classifier') 

st.write("This app uses 6 inputs to predict the species of penguin using " 

         "a model built on the Palmer's Penguin's dataset. Use the form below" 

         " to get started!") 

  

password_guess = st.text_input('What is the Password?') 

if password_guess != 'streamlit_is_great': 
  st.stop() 

  

penguin_file = st.file_uploader('Upload your own penguin data') 