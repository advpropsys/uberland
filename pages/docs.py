import streamlit as st

with open('module.md') as f:
    st.write(f.read(), unsafe_allow_html=True)
