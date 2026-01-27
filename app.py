
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# -----------------------------
# Streamlit page setup
# -----------------------------
st.set_page_config(page_title="NCERT Learning Assistant", layout="wide")
st.title("📘 NCERT Learning Assistant")
st.write("Get personalized chapter, book, and video recommendations for Class 11–12 students")

# -----------------------------
# Subjects, 50 Topics each
# -----------------------------
subjects = ["Sociology", "Polity", "Psychology", "Economics", "Business Studies"]
subjects_topics = {subject: [f"{subject} Topic {i+1}" for i in range(50)] for subject in subjects}

# -----------------------------
# Chapters / Resource content
# -----------------------------
resources_list = []

resource_id = 1
for subject in subjects:
    for i in range(50):
        resources_list.append({
            "resource_id": resource_id,
            "subject": subject,
            "chapter": f"{subject} Topic {i+1}",
            "class": 11 if i % 2 == 0 else 12,
            "difficulty": "Beginner" if i % 3 == 0 else "Intermediate",
            "content": f"{subject} content about topic {i+1}"
        })
        resource_id += 1

resources = pd.DataFrame(resources_list)

# -----------------------------
# Student Learning History
# -----------------------------
student_data = pd.DataFrame({
    "student_id": [2001, 2001, 2002, 2002],
    "resource_id": [1, 55, 2, 60],
    "rating": [5, 4, 3, 4],
    "progress_percent": [85, 70, 50, 60]
})

# -----------------------------
# TF-IDF Vectorization
# -----------------------------
vectorizer = TfidfVectorizer(stop_words="english")
tfidf_matrix = vectorizer.fit_transform(resources["content"])

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
        "Beginner": ["NCERT Psychology Class 11", "Psychology Basics Intro"],
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
# Videos dictionary
# -----------------------------
videos = {
    subject: {
        level: [f"https://www.youtube.com/watch?v={subject}_{level}_{i+1}" for i in range(3)]
        for level in ["Beginner", "Intermediate", "Advanced"]
    }
    for subject in subjects
}

# -----------------------------
# Student Profile & Chapter Recommendation
# -----------------------------
def build_student_profile(student_id):
    history = student_data[student_data["student_id"] == student_id]
    if history.empty:
        return None
    indices = history["resource_id"].values - 1
    valid_indices = [i for i in indices if 0 <= i < tfidf_matrix.shape[0]]
    if not valid_indices:
        return None
    selected_matrix = tfidf_matrix[valid_indices]
    student_vector = selected_matrix.mean(axis=0)
    student_vector = np.asarray(student_vector).reshape(1, -1)
    return student_vector

def recommend_chapters(student_id, top_n=10):
    student_vector = build_student_profile(student_id)
    if student_vector is None:
        # New student: recommend random beginner chapters
        recs = resources[resources["difficulty"]=="Beginner"].sample(top_n)
        recs["similarity_score"] = np.nan
        return recs
    similarity = cosine_similarity(student_vector, tfidf_matrix).flatten()
    recs = resources.copy()
    recs["similarity_score"] = similarity
    studied = student_data[student_data["student_id"]==student_id]["resource_id"]
    recs = recs[~recs["resource_id"].isin(studied)]
    return recs.sort_values("similarity_score", ascending=False).head(top_n)

# -----------------------------
# Book & Video Recommendation
# -----------------------------
def recommend_materials(subject, level, topics):
    if not topics:
        return pd.DataFrame({"Message":["Please select at least one topic"]})
    recommended_books = books.get(subject, {}).get(level, [])
    recommended_videos = videos.get(subject, {}).get(level, [])
    data = {
        "Topics": [", ".join(topics)],
        "Recommended Books": [", ".join(recommended_books)],
        "Recommended Videos": [", ".join(recommended_videos)]
    }
    return pd.DataFrame(data)

# -----------------------------
# Streamlit Sidebar
# -----------------------------
st.sidebar.header("🎓 Student Settings")
student_id = st.sidebar.number_input("Student ID", value=2001)
show_history = st.sidebar.checkbox("Show Learning History")

selected_subject = st.sidebar.selectbox("Select Subject", subjects)
selected_level = st.sidebar.selectbox("Select Level", ["Beginner", "Intermediate", "Advanced"])
selected_topics = st.sidebar.multiselect(
    "Select Topic(s)", subjects_topics[selected_subject]
)

# -----------------------------
# Show Student History
# -----------------------------
st.subheader("📈 Student Learning History")
filtered_history = student_data[student_data["student_id"]==student_id]
if show_history:
    if filtered_history.empty:
        st.warning(f"No learning history for Student ID {student_id}")
    else:
        st.dataframe(filtered_history)

# -----------------------------
# Show Chapter Recommendations
# -----------------------------
st.subheader("📚 Recommended Chapters")
if st.button("Generate Chapter Recommendations"):
    chapters = recommend_chapters(student_id)
    st.dataframe(chapters[["subject","chapter","class","difficulty","similarity_score"]].reset_index(drop=True))

# -----------------------------
# Show Book & Video Recommendations
# -----------------------------
st.subheader("📖 Book & Video Recommendations")
if st.button("Get Books & Videos"):
    materials = recommend_materials(selected_subject, selected_level, selected_topics)
    st.dataframe(materials)

st.markdown("---")
st.caption("NCERT Learning Assistant: Chapters, Books, and Videos Recommendations")
