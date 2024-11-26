import streamlit as st
import os
# Set page config for wider layout
st.set_page_config(layout="wide", page_title="Market Analysis")
import base64

from contracts_page import contracts_page
from market_page import market_data
from overlap import overlap
from add_contract import add_contract
from cost_analysis import cost_analysis

def get_base64_of_bin_file(file_path):
    with open(file_path, 'rb') as file:
        data = file.read()
    return base64.b64encode(data).decode()

# Encode your logo
logo_base64 = get_base64_of_bin_file("img/icon_atf.png")


# Path to the uploaded local image
#logo_path = "img/background.jpg"  # Update to your uploaded file path

# Encode the image
#base64_image = get_base64_of_bin_file(logo_path)

# Custom CSS for design

# Set page config

# Custom CSS to completely remove the sidebar
hide_sidebar_and_adjust_content = """
    <style>
        [data-testid="stSidebar"] {
            display: none;  /* Hide the sidebar */
        }
        [data-testid="stAppViewContainer"] {
            margin-left: 0;  /* Remove left margin for the content */
            padding: 0;      /* Optional: Remove padding around the content */
        }
        [data-testid="stHeader"] {
            padding-top: 0;  /* Optional: Adjust header spacing */
        }
    </style>
"""
st.markdown(hide_sidebar_and_adjust_content, unsafe_allow_html=True)

st.markdown(f"""
    <style>
    /* General body style */
    body {{
        margin-left:-1000px;
        font-family: 'Arial', sans-serif;
    }}
    /* Header with background image */
    .header-container {{
            background-image:linear-gradient(#0A1128, #002244, #0A1128);
            display: flex;
            justify-content: space-between;
            align-items: center;
            height: 200px;
        }}
        .header-title {{
            padding: 20px;
            color:white;
            font-size: 30px;
            font-weight: bold;
            margin: 0;
        }}
        .header-logo img {{
            max-width: 150px;
            padding-right: 20px;
            height: auto;
        }}
    /* Navigation bar */
    .nav-bar {{
        background-color: #34495E;
        padding: 10px 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        display: flex;
        justify-content: center;
        gap: 20px;
    }}
    .nav-bar a {{
        color: white;
        text-decoration: none;
        font-weight: bold;
    }}
    .nav-bar a:hover {{
        text-decoration: underline;
    }}
    /* Links in columns */
    .links-section {{
        padding: 20px;
        background-color: #ECF0F1;
        border-radius: 10px;
    }}
    .link-column {{
        text-align: center;
        padding: 10px;
    }}
    .link-column a {{
        display: block;
        margin: 5px 0;
        color: #2980B9;
        text-decoration: none;
    }}
    .link-column a:hover {{
        text-decoration: underline;
    }}
            </style>
            """, unsafe_allow_html=True)

st.markdown(f"""
    
            <div class="header-container">
            <div class="header-title">Market Data Contract Management Tool</div>
            <div class="header-logo">
            <img src="data:image/png;base64,{logo_base64}" width="50" height="50" alt="Logo">
        </div>
    </div>
""",unsafe_allow_html=True)


# Define the paths to the pages

hide_sidebar_style = """
    <style>
        [data-testid="stSidebar"] {visibility: hidden;}
        [data-testid="stSidebarNav"] {visibility: hidden;}
        [data-testid="collapsedControl"] {visibility: hidden;}
    </style>
"""
st.markdown(hide_sidebar_style, unsafe_allow_html=True)

tabs = st.tabs(["Home", "Contracts", "Cost Analysis", "Market Data", "Overlap", "Add Contract"])

# Assign functionality to each tab
with tabs[0]:
    st.subheader("Centralized solution for managing market data contracts effectively.")
    st.markdown(
    """
    Welcome to our Market Data Contract Management Tool! This application helps you:""")

    # Create 4 columns
    col1, col2, col3, col4 = st.columns(4)

    # Define the card content
    cards = [
        {"icon": "📦", "text": "Eliminate data redundancy"},
        {"icon": "✔️", "text": "Ensure compliance with contract terms"},
        {"icon": "💰", "text": "Track costs efficiently"},
        {"icon": "📅", "text": "Manage contract renewals with ease"},
    ]

    # Populate the columns with cards
    for col, card in zip([col1, col2, col3, col4], cards):
        with col:
            st.markdown(
                f"""
                <div style="height:200px; text-align: center; background-color: #f4f4f4; border-radius: 10px; padding: 20px; box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);">
                    <div style="font-size: 50px;">{card['icon']}</div>
                    <div style="margin-top: 10px; font-size: 16px; font-weight: bold;">{card['text']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
with tabs[1]:
    st.title("Contracts")
    st.write("This is the Contracts page.")
    contracts_page()

with tabs[2]:
    st.title("Market Data")
    st.write("This is the Market Data page.")
    # Call the function or logic for Market Data page
    cost_analysis()

with tabs[3]:
    st.title("Market Data")
    st.write("This is the Market Data page.")
    # Call the function or logic for Market Data page
    market_data()

with tabs[4]:
    st.title("Overlap")
    st.write("This is the Overlap page.")
    overlap()

with tabs[5]:
    st.title("Add Contract")
    st.write("This is the Add Contract page.")
    # Call the function or logic for Add Contract page
    add_contract()

    



        
        #st.write(f"Redirecting to {tab_name} page...")
        #os.system(f"streamlit run {page_paths[tab_name]}")

