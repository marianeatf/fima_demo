import os, sys
import streamlit as st
import pandas as pd
from datetime import datetime

BASE_PATH: str = os.path.realpath(__file__)
sys.path.insert(0, BASE_PATH)
from src.filter import filter_dataframe


def market_data():

    data: pd.DataFrame = pd.read_csv("data/csv/market.csv")
    # data['Start'] = data['Start'].apply(lambda x: datetime.strftime(x, format="%Y-%m-%d"))
    data["Start"] = pd.to_datetime(data["Start"])
    data["End"] = pd.to_datetime(data["End"])
    data.drop(columns=["Id"], inplace=True)
    print(data.dtypes)


    st.data_editor(
        filter_dataframe(data,'Add filters'),
        column_config={
            "Start": st.column_config.DateColumn(),
            "End": st.column_config.DateColumn(),
            # "Amount": st.column_config.LinkColumn(max_chars=4),
            "Amount": st.column_config.NumberColumn(format="$%d", step=1),
            "Sub-category": st.column_config.ListColumn(),
        },
        use_container_width=True,
    )
