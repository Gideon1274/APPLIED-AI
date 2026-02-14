import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="My Portfolio", page_icon="🚀", layout="wide")

with st.sidebar:
    st.image("https://via.placeholder.com/150")
    st.title("Contact Me")
    st.write("📧 email@example.com")
    st.write("🔗 [LinkedIn](https://linkedin.com)")
    st.write("💻 [GitHub](https://github.com)")
    
    status = st.radio("Current Status", ["Available for Hire", "Busy", "Open to Collab"])
    if status == "Available for Hire":
        st.success("I'm ready to work!")

tab1, tab2, tab3 = st.tabs(["📖 Autobiography", "🛠️ Portfolio", "📩 Connect"])

with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("Who Am I?")
        st.markdown("""
        I am a passionate **Full-Stack Developer** and **Data Enthusiast** based in the digital world. 
        I believe in building tools that make people's lives easier and more efficient.
        """)
        
        st.subheader("The Journey")
        st.info("Started coding in 2018. Transitioned from manual spreadsheets to automated Python scripts.")
        
    with col2:
        st.subheader("Core Skills")
        skills = ["Python", "Streamlit", "SQL", "React", "AWS"]
        for skill in skills:
            st.button(skill, disabled=True)

with tab2:
    st.header("Projects & Experience")
    
    with st.expander("📊 Data Analytics Dashboard"):
        st.write("A real-time dashboard tracking global stock market trends.")
        chart_data = pd.DataFrame({"Trends": [10, 25, 15, 40, 35]})
        st.line_chart(chart_data)
        
    with st.expander("🤖 AI Image Generator"):
        st.write("An interface for generating art using generative models.")
        st.progress(85, text="Project Completion")

    st.divider()
    
    st.subheader("Technical Proficiency")
    skill_data = pd.DataFrame({
        "Skill": ["Backend", "Frontend", "Cloud", "UI/UX"],
        "Level": [90, 75, 60, 80]
    })
    st.bar_chart(skill_data, x="Skill", y="Level")

with tab3:
    st.header("Get In Touch")
    
    with st.form("contact_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        msg = st.text_area("Message")
        rating = st.select_slider("Rate my portfolio", options=["Beginner", "Decent", "Pro", "Mind-blown"])
        submit = st.form_submit_button("Send Message")
        
        if submit:
            st.balloons()
            st.write(f"Thanks for reaching out, {name}!")

st.divider()
st.caption(f"Built with ❤️ using Streamlit | {date.today().year}")