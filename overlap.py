import os, sys
import streamlit as st
import pandas as pd
import seaborn as sns
import locale
from src.filter import filter_dataframe

def overlap():
    locale.setlocale(locale.LC_ALL, "en_US.UTF-8")

    cm = sns.dark_palette((20, 60, 50), input="husl", as_cmap=True)

    BASE_PATH: str = os.path.realpath(__file__)
    sys.path.insert(0, BASE_PATH)


    

    data: pd.DataFrame = pd.read_csv("data/csv/fees.csv")
    data["Start"] = pd.to_datetime(data["Start"]).dt.strftime("%Y-%m-%d")
    data["End"] = pd.to_datetime(data["End"]).dt.strftime("%Y-%m-%d")
    data.drop(columns=["Id"], inplace=True)

    dff = filter_dataframe(data,'Add filters ')
    sum_fees = dff["Amount"].sum()
    sum_ = locale.currency(sum_fees, grouping=True)
    vendors_ = list(dff["Vendor"].unique())
    vendors_ = ", ".join(vendors_)
    vendors_ = vendors_[:-1]


    col1, col2 = st.columns(2)
    with col1:
        try:
            st.bar_chart(
                dff[["Year", "Amount", "Vendor"]], x="Year", y="Amount", color="Vendor"
            )
        except:
            print("")
    with col2:
        st.markdown("##### :grey[Summary]")
        st.markdown(f"Total fees: **{sum_}**")
        st.markdown(f"Vendors: {vendors_}")
        st.markdown("")


    st.dataframe(
        # dff.style \
        #     .format(subset="Amount", precision=2, thousands=",", decimal=".", ) \
        #     .text_gradient(cmap=cm),
        dff,
        hide_index=True,
        column_config={
            "Category": st.column_config.TextColumn(width="small"),
            "Sub-Category": st.column_config.TextColumn(width="small"),
            "Amount": st.column_config.NumberColumn(width="small"),
            # "Prop": st.column_config.BarChartColumn(label=""),
            "Start": st.column_config.DateColumn(width="small", format="DD.MM.YYYY"),
            "End": st.column_config.DateColumn(width="small", format="DD.MM.YYYY"),
            "Contract": st.column_config.TextColumn(width="large"),
            "Vendor": st.column_config.TextColumn(width="small"),
        },
        use_container_width=True,
        column_order=(
            "Category",
            "Sub-Category",
            "Amount",
            "Start",
            "End",
            "Vendor",
            "Contract",
        ),
    )
