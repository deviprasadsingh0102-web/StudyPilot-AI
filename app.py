import sqlite3
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st

DB_PATH = Path(__file__).resolve().parent / "studypilot.db"

st.set_page_config(
    page_title="StudyPilot AI | Student Workspace",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------- SAFE & VIBRANT DESIGN SYSTEM --------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Outfit:wght@500;600;700;800&display=swap');

:root {
    --ink: #0f172a;
    --muted: #475569;
    --line: #e2e8f0;
    --surface: #ffffff;
}

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

/* Vibrant Mesh Background */
.stApp {
    background: 
        radial-gradient(circle at 12% 8%, rgba(139, 92, 246, 0.14), transparent 28rem),
        radial-gradient(circle at 88% 12%, rgba(236, 72, 153, 0.12), transparent 28rem),
        radial-gradient(circle at 50% 85%, rgba(14, 165, 233, 0.10), transparent 35rem),
        #f4f7fe;
    color: var(--ink);
}

[data-testid="stHeader"] {
    background: rgba(244, 247, 254, 0.80);
    backdrop-filter: blur(10px);
}

.block-container {
    max-width: 1400px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

h1, h2, h3, h4 {
    font-family: 'Outfit', sans-serif !important;
    color: var(--ink) !important;
    letter-spacing: -0.02em;
}
h1 { font-weight: 800 !important; }
h2, h3 { font-weight: 700 !important; }

/* ==================== UPGRADED SIDE PANEL ==================== */
[data-testid="stSidebar"] {
    background: 
        radial-gradient(circle at 100% 0%, rgba(236, 72, 153, 0.28), transparent 18rem),
        radial-gradient(circle at 0% 100%, rgba(56, 189, 248, 0.22), transparent 20rem),
        linear-gradient(165deg, #0f0c29 0%, #1e1b4b 52%, #111827 100%) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.12);
    box-shadow: 8px 0 32px rgba(15, 23, 42, 0.18);
}
[data-testid="stSidebar"] > div:first-child {
    padding-top: 1rem;
}
[data-testid="stSidebar"] hr {
    border-color: rgba(255, 255, 255, 0.14);
    margin: 0.9rem 0;
}

/* Sidebar Navigation Buttons (Full Width & Glowing) */
[data-testid="stSidebar"] .stButton > button {
    width: 100% !important;
    justify-content: flex-start !important;
    text-align: left !important;
    padding: 0.65rem 1rem !important;
    border-radius: 13px !important;
    font-size: 0.94rem !important;
    font-weight: 600 !important;
    margin-bottom: 0.18rem !important;
    transition: all 0.2s ease !important;
}

/* Inactive Sidebar Buttons */
[data-testid="stSidebar"] .stButton > button[kind="secondary"] {
    background: rgba(255, 255, 255, 0.06) !important;
    color: #e2e8f0 !important;
    border: 1px solid rgba(255, 255, 255, 0.10) !important;
}
[data-testid="stSidebar"] .stButton > button[kind="secondary"]:hover {
    background: rgba(255, 255, 255, 0.15) !important;
    border-color: rgba(255, 255, 255, 0.30) !important;
    color: #ffffff !important;
    transform: translateX(4px);
}

/* Active Selected Sidebar Button */
[data-testid="stSidebar"] .stButton > button[kind="primary"] {
    background: linear-gradient(90deg, #6366f1 0%, #a855f7 50%, #ec4899 100%) !important;
    color: #ffffff !important;
    font-weight: 800 !important;
    border: 1px solid rgba(255, 255, 255, 0.45) !important;
    box-shadow: 0 8px 20px rgba(236, 72, 153, 0.40) !important;
}

/* Brand Header in Sidebar */
.sb-brand {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 0.2rem 0.2rem 0.9rem 0.2rem;
}
.sb-logo {
    width: 44px;
    height: 44px;
    border-radius: 14px;
    background: linear-gradient(135deg, #6366f1 0%, #ec4899 55%, #f59e0b 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.45rem;
    box-shadow: 0 8px 20px rgba(236, 72, 153, 0.45);
}
.sb-title {
    font-family: 'Outfit', sans-serif;
    font-size: 1.3rem;
    font-weight: 800;
    color: #ffffff !important;
    line-height: 1.1;
}
.sb-sub {
    font-size: 0.68rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #a5b4fc !important;
    font-weight: 700;
}

/* Student Profile Card in Sidebar */
.sb-profile {
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.16);
    border-radius: 18px;
    padding: 0.95rem 1rem;
    margin-bottom: 1rem;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
}
.sb-profile-top {
    display: flex;
    align-items: center;
    gap: 11px;
}
.sb-avatar {
    width: 42px;
    height: 42px;
    border-radius: 50%;
    background: linear-gradient(135deg, #06b6d4, #3b82f6);
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    font-size: 1.1rem;
    color: #fff !important;
    border: 2px solid rgba(255, 255, 255, 0.4);
}
.sb-name {
    font-weight: 700;
    font-size: 0.98rem;
    color: #ffffff !important;
    margin: 0;
}
.sb-rank {
    font-size: 0.74rem;
    color: #fde047 !important;
    font-weight: 600;
}
.sb-xp-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.75rem;
    margin-top: 0.65rem;
    padding-top: 0.55rem;
    border-top: 1px solid rgba(255, 255, 255, 0.12);
    color: #e2e8f0 !important;
}
.sb-xp-badge {
    background: linear-gradient(90deg, #ec4899, #8b5cf6);
    color: #ffffff !important;
    padding: 0.15rem 0.6rem;
    border-radius: 99px;
    font-weight: 800;
}

/* Glass Goal Box in Sidebar */
.sb-goal-box {
    background: rgba(255, 255, 255, 0.07);
    border: 1px solid rgba(255, 255, 255, 0.14);
    border-radius: 16px;
    padding: 0.9rem 1rem;
    margin-top: 0.8rem;
}
.sb-goal-head {
    display: flex;
    justify-content: space-between;
    font-size: 0.78rem;
    font-weight: 700;
    margin-bottom: 0.4rem;
    color: #f1f5f9 !important;
}
.sb-bar-bg {
    width: 100%;
    height: 8px;
    background: rgba(255, 255, 255, 0.15);
    border-radius: 99px;
    overflow: hidden;
    margin-bottom: 0.75rem;
}
.sb-bar-fill-1 {
    height: 100%;
    background: linear-gradient(90deg, #38bdf8, #818cf8, #f472b6);
    border-radius: 99px;
}
.sb-bar-fill-2 {
    height: 100%;
    background: linear-gradient(90deg, #34d399, #10b981, #06b6d4);
    border-radius: 99px;
}

/* ==================== COLORFUL HERO BANNER ==================== */
.hero {
    position: relative;
    overflow: hidden;
    padding: 2.2rem 2.5rem;
    border-radius: 26px;
    color: #fff !important;
    background: linear-gradient(120deg, #311042 0%, #4f46e5 45%, #7c3aed 75%, #ec4899 100%);
    margin-bottom: 1.5rem;
    box-shadow: 0 20px 45px -12px rgba(99, 102, 241, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.22);
}
.hero .eyebrow {
    display: inline-block;
    background: rgba(255, 255, 255, 0.18);
    color: #fef08a !important;
    text-transform: uppercase;
    font-size: 0.74rem;
    font-weight: 800;
    letter-spacing: 0.12em;
    padding: 0.35rem 0.9rem;
    border-radius: 99px;
    margin-bottom: 0.85rem;
}
.hero h1 {
    color: #ffffff !important;
    font-size: clamp(1.85rem, 3vw, 2.55rem) !important;
    line-height: 1.15;
    margin: 0 0 0.65rem 0;
}
.hero p {
    color: #f3e8ff !important;
    font-size: 1.03rem;
    margin: 0;
    max-width: 740px;
}

/* ==================== COLORFUL METRIC CARDS ==================== */
.metric-card {
    background: #ffffff;
    border-radius: 20px;
    padding: 1.25rem 1.35rem;
    border: 1px solid #e2e8f0;
    box-shadow: 0 8px 24px rgba(15, 23, 42, 0.05);
    transition: transform 0.22s ease, box-shadow 0.22s ease;
    position: relative;
    overflow: hidden;
}
.metric-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 14px 30px rgba(99, 102, 241, 0.14);
}
.metric-top-bar {
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 6px;
}
.metric-icon-pill {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 42px;
    height: 42px;
    border-radius: 12px;
    font-size: 1.3rem;
    margin-bottom: 0.65rem;
}
.metric-label {
    font-size: 0.84rem;
    font-weight: 700;
    color: #64748b;
    margin-bottom: 0.2rem;
}
.metric-val {
    font-family: 'Outfit', sans-serif;
    font-size: 1.85rem;
    font-weight: 800;
    color: #0f172a;
    line-height: 1.15;
}
.metric-sub {
    font-size: 0.76rem;
    font-weight: 700;
    margin-top: 0.35rem;
}

/* ==================== SUBJECT CARDS ==================== */
.card {
    height: 100%;
    padding: 1.45rem;
    border-radius: 22px;
    border: 1px solid #e2e8f0;
    background: #ffffff;
    margin-bottom: 1.1rem;
    box-shadow: 0 8px 22px rgba(15, 23, 42, 0.04);
    transition: all 0.25s ease;
}
.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 18px 34px rgba(99, 102, 241, 0.13);
}
.card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0.9rem;
}
.card-icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 52px;
    height: 52px;
    border-radius: 16px;
    font-size: 1.65rem;
}
.card-badge {
    font-size: 0.76rem;
    font-weight: 800;
    padding: 0.32rem 0.75rem;
    border-radius: 99px;
}
.card h3 {
    color: #0f172a !important;
    font-size: 1.18rem !important;
    margin: 0 0 0.45rem 0;
}
.card p {
    color: #475569 !important;
    line-height: 1.55;
    margin: 0 0 1rem 0;
    font-size: 0.93rem;
}
.progress-mini {
    width: 100%;
    height: 8px;
    background: #f1f5f9;
    border-radius: 99px;
    overflow: hidden;
}
.progress-mini-fill {
    height: 100%;
    border-radius: 99px;
}

/* Reusable Panels */
.panel {
    padding: 1.4rem 1.55rem;
    border: 1px solid #e2e8f0;
    background: #ffffff;
    border-radius: 20px;
    margin: 0.45rem 0 1rem 0;
    box-shadow: 0 6px 20px rgba(15, 23, 42, 0.04);
}
.pill {
    display: inline-block;
    padding: 0.32rem 0.78rem;
    border-radius: 99px;
    color: #ffffff !important;
    background: linear-gradient(90deg, #6366f1, #ec4899);
    font-size: 0.73rem;
    font-weight: 800;
    letter-spacing: 0.05em;
}

/* Main Area Primary Buttons */
.main .stButton button[kind="primary"], .stFormSubmitButton button[kind="primary"] {
    background: linear-gradient(90deg, #4f46e5 0%, #7c3aed 50%, #ec4899 100%) !important;
    border: none !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    border-radius: 12px !important;
    box-shadow: 0 6px 18px rgba(124, 58, 237, 0.32);
}

.footer {
    text-align: center;
    color: #64748b !important;
    font-size: 0.85rem;
    padding-top: 1rem;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)


# -------------------- DATABASE LAYER --------------------
def connect():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_db():
    with connect() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS profile (
            id INTEGER PRIMARY KEY CHECK(id=1),
            name TEXT NOT NULL DEFAULT 'Student',
            goal TEXT NOT NULL DEFAULT 'Master Python & Machine Learning fundamentals',
            weekly_target INTEGER NOT NULL DEFAULT 180)""")

        cols = [row["name"] for row in conn.execute("PRAGMA table_info(profile)").fetchall()]
        if "weekly_target" not in cols:
            conn.execute("ALTER TABLE profile ADD COLUMN weekly_target INTEGER NOT NULL DEFAULT 180")

        conn.execute("""CREATE TABLE IF NOT EXISTS quiz_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            quiz_name TEXT NOT NULL,
            score INTEGER NOT NULL,
            total INTEGER NOT NULL,
            percentage REAL NOT NULL,
            attempted_at TEXT NOT NULL)""")

        conn.execute("""CREATE TABLE IF NOT EXISTS study_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            minutes INTEGER NOT NULL,
            note TEXT DEFAULT '',
            logged_at TEXT NOT NULL)""")

        conn.execute("""CREATE TABLE IF NOT EXISTS topic_progress (
            subject TEXT NOT NULL,
            topic TEXT NOT NULL,
            completed INTEGER NOT NULL DEFAULT 0,
            PRIMARY KEY (subject, topic))""")

        conn.execute("""INSERT OR IGNORE INTO profile(id, name, goal, weekly_target)
            VALUES(1, 'Student', 'Master Python & Machine Learning fundamentals', 180)""")


def get_profile():
    with connect() as conn:
        return conn.execute("SELECT * FROM profile WHERE id=1").fetchone()


def save_profile(name, goal, weekly_target):
    with connect() as conn:
        conn.execute(
            "UPDATE profile SET name=?, goal=?, weekly_target=? WHERE id=1",
            (name.strip() or "Student", goal.strip() or "Build strong programming skills", int(weekly_target)),
        )


def save_quiz(name, quiz_name, score, total):
    with connect() as conn:
        conn.execute(
            """INSERT INTO quiz_attempts
            (student_name, quiz_name, score, total, percentage, attempted_at)
            VALUES(?, ?, ?, ?, ?, ?)""",
            (name, quiz_name, score, total, round(score * 100 / total, 1),
             datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        )


def get_df(table):
    if table not in {"quiz_attempts", "study_logs"}:
        return pd.DataFrame()
    with connect() as conn:
        rows = conn.execute(f"SELECT * FROM {table} ORDER BY id DESC").fetchall()
    return pd.DataFrame([dict(row) for row in rows])


def save_study(subject, minutes, note):
    with connect() as conn:
        conn.execute(
            "INSERT INTO study_logs(subject, minutes, note, logged_at) VALUES(?, ?, ?, ?)",
            (subject, minutes, note.strip(), datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        )


def get_completed_topics(subject):
    with connect() as conn:
        rows = conn.execute(
            "SELECT topic FROM topic_progress WHERE subject=? AND completed=1", (subject,)
        ).fetchall()
    return {r["topic"] for r in rows}


def set_topic_status(subject, topic, completed):
    with connect() as conn:
        conn.execute(
            """INSERT INTO topic_progress(subject, topic, completed) VALUES(?, ?, ?)
               ON CONFLICT(subject, topic) DO UPDATE SET completed=excluded.completed""",
            (subject, topic, int(completed)),
        )


def reset_all_data():
    with connect() as conn:
        conn.execute("DELETE FROM quiz_attempts")
        conn.execute("DELETE FROM study_logs")
        conn.execute("DELETE FROM topic_progress")


# -------------------- COLORFUL LEARNING CONTENT --------------------
SUBJECTS = {
    "Python Programming": {
        "icon": "🐍",
        "accent": "#2563eb",
        "grad": "linear-gradient(90deg, #2563eb, #06b6d4)",
        "soft_bg": "#dbeafe",
        "description": "Build a strong foundation in Python, from variables and control flow to functions, data structures, and OOP.",
        "topics": [
            "Variables and data types", "Input and output", "Operators", "Conditions (if/elif/else)",
            "For & While Loops", "Functions & Scope", "Strings & Formatting", "Lists & Comprehensions",
            "Tuples & Sets", "Dictionaries", "Exception Handling", "OOP Basics"
        ],
        "url": "https://docs.python.org/3/tutorial/",
    },
    "Machine Learning": {
        "icon": "🧠",
        "accent": "#9333ea",
        "grad": "linear-gradient(90deg, #9333ea, #ec4899)",
        "soft_bg": "#f3e8ff",
        "description": "Learn how feature engineering, model training, cross-validation, and evaluation metrics work together.",
        "topics": [
            "ML Fundamentals", "Data Preprocessing", "Supervised Learning", "Linear & Logistic Regression",
            "Decision Trees & Random Forests", "Train/Test Split & Cross-Validation", "Evaluation Metrics (F1, ROC-AUC)"
        ],
        "url": "https://scikit-learn.org/stable/getting_started.html",
    },
    "Data Science": {
        "icon": "📊",
        "accent": "#0d9488",
        "grad": "linear-gradient(90deg, #0d9488, #10b981)",
        "soft_bg": "#ccfbf1",
        "description": "Explore datasets, handle missing values, build visualizations, and uncover actionable insights.",
        "topics": [
            "NumPy Arrays", "Pandas DataFrames", "Data Cleaning & Imputation",
            "Exploratory Data Analysis (EDA)", "Data Visualization", "Statistical Summary & Reporting"
        ],
        "url": "https://pandas.pydata.org/docs/getting_started/index.html",
    },
    "Artificial Intelligence": {
        "icon": "✨",
        "accent": "#ea580c",
        "grad": "linear-gradient(90deg, #f59e0b, #ea580c)",
        "soft_bg": "#ffedd5",
        "description": "Understand neural networks, Large Language Models (LLMs), prompt engineering, and AI safety.",
        "topics": [
            "AI vs ML vs Deep Learning", "Neural Network Basics", "Generative AI & LLMs",
            "Prompt Engineering Patterns", "RAG & Embeddings", "Hallucinations & Responsible AI"
        ],
        "url": "https://ai.google/education/",
    },
}

QUIZ_BANK = {
    "Python Programming": [
        {"q": "Which keyword defines a function in Python?", "options": ["func", "def", "function", "define"], "answer": "def", "why": "Python uses the 'def' keyword followed by the function name."},
        {"q": "Which data type represents True or False?", "options": ["int", "str", "bool", "list"], "answer": "bool", "why": "Boolean (bool) holds only True or False."},
        {"q": "What is the result of 2 ** 3 in Python?", "options": ["5", "6", "8", "9"], "answer": "8", "why": "** is the exponentiation operator (2 raised to the power of 3)."},
        {"q": "Which collection stores key-value pairs?", "options": ["List", "Tuple", "Set", "Dictionary"], "answer": "Dictionary", "why": "Dictionaries store mappings of unique keys to values."},
        {"q": "Which list method adds a single item to the end?", "options": ["add()", "append()", "push()", "insert()"], "answer": "append()", "why": "list.append(item) adds the element to the end of the list."},
        {"q": "Which value evaluates to False (falsy) in Python?", "options": ["'False'", "[0]", "1", "''"], "answer": "''", "why": "Empty strings (''), empty lists ([]), 0, and None are falsy."},
        {"q": "Which block catches and handles runtime errors?", "options": ["if/else", "try/except", "for/in", "with/as"], "answer": "try/except", "why": "try/except catches exceptions so your program doesn't crash."},
    ],
    "Machine Learning": [
        {"q": "Why do we split data into training and testing sets?", "options": ["To speed up training", "To evaluate performance on unseen data", "To remove missing values", "To reduce column count"], "answer": "To evaluate performance on unseen data", "why": "Testing on unseen data detects overfitting and measures generalization."},
        {"q": "Predicting house prices (continuous numbers) is an example of:", "options": ["Classification", "Clustering", "Regression", "Reinforcement Learning"], "answer": "Regression", "why": "Regression predicts continuous numerical outputs."},
        {"q": "What happens when a model memorizes noise in the training data?", "options": ["Underfitting", "Overfitting", "Regularization", "Normalization"], "answer": "Overfitting", "why": "Overfitting means high training accuracy but poor test accuracy."},
        {"q": "Which metric is best for imbalanced classification datasets?", "options": ["Raw Accuracy", "Mean Squared Error", "F1-Score", "R-Squared"], "answer": "F1-Score", "why": "F1-Score balances Precision and Recall, unlike raw accuracy."},
        {"q": "Which library is the standard for classical ML in Python?", "options": ["Flask", "Scikit-learn", "BeautifulSoup", "Pygame"], "answer": "Scikit-learn", "why": "Scikit-learn provides consistent APIs for classification, regression, and clustering."},
    ],
    "Data Science": [
        {"q": "Which Pandas method shows the first 5 rows of a DataFrame?", "options": ["df.first()", "df.top()", "df.head()", "df.peek()"], "answer": "df.head()", "why": "df.head() returns the top 5 rows by default."},
        {"q": "How do you check the number of missing values per column in Pandas?", "options": ["df.isna().sum()", "df.missing()", "df.null_count()", "df.empty()"], "answer": "df.isna().sum()", "why": "df.isna() creates a boolean mask and .sum() counts True values per column."},
        {"q": "Which chart is best for viewing the distribution of a single numerical variable?", "options": ["Pie chart", "Histogram", "Line chart", "Scatter plot"], "answer": "Histogram", "why": "Histograms group numeric data into bins to show frequency distributions."},
        {"q": "What does df.describe() generate?", "options": ["Column data types", "Summary statistics (mean, std, quartiles)", "A bar chart", "Missing value rows"], "answer": "Summary statistics (mean, std, quartiles)", "why": "describe() computes count, mean, std, min, quartiles, and max."},
        {"q": "Which Pandas property selects rows and columns by integer position?", "options": ["df.loc", "df.iloc", "df.select", "df.find"], "answer": "df.iloc", "why": "iloc uses integer-location indexing, while loc uses labels."},
    ],
    "Artificial Intelligence": [
        {"q": "What does LLM stand for in modern AI?", "options": ["Linear Logic Model", "Large Language Model", "Local Learning Machine", "Layered Lexical Module"], "answer": "Large Language Model", "why": "LLMs are deep learning models trained on massive text corpora."},
        {"q": "When an AI confidently generates false information, it is called a:", "options": ["Bug", "Hallucination", "Gradient explosion", "Token overflow"], "answer": "Hallucination", "why": "Hallucinations occur when models predict plausible-sounding but factually incorrect tokens."},
        {"q": "Giving an AI 2-3 input/output examples inside your prompt is known as:", "options": ["Zero-shot prompting", "Few-shot prompting", "Model fine-tuning", "Tokenization"], "answer": "Few-shot prompting", "why": "Few-shot prompting guides the model's output format using in-context examples."},
        {"q": "What does RAG stand for?", "options": ["Rapid AI Generation", "Retrieval-Augmented Generation", "Random Access Graph", "Recurrent Attention Gate"], "answer": "Retrieval-Augmented Generation", "why": "RAG fetches relevant documents from a knowledge base before generating an answer."},
        {"q": "Which parameter controls the randomness/creativity of an LLM's response?", "options": ["Epoch", "Batch size", "Temperature", "Learning rate"], "answer": "Temperature", "why": "Lower temperature makes outputs deterministic; higher temperature increases creativity."},
    ],
}

MENTOR_KB = {
    "Python Lists": {
        "keywords": ["list", "append", "slice"],
        "reply": "A **Python List** is an ordered, mutable collection.\n```python\nfruits = ['apple', 'banana']\nfruits.append('cherry')      # Add to end\nprint(fruits[0])             # 'apple'\nprint([x.upper() for x in fruits]) # List comprehension\n```"
    },
    "Dictionaries": {
        "keywords": ["dictionary", "dict", "key-value", "key"],
        "reply": "A **Dictionary** stores fast key-value mappings.\n```python\nuser = {'name': 'Asha', 'score': 92}\nprint(user.get('name'))      # Safe lookup -> 'Asha'\nuser['role'] = 'Student'     # Add or update key\n```"
    },
    "Loops (For / While)": {
        "keywords": ["loop", "for", "while", "range", "iterate"],
        "reply": "Use a **`for` loop** when iterating over a sequence, and a **`while` loop** when repeating until a condition changes:\n```python\nfor i in range(1, 4):\n    print(f'Step {i}')\n```"
    },
    "Functions": {
        "keywords": ["function", "def", "return", "parameter"],
        "reply": "**Functions** keep code reusable and organized:\n```python\ndef calculate_grade(score: int) -> str:\n    return 'Pass' if score >= 60 else 'Review'\n```"
    },
    "Machine Learning Workflow": {
        "keywords": ["machine learning", "ml", "overfitting", "train", "model"],
        "reply": "**Standard ML Pipeline:**\n1. **Clean Data**: Handle missing values & outliers.\n2. **Split**: `train_test_split(X, y, test_size=0.2)`\n3. **Train**: `model.fit(X_train, y_train)`\n4. **Evaluate**: Check accuracy, precision, recall, or RMSE on `X_test`."
    },
    "Pandas Basics": {
        "keywords": ["pandas", "dataframe", "csv", "clean"],
        "reply": "**Essential Pandas Commands:**\n```python\nimport pandas as pd\ndf = pd.read_csv('data.csv')\ndf.info()                    # Check types and nulls\ndf.dropna(inplace=True)      # Remove missing rows\ndf.groupby('category')['sales'].mean()\n```"
    },
    "Study Strategy (Pomodoro)": {
        "keywords": ["study", "focus", "plan", "pomodoro", "habit"],
        "reply": "**Active Recall + Pomodoro Method:**\n* **25 mins**: Deep study with zero phone distractions.\n* **5 mins**: Write down 3 things you learned from memory (Active Recall).\n* **Test**: Take a quick quiz in the **Quiz** tab to lock in retention."
    },
}


# -------------------- INITIALIZE APP STATE --------------------
initialize_db()
profile = get_profile()
student_name = profile["name"]
weekly_target = int(profile["weekly_target"])

attempts_df = get_df("quiz_attempts")
logs_df = get_df("study_logs")

total_mins = int(logs_df["minutes"].sum()) if not logs_df.empty else 0
avg_score = float(attempts_df["percentage"].mean()) if not attempts_df.empty else 0.0

total_topics_count = sum(len(v["topics"]) for v in SUBJECTS.values())
completed_topics_count = sum(len(get_completed_topics(subj)) for subj in SUBJECTS)

# Calculate XP & Student Rank for Sidebar
xp_points = (completed_topics_count * 50) + (len(attempts_df) * 100) + (total_mins * 2)
if xp_points >= 1500:
    rank_title = "🏆 Grandmaster Scholar"
elif xp_points >= 750:
    rank_title = "⚡ Pro Explorer"
elif xp_points >= 250:
    rank_title = "🚀 Rising Coder"
else:
    rank_title = "🌱 Starter Cadet"

# Initialize Active Page in Session State (Prevents Blank Screen Bug!)
if "active_page" not in st.session_state:
    st.session_state.active_page = "Dashboard"


# -------------------- REDESIGNED BULLETPROOF SIDEBAR --------------------
with st.sidebar:
    # 1. Custom Glowing Brand Header
    st.markdown(
        '<div class="sb-brand">'
        '<div class="sb-logo">🚀</div>'
        '<div><div class="sb-title">StudyPilot AI</div>'
        '<div class="sb-sub">Smart Learning OS</div></div>'
        '</div>',
        unsafe_allow_html=True,
    )

    # 2. Student Avatar & XP Level Card
    initials = "".join([part[0].upper() for part in student_name.split()[:2]]) or "S"
    st.markdown(
        f'<div class="sb-profile">'
        f'<div class="sb-profile-top">'
        f'<div class="sb-avatar">{initials}</div>'
        f'<div><div class="sb-name">{student_name}</div>'
        f'<div class="sb-rank">{rank_title}</div></div>'
        f'</div>'
        f'<div class="sb-xp-row">'
        f'<span>Total Experience</span>'
        f'<span class="sb-xp-badge">✨ {xp_points} XP</span>'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # 3. Full-Width Glowing Navigation Buttons (100% Reliable)
    MENU_ITEMS = [
        ("Dashboard", "🏠  Dashboard"),
        ("Subjects", "📚  Subjects & Syllabus"),
        ("Quiz", "📝  Knowledge Quiz"),
        ("AI Mentor", "🤖  AI Study Mentor"),
        ("Progress", "📈  Progress Analytics"),
        ("Study Planner", "🗓️  Study Planner"),
        ("Profile", "👤  Profile & Settings"),
    ]

    for page_key, label in MENU_ITEMS:
        is_active = st.session_state.active_page == page_key
        if st.button(
            label,
            key=f"nav_btn_{page_key}",
            type="primary" if is_active else "secondary",
            use_container_width=True,
        ):
            st.session_state.active_page = page_key
            st.rerun()

    # 4. Custom Glassmorphic Progress Trackers
    goal_pct = min(int((total_mins / max(weekly_target, 1)) * 100), 100)
    topic_pct = int((completed_topics_count / max(total_topics_count, 1)) * 100)

    st.markdown(
        f'<div class="sb-goal-box">'
        f'<div class="sb-goal-head"><span>⏱️ Weekly Study Target</span><span>{goal_pct}%</span></div>'
        f'<div class="sb-bar-bg"><div class="sb-bar-fill-1" style="width:{goal_pct}%;"></div></div>'
        f'<div class="sb-goal-head"><span>🎓 Syllabus Mastery</span><span>{topic_pct}%</span></div>'
        f'<div class="sb-bar-bg" style="margin-bottom:0.2rem;"><div class="sb-bar-fill-2" style="width:{topic_pct}%;"></div></div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    st.divider()
    st.caption("✨ **Daily Boost:** 25 mins of focused coding today builds unstoppable momentum!")

page = st.session_state.active_page


# -------------------- PAGE 1: DASHBOARD --------------------
if page == "Dashboard":
    st.markdown(
        f'<div class="hero">'
        f'<div class="eyebrow">✨ {rank_title.upper()} · {xp_points} XP EARNED</div>'
        f'<h1>Welcome back, {student_name}! 🌟</h1>'
        f'<p>Active Mission: <strong>{profile["goal"]}</strong> — Keep checking off your syllabus, testing your skills, and stacking daily XP.</p>'
        f'</div>',
        unsafe_allow_html=True,
    )

    m1, m2, m3, m4 = st.columns(4)
    metrics_data = [
        (m1, "📚", "Topics Mastered", f"{completed_topics_count}/{total_topics_count}", f"{topic_pct}% Syllabus Completed", "linear-gradient(90deg, #3b82f6, #06b6d4)", "#dbeafe", "#1d4ed8"),
        (m2, "📝", "Quizzes Completed", str(len(attempts_df)), "Across 4 Learning Tracks", "linear-gradient(90deg, #8b5cf6, #ec4899)", "#f3e8ff", "#7e22ce"),
        (m3, "🎯", "Average Quiz Score", f"{avg_score:.0f}%", "Target: 80%+ Mastery", "linear-gradient(90deg, #10b981, #14b8a6)", "#d1fae5", "#047857"),
        (m4, "⏱️", "Total Study Time", f"{total_mins // 60}h {total_mins % 60}m", f"Weekly Target: {weekly_target}m", "linear-gradient(90deg, #f59e0b, #ef4444)", "#ffedd5", "#b45309"),
    ]
    for col, icon, label, val, sub, bar_grad, icon_bg, sub_color in metrics_data:
        with col:
            st.markdown(
                f'<div class="metric-card">'
                f'<div class="metric-top-bar" style="background:{bar_grad};"></div>'
                f'<div class="metric-icon-pill" style="background:{icon_bg};">{icon}</div>'
                f'<div class="metric-label">{label}</div>'
                f'<div class="metric-val">{val}</div>'
                f'<div class="metric-sub" style="color:{sub_color};">{sub}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("## 🎨 Interactive Learning Tracks")
    cols = st.columns(2, gap="medium")
    for i, (subj_name, info) in enumerate(SUBJECTS.items()):
        done_set = get_completed_topics(subj_name)
        total_t = len(info["topics"])
        done_t = len(done_set)
        pct_t = int((done_t / total_t) * 100) if total_t else 0

        with cols[i % 2]:
            st.markdown(
                f'<div class="card" style="border-top: 5px solid {info["accent"]};">'
                f'<div class="card-header">'
                f'<div class="card-icon" style="background:{info["soft_bg"]};">{info["icon"]}</div>'
                f'<span class="card-badge" style="background:{info["soft_bg"]}; color:{info["accent"]};">'
                f'{done_t}/{total_t} Topics · {pct_t}%</span>'
                f'</div>'
                f'<h3>{subj_name}</h3>'
                f'<p>{info["description"]}</p>'
                f'<div class="progress-mini">'
                f'<div class="progress-mini-fill" style="width:{pct_t}%; background:{info["grad"]};"></div>'
                f'</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    left, right = st.columns([1.25, 1], gap="medium")
    with left:
        st.markdown("### 🚀 Recommended Next Move")
        if attempts_df.empty:
            rec_title = "Take your first diagnostic quiz (+100 XP)"
            rec_desc = "Head to the Knowledge Quiz tab and complete a quick check to unlock your score analytics."
        elif avg_score < 70:
            rec_title = "Boost your quiz average above 70%"
            rec_desc = f"Your current average is {avg_score:.0f}%. Review quick concepts in the AI Mentor tab and retry!"
        else:
            rec_title = "Master new syllabus topics (+50 XP each)"
            rec_desc = f"Awesome {avg_score:.0f}% quiz average! Check off your next topic in Subjects and log a focus session."

        st.markdown(
            f'<div class="panel"><span class="pill">NEXT ACTION</span>'
            f'<h3 style="margin-top:0.75rem;">{rec_title}</h3>'
            f'<p style="margin-bottom:0;">{rec_desc}</p></div>',
            unsafe_allow_html=True,
        )

    with right:
        st.markdown("### 🎯 Current Goal")
        st.markdown(
            f'<div class="panel"><span class="pill">ACTIVE GOAL</span>'
            f'<h3 style="margin-top:0.75rem;">{profile["goal"]}</h3>'
            f'<p style="margin-bottom:0;">Weekly habit target: <strong>{weekly_target} minutes</strong>.</p></div>',
            unsafe_allow_html=True,
        )


# -------------------- PAGE 2: SUBJECTS --------------------
elif page == "Subjects":
    st.title("📚 Learning Tracks & Syllabus")
    st.write("Select a colorful track below and check off completed topics. Each checked topic awards **+50 XP**!")

    chosen = st.selectbox("Select learning track", list(SUBJECTS.keys()))
    info = SUBJECTS[chosen]
    done_topics = get_completed_topics(chosen)

    st.markdown(
        f'<div class="panel" style="border-left: 6px solid {info["accent"]};">'
        f'<span class="pill" style="background:{info["grad"]};">SYLLABUS TRACKER</span>'
        f'<h2 style="margin-top:0.65rem;">{info["icon"]} {chosen}</h2>'
        f'<p style="margin-bottom:0;">{info["description"]}</p></div>',
        unsafe_allow_html=True,
    )

    st.markdown("### ✅ Topic Mastery Checklist")
    topic_cols = st.columns(2)
    current_checked = 0

    for i, topic in enumerate(info["topics"]):
        is_done = topic in done_topics
        with topic_cols[i % 2]:
            new_val = st.checkbox(topic, value=is_done, key=f"chk_{chosen}_{topic}")
            if new_val != is_done:
                set_topic_status(chosen, topic, new_val)
                st.rerun()
            if new_val:
                current_checked += 1

    pct_done = current_checked / len(info["topics"])
    st.progress(pct_done, text=f"{current_checked} of {len(info['topics'])} topics mastered ({pct_done*100:.0f}%)")
    st.link_button(f"Open Official {chosen} Documentation ↗", info["url"])


# -------------------- PAGE 3: QUIZ --------------------
elif page == "Quiz":
    st.title("📝 Multi-Track Knowledge Quiz")
    st.write("Test your skills across any subject. Every completed quiz awards **+100 XP**!")

    quiz_subject = st.selectbox("Choose Quiz Subject", list(QUIZ_BANK.keys()))
    questions = QUIZ_BANK[quiz_subject]
    subj_style = SUBJECTS[quiz_subject]

    st.markdown(
        f'<div class="panel" style="border-left: 6px solid {subj_style["accent"]};">'
        f'<span class="pill" style="background:{subj_style["grad"]};">{len(questions)} QUESTIONS · {quiz_subject.upper()}</span> &nbsp; '
        f'Answer all questions below and submit to record your score.</div>',
        unsafe_allow_html=True,
    )

    with st.form(f"quiz_form_{quiz_subject}"):
        answers = []
        for i, item in enumerate(questions):
            st.markdown(f"**Q{i + 1}. {item['q']}**")
            ans = st.radio(
                "Select option",
                item["options"],
                index=None,
                key=f"q_{quiz_subject}_{i}",
                horizontal=True,
                label_visibility="collapsed",
            )
            answers.append(ans)
            if i < len(questions) - 1:
                st.divider()

        submitted = st.form_submit_button("🚀 Submit Quiz Answers", type="primary", use_container_width=True)

    if submitted:
        unanswered = sum(1 for a in answers if a is None)
        if unanswered > 0:
            st.warning(f"You left {unanswered} question(s) blank. Unanswered items are marked incorrect.")

        score = sum(answers[i] == item["answer"] for i, item in enumerate(questions))
        pct = score * 100 / len(questions)
        save_quiz(student_name, quiz_subject, score, len(questions))

        st.balloons()
        st.success(f"🎉 Quiz saved! You earned **+100 XP** in **{quiz_subject}**.")
        c1, c2, c3 = st.columns(3)
        c1.metric("Correct Answers", f"{score} / {len(questions)}")
        c2.metric("Percentage", f"{pct:.0f}%")
        c3.metric("Rating", "🌟 Mastery" if pct >= 80 else "👍 Good Job" if pct >= 60 else "📖 Keep Practicing")

        with st.expander("🔍 Review Answers & Explanations", expanded=True):
            for i, item in enumerate(questions):
                is_correct = answers[i] == item["answer"]
                icon = "✅" if is_correct else "❌"
                st.markdown(f"**{icon} Q{i + 1}. {item['q']}**")
                st.write(f"Your answer: `{answers[i] or 'Not answered'}` | Correct answer: `{item['answer']}`")
                st.caption(f"💡 **Why:** {item['why']}")
                st.divider()


# -------------------- PAGE 4: AI MENTOR --------------------
elif page == "AI Mentor":
    st.title("🤖 Interactive AI Study Mentor")
    st.write("Click a quick-topic button below or ask a question in the chat box for instant code snippets and explanations.")

    if "mentor_messages" not in st.session_state:
        st.session_state.mentor_messages = [
            {
                "role": "assistant",
                "content": f"Hey **{student_name}**! 👋 Pick a topic button above or ask me about **Python lists, dictionaries, loops, functions, Pandas, Machine Learning**, or **study tips**."
            }
        ]

    st.markdown("##### ✨ Quick Topic Lookup:")
    q_cols = st.columns(4)
    clicked_topic = None
    for idx, topic_name in enumerate(MENTOR_KB.keys()):
        with q_cols[idx % 4]:
            if st.button(topic_name, key=f"mentor_btn_{idx}", use_container_width=True):
                clicked_topic = topic_name

    st.divider()

    for msg in st.session_state.mentor_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_prompt = st.chat_input("Ask a question (e.g., Show me how Python dictionaries work)...")

    active_query = user_prompt or clicked_topic

    if active_query:
        st.session_state.mentor_messages.append({"role": "user", "content": active_query})
        q_lower = active_query.lower()

        matched_reply = None
        if active_query in MENTOR_KB:
            matched_reply = MENTOR_KB[active_query]["reply"]
        else:
            for topic_title, data in MENTOR_KB.items():
                if any(k in q_lower for k in data["keywords"]):
                    matched_reply = data["reply"]
                    break

        if not matched_reply:
            matched_reply = (
                "I'm currently in **Offline Mentor Mode**. Try asking about: "
                "**Python Lists, Dictionaries, Loops, Functions, Pandas, Machine Learning**, or **Study Strategy**!"
            )

        st.session_state.mentor_messages.append({"role": "assistant", "content": matched_reply})
        st.rerun()


# -------------------- PAGE 5: PROGRESS --------------------
elif page == "Progress":
    st.title("📈 Progress & Analytics")
    st.write("Track your quiz score trends, study time by subject, and export your records.")

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Quiz Attempts", len(attempts_df))
    c2.metric("Logged Study Sessions", len(logs_df))
    c3.metric("Total XP Earned", f"✨ {xp_points} XP")

    col_left, col_right = st.columns(2, gap="medium")

    with col_left:
        st.markdown("### 🎯 Quiz Score Trend (%)")
        if not attempts_df.empty:
            chart_df = attempts_df.iloc[::-1].copy()
            chart_df["Attempt"] = range(1, len(chart_df) + 1)
            st.line_chart(chart_df.set_index("Attempt")["percentage"])
        else:
            st.info("Complete a quiz in the Knowledge Quiz tab to see your score trend chart.")

    with col_right:
        st.markdown("### ⏱️ Study Minutes by Subject")
        if not logs_df.empty:
            subj_totals = logs_df.groupby("subject")["minutes"].sum()
            st.bar_chart(subj_totals)
        else:
            st.info("Log a session in Study Planner to see your subject breakdown.")

    if not attempts_df.empty:
        st.markdown("### 📋 Recent Quiz Results")
        st.dataframe(
            attempts_df[["quiz_name", "score", "total", "percentage", "attempted_at"]],
            use_container_width=True,
            hide_index=True,
        )

    if not logs_df.empty:
        st.markdown("### 🗂️ Study Logs")
        st.dataframe(
            logs_df[["subject", "minutes", "note", "logged_at"]],
            use_container_width=True,
            hide_index=True,
        )
        csv_data = logs_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Download Study Logs (CSV)",
            data=csv_data,
            file_name="studypilot_logs.csv",
            mime="text/csv",
        )


# -------------------- PAGE 6: STUDY PLANNER --------------------
elif page == "Study Planner":
    st.title("🗓️ Study Session Logger")
    st.write("Record your study sessions to hit your weekly target and earn **+2 XP per minute**!")

    col_form, col_timer = st.columns([1.4, 1], gap="medium")

    with col_form:
        with st.form("study_form"):
            subject = st.selectbox("Subject Track", list(SUBJECTS.keys()))
            minutes = st.number_input("Study Duration (minutes)", min_value=5, max_value=480, value=30, step=5)
            note = st.text_area("Session Notes", placeholder="e.g., Practiced Python functions and completed 10 coding exercises.")
            save = st.form_submit_button("✨ Save Study Session", type="primary", use_container_width=True)

        if save:
            save_study(subject, int(minutes), note)
            st.success(f"Awesome! Logged {minutes} mins (+{int(minutes)*2} XP).")
            st.rerun()

    with col_timer:
        st.markdown(
            '<div class="panel" style="border-top: 5px solid #ec4899;">'
            '<span class="pill">POMODORO BOOST</span>'
            '<h3 style="margin-top:0.75rem;">25-Minute Sprint</h3>'
            '<p>1. Pick <strong>one topic</strong> from Subjects.<br>'
            '2. Study distraction-free for <strong>25 minutes</strong>.<br>'
            '3. Write 3 key takeaways from memory.<br>'
            '4. Log your session here to level up your rank!</p></div>',
            unsafe_allow_html=True,
        )

    if not logs_df.empty:
        st.markdown("### 🕒 Recent Sessions")
        st.dataframe(
            logs_df[["subject", "minutes", "note", "logged_at"]].head(8),
            use_container_width=True,
            hide_index=True,
        )


# -------------------- PAGE 7: PROFILE --------------------
elif page == "Profile":
    st.title("👤 Student Profile & Settings")
    st.write("Update your name, learning goal, and weekly target. Your sidebar badge updates automatically!")

    with st.form("profile_form"):
        name = st.text_input("Your Name", value=profile["name"])
        goal = st.text_area("Your Learning Goal", value=profile["goal"])
        target = st.slider("Weekly Study Target (minutes)", min_value=30, max_value=1200, value=weekly_target, step=30)
        save = st.form_submit_button("💾 Save Profile Changes", type="primary", use_container_width=True)

    if save:
        save_profile(name, goal, target)
        st.success("Profile updated! Check the sidebar to see your updated card.")
        st.rerun()

    st.markdown("### ⚙️ Reset Workspace")
    with st.expander("Danger Zone: Clear All Progress"):
        st.warning("This will permanently delete all quiz attempts, study logs, XP, and checked syllabus topics.")
        if st.button("🗑️ Reset All Data"):
            reset_all_data()
            st.success("All workspace data has been reset.")
            st.rerun()

st.divider()
st.markdown(
    '<div class="footer">🚀 StudyPilot AI · Vibrant Student Edition · Keep learning, keep leveling up!</div>',
    unsafe_allow_html=True,
)
