import streamlit as st 
from streamlit_embedcode import github_gist

st.title("Github Gist Example") 
st.write("Code from Palmer's Penguin Streamlit app.")
github_gist('https://gist.github.com/tylerjrichards/9dcf6df0c17ccb7b91baafbe3cdf7654')