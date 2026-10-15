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

# -------------------- DESIGN SYSTEM --------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

:root {
    --navy: #142747;
    --navy-deep: #0c1b33;
    --blue: #356df3;
    --blue-dark: #2455d6;
    --teal: #16b8a6;
    --ink: #17243b;
    --muted: #63718a;
    --line: #e1e8f3;
    --surface: #ffffff;
    --canvas: #f4f7fc;
}
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}
.stApp {
    background:
        radial-gradient(circle at 85% 0%, rgba(53,109,243,.09), transparent 26rem),
        var(--canvas);
    color: var(--ink);
}
[data-testid="stHeader"] { background: rgba(244,247,252,.92); }
.block-container {
    max-width: 1440px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}
h1, h2, h3, h4 {
    font-family: 'Manrope', sans-serif !important;
    color: var(--ink) !important;
    letter-spacing: -.025em;
}
h1 { font-weight: 800 !important; }
h2, h3 { font-weight: 750 !important; }
p, li, label, .stMarkdown, [data-testid="stCaptionContainer"] {
    color: #334155;
}
[data-testid="stCaptionContainer"] p { color: var(--muted) !important; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--navy-deep), var(--navy));
    border-right: 1px solid rgba(255,255,255,.08);
}
[data-testid="stSidebar"] > div:first-child { padding-top: 1.4rem; }
[data-testid="stSidebar"] * { color: #edf4ff; }
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p { color: #b7c5dd !important; }
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,.16); }
[data-testid="stSidebar"] [role="radiogroup"] label {
    padding: .55rem .65rem;
    border-radius: 10px;
    margin-bottom: .12rem;
}
[data-testid="stSidebar"] [role="radiogroup"] label:hover {
    background: rgba(255,255,255,.09);
}

/* Hero */
.hero {
    position: relative;
    overflow: hidden;
    padding: 2.1rem 2.25rem;
    border-radius: 24px;
    color: #fff !important;
    background: linear-gradient(118deg, #142747 0%, #214b9c 54%, #356df3 100%);
    margin-bottom: 1.4rem;
    box-shadow: 0 16px 38px rgba(34, 78, 160, .17);
}
.hero:after {
    content: "";
    position: absolute;
    right: -55px;
    top: -115px;
    width: 300px;
    height: 300px;
    border: 1px solid rgba(255,255,255,.16);
    border-radius: 50%;
    box-shadow: 0 0 0 35px rgba(255,255,255,.035), 0 0 0 75px rgba(255,255,255,.025);
}
.hero .eyebrow {
    color: #c6dcff !important;
    text-transform: uppercase;
    font-size: .75rem;
    font-weight: 700;
    letter-spacing: .13em;
    margin-bottom: .65rem;
}
.hero h1 {
    color: #fff !important;
    font-size: clamp(1.8rem, 3vw, 2.65rem) !important;
    line-height: 1.18;
    margin: 0 0 .7rem 0;
}
.hero p { color: #e7efff !important; font-size: 1.03rem; margin: 0; }

/* Metric tiles */
div[data-testid="stMetric"] {
    background: var(--surface);
    border: 1px solid var(--line);
    padding: 1.1rem 1.15rem;
    border-radius: 18px;
    box-shadow: 0 5px 18px rgba(22, 43, 79, .045);
    min-height: 118px;
}
div[data-testid="stMetric"] label,
div[data-testid="stMetric"] label *,
div[data-testid="stMetricValue"],
div[data-testid="stMetricValue"] *,
div[data-testid="stMetricDelta"],
div[data-testid="stMetricDelta"] * {
    color: var(--ink) !important;
}
div[data-testid="stMetric"] label { font-weight: 600; }
div[data-testid="stMetricValue"] { font-family: 'Manrope', sans-serif; font-weight: 800; }

/* Subject cards */
.card {
    height: 100%;
    min-height: 155px;
    padding: 1.35rem;
    border-radius: 18px;
    border: 1px solid var(--line);
    background: #fff;
    margin-bottom: .8rem;
    box-shadow: 0 5px 18px rgba(22,43,79,.04);
}
.card .card-icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 44px;
    height: 44px;
    border-radius: 13px;
    background: #edf3ff;
    font-size: 1.45rem;
    margin-bottom: .75rem;
}
.card h3 { color: #1b3768 !important; font-size: 1.08rem !important; margin: 0 0 .45rem 0; }
.card p { color: #596981 !important; line-height: 1.55; margin: 0; font-size: .93rem; }

/* Small reusable panels */
.panel {
    padding: 1.2rem 1.35rem;
    border: 1px solid var(--line);
    background: #fff;
    border-radius: 17px;
    margin: .45rem 0 .9rem 0;
}
.panel h3 { margin-top: 0; }
.pill {
    display: inline-block;
    padding: .32rem .65rem;
    border-radius: 99px;
    color: #2455b8 !important;
    background: #eaf1ff;
    font-size: .78rem;
    font-weight: 700;
}
div[data-testid="stAlert"] { border-radius: 14px; }
.stButton button, .stFormSubmitButton button, .stLinkButton a {
    border-radius: 11px !important;
    font-weight: 700 !important;
    min-height: 2.65rem;
}
.stButton button[kind="primary"], .stFormSubmitButton button[kind="primary"] {
    background: var(--blue) !important;
    border-color: var(--blue) !important;
}
.stButton button[kind="primary"]:hover, .stFormSubmitButton button[kind="primary"]:hover {
    background: var(--blue-dark) !important;
    border-color: var(--blue-dark) !important;
}
.stTextInput input, .stTextArea textarea, .stNumberInput input {
    border-radius: 10px !important;
    color: var(--ink) !important;
    background: #fff !important;
}
[data-baseweb="select"] > div {
    background: #fff;
    border-radius: 10px;
}
[data-testid="stDataFrame"], [data-testid="stTable"] {
    border: 1px solid var(--line);
    border-radius: 12px;
    overflow: hidden;
}
hr { border-color: var(--line); }
.footer {
    text-align: center;
    color: #7b879a !important;
    font-size: .82rem;
    padding-top: .8rem;
}
@media (max-width: 800px) {
    .block-container { padding: 1rem 1rem 2rem 1rem; }
    .hero { padding: 1.5rem; border-radius: 18px; }
    div[data-testid="stMetric"] { padding: .8rem; min-height: 100px; }
}
</style>
""", unsafe_allow_html=True)


# -------------------- DATABASE --------------------
def connect():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_db():
    with connect() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS profile (
            id INTEGER PRIMARY KEY CHECK(id=1),
            name TEXT NOT NULL DEFAULT 'Student',
            goal TEXT NOT NULL DEFAULT 'Build strong programming skills')""")
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
        conn.execute("""INSERT OR IGNORE INTO profile(id,name,goal)
            VALUES(1,'Student','Build strong programming skills')""")


def get_profile():
    with connect() as conn:
        return conn.execute("SELECT * FROM profile WHERE id=1").fetchone()


def save_profile(name, goal):
    with connect() as conn:
        conn.execute(
            "UPDATE profile SET name=?, goal=? WHERE id=1",
            (name.strip() or "Student", goal.strip() or "Build strong programming skills"),
        )


def save_quiz(name, score, total):
    with connect() as conn:
        conn.execute(
            """INSERT INTO quiz_attempts
            (student_name,quiz_name,score,total,percentage,attempted_at)
            VALUES(?,?,?,?,?,?)""",
            (name, "Python Programming", score, total, score * 100 / total,
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
            "INSERT INTO study_logs(subject,minutes,note,logged_at) VALUES(?,?,?,?)",
            (subject, minutes, note.strip(),
             datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        )


initialize_db()
profile = get_profile()
student_name = profile["name"]


# -------------------- LEARNING CONTENT --------------------
SUBJECTS = {
    "Python Programming": {
        "icon": "🐍",
        "description": "Build a strong foundation in Python, from variables and operators to functions and collections.",
        "topics": ["Variables and data types", "Input and output", "Operators", "Conditions", "Loops",
                   "Functions", "Strings", "Lists", "Tuples", "Sets", "Dictionaries", "OOP basics"],
        "url": "https://docs.python.org/3/tutorial/",
    },
    "Machine Learning": {
        "icon": "🧠",
        "description": "Learn how data, features, model training and evaluation work together.",
        "topics": ["ML fundamentals", "Data preparation", "Supervised learning", "Classification",
                   "Regression", "Train/test split", "Model evaluation"],
        "url": "https://scikit-learn.org/stable/getting_started.html",
    },
    "Data Science": {
        "icon": "📊",
        "description": "Explore datasets, data cleaning, visualisation and useful insights.",
        "topics": ["Pandas basics", "Data cleaning", "Exploratory analysis", "Charts", "Reporting"],
        "url": "https://pandas.pydata.org/docs/getting_started/index.html",
    },
    "Artificial Intelligence": {
        "icon": "✨",
        "description": "Understand AI concepts, generative AI, prompt design and responsible use.",
        "topics": ["AI fundamentals", "Generative AI", "Prompt writing", "Limitations", "Responsible AI"],
        "url": "https://ai.google/education/",
    },
}

QUESTIONS = [
    {"q": "Which keyword defines a function in Python?", "options": ["func", "def", "function", "define"], "answer": "def", "why": "Python uses def to define a function."},
    {"q": "Which type represents True or False?", "options": ["int", "str", "bool", "list"], "answer": "bool", "why": "bool has two values: True and False."},
    {"q": "Which symbol starts a single-line comment?", "options": ["//", "#", "/*", "&"], "answer": "#", "why": "Python comments start with #."},
    {"q": "What is 2 ** 3?", "options": ["5", "6", "8", "9"], "answer": "8", "why": "** is exponentiation: 2 to the power 3 is 8."},
    {"q": "Which collection stores key-value pairs?", "options": ["List", "Tuple", "Set", "Dictionary"], "answer": "Dictionary", "why": "A dictionary stores key-value pairs."},
    {"q": "Which list method adds an item at the end?", "options": ["add()", "append()", "push()", "insert_end()"], "answer": "append()", "why": "append(value) adds one item to the end of a list."},
    {"q": "What does len('AI') return?", "options": ["1", "2", "3", "AI"], "answer": "2", "why": "The string AI has two characters."},
    {"q": "Which loop iterates over items in a sequence?", "options": ["repeat", "foreach", "for", "iterate"], "answer": "for", "why": "A for loop iterates over an iterable."},
    {"q": "Which value is falsy in Python?", "options": ["'hello'", "[1]", "1", "''"], "answer": "''", "why": "An empty string is falsy."},
    {"q": "Which construct handles exceptions?", "options": ["if/else", "try/except", "for/in", "def/return"], "answer": "try/except", "why": "try/except lets you handle exceptions."},
]


# -------------------- NAVIGATION --------------------
st.sidebar.markdown("# 🎓 StudyPilot AI")
st.sidebar.caption("YOUR PERSONAL LEARNING WORKSPACE")
page = st.sidebar.radio(
    "NAVIGATION",
    ["Dashboard", "Subjects", "Quiz", "AI Mentor", "Progress", "Study Planner", "Profile"],
)
st.sidebar.divider()
st.sidebar.markdown("### 💡 Daily reminder")
st.sidebar.write("Small daily practice beats last-minute cramming.")
st.sidebar.divider()
st.sidebar.caption("StudyPilot AI · Learning MVP")

# -------------------- DASHBOARD --------------------
if page == "Dashboard":
    attempts, logs = get_df("quiz_attempts"), get_df("study_logs")
    avg = float(attempts["percentage"].mean()) if not attempts.empty else 0
    mins = int(logs["minutes"].sum()) if not logs.empty else 0
    st.markdown(
        f'<div class="hero"><div class="eyebrow">YOUR LEARNING SPACE</div>'
        f'<h1>Welcome back, {student_name} 👋</h1>'
        '<p>Build your skills one focused session at a time. Learn smarter, practice better, grow every day.</p></div>',
        unsafe_allow_html=True,
    )
    a, b, c, d = st.columns(4)
    a.metric("📚 Learning tracks", len(SUBJECTS))
    b.metric("📝 Quiz attempts", len(attempts))
    c.metric("🎯 Average score", f"{avg:.0f}%")
    d.metric("⏱️ Total study time", f"{mins // 60}h {mins % 60}m")

    st.markdown("## 🚀 Pick up where you left off")
    cols = st.columns(2, gap="medium")
    for i, (name, info) in enumerate(SUBJECTS.items()):
        with cols[i % 2]:
            st.markdown(
                f'<div class="card"><div class="card-icon">{info["icon"]}</div>'
                f'<h3>{name}</h3><p>{info["description"]}</p></div>',
                unsafe_allow_html=True,
            )
    left, right = st.columns([1.2, 1], gap="medium")
    with left:
        st.markdown("### 📌 Recommended next step")
        st.markdown(
            '<div class="panel"><span class="pill">SUGGESTED</span>'
            '<h3 style="margin-top: .8rem;">Practice Python fundamentals</h3>'
            '<p>Take a short quiz, review the explanations and log your next study session.</p></div>',
            unsafe_allow_html=True,
        )
    with right:
        st.markdown("### 🎯 Your current goal")
        st.markdown(
            f'<div class="panel"><p style="margin-bottom:.4rem;color:#63718a;">LEARNING GOAL</p>'
            f'<h3>{profile["goal"]}</h3><p>Update your goal anytime from Profile.</p></div>',
            unsafe_allow_html=True,
        )
    if not attempts.empty:
        st.markdown("### 🕘 Recent quiz activity")
        st.dataframe(attempts[["quiz_name", "score", "total", "percentage", "attempted_at"]].head(5),
                     use_container_width=True, hide_index=True)

# -------------------- SUBJECTS --------------------
elif page == "Subjects":
    st.title("📚 Learning tracks")
    st.write("Choose a track, review its topics and continue with an official learning resource.")
    chosen = st.selectbox("Choose your subject", list(SUBJECTS))
    info = SUBJECTS[chosen]
    st.markdown(
        f'<div class="panel"><span class="pill">LEARNING TRACK</span>'
        f'<h2 style="margin-top:.7rem;">{info["icon"]} {chosen}</h2>'
        f'<p>{info["description"]}</p></div>',
        unsafe_allow_html=True,
    )
    st.markdown("### Your topic checklist")
    checked = 0
    topic_cols = st.columns(2)
    for i, topic in enumerate(info["topics"]):
        with topic_cols[i % 2]:
            if st.checkbox(topic, key=f"topic_{chosen}_{topic}"):
                checked += 1
    st.progress(checked / len(info["topics"]), text=f"{checked} of {len(info['topics'])} topics checked")
    st.link_button("Open official learning resource ↗", info["url"], use_container_width=False)
    st.caption("Topic checklist selections are temporary and reset when the app session resets.")

# -------------------- QUIZ --------------------
elif page == "Quiz":
    st.title("📝 Python knowledge check")
    st.write("Ten quick questions to check your Python fundamentals.")
    st.markdown('<div class="panel"><span class="pill">10 QUESTIONS</span> &nbsp; Select one answer for each question, then submit to review your score.</div>',
                unsafe_allow_html=True)
    with st.form("quiz_form"):
        answers = []
        for i, item in enumerate(QUESTIONS):
            st.markdown(f"**Question {i + 1} of {len(QUESTIONS)}**")
            st.write(item["q"])
            answers.append(st.radio("Choose an answer", item["options"], index=None,
                                    key=f"answer_{i}", horizontal=True, label_visibility="collapsed"))
            st.divider()
        submitted = st.form_submit_button("Submit quiz", type="primary", use_container_width=True)
    if submitted:
        score = sum(answers[i] == item["answer"] for i, item in enumerate(QUESTIONS))
        pct = score * 100 / len(QUESTIONS)
        save_quiz(student_name, score, len(QUESTIONS))
        st.success("Quiz submitted. Your result has been saved in the app database.")
        x, y, z = st.columns(3)
        x.metric("Correct answers", f"{score}/{len(QUESTIONS)}")
        y.metric("Your score", f"{pct:.0f}%")
        z.metric("Feedback", "Excellent" if pct >= 80 else "Good progress" if pct >= 60 else "Keep practicing")
        st.progress(pct / 100, text=f"{pct:.0f}% complete")
        with st.expander("Review answers and explanations", expanded=True):
            for i, item in enumerate(QUESTIONS):
                st.markdown(f'**{i + 1}. {item["q"]}**')
                st.write(f"Your answer: {answers[i] or 'Not answered'}")
                st.write(f'Correct answer: {item["answer"]}')
                st.caption(item["why"])
                st.write("✅ Correct" if answers[i] == item["answer"] else "❌ Review this topic")
                st.divider()

# -------------------- AI MENTOR --------------------
elif page == "AI Mentor":
    st.title("🤖 AI Mentor")
    st.write("Get quick explanations for supported beginner topics.")
    st.info("This starter version uses a built-in FAQ. It is not connected to a live generative AI model.")
    question = st.text_input("What would you like help with?", placeholder="e.g. What is a Python list?")
    if st.button("Get explanation", type="primary"):
        q = question.lower().strip()
        faq = [
            (["list"], "A **Python list** is an ordered, mutable collection. Example: `numbers = [1, 2, 3]`. Use `append()` to add an item."),
            (["tuple"], "A **tuple** is ordered and cannot be changed after creation. Example: `point = (3, 5)`."),
            (["dictionary", "dict", "key-value"], "A **dictionary** stores key-value pairs. Example: `student = {'name': 'Asha'}`. Access the value using `student['name']`."),
            (["set"], "A **set** stores unique values. Example: `unique = {1, 2, 3}`. Duplicate values are removed."),
            (["loop", "for loop", "while loop"], "A **for loop** iterates over an iterable. A **while loop** repeats while its condition is true."),
            (["function", "def"], "A **function** is reusable code. Define one using `def greet():` and indent its body."),
            (["machine learning", " ml"], "**Machine learning** finds patterns in data. Typical steps: prepare data, split train/test, train a model, then evaluate it."),
            (["variable"], "A **variable** is a name referring to a value. Example: `score = 85`."),
            (["condition", "if statement"], "An **if statement** runs code when a condition is true. Use `elif` for another condition and `else` as a fallback."),
            (["study", "focus", "plan"], "Try 25 minutes of focused study, a 5-minute break, then practice questions. Review your mistakes."),
            (["string"], "A **string** is text in Python, written inside quotes. Example: `name = 'Riya'`."),
            (["operator"], "Python operators perform actions on values. Examples include `+`, `-`, `*`, `/`, `//`, `%`, `**`, `and`, `or`, and `not`."),
        ]
        found = next((ans for keys, ans in faq if any(k in q for k in keys)), None)
        if not q:
            st.warning("Please enter a question first.")
        elif found:
            st.markdown(f'<div class="panel">{found}</div>', unsafe_allow_html=False)
        else:
            st.info("Try asking about Python strings, lists, tuples, dictionaries, sets, loops, functions, variables, operators, conditions, machine learning or study planning.")

# -------------------- PROGRESS --------------------
elif page == "Progress":
    st.title("📈 Your progress")
    st.write("Review quiz results and study sessions recorded in this app.")
    attempts, logs = get_df("quiz_attempts"), get_df("study_logs")
    mins = int(logs["minutes"].sum()) if not logs.empty else 0
    a, b, c = st.columns(3)
    a.metric("Quiz attempts", len(attempts))
    b.metric("Study sessions", len(logs))
    c.metric("Total study time", f"{mins} min")
    if not attempts.empty:
        st.markdown("### Quiz score history")
        chart_data = attempts.iloc[::-1].copy()
        chart_data["attempted_at"] = pd.to_datetime(chart_data["attempted_at"])
        st.line_chart(chart_data.set_index("attempted_at")["percentage"])
        st.dataframe(attempts[["quiz_name", "score", "total", "percentage", "attempted_at"]],
                     use_container_width=True, hide_index=True)
    else:
        st.info("Complete the Python quiz to see your score history.")
    if not logs.empty:
        st.markdown("### Study time by subject")
        st.bar_chart(logs.groupby("subject")["minutes"].sum())
        st.dataframe(logs[["subject", "minutes", "note", "logged_at"]],
                     use_container_width=True, hide_index=True)
    else:
        st.info("Add a session in Study Planner to track your study time.")

# -------------------- STUDY PLANNER --------------------
elif page == "Study Planner":
    st.title("🗓️ Study planner")
    st.write("Record a learning session to build a consistent study habit.")
    with st.form("study_form"):
        subject = st.selectbox("Subject", list(SUBJECTS))
        minutes = st.number_input("Study duration (minutes)", min_value=1, max_value=1440, value=30, step=5)
        note = st.text_area("Session notes", placeholder="Example: Practised Python loops and range().")
        save = st.form_submit_button("Save study session", type="primary", use_container_width=True)
    if save:
        save_study(subject, int(minutes), note)
        st.success("Study session saved.")
        st.rerun()
    logs = get_df("study_logs")
    if not logs.empty:
        st.markdown("### Recent sessions")
        st.dataframe(logs[["subject", "minutes", "note", "logged_at"]].head(10),
                     use_container_width=True, hide_index=True)

# -------------------- PROFILE --------------------
elif page == "Profile":
    st.title("👤 Student profile")
    st.write("Personalise your learning workspace.")
    current = get_profile()
    with st.form("profile_form"):
        name = st.text_input("Your name", value=current["name"])
        goal = st.text_area("Your learning goal", value=current["goal"])
        save = st.form_submit_button("Save profile", type="primary", use_container_width=True)
    if save:
        save_profile(name, goal)
        st.success("Profile updated.")
        st.rerun()
    st.markdown('<div class="panel"><h3>Privacy note</h3><p>This app stores profile, quiz and study-session data in a local SQLite file. On hosted Streamlit deployments, local file persistence may not be guaranteed across restarts.</p></div>',
                unsafe_allow_html=True)

st.divider()
st.markdown('<div class="footer">StudyPilot AI · Student Learning Support · Keep learning, one step at a time.</div>',
            unsafe_allow_html=True)
