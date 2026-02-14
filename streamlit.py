import streamlit as st
from datetime import datetime
import pandas as pd
import numpy as np

st.set_page_config(page_title="Autobiography & Portfolio", page_icon="🚀", layout="wide")

st.title("Rainric Randy Yu")
st.subheader("BSIT Graduate | Aspiring Developer | JLPT Learner")

menu = st.sidebar.radio(
    "Navigation",
    ["Home", "About Me", "Skills", "Projects", "Experience", "Contact"]
)

if menu == "Home":
    st.header("Welcome")
    st.write("This is my personal Streamlit autobiography and portfolio application.")
    st.image("https://via.placeholder.com/800x300.png?text=Portfolio+Banner")
    st.success("Currently open for opportunities.")
    st.info(f"Last updated: {datetime.now().strftime('%B %d, %Y')}")

elif menu == "About Me":
    st.header("About Me")
    col1, col2 = st.columns(2)
    with col1:
        st.write("I am a BSIT graduate passionate about software development and Japanese language learning.")
        st.write("I enjoy building web applications, solving problems, and improving my technical skills.")
        st.metric("Height (cm)", 160)
        st.metric("Weight (kg)", 65)
    with col2:
        st.write("Interests")
        st.checkbox("Web Development", value=True)
        st.checkbox("Machine Learning")
        st.checkbox("Calisthenics")
        st.checkbox("Japanese Language")
        st.progress(75)

elif menu == "Skills":
    st.header("Technical Skills")
    skills = {
        "Python": 85,
        "Java": 70,
        "SQL": 75,
        "HTML/CSS": 80,
        "JavaScript": 65
    }
    for skill, level in skills.items():
        st.write(skill)
        st.progress(level)

    st.subheader("Skill Distribution")
    df = pd.DataFrame({
        "Skill": list(skills.keys()),
        "Level": list(skills.values())
    })
    st.bar_chart(df.set_index("Skill"))

elif menu == "Projects":
    st.header("Projects")
    project = st.selectbox(
        "Select a Project",
        ["Portfolio Website", "Student Management System", "Data Analysis App"]
    )

    if project == "Portfolio Website":
        st.write("A responsive personal website built using HTML, CSS, and JavaScript.")
        st.button("View Code")

    elif project == "Student Management System":
        st.write("A CRUD-based system developed using Python and MySQL.")
        st.button("View Code")

    elif project == "Data Analysis App":
        st.write("A data visualization tool built using Streamlit and Pandas.")
        st.button("View Code")

    st.subheader("Project Rating")
    rating = st.slider("Rate this portfolio", 1, 10, 8)
    st.write("Rating:", rating)

elif menu == "Experience":
    st.header("Experience")
    data = {
        "Year": ["2022", "2023", "2024"],
        "Role": ["Intern Developer", "Freelance Developer", "IT Support"],
        "Company": ["ABC Tech", "Self-Employed", "XYZ Solutions"]
    }
    df_exp = pd.DataFrame(data)
    st.table(df_exp)
    st.area_chart(pd.DataFrame(np.random.randn(20, 3), columns=["Python", "Java", "SQL"]))

elif menu == "Contact":
    st.header("Contact Me")
    with st.form("contact_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        message = st.text_area("Message")
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.success("Message submitted successfully!")

    st.write("Social Links")
    st.markdown("[GitHub](https://github.com)")
    st.markdown("[LinkedIn](https://linkedin.com)")

st.sidebar.markdown("---")
st.sidebar.write("© 2030 Rainric Randy Yu")
