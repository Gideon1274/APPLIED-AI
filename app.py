import streamlit as st
import sqlite3
import pandas as pd
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
st.set_page_config(page_title="MindMapper AI", page_icon="🧠", layout="wide")

def apply_messenger_design():
    st.markdown("""
    <style>
        .main { background-color: #0E1117; }
        section[data-testid="stSidebar"] { 
            background-color: #161B22 !important; 
            border-right: 1px solid #30363D; 
        }
        
        [data-testid="stChatMessage"] {
            background-color: transparent !important;
            padding: 0 !important;
            margin-bottom: 20px !important;
        }

        /* User Message (Right Side) */
        [data-testid="stChatMessage"]:has(div[aria-label="chat user"]) {
            display: flex;
            flex-direction: row-reverse;
            text-align: right;
        }
        [data-testid="stChatMessage"]:has(div[aria-label="chat user"]) .stChatMessageContent {
            background-color: #0084FF !important;
            color: white !important;
            border-radius: 18px 18px 2px 18px !important;
            padding: 12px 16px !important;
            margin-left: 25% !important;
            width: fit-content !important;
        }

        /* AI Message (Left Side) */
        [data-testid="stChatMessage"]:has(div[aria-label="chat assistant"]) .stChatMessageContent {
            background-color: #3E4042 !important;
            color: #E4E6EB !important;
            border-radius: 18px 18px 18px 2px !important;
            padding: 12px 16px !important;
            margin-right: 25% !important;
            width: fit-content !important;
        }

        .breathing-box {
            background: rgba(0, 255, 195, 0.05);
            border: 1px solid #00FFC3;
            border-radius: 12px;
            padding: 15px;
            text-align: center;
            margin-bottom: 25px;
        }

        .stButton>button {
            background-color: #00FFC3;
            color: #0E1117;
            font-weight: bold;
            border-radius: 20px;
            border: none;
        }

        h1, h2, h3 { color: #00FFC3 !important; }
    </style>
    """, unsafe_allow_html=True)

def init_db():
    conn = sqlite3.connect('mindmapper.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS sessions 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                  mood INTEGER, 
                  emotion TEXT, 
                  summary TEXT)''')
    conn.commit()
    conn.close()

def save_session_to_db(mood, emotion, summary):
    conn = sqlite3.connect('mindmapper.db')
    c = conn.cursor()
    c.execute("INSERT INTO sessions (mood, emotion, summary) VALUES (?, ?, ?)", 
              (mood, emotion, summary))
    conn.commit()
    conn.close()

def get_history():
    try:
        conn = sqlite3.connect('mindmapper.db')
        df = pd.read_sql_query("SELECT timestamp, mood, emotion, summary FROM sessions ORDER BY id DESC LIMIT 3", conn)
        conn.close()
        return df
    except:
        return pd.DataFrame()

apply_messenger_design()
init_db()

# Security Handlers
if "GROQ_API_KEY" in st.secrets:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
else:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("API Key missing.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

with st.sidebar:
    st.title("MindMapper Settings")
    mood_score = st.slider("Mood Intensity", 1, 10, 5)
    emotion = st.selectbox("Primary Feeling", ["Overwhelmed", "Anxious", "Stressed", "Sad", "Calm", "Hopeful"])
    
    if st.button("New Chat Session"):
        st.session_state.messages = []
        initial_msg = f"I've noted you're feeling {emotion.lower()} ({mood_score}/10). I'm here. What's on your mind?"
        st.session_state.messages.append({"role": "assistant", "content": initial_msg})

    st.divider()
    st.subheader("Previous Logs")
    history = get_history()
    if not history.empty:
        st.dataframe(history, use_container_width=True)

st.title("MindMapper AI")

if mood_score >= 7:
    st.markdown("""
    <div class="breathing-box">
        <p style="margin:0; color:#00FFC3;">🧘 Intense energy detected. Breathe with me: 4s In ... 7s Hold ... 8s Out.</p>
    </div>
    """, unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Type your message..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are MindMapper, a warm AI journaling companion. Use CBT Socratic questioning. Reflect feelings first. Keep it conversational and under 120 words."},
                *st.session_state.messages
            ],
            model="llama-3.3-70b-versatile",
        )
        response_text = chat_completion.choices[0].message.content
        with st.chat_message("assistant"):
            st.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})
    except:
        st.error("Connection lost.")

st.divider()
if st.button("Close & Save Session"):
    if st.session_state.get("messages"):
        try:
            summary_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "Summarize session themes and provide one affirmation."},
                    *st.session_state.messages
                ],
                model="llama-3.3-70b-versatile",
            )
            summary_text = summary_completion.choices[0].message.content
            st.info(summary_text)
            save_session_to_db(mood_score, emotion, summary_text)
            st.success("Log saved.")
        except:
            save_session_to_db(mood_score, emotion, "No summary.")