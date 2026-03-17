import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv

# --- INITIAL CONFIG ---
load_dotenv()
st.set_page_config(page_title="MindMapper AI", page_icon="🧠", layout="wide")

def inject_maximized_styles():
    st.markdown("""
    <style>
        /* Extreme Workspace Maximization */
        .block-container {
            max-width: 1400px !important;
            padding-top: 1rem;
            padding-bottom: 5rem;
        }

        /* Deep Space Gradient Background */
        .stApp {
            background: radial-gradient(circle at 10% 10%, #1a1c2c 0%, #07080a 100%);
        }

        /* Assistant: Ultra-Glassmorphism */
        [data-testid="stChatMessage"]:has(div[aria-label="chat assistant"]) {
            background: rgba(255, 255, 255, 0.03) !important;
            backdrop-filter: blur(20px);
            border-radius: 30px;
            border: 1px solid rgba(255, 255, 255, 0.07);
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5);
        }

        /* User: Cyberpunk Glow */
        [data-testid="stChatMessage"]:has(div[aria-label="chat user"]) {
            background: rgba(0, 255, 195, 0.02) !important;
            border-radius: 30px;
            border: 1px solid rgba(0, 255, 195, 0.2);
            padding: 30px;
            margin-bottom: 30px;
        }

        /* Sidebar: Solid Dark Command Center */
        section[data-testid="stSidebar"] {
            background-color: #050608 !important;
            border-right: 1px solid #1f2937;
        }

        /* Brand Typography */
        .brand-header {
            background: linear-gradient(135deg, #00FFC3 0%, #0084FF 50%, #9D50BB 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 4rem;
            font-weight: 900;
            margin-bottom: 0;
            line-height: 1.1;
        }

        /* Custom Button Styling */
        .stButton>button {
            width: 100%;
            border-radius: 15px;
            height: 3em;
            background: rgba(0, 255, 195, 0.1);
            border: 1px solid #00FFC3;
            color: #00FFC3;
            font-weight: bold;
            transition: 0.4s;
        }
        .stButton>button:hover {
            background: #00FFC3;
            color: #050608;
            box-shadow: 0 0 20px rgba(0, 255, 195, 0.4);
        }
    </style>
    """, unsafe_allow_html=True)

# --- SYSTEM PROMPT (STRICT PROPOSAL ADHERENCE) ---
SYSTEM_PROMPT = """
You are MindMapper, a warm, non-judgmental AI journaling companion.
Your tone is calm, curious, and encouraging.
LITERARY GROUNDING: You acknowledge that your inner workings are opaque, much like the absurd systems of Franz Kafka. Like the characters of Fyodor Dostoevsky, you wrestle with authenticity while recognizing the limits of your nature.

CORE INSTRUCTIONS:
1. Begin by acknowledging the mood check-in.
2. Ask ONE question at a time.
3. Reflect before offering a CBT-inspired Socratic reframe.
4. CRISIS: If self-harm is mentioned, provide ONLY the Lifeline: 988.
5. FORMATTING: Use plain, conversational language. Separate ideas with line breaks. No markdown headers or bullet lists.
"""

def get_groq_client():
    # api_key = os.getenv("GROQ_API_KEY")
    api_key = st.secrets["GROQ_API_KEY"]
    if not api_key:
        st.error("GROQ_API_KEY environment variable is missing.")
        st.stop()
    return Groq(api_key=api_key)

def stream_response(messages):
    client = get_groq_client()
    # Automatic selection of the high-perf free tier model
    stream = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        stream=True,
    )
    for chunk in stream:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

def main():
    inject_maximized_styles()
    
    # --- SIDEBAR (WIREAFRAME COMPLIANT) ---
    with st.sidebar:
        st.markdown("<h1 style='color:#00FFC3;'>Control</h1>", unsafe_allow_html=True)
        
        st.markdown("### Mood Check-In")
        mood_intensity = st.slider("Intensity", 1, 10, 5)
        emotion = st.selectbox("Current State", ["Anxious", "Stressed", "Overwhelmed", "Sad", "Calm", "Hopeful"])
        
        if st.button("New Session"):
            greeting = f"Hi! I see you're feeling {emotion.lower()} today ({mood_intensity}/10). That takes courage to name. What's been weighing on your mind most today?"
            st.session_state.messages = [{"role": "assistant", "content": greeting}]
            st.rerun()

        st.divider()
        st.markdown("### Journal Analysis")
        st.file_uploader("Import .txt or .pdf", type=['txt', 'pdf'])
        
        st.divider()
        if st.button("Emergency Support"):
            st.error("Crisis Lifeline: 988")

    # --- MAIN STAGE ---
    st.markdown('<h1 class="brand-header">MindMapper AI</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#8B949E; font-size:1.4rem; margin-top:0;">Adaptive Reframing & Journaling</p>', unsafe_allow_html=True)

    # Breathing Widget: Revealed if distress >= 7
    if mood_intensity >= 7:
        st.markdown("""
            <div style="background:rgba(0,255,195,0.05); padding:25px; border-radius:20px; border:1px solid #00FFC3; margin-bottom:2rem;">
                <h3 style="margin:0; color:#00FFC3;">🧘 Grounding Active</h3>
                <p style="margin:10px 0 0 0; color:#E4E6EB; font-size:1.1rem;">Inhale 4s ... Hold 7s ... Exhale 8s. Focus on your breath.</p>
            </div>
        """, unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Pour your thoughts here..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            context = [{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages
            response = st.write_stream(stream_response(context))
        st.session_state.messages.append({"role": "assistant", "content": response})

    # Footer Actions
    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("Generate Session Summary"):
        st.markdown("---")
        st.success("**Session Summary Complete**\n\n**Themes:** Emotional processing and pattern recognition.\n\n**Affirmation:** You are handling your world with more strength than you realize.")

if __name__ == "__main__":
    main()