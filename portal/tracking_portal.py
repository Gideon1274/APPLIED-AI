import streamlit as st
import sqlite3
import pandas as pd
import os

# --- CONFIGURATION ---
st.set_page_config(page_title="PASTrack - Public Portal", page_icon="🏛️", layout="centered")

def get_db_connection():
    # Assumes the database is in the parent directory or same relative path
    # In a real deployment with separate repos, you'd use a shared RDS/Postgres
    db_path = os.path.join("..", "pas_track.db")
    if not os.path.exists(db_path):
        db_path = "pas_track.db" # Fallback
    return sqlite3.connect(db_path)

def local_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            background-color: #F8FAFC;
        }
        
        .portal-header {
            text-align: center;
            padding: 3rem 1rem;
            background: linear-gradient(135deg, #1E3A8A 0%, #1E40AF 100%);
            color: white;
            border-radius: 0 0 20px 20px;
            margin-bottom: 2rem;
        }
        
        .stButton>button {
            background-color: #F59E0B;
            color: #1E3A8A;
            border-radius: 8px;
            font-weight: 700;
            height: 3rem;
        }
        
        .status-badge {
            padding: 0.5rem 1rem;
            border-radius: 999px;
            font-weight: 600;
            display: inline-block;
        }
    </style>
    """, unsafe_allow_html=True)

local_css()

st.markdown("<div class='portal-header'><h1>PAS<span>track</span> Portal</h1><p>Track your Land Transfer & Tax Declaration transactions</p></div>", unsafe_allow_html=True)

with st.container():
    tracking_no = st.text_input("Enter your Tracking Number (e.g., PAS26...)", placeholder="PAS26XXXXXX")
    
    if st.button("Track Status"):
        if tracking_no:
            conn = get_db_connection()
            query = "SELECT tracking_number, owner_first_name, owner_last_name, status, municipality, transaction_type, updated_at FROM transactions WHERE tracking_number=?"
            df = pd.read_sql_query(query, conn, params=(tracking_no,))
            conn.close()
            
            if not df.empty:
                res = df.iloc[0]
                st.markdown("### Transaction Found")
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Tracking Number:** {res['tracking_number']}")
                    st.write(f"**Owner:** {res['owner_first_name']} {res['owner_last_name']}")
                    st.write(f"**Municipality:** {res['municipality']}")
                with col2:
                    st.write(f"**Type:** {res['transaction_type']}")
                    st.write(f"**Last Update:** {res['updated_at']}")
                    st.markdown(f"**Current Status:** <span class='status-badge' style='background-color: #DBEAFE; color: #1E40AF;'>{res['status']}</span>", unsafe_allow_html=True)
            else:
                st.error("No transaction found with that tracking number. Please check and try again.")
        else:
            st.warning("Please enter a tracking number.")

st.markdown("<br><br><p style='text-align: center; color: #64748B;'>Province of Cebu - Official Tracking Portal</p>", unsafe_allow_html=True)
