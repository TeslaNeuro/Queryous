"""""
 Basic Research Tool using Streamlit and Wikipedia
 To summarize information about a thing from Wikipedia
"""""
# TO RUN:
# streamlit run Basic_Wiki_Sum.py

# Author: Arshia Keshvari
# Date: 2025-05-29

import streamlit as st
import wikipedia

st.title("Basic Research Tool")
company = st.text_input("Enter a Basic name")
if company:
    summary = wikipedia.summary(company, sentences=8)
    st.write(summary)
