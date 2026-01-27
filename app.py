
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# -----------------------------
# Streamlit page setup
# -----------------------------
st.set_page_config(page_title="NCERT Learning Recommender", layout="wide")
st.title("📘 NCERT Learning Resource Recommender")
st.write("Personalized chapter recommendations for Class 11–12 students")

# -----------------------------
# Dataset: Chapters/Resources
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

# -----------------------------
# Dataset: Student Learning History
# -----------------------------
student_data = pd.DataFrame({
    "student_id": [2001, 2001, 2001, 2002, 2002],
    "resource_id": [1, 3, 7, 2, 4],
    "rating": [5, 4, 5, 3, 4],
    "progress_percent": [85, 70, 60, 50, 65]
})

# -----------------------------
# NLP: Convert chapter content into vectors
# -----------------------------
vectorizer = TfidfVectorizer(stop_words="english")
tfidf_matrix = vectorizer.fit_transform(resources["content"])

# -----------------------------
# Function: Build Student Profile
# -----------------------------
def build_student_profile(student_id):
    """
    Create a vector representation of a student based on chapters they studied.
    If no history, return a zero vector.
    """
    history = student_data[student_data["student_id"] == student_id]
    
    if history.empty:
        # New student → return zero vector
        return np.zeros((1, tfidf_matrix.shape[1]))
    
    # Get the indices of resources studied (adjust for 0-based indexing)
    indices = history["resource_id"].values - 1
    valid_indices = [i for i in indices if 0 <= i < tfidf_matrix.shape[0]]
    
    if not valid_indices:
        return np.zeros((1, tfidf_matrix.shape[1]))
    
    # Select corresponding rows from TF-IDF matrix
    selected_matrix = tfidf_matrix[valid_indices]
    
    # Compute mean vector
    student_vector = selected_matrix.mean(axis=0)
    student_vector = np.asarray(student_vector).reshape(1, -1)
    
    return student_vector

# -----------------------------
# Function: Recommend Chapters
# -----------------------------
def recommend_resources(student_id, top_n=5):
    """
    Recommend chapters most similar to the student's profile.
    Excludes chapters already studied.
    """
    student_vector = build_student_profile(student_id)
    similarity = cosine_similarity(student_vector, tfidf_matrix).flatten()

    recs = resources.copy()
    recs["similarity_score"] = similarity

    studied = student_data[student_data["student_id"] == student_id]["resource_id"]
    recs = recs[~recs["resource_id"].isin(studied)]

    return recs.sort_values("similarity_score", ascending=False).head(top_n)

# -----------------------------
# Function: Adaptive Recommendation
# -----------------------------
def adaptive_recommendation(student_id):
    """
    Filter recommendations based on student progress:
    - avg_progress >= 80 → Intermediate
    - otherwise → Beginner
    """
    history = student_data[student_data["student_id"] == student_id]
    avg_progress = history["progress_percent"].mean() if not history.empty else 0

    level = "Intermediate" if avg_progress >= 80 else "Beginner"

    recs = recommend_resources(student_id)
    
    # Filter by difficulty level
    filtered_recs = recs[recs["difficulty"] == level]
    if filtered_recs.empty:
        return recs  # fallback if no chapters match difficulty
    return filtered_recs

# -----------------------------
# Streamlit UI
# -----------------------------
st.sidebar.header("🎓 Student Settings")
student_id = st.sidebar.number_input("Student ID", value=2001)
show_data = st.sidebar.checkbox("Show Student History")

# Show student history filtered by ID
st.subheader("📈 Student Learning History")
filtered_history = student_data[student_data["student_id"] == student_id]
if filtered_history.empty:
    st.warning(f"No learning history found for Student ID {student_id}.")
else:
    st.dataframe(filtered_history)

# Show recommendations
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
