import streamlit as st
import pdfplumber
import pandas as pd
import re
import io

def setup_page_configuration():
    st.set_page_config(
        page_title="PDF ETL Inspector",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.markdown("""
    <style>
        .main-header {
            font-size: 28px;
            font-weight: 700;
            color: #0F172A;
            margin-bottom: 20px;
            border-bottom: 2px solid #E2E8F0;
            padding-bottom: 10px;
        }
        .section-header {
            font-size: 20px;
            font-weight: 600;
            color: #334155;
            margin-top: 20px;
            margin-bottom: 10px;
        }
        .metric-container {
            background-color: #F8FAFC;
            border: 1px solid #E2E8F0;
            border-radius: 8px;
            padding: 15px;
            text-align: center;
        }
        .status-box {
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 10px;
            font-family: monospace;
        }
        .status-success {
            background-color: #DCFCE7;
            color: #166534;
            border-left: 5px solid #166534;
        }
        .status-info {
            background-color: #DBEAFE;
            color: #1E40AF;
            border-left: 5px solid #1E40AF;
        }
        .stButton button {
            background-color: #0F172A;
            color: white;
            font-weight: bold;
        }
    </style>
    """, unsafe_allow_html=True)

setup_page_configuration()
