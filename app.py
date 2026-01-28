import streamlit as st

# -------------------------------------------------
# CONFIG
# -------------------------------------------------
st.set_page_config(page_title="Smart Study Book Recommender", layout="wide")
st.title("📚 Smart Study Book & Video Recommender")

st.write(
    "Select a **subject**, **topic**, and **your level**.\n\n"
    "You will get a **strong stack of books** suitable for your understanding level."
)

# -------------------------------------------------
# SUBJECTS & TOPICS (Expandable to 50+)
# -------------------------------------------------

subjects = {
    "Polity": [
        "Indian Constitution", "Fundamental Rights", "DPSP",
        "Parliament", "Judiciary", "Federalism",
        "President", "Prime Minister", "Election System", "Local Government"
    ],
    "Economics": [
        "Demand and Supply", "Elasticity", "Production",
        "Cost and Revenue", "Market Structures",
        "National Income", "Inflation", "Money and Banking",
        "Fiscal Policy", "Economic Growth"
    ],
    "Psychology": [
        "Human Behaviour", "Learning", "Motivation",
        "Emotion", "Personality", "Intelligence",
        "Memory", "Thinking", "Stress and Coping", "Mental Health"
    ],
    "Sociology": [
        "Culture and Society", "Social Stratification",
        "Family and Kinship", "Religion", "Education",
        "Caste System", "Gender", "Social Change",
        "Globalization", "Indian Society"
    ],
    "Business Studies": [
        "Nature of Business", "Forms of Business",
        "Management", "Planning", "Organizing",
        "Staffing", "Directing", "Controlling",
        "Marketing", "Financial Management"
    ]
}

# -------------------------------------------------
# MASSIVE BOOK BANK (CORE FEATURE)
# -------------------------------------------------

books = {
    "Polity": {
        "Beginner": [
            "NCERT Class 9–12 Political Science",
            "M. Laxmikanth – Indian Polity (Basic Reading)",
            "Oxford Student Atlas (Indian Polity Sections)",
            "Spectrum – Indian Polity (Simplified Edition)"
        ],
        "Intermediate": [
            "M. Laxmikanth – Indian Polity",
            "Subhash Kashyap – Our Constitution",
            "Bipan Chandra – India Since Independence",
            "DD Basu – Introduction to the Constitution of India"
        ],
        "Advanced": [
            "Granville Austin – Indian Constitution",
            "V. N. Shukla – Constitution of India",
            "MP Jain – Indian Constitutional Law",
            "D. D. Basu – Constitutional Law of India"
        ]
    },

    "Economics": {
        "Beginner": [
            "NCERT Class 11 – Microeconomics",
            "NCERT Class 12 – Macroeconomics",
            "S. Chand – Basic Economics",
            "Trueman’s – Elementary Economics"
        ],
        "Intermediate": [
            "HL Ahuja – Micro & Macro Economics",
            "Paul Samuelson – Economics",
            "Ramesh Singh – Indian Economy",
            "Mishra & Puri – Indian Economy"
        ],
        "Advanced": [
            "Varian – Intermediate Microeconomics",
            "Dornbusch & Fischer – Macroeconomics",
            "Froyen – Macroeconomics",
            "Debraj Ray – Development Economics"
        ]
    },

    "Psychology": {
        "Beginner": [
            "NCERT Class 11 – Psychology",
            "Morgan & King – Introduction to Psychology",
            "Ciccarelli – Psychology",
            "Passer & Smith – Psychology"
        ],
        "Intermediate": [
            "Baron – Psychology",
            "Hilgard – Introduction to Psychology",
            "Atkinson & Hilgard – Psychology",
            "Weiten – Psychology: Themes & Variations"
        ],
        "Advanced": [
            "DSM-5 Diagnostic Manual",
            "Goldstein – Sensation and Perception",
            "Carlson – Physiology of Behavior",
            "Eysenck – Personality Theory"
        ]
    },

    "Sociology": {
        "Beginner": [
            "NCERT Class 11–12 Sociology",
            "IGNOU BA Sociology Material",
            "Haralambos – Sociology (Student Edition)",
            "Anthony Giddens – Sociology (Introductory)"
        ],
        "Intermediate": [
            "Haralambos & Holborn – Sociology",
            "Anthony Giddens – Sociology",
            "Ritzer – Sociological Theory",
            "Bottomore – Sociology"
        ],
        "Advanced": [
            "George Ritzer – Classical Sociological Theory",
            "Turner – Sociological Theory",
            "Smelser – Sociology",
            "Marx, Weber, Durkheim – Original Works"
        ]
    },

    "Business Studies": {
        "Beginner": [
            "NCERT Class 11–12 Business Studies",
            "P. C. Tulsian – Business Studies",
            "Kumar & Mittal – Business Studies",
            "CBSE Exam-Oriented Business Studies Guide"
        ],
        "Intermediate": [
            "Koontz & Weihrich – Essentials of Management",
            "Robbins – Management Fundamentals",
            "Kotler – Marketing Management",
            "K. Aswathappa – Human Resource Management"
        ],
        "Advanced": [
            "Robbins – Organizational Behaviour",
            "Kotler & Keller – Marketing Management",
            "Porter – Competitive Strategy",
            "Grant – Contemporary Strategy Analysis"
        ]
    }
}

# -------------------------------------------------
# VIDEO BANK (MULTIPLE PER SUBJECT)
# -------------------------------------------------

videos = {
    "Polity": [
        "https://www.youtube.com/watch?v=4H2z2z3qZyA",
        "https://www.youtube.com/watch?v=YQyZKzZKJpU",
        "https://www.youtube.com/watch?v=8rFz6pPpE2Q"
    ],
    "Economics": [
        "https://www.youtube.com/watch?v=k2Yv6V2kYhU",
        "https://www.youtube.com/watch?v=3ez10ADR_gM",
        "https://www.youtube.com/watch?v=ZtWzBq5B9Yg"
    ],
    "Psychology": [
        "https://www.youtube.com/watch?v=vo4pMVb0R6M",
        "https://www.youtube.com/watch?v=9Xn6nYz8z0k",
        "https://www.youtube.com/watch?v=J0nTQpN8YkA"
    ],
    "Sociology": [
        "https://www.youtube.com/watch?v=G8qY0WcYjK4",
        "https://www.youtube.com/watch?v=YcN3rTj6mXk",
        "https://www.youtube.com/watch?v=6tN9JpXzL2A"
    ],
    "Business Studies": [
        "https://www.youtube.com/watch?v=2C5WmC6p2Wk",
        "https://www.youtube.com/watch?v=KX8N3Yp0F9I",
        "https://www.youtube.com/watch?v=F6K8M7t9N3Q"
    ]
}

# -------------------------------------------------
# UI
# -------------------------------------------------

subject = st.selectbox("📘 Select Subject", list(subjects.keys()))
topic = st.selectbox("📌 Select Topic", subjects[subject])
level = st.radio("🎯 Select Your Level", ["Beginner", "Intermediate", "Advanced"])

# -------------------------------------------------
# OUTPUT
# -------------------------------------------------

if st.button("📖 Get Study Resources"):
    st.subheader("📚 Recommended Books")

    for book in books[subject][level]:
        st.write(f"• {book}")

    st.subheader("🎥 Recommended Video Lectures")

    for link in videos[subject]:
        st.markdown(f"▶ {link}")
