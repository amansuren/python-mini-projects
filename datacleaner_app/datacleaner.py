import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="📑 Data Cleaner", layout="wide")
st.title("Data Cleaner")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualisation!")

upload_files = st.file_uploader(
    "Upload your files (CSV or Excel):",
    type=["csv", "xlsx"],
    accept_multiple_files=True
)

if upload_files:
    for file in upload_files:
        # 1. Determine extension
        file_ext = os.path.splitext(file.name)[-1].lower()

        # 2. Read into a DataFrame (or error out)
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue  # Skip the rest for this file

        # 3. Show file metadata + preview
        st.write(f"**File Name:** {file.name}")
        st.write(f"**File Size:** {file.size / 1024:.2f} KB")
        st.write("Preview the head of the DataFrame:")
        st.dataframe(df.head())

        # 4. Data Cleaning UI for this file
        st.subheader(f"Data Cleaning options for {file.name}")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates removed!")

            with col2:
                if st.button(f"Fill missing values for {file.name}"):
                    # Note: use 'number' not 'numbers'
                    numeric_cols = df.select_dtypes(include=["number"]).columns
                    if len(numeric_cols) == 0:
                        st.warning("No numeric columns found to fill.")
                    else:
                        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                        st.write("Missing values have been filled!")
