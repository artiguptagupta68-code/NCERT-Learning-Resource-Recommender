import streamlit as st

# ----------------------------------
# CONFIG
# ----------------------------------
st.set_page_config(page_title="Study Book Recommender", layout="wide")
st.title("📚 Smart Study Book Recommender")

st.write("Choose a subject, topic, and your level to get the **best books** to study.")

# ----------------------------------
# DATA
# ----------------------------------

subjects = {
    "Sociology": [
        "Social Institutions", "Culture and Society", "Social Stratification",
        "Family and Kinship", "Religion", "Education", "Caste System",
        "Social Change", "Globalization", "Gender and Society"
    ],
    "Psychology": [
        "Human Behaviour", "Learning", "Motivation", "Emotion",
        "Personality", "Intelligence", "Memory", "Thinking",
        "Stress and Coping", "Mental Health"
    ],
    "Economics": [
        "Demand and Supply", "Elasticity", "Production",
        "Cost and Revenue", "Market Structures", "National Income",
        "Inflation", "Money and Banking", "Fiscal Policy", "Economic Growth"
    ],
    "Polity": [
        "Indian Constitution", "Fundamental Rights", "DPSP",
        "Parliament", "Judiciary", "Federalism", "President",
        "Prime Minister", "Election System", "Local Government"
    ],
    "Business Studies": [
        "Nature of Business", "Forms of Business", "Management",
        "Planning", "Organizing", "Staffing", "Directing",
        "Controlling", "Marketing", "Financial Management"
    ]
}

# ----------------------------------
# BOOK RECOMMENDATIONS
# ----------------------------------

book_recommendations = {
    "Indian Constitution": {
        "Beginner": [
            "NCERT Class 11 – Indian Constitution at Work",
            "M. Laxmikanth (Basic Reading)"
        ],
        "Intermediate": [
            "M. Laxmikanth – Indian Polity",
            "Subhash Kashyap – Constitution of India"
        ],
        "Advanced": [
            "D. D. Basu – Introduction to the Constitution of India",
            "Granville Austin – Indian Constitution"
        ]
    },

    "Demand and Supply": {
        "Beginner": [
            "NCERT Class 11 – Microeconomics",
            "S. Chand – Basic Economics"
        ],
        "Intermediate": [
            "HL Ahuja – Microeconomics",
            "Paul Samuelson – Economics"
        ],
        "Advanced": [
            "Varian – Intermediate Microeconomics",
            "Nicholson – Microeconomic Theory"
        ]
    },

    "Human Behaviour": {
        "Beginner": [
            "NCERT Class 11 – Psychology",
            "Morgan & King – Introduction to Psychology"
        ],
        "Intermediate": [
            "Baron – Psychology",
            "Ciccarelli – Psychology"
        ],
        "Advanced": [
            "Goldstein – Sensation and Perception",
            "DSM-5 Reference Text"
        ]
    }
}

# ----------------------------------
# VIDEO LINKS
# ----------------------------------

video_links = {
    "Indian Constitution": [
        {
            "title": "Indian Constitution Explained",
            "thumbnail": "https://img.youtube.com/vi/4H2z2z3qZyA/0.jpg",
            "url": "https://www.youtube.com/watch?v=4H2z2z3qZyA"
        }
    ],
    "Demand and Supply": [
        {
            "title": "Demand & Supply Basics",
            "thumbnail": "https://img.youtube.com/vi/k2Yv6V2kYhU/0.jpg",
            "url": "https://www.youtube.com/watch?v=k2Yv6V2kYhU"
        }
    ]
}

# ----------------------------------
# UI
# ----------------------------------

subject = st.selectbox("📘 Select Subject", list(subjects.keys()))

topic = st.selectbox(
    "📌 Select Topic",
    subjects[subject]
)

level = st.radio(
    "🎯 Select Your Level",
    ["Beginner", "Intermediate", "Advanced"]
)

# ----------------------------------
# OUTPUT
# ----------------------------------

if st.button("📖 Recommend Books"):
    st.subheader("📚 Recommended Books")

    books = book_recommendations.get(topic, {}).get(level, [])

    if not books:
        st.warning("No books available yet for this topic and level.")
    else:
        for b in books:
            st.write(f"• {b}")

    st.subheader("🎥 Recommended Videos")

    videos = video_links.get(topic, [])

    if not videos:
        st.info("No videos available for this topic yet.")
    else:
        cols = st.columns(len(videos))
        for col, v in zip(cols, videos):
            with col:
                st.image(v["thumbnail"])
                st.markdown(f"[▶ {v['title']}]({v['url']})")
