
import os, sys
import streamlit as st
from st_aggrid import (
    GridOptionsBuilder,
    AgGrid,
    GridUpdateMode,
    JsCode,
    ColumnsAutoSizeMode,
)
from streamlit_pdf_viewer import pdf_viewer
import pandas as pd

def contracts_page():
    def get_df(df_id, df: pd.DataFrame) -> pd.DataFrame:
        df = df[df["Id"] == df_id]
        df.drop(columns=["Id", "Vendor"], inplace=True)
        return df


    contracts: pd.DataFrame = pd.read_csv("data/csv/contracts.csv")
    datastreams: pd.DataFrame = pd.read_csv("data/csv/data.csv")
    fees: pd.DataFrame = pd.read_csv("data/csv/fees.csv")
    users: pd.DataFrame = pd.read_csv("data/csv/users.csv")

    gb: GridOptionsBuilder = GridOptionsBuilder.from_dataframe(contracts)
    gb.configure_column("Id", width=60)
    gb.configure_column("Contract", width=260)
    gb.configure_column("Vendor", width=140, rowGroup=False)

    gb.configure_column(
        "Total_Fees",
        header_name="Fees (Total)",
        width=110,
        enableValue=True,
        aggFunc="sum",
        type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
        valueFormatter="data.Total_Fees.toLocaleString('en-US', {style: 'currency', currency: 'USD', maximumFractionDigits:2});",
    )
    gb.configure_columns(
        [
            "Date Effective",
            "Date",
            "Date Expiry",
        ],
        filter="agDateColumnFilter",
        width=95,
    )
    gb.configure_columns(["Source Document", "Term Primary", "Term Optional"], hide=True)

    gb.configure_selection(selection_mode="single", use_checkbox=False)


    # gb.configure_side_bar()

    vgo = gb.build()
    data = AgGrid(
        contracts,
        enable_enterprise_modules=True,
        gridOptions=vgo,
        allow_unsafe_jscode=True,
        update_mode=GridUpdateMode.SELECTION_CHANGED,
        height=370,
    )

    selected_rows = data["selected_rows"]


    if isinstance(selected_rows, pd.core.frame.DataFrame):
        tab1, tab2 = st.tabs(["Extracted data", "Source document"])

        with tab1:
            id_ = selected_rows["Id"][0]
            st.markdown(f"#### :navy[{selected_rows['Contract'][0]}]")
            st.markdown(f"#### :grey[{selected_rows['Vendor'][0]}]")
            st.markdown(f"Source Document: {selected_rows['Id'][0]}")

            st.markdown("##### :grey[Data]")
            df = get_df(id_, datastreams)
            st.dataframe(
                df,
                column_config={
                    "Channels": st.column_config.TextColumn(width="large"),
                    "Data": st.column_config.TextColumn(
                        width="large",
                        required=True,
                    ),
                },
                column_order=("Data", "Category", "Frequency", "Channels"),
            )

            st.markdown("##### :grey[Fees]")
            df = get_df(id_, fees)
            st.dataframe(
                df,
                column_config={
                    "Category": st.column_config.TextColumn(width="small"),
                    "Contract": st.column_config.TextColumn(width="large"),
                    "Amount": st.column_config.NumberColumn(width="small"),
                },
                column_order=(
                    "Category",
                    "Sub-Category",
                    "Amount",
                    "Start",
                    "End",
                    "Contract",
                ),
            )

            st.markdown("##### :grey[Users]")
            df = get_df(id_, users)
            st.dataframe(
                df,
                column_config={
                    "Group": st.column_config.TextColumn(width="large"),
                    "Limits": st.column_config.TextColumn(width="large"),
                },
            )

        with tab2:
            pdf_viewer(f"./data/pdf/{id_}.pdf")