import os
import re
import zipfile
import urllib.parse
from pathlib import Path

import streamlit as st
import gdown
import pandas as pd
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# --------------------------------------------------
# CONFIG
# --------------------------------------------------
FILE_ID = "1GoY0DZj1KLdC0Xvur0tQlvW_993biwcZ"
ZIP_PATH = "ncert.zip"
EXTRACT_DIR = "ncert_extracted"

SUBJECTS = ["Polity", "Economics", "Sociology", "Psychology", "Business Studies"]
LEVELS = ["Beginner", "Intermediate", "Advanced"]

# --------------------------------------------------
# STREAMLIT SETUP
# --------------------------------------------------
st.set_page_config(page_title="NCERT Learning Assistant", layout="wide")
st.title("📘 NCERT Learning Assistant")
st.caption("Topic → Chapter → Book → Video recommendations")

# --------------------------------------------------
# DOWNLOAD & EXTRACT NCERT PDFs
# --------------------------------------------------
def download_and_extract():
    if not os.path.exists(ZIP_PATH):
        gdown.download(
            f"https://drive.google.com/uc?id={FILE_ID}",
            ZIP_PATH,
            quiet=False,
        )

    os.makedirs(EXTRACT_DIR, exist_ok=True)

    with zipfile.ZipFile(ZIP_PATH, "r") as z:
        z.extractall(EXTRACT_DIR)

    for zfile in Path(EXTRACT_DIR).rglob("*.zip"):
        try:
            target = zfile.parent / zfile.stem
            target.mkdir(exist_ok=True)
            with zipfile.ZipFile(zfile, "r") as inner:
                inner.extractall(target)
        except:
            pass


download_and_extract()

# --------------------------------------------------
# PDF UTILITIES
# --------------------------------------------------
def read_pdf(path):
    try:
        reader = PdfReader(path)
        return " ".join(page.extract_text() or "" for page in reader.pages)
    except:
        return ""


def clean_text(text):
    text = re.sub(
        r"(activity|exercise|project|copyright|isbn).*",
        " ",
        text,
        flags=re.I,
    )
    return re.sub(r"\s+", " ", text).strip()


@st.cache_data
def load_all_texts():
    texts, paths = [], []
    for pdf in Path(EXTRACT_DIR).rglob("*.pdf"):
        txt = clean_text(read_pdf(str(pdf)))
        if len(txt.split()) > 100:
            texts.append(txt)
            paths.append(pdf.name)
    return texts, paths


# --------------------------------------------------
# TOPIC EXTRACTION
# --------------------------------------------------
def extract_topics_from_text(text):
    sentences = re.split(r"[.\n]", text)
    topics = []

    for s in sentences:
        s = s.strip()
        if 2 <= len(s.split()) <= 6:
            if not any(x in s.lower() for x in ["isbn", "copyright", "exercise"]):
                topics.append(s.title())

    return list(set(topics))


@st.cache_data
def get_all_topics():
    texts, _ = load_all_texts()
    all_topics = []
    for t in texts:
        all_topics.extend(extract_topics_from_text(t))
    return sorted(set(all_topics))


all_topics = get_all_topics()

# --------------------------------------------------
# EMBEDDING MODEL
# --------------------------------------------------
@st.cache_resource
def load_embedder():
    return SentenceTransformer("all-MiniLM-L6-v2")


embedder = load_embedder()

# --------------------------------------------------
# BOOKS & VIDEOS
# --------------------------------------------------
books = {
    "Economics": {
        "Beginner": ["NCERT Economics Class 11", "Basic Economics – Mankiw"],
        "Intermediate": ["Principles of Economics – Mankiw"],
        "Advanced": ["Advanced Economic Theory – H L Ahuja"],
    },
    "Polity": {
        "Beginner": ["NCERT Political Science Class 11"],
        "Intermediate": ["Indian Polity – M. Laxmikanth"],
        "Advanced": ["Constitution of India – D D Basu"],
    },
    "Sociology": {
        "Beginner": ["NCERT Sociology Class 11"],
        "Intermediate": ["Sociology – Haralambos"],
        "Advanced": ["Sociology – Anthony Giddens"],
    },
    "Psychology": {
        "Beginner": ["NCERT Psychology Class 11"],
        "Intermediate": ["Understanding Psychology – Feldman"],
        "Advanced": ["Handbook of Psychology"],
    },
    "Business Studies": {
        "Beginner": ["NCERT Business Studies Class 11"],
        "Intermediate": ["Business Studies – Poonam Gandhi"],
        "Advanced": ["Strategic Management – Robbins"],
    },
}

videos = {
    "Economics": {
        "Beginner": ["https://www.youtube.com/watch?v=3ez10ADR_gM"],
        "Intermediate": ["https://www.youtube.com/watch?v=9M0xQ2uN8Fk"],
        "Advanced": ["https://www.youtube.com/watch?v=H5oZ4wN9bEY"],
    },
    "Polity": {
        "Beginner": ["https://www.youtube.com/watch?v=Y2nZ6C3V0ks"],
        "Intermediate": ["https://www.youtube.com/watch?v=KkMZP9Q8vYQ"],
        "Advanced": ["https://www.youtube.com/watch?v=bL5G8K0qZ8s"],
    },
}

# --------------------------------------------------
# VIDEO THUMBNAILS
# --------------------------------------------------
def get_youtube_id(url):
    parsed = urllib.parse.urlparse(url)
    if parsed.hostname in ("www.youtube.com", "youtube.com"):
        return urllib.parse.parse_qs(parsed.query).get("v", [None])[0]
    elif parsed.hostname == "youtu.be":
        return parsed.path.lstrip("/")
    return None


def show_video_thumbnails(video_urls, cols=3):
    if not video_urls:
        st.info("No videos available.")
        return

    columns = st.columns(cols)
    for i, url in enumerate(video_urls):
        vid = get_youtube_id(url)
        if not vid:
            continue

        thumb = f"https://img.youtube.com/vi/{vid}/0.jpg"
        with columns[i % cols]:
            st.markdown(
                f"""
                <a href="{url}" target="_blank">
                    <img src="{thumb}" style="width:100%; border-radius:10px;">
                </a>
                """,
                unsafe_allow_html=True,
            )

# --------------------------------------------------
# SIDEBAR UI
# --------------------------------------------------
st.sidebar.header("🎓 Learning Preferences")

subject = st.sidebar.selectbox("Subject", SUBJECTS)
level = st.sidebar.selectbox("Level", LEVELS)

if all_topics:
    topics = st.sidebar.multiselect("Select Topics", all_topics)
else:
    topics = []

# --------------------------------------------------
# CHAPTER RECOMMENDATION
# --------------------------------------------------
def recommend_chapters(topics, top_n=5):
    if not topics:
        return pd.DataFrame()

    texts, paths = load_all_texts()
    text_emb = embedder.encode(texts)
    topic_emb = embedder.encode([" ".join(topics)])

    sims = cosine_similarity(topic_emb, text_emb)[0]
    top_idx = sims.argsort()[-top_n:][::-1]

    return pd.DataFrame({
        "Chapter PDF": [paths[i] for i in top_idx],
        "Similarity": [round(float(sims[i]), 3) for i in top_idx],
    })


# --------------------------------------------------
# OUTPUT
# --------------------------------------------------
st.subheader("📚 Recommended Chapters")

if st.button("Generate Recommendations"):
    chapter_df = recommend_chapters(topics)
    if chapter_df.empty:
        st.warning("Please select at least one topic.")
    else:
        st.dataframe(chapter_df)

    st.subheader("📖 Recommended Books")
    for b in books.get(subject, {}).get(level, []):
        st.write("📘", b)

    st.subheader("🎥 Recommended Videos")
    show_video_thumbnails(videos.get(subject, {}).get(level, []))
