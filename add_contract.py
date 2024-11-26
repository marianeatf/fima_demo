import os, sys
import streamlit as st
import pandas as pd
from datetime import datetime

BASE_PATH: str = os.path.realpath(__file__)
sys.path.insert(0, BASE_PATH)
from src.filter import filter_dataframe

def add_contract():
    

    # Create 'new_data' directory if it doesn't exist
    os.makedirs('new_data', exist_ok=True)

    # File uploader widget
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

    if uploaded_file is not None:
        # Read the uploaded PDF file
        data = pd.read_csv(uploaded_file)

        # Save the uploaded file to 'new_data' folder
        save_path = os.path.join('new_data', uploaded_file.name)
        with open(save_path, 'wb') as f:
            f.write(uploaded_file.getbuffer())

        # Data processing
        if 'Start' in data.columns:
            data["Start"] = pd.to_datetime(data["Start"])
        if 'End' in data.columns:
            data["End"] = pd.to_datetime(data["End"])
        if 'Id' in data.columns:
            data.drop(columns=["Id"], inplace=True)
        print(data.dtypes)

        # Display data editor
        st.data_editor(
            filter_dataframe(data),
            column_config={
                "Start": st.column_config.DateColumn(),
                "End": st.column_config.DateColumn(),
                "Amount": st.column_config.NumberColumn(format="$%d", step=1),
                "Sub-category": st.column_config.ListColumn(),
            },
            use_container_width=True,
        )
    else:
        st.write("Please upload a CSV file to proceed.")
