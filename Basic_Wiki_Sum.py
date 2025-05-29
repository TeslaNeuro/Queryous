# Basic Research Tool using Streamlit and Wikipedia
# To summarize information about a thing from Wikipedia

import streamlit as st
import wikipedia

st.title("Basic Research Tool")
company = st.text_input("Enter a Basic name")
if company:
    summary = wikipedia.summary(company, sentences=3)
    st.write(summary)
