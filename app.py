%%writefile app.py
import streamlit as st
import pandas as pd

st.set_page_config(page_title="NCERT Book Recommender", layout="wide")
st.title("📚 NCERT Book Recommender")
st.write("Select your subject, level, and topics to get book recommendations")

# -----------------------------
# Subjects and Topics
# -----------------------------
subjects_topics = {
    "Sociology": ["Social Institutions", "Culture and Socialization"],
    "Polity": ["Indian Constitution", "Fundamental Rights"],
    "Psychology": ["Human Behaviour", "Learning and Motivation"],
    "Economics": ["Demand and Supply", "National Income"],
    "Business Studies": ["Principles of Management", "Marketing Management"]
}

# -----------------------------
# Books dictionary
# -----------------------------
books = {
    "Sociology": {
        "Beginner": ["NCERT Sociology Class 11", "Understanding Society by Haralambos (Intro)"],
        "Intermediate": ["Introduction to Sociology by Bottomore", "Sociology: Themes and Perspectives by Haralambos"],
        "Advanced": ["Advanced Sociology by Giddens", "Sociology: Concepts and Theories by Macionis"]
    },
    "Polity": {
        "Beginner": ["NCERT Political Science Class 11", "Indian Constitution Made Easy"],
        "Intermediate": ["Indian Polity by M. Laxmikanth", "Governance in India by D.D. Basu"],
        "Advanced": ["Introduction to the Constitution of India by D.D. Basu", "Indian Constitutional Law Advanced"]
    },
    "Psychology": {
        "Beginner": ["NCERT Psychology Class 11", "Psychology Basics by Ciccarelli Intro"],
        "Intermediate": ["Psychology: An Exploration by Saundra K. Ciccarelli", "Understanding Psychology by Feldman"],
        "Advanced": ["Advanced Psychology by Baron & Misra", "Handbook of Psychology by Weiner"]
    },
    "Economics": {
        "Beginner": ["NCERT Economics Class 11", "Principles of Economics Intro by Mankiw"],
        "Intermediate": ["Principles of Economics by N. Gregory Mankiw", "Economic Theory by Samuelson"],
        "Advanced": ["Advanced Economic Theory by H.L. Ahuja", "Micro and Macro Economics Advanced"]
    },
    "Business Studies": {
        "Beginner": ["NCERT Business Studies Class 11", "Introduction to Management Basics"],
        "Intermediate": ["Business Studies by Poonam Gandhi", "Business Management Concepts"],
        "Advanced": ["Advanced Business Management by Robbins", "Strategic Management Advanced"]
    }
}

# -----------------------------
# Streamlit sidebar: select options
# -----------------------------
st.sidebar.header("🎓 Student Selection")
selected_subject = st.sidebar.selectbox("Select Subject", list(subjects_topics.keys()))
selected_level = st.sidebar.selectbox("Select Level", ["Beginner", "Intermediate", "Advanced"])
selected_topics = st.sidebar.multiselect(
    "Select Topic(s) you are interested in", subjects_topics[selected_subject]
)

# -----------------------------
# Recommend books
# -----------------------------
def recommend_books(subject, level, topics):
    """
    Recommend books based on subject and level.
    """
    if not topics:
        return pd.DataFrame({"Message": ["Please select at least one topic"]})
    
    recommended = books.get(subject, {}).get(level, [])
    # Show topics as info
    data = {"Topics": [", ".join(topics)], "Recommended Books": [", ".join(recommended)]}
    return pd.DataFrame(data)

# -----------------------------
# Show recommendation button
# -----------------------------
if st.button("Get Book Recommendations"):
    recommendations = recommend_books(selected_subject, selected_level, selected_topics)
    st.subheader("📖 Recommended Books")
    st.dataframe(recommendations)

st.markdown("---")
st.caption("Book recommendations based on subject, level, and topics")
