import os, sys
import streamlit as st
import pandas as pd
from datetime import datetime
from numerize import numerize
from streamlit_echarts import st_echarts


BASE_PATH: str = os.path.realpath(__file__)
sys.path.insert(0, BASE_PATH)
from src.filter import filter_dataframe

#st.set_page_config(page_title="Cost Analysis", page_icon="💰", layout="wide")
# st.image("img/artefact_.png", width = 250)


def _yoy_cost(df):
    st.markdown("#### :grey[YoY of Total Amount]")
   
    df2 =   df.pivot_table(
        index='Year', columns='Vendor', values='Amount', aggfunc='sum').fillna(0)

    years = df2.index.tolist()
    categories = df2.columns.tolist() 
    
    series = [
        {
            "name": category,
            "type": "bar",
            "stack": "total",
            "data": df2[category].tolist()
        }
        for category in categories
    ]

    options = {
        "legend": {
            "orient": "horizontal",
            "top": 5,
        },
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {"type": "shadow"}
        },
        "xAxis": {
            "type": "category",
            "data": years, 
        },
        "yAxis": {
            "type": "value",
            "name": "Amount ($)",
            "nameLocation": "middle",
            "nameRotate": 90,
            "nameGap": 80,
            "axisLabel": {"formatter": '{value}'}
        },
        "series": series
    }

    return st_echarts(options=options, width=1000, height=400)


def _vendor_cost(df):
    st.markdown("#### :grey[Total Amount per Vendor]")
   
    df2 =   df[['Vendor', 'Amount']].groupby('Vendor').sum().sort_values('Amount')
    df2['AmountFormatted'] = df2['Amount'].apply(numerize.numerize)


    vendors = df2.index.tolist()

    options = {
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {"type": "shadow"}
        },
        "grid": {
            "left": "5%",
            "containLabel": True,
            'top': '5%'
        },
        "xAxis": {
            "type": "value",
            "name": "Amount ($)",
            "nameLocation": "middle",
            "nameGap": 30,
            "axisLabel": {"formatter": '{value}'}
        },
        "yAxis": {
            "type": "category",
            "data": vendors,
        },
        "series": [
            {
                "name": "Amount",
                "type": "bar",
                "stack": "total",
                "data": df2['Amount'].tolist(), 
                "label": {
                "show": True,
                "position": "right",
                }
            }
        ]
    }

    return st_echarts(options=options)


def _data_cost_gross(df):
    st.markdown("#### :grey[Cost by Dataset (Total Amount)]")


    options = {
        'tooltip': {
            'trigger': 'axis'
        },
        "legend": {
            "orient": "horizontal",
            "top": 5,
        },
        'grid': {
            'left': '3%',
            'right': '4%',
            'bottom': '3%',
            'containLabel': True
        },
        'xAxis': {
            'type': 'category',
            'boundaryGap': False,
            'data': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        },
        'yAxis': {
            'type': 'value'
        },
        'series': [
            {
            'name': 'Information related to ratings',
            'type': 'line',
            'stack': 'Total',
            'data': [120, 132, 101, 134, 90, 230, 210]
            },
            {
            'name': 'Public Finance',
            'type': 'line',
            'stack': 'Total',
            'data': [220, 182, 191, 234, 290, 330, 310]
            },
            {
            'name': 'Custody',
            'type': 'line',
            'stack': 'Total',
            'data': [150, 232, 201, 154, 190, 330, 410]
            },
            {
            'name': 'Clearing',
            'type': 'line',
            'stack': 'Total',
            'data': [320, 332, 301, 334, 390, 330, 320]
            },
            {
            'name': 'Periodic Statements License',
            'type': 'line',
            'stack': 'Total',
            'data': [820, 932, 901, 934, 1290, 1330, 1320]
            }
        ]
    }

    return st_echarts(options=options)

def _data_cost_perc(df):
    st.markdown("#### :grey[Cost by Dataset (Total Amount Percentage)]")


    options = {
        "legend": {
            "orient": "horizontal",
            "top": 5,
        },
        'tooltip': {
            'trigger': 'axis'
        },
        'xAxis': {
            'type': 'category',
            'data': ['2020', '2021', '2022', '2023', '2024', '2025']
        },
        'yAxis': {
            "type": "value",
            "name": "Amount (%)",
            "nameLocation": "middle",
            "nameRotate": 90,
            "nameGap": 80,
            "label": {
                "show": True,
                "position": "insideTop",  # Position labels inside the top of the bars
                "formatter": "{c}%"  # Display the value as a percentage
            }
        },
        'series': [
            {
            'name': 'Information related to ratings',
            'type': 'bar',
            'stack': 'Total',
            'data': [0, 10, 20, 5, 10, 0]
            },
            {
            'name': 'Public Finance',
            'type': 'bar',
            'stack': 'Total',
            'data': [20, 40, 10, 10, 20, 30]
            },
            {
            'name': 'Custody',
            'type': 'bar',
            'stack': 'Total',
            'data': [20, 10, 50, 40, 30, 40]
            },
            {
            'name': 'Clearing',
            'type': 'bar',
            'stack': 'Total',
            'data': [35, 30, 10, 25, 20, 20]
            },
            {
            'name': 'Periodic Statements License',
            'type': 'bar',
            'stack': 'Total',
            'data': [25, 10, 10, 20, 20, 10]
            }
        ], 
        # "label": {  # Configure label globally for all series
        # "show": True,
        # "position": "insideTop",  # Position labels at the top inside each bar
        # "formatter": "{c}%"  # Display the value as a percentage
        # }
    }

    return st_echarts(options=options)


def cost_analysis():

    data: pd.DataFrame = pd.read_csv("data/csv/fees.csv")
    data["Start"] = pd.to_datetime(data["Start"])
    data["End"] = pd.to_datetime(data["End"])
    data.drop(columns=["Id"], inplace=True)
    print(data.dtypes)

    df = filter_dataframe(data,'Add Filter  ')

    st.markdown("#### :grey[Fees Summary]")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric('Total Contracts', df['Contract'].drop_duplicates().shape[0])
    col2.metric('Fees', df.shape[0])
    col3.metric('Vendors', df['Vendor'].drop_duplicates().shape[0])
    col4.metric('Total Amount ($)', numerize.numerize(df['Amount'].sum()))

    st.write('')

    _yoy_cost(df)

    _vendor_cost(df)

    _data_cost_gross(df)

    _data_cost_perc(df)


