import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="NCERT Learning Recommender", layout="wide")

st.title("📘 NCERT Learning Resource Recommender")
st.write("Personalized recommendations for Class 11–12 students")

# -----------------------------
# Dataset
# -----------------------------
resources = pd.DataFrame({
    "resource_id": [1,2,3,4,5,6,7,8,9,10],
    "subject": [
        "Sociology","Sociology",
        "Polity","Polity",
        "Psychology","Psychology",
        "Economics","Economics",
        "Business Studies","Business Studies"
    ],
    "chapter": [
        "Social Institutions",
        "Culture and Socialization",
        "Indian Constitution",
        "Fundamental Rights",
        "Human Behaviour",
        "Learning and Motivation",
        "Demand and Supply",
        "National Income",
        "Principles of Management",
        "Marketing Management"
    ],
    "class": [11,11,11,12,11,12,11,12,11,12],
    "difficulty": [
        "Beginner","Intermediate",
        "Beginner","Intermediate",
        "Beginner","Intermediate",
        "Beginner","Intermediate",
        "Beginner","Intermediate"
    ],
    "content": [
        "family kinship social norms institutions",
        "culture values socialization identity",
        "constitution democracy republic justice",
        "rights equality freedom remedies",
        "behaviour cognition emotions personality",
        "learning theories motivation reinforcement",
        "demand supply market equilibrium",
        "national income gdp gnp accounting",
        "management planning organizing controlling",
        "marketing mix product price promotion"
    ]
})

student_data = pd.DataFrame({
    "student_id": [2001, 2001, 2001],
    "resource_id": [1, 3, 7],
    "rating": [5, 4, 5],
    "progress_percent": [85, 70, 60]
})

# -----------------------------
# NLP Vectorization
# -----------------------------
vectorizer = TfidfVectorizer(stop_words="english")
tfidf_matrix = vectorizer.fit_transform(resources["content"])

# -----------------------------
# Functions
# -----------------------------
def build_student_profile(student_id):
    history = student_data[student_data["student_id"] == student_id]
    
    if history.empty:
        # No history → return zero vector
        return np.zeros((1, tfidf_matrix.shape[1]))
    
    # Get valid indices
    indices = history["resource_id"].values - 1
    valid_indices = [i for i in indices if 0 <= i < tfidf_matrix.shape[0]]
    
    if not valid_indices:
        return np.zeros((1, tfidf_matrix.shape[1]))
    
    # Select rows from sparse matrix
    selected_matrix = tfidf_matrix[valid_indices]
    
    # If selected_matrix has no rows, return zeros
    if selected_matrix.shape[0] == 0:
        return np.zeros((1, tfidf_matrix.shape[1]))
    
    # Compute mean safely
    student_vector = selected_matrix.mean(axis=0)
    
    # Convert sparse matrix to dense numpy array
    student_vector = np.asarray(student_vector).reshape(1, -1)
    
    return student_vector
r



def recommend_resources(student_id, top_n=5):
    student_vector = build_student_profile(student_id)
    similarity = cosine_similarity(student_vector, tfidf_matrix).flatten()

    recs = resources.copy()
    recs["similarity_score"] = similarity

    studied = student_data[student_data["student_id"] == student_id]["resource_id"]
    recs = recs[~recs["resource_id"].isin(studied)]

    return recs.sort_values("similarity_score", ascending=False).head(top_n)

def adaptive_recommendation(student_id):
    avg_progress = student_data[student_data["student_id"] == student_id]["progress_percent"].mean()

    if avg_progress >= 80:
        level = "Intermediate"
    else:
        level = "Beginner"

    recs = recommend_resources(student_id)
    return recs[recs["difficulty"] == level]

# -----------------------------
# Streamlit UI
# -----------------------------
st.sidebar.header("🎓 Student Settings")

student_id = st.sidebar.number_input("Student ID", value=2001)
show_data = st.sidebar.checkbox("Show Student History")

if show_data:
    st.subheader("📈 Student Learning History")
    st.dataframe(student_data)

st.subheader("📚 Recommended Chapters")

if st.button("Generate Recommendations"):
    final_recs = adaptive_recommendation(student_id)

    if final_recs.empty:
        st.warning("No recommendations found. Try adjusting progress or data.")
    else:
        st.dataframe(
            final_recs[[
                "subject",
                "chapter",
                "class",
                "difficulty",
                "similarity_score"
            ]].reset_index(drop=True)
        )

st.markdown("---")
st.caption("Built using Python, NLP (TF-IDF), and Recommendation Systems")
