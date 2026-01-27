import streamlit as st

# ----------------------------------
# CONFIG
# ----------------------------------
st.set_page_config(page_title="Study Book Recommender", layout="wide")
st.title("📚 Smart Study Book & Video Recommender")


# ----------------------------------
# SUBJECTS & TOPICS
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
# SUBJECT-LEVEL BOOK BANK (KEY FIX)
# ----------------------------------

subject_books = {
    "Polity": {
        "Beginner": [
            "NCERT Class 11 – Indian Constitution at Work",
            "NCERT Class 12 – Contemporary World Politics",
            "M. Laxmikanth (Selective Reading)"
        ],
        "Intermediate": [
            "M. Laxmikanth – Indian Polity",
            "Subhash Kashyap – Constitution of India"
        ],
        "Advanced": [
            "D. D. Basu – Constitution of India",
            "Granville Austin – Indian Constitution"
        ]
    },

    "Economics": {
        "Beginner": [
            "NCERT Class 11 – Microeconomics",
            "NCERT Class 12 – Macroeconomics"
        ],
        "Intermediate": [
            "HL Ahuja – Micro & Macro Economics",
            "Paul Samuelson – Economics"
        ],
        "Advanced": [
            "Varian – Intermediate Microeconomics",
            "Dornbusch & Fischer – Macroeconomics"
        ]
    },

    "Psychology": {
        "Beginner": [
            "NCERT Class 11 – Psychology",
            "Morgan & King – Introduction to Psychology"
        ],
        "Intermediate": [
            "Baron – Psychology",
            "Ciccarelli – Psychology"
        ],
        "Advanced": [
            "DSM-5 Reference Text",
            "Goldstein – Sensation and Perception"
        ]
    },

    "Sociology": {
        "Beginner": [
            "NCERT Class 11 – Sociology",
            "NCERT Class 12 – Sociology"
        ],
        "Intermediate": [
            "Haralambos – Sociology",
            "Anthony Giddens – Sociology"
        ],
        "Advanced": [
            "Ritzer – Sociological Theory",
            "Bottomore – Sociology"
        ]
    },

    "Business Studies": {
        "Beginner": [
            "NCERT Class 11 – Business Studies",
            "NCERT Class 12 – Business Studies"
        ],
        "Intermediate": [
            "P. C. Tulsian – Business Studies",
            "Koontz – Management"
        ],
        "Advanced": [
            "Robbins – Organizational Behaviour",
            "Kotler – Marketing Management"
        ]
    }
}

# ----------------------------------
# VIDEO BANK (SUBJECT-LEVEL)
# ----------------------------------

subject_videos = {
    "Polity": [
        ("Indian Polity by Laxmikanth", "https://www.youtube.com/watch?v=4H2z2z3qZyA"),
        ("Unacademy Polity Series", "https://www.youtube.com/watch?v=YQyZKzZKJpU")
    ],
    "Economics": [
        ("Demand & Supply Basics", "https://www.youtube.com/watch?v=k2Yv6V2kYhU"),
        ("Macro Economics Explained", "https://www.youtube.com/watch?v=3ez10ADR_gM")
    ],
    "Psychology": [
        ("Human Behaviour Explained", "https://www.youtube.com/watch?v=vo4pMVb0R6M"),
        ("Learning & Motivation", "https://www.youtube.com/watch?v=9Xn6nYz8z0k")
    ],
    "Sociology": [
        ("Indian Society Explained", "https://www.youtube.com/watch?v=G8qY0WcYjK4"),
        ("Social Change & Stratification", "https://www.youtube.com/watch?v=YcN3rTj6mXk")
    ],
    "Business Studies": [
        ("Principles of Management", "https://www.youtube.com/watch?v=2C5WmC6p2Wk"),
        ("Marketing Basics", "https://www.youtube.com/watch?v=KX8N3Yp0F9I")
    ]
}

# ----------------------------------
# UI
# ----------------------------------

subject = st.selectbox("📘 Select Subject", list(subjects.keys()))
topic = st.selectbox("📌 Select Topic", subjects[subject])
level = st.radio("🎯 Select Level", ["Beginner", "Intermediate", "Advanced"])

# ----------------------------------
# OUTPUT
# ----------------------------------

if st.button("📖 Recommend Study Resources"):
    st.subheader("📚 Recommended Books")

    books = subject_books[subject][level]

    for b in books:
        st.write(f"• {b}")

    st.subheader("🎥 Recommended Videos")

    cols = st.columns(2)
    for i, (title, link) in enumerate(subject_videos[subject]):
        with cols[i % 2]:
            st.markdown(f"▶ **[{title}]({link})**")
