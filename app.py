import sqlite3
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st

DB_PATH = Path(__file__).resolve().parent / "studypilot.db"

st.set_page_config(
    page_title="StudyPilot AI | Student Workspace",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------- ENHANCED DESIGN SYSTEM --------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');

:root {
    --navy: #0f172a;
    --navy-light: #1e293b;
    --blue: #2563eb;
    --blue-dark: #1d4ed8;
    --teal: #0d9488;
    --ink: #0f172a;
    --muted: #64748b;
    --line: #e2e8f0;
    --surface: #ffffff;
    --canvas: #f8fafc;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: 
        radial-gradient(circle at 90% 0%, rgba(37, 99, 235, 0.08), transparent 35rem),
        radial-gradient(circle at 10% 20%, rgba(13, 148, 136, 0.05), transparent 30rem),
        var(--canvas);
    color: var(--ink);
}

[data-testid="stHeader"] { background: rgba(248, 250, 252, 0.85); backdrop-filter: blur(8px); }

.block-container {
    max-width: 1400px;
    padding-top: 1.8rem;
    padding-bottom: 3rem;
}

h1, h2, h3, h4 {
    font-family: 'Manrope', sans-serif !important;
    color: var(--ink) !important;
    letter-spacing: -0.025em;
}
h1 { font-weight: 800 !important; }
h2, h3 { font-weight: 700 !important; }

/* Sidebar Styling */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #090d16 0%, #111827 60%, #1e293b 100%);
    border-right: 1px solid rgba(255, 255, 255, 0.08);
}
[data-testid="stSidebar"] > div:first-child { padding-top: 1.2rem; }
[data-testid="stSidebar"] * { color: #f1f5f9; }
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p { color: #94a3b8 !important; }
[data-testid="stSidebar"] hr { border-color: rgba(255, 255, 255, 0.12); }
[data-testid="stSidebar"] [role="radiogroup"] label {
    padding: 0.6rem 0.8rem;
    border-radius: 12px;
    margin-bottom: 0.2rem;
    transition: all 0.2s ease;
}
[data-testid="stSidebar"] [role="radiogroup"] label:hover {
    background: rgba(255, 255, 255, 0.08);
    transform: translateX(3px);
}

/* Hero Banner */
.hero {
    position: relative;
    overflow: hidden;
    padding: 2.3rem 2.5rem;
    border-radius: 24px;
    color: #fff !important;
    background: linear-gradient(125deg, #0f172a 0%, #1e3a8a 55%, #2563eb 100%);
    margin-bottom: 1.5rem;
    box-shadow: 0 20px 40px -15px rgba(30, 58, 138, 0.25);
    border: 1px solid rgba(255, 255, 255, 0.12);
}
.hero:after {
    content: "";
    position: absolute;
    right: -60px;
    top: -120px;
    width: 320px;
    height: 320px;
    border: 1px solid rgba(255, 255, 255, 0.14);
    border-radius: 50%;
    box-shadow: 0 0 0 40px rgba(255, 255, 255, 0.03), 0 0 0 80px rgba(255, 255, 255, 0.02);
}
.hero .eyebrow {
    display: inline-block;
    background: rgba(255, 255, 255, 0.12);
    backdrop-filter: blur(4px);
    color: #bfdbfe !important;
    text-transform: uppercase;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    padding: 0.35rem 0.8rem;
    border-radius: 99px;
    margin-bottom: 0.85rem;
}
.hero h1 {
    color: #ffffff !important;
    font-size: clamp(1.85rem, 3vw, 2.55rem) !important;
    line-height: 1.15;
    margin: 0 0 0.65rem 0;
}
.hero p { color: #dbeafe !important; font-size: 1.04rem; margin: 0; max-width: 680px; }

/* Metric Tiles */
div[data-testid="stMetric"] {
    background: var(--surface);
    border: 1px solid var(--line);
    padding: 1.2rem 1.3rem;
    border-radius: 18px;
    box-shadow: 0 4px 12px rgba(15, 23, 42, 0.03);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
div[data-testid="stMetric"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 24px rgba(15, 23, 42, 0.06);
}
div[data-testid="stMetric"] label { color: var(--muted) !important; font-weight: 600; }
div[data-testid="stMetricValue"] {
    font-family: 'Manrope', sans-serif;
    font-weight: 800;
    color: var(--ink) !important;
}

/* Interactive Subject Cards */
.card {
    height: 100%;
    padding: 1.4rem;
    border-radius: 20px;
    border: 1px solid var(--line);
    background: var(--surface);
    margin-bottom: 1rem;
    box-shadow: 0 4px 14px rgba(15, 23, 42, 0.03);
    transition: all 0.22s ease;
}
.card:hover {
    transform: translateY(-4px);
    border-color: #bfdbfe;
    box-shadow: 0 14px 28px rgba(37, 99, 235, 0.08);
}
.card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0.85rem;
}
.card-icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 48px;
    height: 48px;
    border-radius: 14px;
    background: #eff6ff;
    font-size: 1.5rem;
}
.card-badge {
    font-size: 0.76rem;
    font-weight: 700;
    padding: 0.28rem 0.65rem;
    border-radius: 99px;
    background: #f1f5f9;
    color: #334155;
}
.card h3 { color: var(--ink) !important; font-size: 1.12rem !important; margin: 0 0 0.4rem 0; }
.card p { color: var(--muted) !important; line-height: 1.55; margin: 0 0 0.9rem 0; font-size: 0.92rem; }
.progress-mini {
    width: 100%;
    height: 7px;
    background: #e2e8f0;
    border-radius: 99px;
    overflow: hidden;
}
.progress-mini-fill {
    height: 100%;
    background: linear-gradient(90deg, #2563eb, #0d9488);
    border-radius: 99px;
}

/* Reusable Panels */
.panel {
    padding: 1.35rem 1.5rem;
    border: 1px solid var(--line);
    background: var(--surface);
    border-radius: 18px;
    margin: 0.45rem 0 1rem 0;
    box-shadow: 0 4px 12px rgba(15, 23, 42, 0.025);
}
.panel h3 { margin-top: 0; }
.pill {
    display: inline-block;
    padding: 0.3rem 0.7rem;
    border-radius: 99px;
    color: #1d4ed8 !important;
    background: #dbeafe;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.03em;
}

/* Buttons & Inputs */
.stButton button, .stFormSubmitButton button, .stLinkButton a, .stDownloadButton button {
    border-radius: 11px !important;
    font-weight: 600 !important;
    min-height: 2.65rem;
    transition: all 0.18s ease !important;
}
.stButton button[kind="primary"], .stFormSubmitButton button[kind="primary"] {
    background: var(--blue) !important;
    border-color: var(--blue) !important;
    color: #fff !important;
}
.stButton button[kind="primary"]:hover, .stFormSubmitButton button[kind="primary"]:hover {
    background: var(--blue-dark) !important;
    border-color: var(--blue-dark) !important;
}
.footer {
    text-align: center;
    color: #64748b !important;
    font-size: 0.84rem;
    padding-top: 1rem;
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
        
        # Safely migrate older databases if weekly_target column doesn't exist
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


# -------------------- LEARNING CONTENT --------------------
SUBJECTS = {
    "Python Programming": {
        "icon": "🐍",
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
        "description": "Learn how feature engineering, model training, cross-validation, and evaluation metrics work together.",
        "topics": [
            "ML Fundamentals", "Data Preprocessing", "Supervised Learning", "Linear & Logistic Regression",
            "Decision Trees & Random Forests", "Train/Test Split & Cross-Validation", "Evaluation Metrics (F1, ROC-AUC)"
        ],
        "url": "https://scikit-learn.org/stable/getting_started.html",
    },
    "Data Science": {
        "icon": "📊",
        "description": "Explore datasets, handle missing values, build visualizations, and uncover actionable insights.",
        "topics": [
            "NumPy Arrays", "Pandas DataFrames", "Data Cleaning & Imputation",
            "Exploratory Data Analysis (EDA)", "Data Visualization", "Statistical Summary & Reporting"
        ],
        "url": "https://pandas.pydata.org/docs/getting_started/index.html",
    },
    "Artificial Intelligence": {
        "icon": "✨",
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


# -------------------- SIDEBAR NAVIGATION --------------------
st.sidebar.markdown("# 🎓 StudyPilot AI")
st.sidebar.caption("PERSONAL LEARNING WORKSPACE")

page = st.sidebar.radio(
    "NAVIGATION",
    ["Dashboard", "Subjects", "Quiz", "AI Mentor", "Progress", "Study Planner", "Profile"],
)

st.sidebar.divider()
st.sidebar.markdown("### 🎯 Weekly Study Target")
goal_pct = min(total_mins / max(weekly_target, 1), 1.0)
st.sidebar.progress(goal_pct, text=f"{total_mins} / {weekly_target} mins ({goal_pct*100:.0f}%)")

st.sidebar.markdown("### 📚 Curriculum Mastery")
topic_pct = completed_topics_count / max(total_topics_count, 1)
st.sidebar.progress(topic_pct, text=f"{completed_topics_count} / {total_topics_count} topics completed")

st.sidebar.divider()
st.sidebar.caption("💡 **Tip:** Consistency beats cramming. Log 25 mins today!")


# -------------------- PAGE 1: DASHBOARD --------------------
if page == "Dashboard":
    st.markdown(
        f'<div class="hero">'
        f'<div class="eyebrow">STUDENT WORKSPACE · ACTIVE</div>'
        f'<h1>Welcome back, {student_name} 👋</h1>'
        f'<p>Current Focus: <strong>{profile["goal"]}</strong> — Track your syllabus mastery, test your knowledge across 4 tracks, and log your daily focus sessions.</p>'
        f'</div>',
        unsafe_allow_html=True,
    )

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("📚 Topics Mastered", f"{completed_topics_count}/{total_topics_count}", f"{topic_pct*100:.0f}% syllabus")
    m2.metric("📝 Quizzes Completed", len(attempts_df))
    m3.metric("🎯 Average Quiz Score", f"{avg_score:.0f}%")
    m4.metric("⏱️ Total Study Time", f"{total_mins // 60}h {total_mins % 60}m", f"Goal: {weekly_target}m")

    st.markdown("## 🚀 Learning Tracks Overview")
    cols = st.columns(2, gap="medium")
    for i, (subj_name, info) in enumerate(SUBJECTS.items()):
        done_set = get_completed_topics(subj_name)
        total_t = len(info["topics"])
        done_t = len(done_set)
        pct_t = int((done_t / total_t) * 100) if total_t else 0

        with cols[i % 2]:
            st.markdown(
                f'<div class="card">'
                f'<div class="card-header">'
                f'<div class="card-icon">{info["icon"]}</div>'
                f'<span class="card-badge">{done_t}/{total_t} Topics · {pct_t}%</span>'
                f'</div>'
                f'<h3>{subj_name}</h3>'
                f'<p>{info["description"]}</p>'
                f'<div class="progress-mini"><div class="progress-mini-fill" style="width: {pct_t}%;"></div></div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    left, right = st.columns([1.25, 1], gap="medium")
    with left:
        st.markdown("### 📌 Smart Next Step")
        if attempts_df.empty:
            rec_title = "Take your first diagnostic quiz"
            rec_desc = "Head to the Quiz tab and complete a 5-7 question check to establish your baseline score."
        elif avg_score < 70:
            rec_title = "Review explanations & strengthen weak spots"
            rec_desc = f"Your average quiz score is {avg_score:.0f}%. Use the AI Mentor to review core concepts before retaking."
        else:
            rec_title = "Advance your topic checklist"
            rec_desc = f"Great quiz average ({avg_score:.0f}%)! Mark off new topics in the Subjects tab and log a 30-minute session."

        st.markdown(
            f'<div class="panel"><span class="pill">RECOMMENDED ACTION</span>'
            f'<h3 style="margin-top:0.75rem;">{rec_title}</h3>'
            f'<p style="margin-bottom:0;">{rec_desc}</p></div>',
            unsafe_allow_html=True,
        )

    with right:
        st.markdown("### 🎯 Active Learning Goal")
        st.markdown(
            f'<div class="panel"><span class="pill">CURRENT OBJECTIVE</span>'
            f'<h3 style="margin-top:0.75rem;">{profile["goal"]}</h3>'
            f'<p style="margin-bottom:0;">Weekly commitment target: <strong>{weekly_target} minutes</strong>.</p></div>',
            unsafe_allow_html=True,
        )


# -------------------- PAGE 2: SUBJECTS --------------------
elif page == "Subjects":
    st.title("📚 Learning Tracks & Syllabus")
    st.write("Select a track below to check off completed topics. Your progress is automatically saved to the database.")

    chosen = st.selectbox("Select learning track", list(SUBJECTS.keys()))
    info = SUBJECTS[chosen]
    done_topics = get_completed_topics(chosen)

    st.markdown(
        f'<div class="panel"><span class="pill">SYLLABUS TRACKER</span>'
        f'<h2 style="margin-top:0.65rem;">{info["icon"]} {chosen}</h2>'
        f'<p style="margin-bottom:0;">{info["description"]}</p></div>',
        unsafe_allow_html=True,
    )

    st.markdown("### ✅ Persistent Topic Checklist")
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
    st.title("📝 Multi-Track Knowledge Check")
    st.write("Test your understanding across any learning track and get instant explanations.")

    quiz_subject = st.selectbox("Choose Quiz Track", list(QUIZ_BANK.keys()))
    questions = QUIZ_BANK[quiz_subject]

    st.markdown(
        f'<div class="panel"><span class="pill">{len(questions)} QUESTIONS · {quiz_subject.upper()}</span> &nbsp; '
        f'Select an answer for each question and submit to record your attempt.</div>',
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

        submitted = st.form_submit_button("Submit Quiz Answers", type="primary", use_container_width=True)

    if submitted:
        unanswered = sum(1 for a in answers if a is None)
        if unanswered > 0:
            st.warning(f"You left {unanswered} question(s) blank. Unanswered questions are marked incorrect.")

        score = sum(answers[i] == item["answer"] for i, item in enumerate(questions))
        pct = score * 100 / len(questions)
        save_quiz(student_name, quiz_subject, score, len(questions))

        st.success(f"Quiz graded and saved to your **{quiz_subject}** history!")
        c1, c2, c3 = st.columns(3)
        c1.metric("Score", f"{score} / {len(questions)}")
        c2.metric("Percentage", f"{pct:.0f}%")
        c3.metric("Performance Rating", "🌟 Mastery" if pct >= 80 else "👍 Solid" if pct >= 60 else "📖 Needs Review")

        with st.expander("🔍 Detailed Answer Breakdown", expanded=True):
            for i, item in enumerate(questions):
                is_correct = answers[i] == item["answer"]
                icon = "✅" if is_correct else "❌"
                st.markdown(f"**{icon} Q{i + 1}. {item['q']}**")
                st.write(f"Your answer: `{answers[i] or 'Not answered'}` | Correct answer: `{item['answer']}`")
                st.caption(f"💡 **Explanation:** {item['why']}")
                st.divider()


# -------------------- PAGE 4: AI MENTOR --------------------
elif page == "AI Mentor":
    st.title("🤖 Interactive AI Study Mentor")
    st.write("Click a quick-topic pill below or type a question in the chat box for instant code examples and study advice.")

    if "mentor_messages" not in st.session_state:
        st.session_state.mentor_messages = [
            {
                "role": "assistant",
                "content": f"Hi **{student_name}**! 👋 Ask me about **Python lists, dictionaries, loops, functions, Pandas, Machine Learning workflows**, or **study habits**."
            }
        ]

    selected_pill = st.pills(
        "Quick Concept Lookup:",
        list(MENTOR_KB.keys()),
        selection_mode="single",
    )

    for msg in st.session_state.mentor_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_prompt = st.chat_input("Ask a question (e.g., How do dictionaries work in Python?)...")

    active_query = None
    if user_prompt:
        active_query = user_prompt
    elif selected_pill and st.session_state.get("last_pill") != selected_pill:
        st.session_state.last_pill = selected_pill
        active_query = selected_pill

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
                "I'm running in **Offline Starter Mode**, so I specialize in core curriculum topics. "
                "Try asking about: **Python Lists, Dictionaries, Loops, Functions, Pandas, Machine Learning**, or **Study Strategy**!"
            )

        st.session_state.mentor_messages.append({"role": "assistant", "content": matched_reply})
        st.rerun()


# -------------------- PAGE 5: PROGRESS --------------------
elif page == "Progress":
    st.title("📈 Analytics & Progress")
    st.write("Visual breakdown of your quiz scores, study time distribution, and downloadable logs.")

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Quiz Attempts", len(attempts_df))
    c2.metric("Logged Study Sessions", len(logs_df))
    c3.metric("Cumulative Study Time", f"{total_mins} mins")

    col_left, col_right = st.columns(2, gap="medium")

    with col_left:
        st.markdown("### 🎯 Quiz Score Trend (%)")
        if not attempts_df.empty:
            chart_df = attempts_df.iloc[::-1].copy()
            chart_df["Attempt"] = range(1, len(chart_df) + 1)
            st.line_chart(chart_df.set_index("Attempt")["percentage"])
        else:
            st.info("Take a quiz in the Quiz tab to unlock your score trend chart.")

    with col_right:
        st.markdown("### ⏱️ Minutes Studied by Subject")
        if not logs_df.empty:
            subj_totals = logs_df.groupby("subject")["minutes"].sum()
            st.bar_chart(subj_totals)
        else:
            st.info("Log a study session in Study Planner to view subject breakdown.")

    if not attempts_df.empty:
        st.markdown("### 📋 Quiz History")
        st.dataframe(
            attempts_df[["quiz_name", "score", "total", "percentage", "attempted_at"]],
            use_container_width=True,
            hide_index=True,
        )

    if not logs_df.empty:
        st.markdown("### 🗂️ Study Session Logs")
        st.dataframe(
            logs_df[["subject", "minutes", "note", "logged_at"]],
            use_container_width=True,
            hide_index=True,
        )
        csv_data = logs_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Export Study Logs as CSV",
            data=csv_data,
            file_name="studypilot_logs.csv",
            mime="text/csv",
        )


# -------------------- PAGE 6: STUDY PLANNER --------------------
elif page == "Study Planner":
    st.title("🗓️ Study Session Logger")
    st.write("Log your focused study blocks to track your weekly target and build momentum.")

    col_form, col_timer = st.columns([1.4, 1], gap="medium")

    with col_form:
        with st.form("study_form"):
            subject = st.selectbox("Subject Track", list(SUBJECTS.keys()))
            minutes = st.number_input("Duration (minutes)", min_value=5, max_value=480, value=30, step=5)
            note = st.text_area("What did you work on?", placeholder="e.g., Completed 5 Python dictionary exercises and reviewed list slicing.")
            save = st.form_submit_button("Log Study Session", type="primary", use_container_width=True)

        if save:
            save_study(subject, int(minutes), note)
            st.success("Session recorded! Your weekly progress bar has been updated.")
            st.rerun()

    with col_timer:
        st.markdown(
            '<div class="panel"><span class="pill">FOCUS FRAMEWORK</span>'
            '<h3 style="margin-top:0.75rem;">The 25-5 Rule</h3>'
            '<p>1. Pick <strong>one single topic</strong> from the Subjects tab.<br>'
            '2. Set a timer for <strong>25 minutes</strong> and close all social tabs.<br>'
            '3. Write code or summary notes from memory.<br>'
            '4. Take a <strong>5-minute break</strong> and log your session here.</p></div>',
            unsafe_allow_html=True,
        )

    if not logs_df.empty:
        st.markdown("### 🕒 Recent Study Logs")
        st.dataframe(
            logs_df[["subject", "minutes", "note", "logged_at"]].head(8),
            use_container_width=True,
            hide_index=True,
        )


# -------------------- PAGE 7: PROFILE --------------------
elif page == "Profile":
    st.title("👤 Student Profile & Settings")
    st.write("Customize your workspace identity, learning objective, and weekly target.")

    with st.form("profile_form"):
        name = st.text_input("Student Name", value=profile["name"])
        goal = st.text_area("Primary Learning Goal", value=profile["goal"])
        target = st.slider("Weekly Study Goal (minutes)", min_value=30, max_value=1200, value=weekly_target, step=30)
        save = st.form_submit_button("Save Profile Settings", type="primary", use_container_width=True)

    if save:
        save_profile(name, goal, target)
        st.success("Profile updated!")
        st.rerun()

    st.markdown("### ⚙️ Workspace Data Management")
    with st.expander("Danger Zone: Reset Workspace Records"):
        st.warning("This will permanently clear all quiz attempts, study logs, and checked syllabus topics.")
        if st.button("🗑️ Clear All Progress Data"):
            reset_all_data()
            st.success("All history cleared.")
            st.rerun()

st.divider()
st.markdown(
    '<div class="footer">StudyPilot AI · Built with Streamlit & SQLite · Keep learning, one focused session at a time.</div>',
    unsafe_allow_html=True,
)
