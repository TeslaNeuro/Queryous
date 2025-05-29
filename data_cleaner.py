"""""
 A simple tool to clean and manipulate 
 data with features like handling 
 missing values, renaming columns, and more.
"""""
# TO RUN:
# streamlit run data_cleaner.py

# Author: Arshia Keshvari
# Date: 2025-05-29

import streamlit as st
import pandas as pd
import numpy as np
from io import StringIO

st.set_page_config(page_title="Data Cleaning Tool", layout="wide")
st.title("🧼 Data Cleaning Tool")

# Session state for undo
if "history" not in st.session_state:
    st.session_state.history = []

# File uploader
uploaded_file = st.file_uploader("Upload your CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # Save original for undo
    st.session_state.history.append(df.copy())

    st.subheader("📄 Data Preview")
    st.dataframe(df.head(100), use_container_width=True)

    with st.expander("📊 Missing Values"):
        missing_info = df.isnull().sum()
        st.write(missing_info[missing_info > 0])
        if missing_info.any():
            col = st.selectbox("Choose a column with missing values", missing_info[missing_info > 0].index.tolist())
            method = st.radio("Fill method", ["Drop rows", "Fill with mean", "Fill with median", "Fill with mode", "Custom value"])
            if method == "Custom value":
                custom_value = st.text_input("Enter custom value")
            if st.button("Apply fill"):
                if method == "Drop rows":
                    df = df.dropna(subset=[col])
                elif method == "Fill with mean":
                    df[col] = df[col].fillna(df[col].mean())
                elif method == "Fill with median":
                    df[col] = df[col].fillna(df[col].median())
                elif method == "Fill with mode":
                    df[col] = df[col].fillna(df[col].mode()[0])
                elif method == "Custom value":
                    df[col] = df[col].fillna(custom_value)
                st.success("Missing values handled.")

    with st.expander("🧱 Batch Operations"):
        cols_to_drop = st.multiselect("Select columns to drop", df.columns.tolist())
        if st.button("Drop selected columns"):
            df.drop(columns=cols_to_drop, inplace=True)
            st.success("Selected columns dropped.")

        st.markdown("---")
        st.subheader("Rename Columns")
        col_map = {}
        for col in df.columns:
            new_name = st.text_input(f"Rename '{col}'", value=col)
            col_map[col] = new_name
        if st.button("Apply renaming"):
            df.rename(columns=col_map, inplace=True)
            st.success("Columns renamed.")

    with st.expander("🔁 Duplicate Handling"):
        if st.button("Show duplicates"):
            dups = df[df.duplicated()]
            st.dataframe(dups)
        if st.button("Remove duplicates"):
            df = df.drop_duplicates()
            st.success("Duplicates removed.")

    with st.expander("🔤 String Operations"):
        str_cols = df.select_dtypes(include=str).columns.tolist()
        if str_cols:
            col = st.selectbox("Choose a string column", str_cols)
            op = st.selectbox("Operation", ["Lowercase", "Uppercase", "Trim whitespace", "Replace text"])
            if op == "Replace text":
                to_replace = st.text_input("Text to replace")
                replace_with = st.text_input("Replace with")
            if st.button("Apply string operation"):
                if op == "Lowercase":
                    df[col] = df[col].str.lower()
                elif op == "Uppercase":
                    df[col] = df[col].str.upper()
                elif op == "Trim whitespace":
                    df[col] = df[col].str.strip()
                elif op == "Replace text":
                    df[col] = df[col].str.replace(to_replace, replace_with, regex=False)
                st.success("String operation applied.")

    with st.expander("📈 Data Profiling"):
        profile_col = st.selectbox("Select a column to profile", df.columns)
        col_data = df[profile_col]

        st.write(f"**Data Type:** {col_data.dtype}")
        st.write(f"**Unique Values:** {col_data.nunique()}")
        st.write(f"**Most Frequent Value:** {col_data.mode()[0] if not col_data.mode().empty else 'N/A'}")

        if pd.api.types.is_numeric_dtype(col_data):
            st.write(f"**Min:** {col_data.min()}")
            st.write(f"**Max:** {col_data.max()}")
            st.write(f"**Mean:** {col_data.mean():.2f}")

    with st.expander("🔎 Validate and Convert Data Types"):
        col_to_check = st.selectbox("Column to validate", df.columns)
        current_dtype = df[col_to_check].dtype
        st.write(f"Current type: `{current_dtype}`")

        new_dtype = st.selectbox("Convert to", ["str", "int", "float", "datetime"])
        if st.button("Convert"):
            try:
                if new_dtype == "str":
                    df[col_to_check] = df[col_to_check].astype(str)
                elif new_dtype == "int":
                    df[col_to_check] = pd.to_numeric(df[col_to_check], errors='coerce').astype('Int64')
                elif new_dtype == "float":
                    df[col_to_check] = pd.to_numeric(df[col_to_check], errors='coerce')
                elif new_dtype == "datetime":
                    df[col_to_check] = pd.to_datetime(df[col_to_check], errors='coerce')
                st.success(f"Converted `{col_to_check}` to `{new_dtype}`.")
            except Exception as e:
                st.error(f"Conversion failed: {e}")

    with st.expander("📝 Export Cleaned Data"):
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download CSV", csv, "cleaned_data.csv", "text/csv")

    if st.button("Undo last action") and len(st.session_state.history) > 1:
        st.session_state.history.pop()  # Remove current state
        df = st.session_state.history[-1]  # Restore previous
        st.success("Reverted to previous state.")
        st.dataframe(df.head(100), use_container_width=True)

else:
    st.info("Upload a CSV or Excel file to begin.")
