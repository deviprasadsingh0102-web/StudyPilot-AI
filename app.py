import sqlite3
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st

DB_PATH = Path(__file__).resolve().parent / "studypilot.db"

st.set_page_config(page_title="StudyPilot AI", page_icon="🎓", layout="wide")

st.markdown("""
<style>
.stApp { background: linear-gradient(135deg,#eef2ff,#f8fafc); }
[data-testid="stSidebar"] { background:#102448; }
[data-testid="stSidebar"] * { color:white; }
.block-container { padding-top:1.8rem; }
.hero { padding:1.6rem; border-radius:18px; color:white;
background:linear-gradient(115deg,#102448,#2563eb); margin-bottom:1rem; }
.hero h1 { color:white !important; }
div[data-testid="stMetric"] { background:white; border:1px solid #dbeafe;
padding:14px; border-radius:13px; }
.card { background:white; padding:1rem; border-radius:14px;
border:1px solid #dbeafe; margin-bottom:.6rem; }
</style>
""", unsafe_allow_html=True)

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
            id INTEGER PRIMARY KEY AUTOINCREMENT, student_name TEXT NOT NULL,
            quiz_name TEXT NOT NULL, score INTEGER NOT NULL, total INTEGER NOT NULL,
            percentage REAL NOT NULL, attempted_at TEXT NOT NULL)""")
        conn.execute("""CREATE TABLE IF NOT EXISTS study_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT, subject TEXT NOT NULL,
            minutes INTEGER NOT NULL, note TEXT DEFAULT '', logged_at TEXT NOT NULL)""")
        conn.execute("INSERT OR IGNORE INTO profile(id,name,goal) VALUES(1,'Student','Build strong programming skills')")

def get_profile():
    with connect() as conn:
        return conn.execute("SELECT * FROM profile WHERE id=1").fetchone()

def save_profile(name, goal):
    with connect() as conn:
        conn.execute("UPDATE profile SET name=?,goal=? WHERE id=1",
                     (name.strip() or "Student", goal.strip() or "Build strong programming skills"))

def save_quiz(name, score, total):
    with connect() as conn:
        conn.execute("INSERT INTO quiz_attempts(student_name,quiz_name,score,total,percentage,attempted_at) VALUES(?,?,?,?,?,?)",
                     (name, "Python Programming", score, total, score * 100 / total,
                      datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

def get_df(table):
    allowed = {"quiz_attempts", "study_logs"}
    if table not in allowed:
        return pd.DataFrame()
    with connect() as conn:
        rows = conn.execute(f"SELECT * FROM {table} ORDER BY id DESC").fetchall()
    return pd.DataFrame([dict(row) for row in rows])

def save_study(subject, minutes, note):
    with connect() as conn:
        conn.execute("INSERT INTO study_logs(subject,minutes,note,logged_at) VALUES(?,?,?,?)",
                     (subject, minutes, note.strip(), datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

initialize_db()
profile = get_profile()
student_name = profile["name"]

SUBJECTS = {
    "Python Programming": {
        "icon": "🐍",
        "description": "Learn variables, data types, operators, conditions, loops, functions and collections.",
        "topics": ["Variables and data types", "Operators", "Conditions", "Loops", "Functions", "Lists, tuples, sets and dictionaries"],
        "url": "https://docs.python.org/3/tutorial/"
    },
    "Machine Learning": {
        "icon": "🧠",
        "description": "Understand data, features, labels, model training, testing and evaluation.",
        "topics": ["ML fundamentals", "Data preparation", "Supervised learning", "Classification", "Model evaluation"],
        "url": "https://scikit-learn.org/stable/getting_started.html"
    },
    "Data Science": {
        "icon": "📊",
        "description": "Work with datasets, tables, charts and simple analysis.",
        "topics": ["Pandas basics", "Cleaning data", "Exploratory analysis", "Charts", "Reporting"],
        "url": "https://pandas.pydata.org/docs/getting_started/index.html"
    },
    "Artificial Intelligence": {
        "icon": "✨",
        "description": "Explore AI concepts, applications, prompt design and responsible use.",
        "topics": ["AI fundamentals", "Generative AI", "Prompt writing", "Limitations", "Responsible AI"],
        "url": "https://ai.google/education/"
    }
}

QUESTIONS = [
    {"q":"Which keyword defines a function in Python?","options":["func","def","function","define"],"answer":"def","why":"Python uses def to define a function."},
    {"q":"Which type represents True or False?","options":["int","str","bool","list"],"answer":"bool","why":"bool has two values: True and False."},
    {"q":"Which symbol starts a single-line comment?","options":["//","#","/*","&"],"answer":"#","why":"Python comments start with #."},
    {"q":"What is 2 ** 3?","options":["5","6","8","9"],"answer":"8","why":"** is exponentiation: 2 to the power 3 is 8."},
    {"q":"Which collection stores key-value pairs?","options":["List","Tuple","Set","Dictionary"],"answer":"Dictionary","why":"A dictionary stores key-value pairs."},
    {"q":"Which list method adds an item at the end?","options":["add()","append()","push()","insert_end()"],"answer":"append()","why":"append(value) adds one item to the end of a list."},
    {"q":"What does len('AI') return?","options":["1","2","3","AI"],"answer":"2","why":"The string AI has two characters."},
    {"q":"Which loop iterates over items in a sequence?","options":["repeat","foreach","for","iterate"],"answer":"for","why":"A for loop iterates over an iterable."},
    {"q":"Which value is falsy in Python?","options":["'hello'","[1]","1","''"],"answer":"''","why":"An empty string is falsy."},
    {"q":"Which construct handles exceptions?","options":["if/else","try/except","for/in","def/return"],"answer":"try/except","why":"try/except lets you handle exceptions."}
]

st.sidebar.markdown("## 🎓 StudyPilot AI")
st.sidebar.caption("Your personal learning companion")
page = st.sidebar.radio("MAIN MENU", ["Dashboard","Subjects","Quiz","AI Mentor","Progress","Study Planner","Profile"])
st.sidebar.divider()
st.sidebar.write("💡 Small daily practice beats last-minute cramming.")
st.sidebar.caption("StudyPilot AI • Local MVP")

if page == "Dashboard":
    attempts, logs = get_df("quiz_attempts"), get_df("study_logs")
    avg = float(attempts["percentage"].mean()) if not attempts.empty else 0
    mins = int(logs["minutes"].sum()) if not logs.empty else 0
    st.markdown(f'<div class="hero"><h1>Welcome back, {student_name} 👋</h1><p>Your learning journey, one step at a time. Learn smarter, practice better, achieve more.</p></div>', unsafe_allow_html=True)
    a,b,c,d = st.columns(4)
    a.metric("📚 Subjects", len(SUBJECTS))
    b.metric("📝 Quiz attempts", len(attempts))
    c.metric("🎯 Average score", f"{avg:.0f}%")
    d.metric("⏱️ Study time", f"{mins//60}h {mins%60}m")
    st.subheader("🚀 Continue learning")
    cols = st.columns(2)
    for i,(name, info) in enumerate(SUBJECTS.items()):
        with cols[i%2]:
            st.markdown(f'<div class="card"><h3>{info["icon"]} {name}</h3><p>{info["description"]}</p></div>', unsafe_allow_html=True)
    st.subheader("📌 Recommended next step")
    st.info("Take the Python quiz, review the explanations, and record a study session.")
    if not attempts.empty:
        st.subheader("Recent quiz activity")
        st.dataframe(attempts[["quiz_name","score","total","percentage","attempted_at"]].head(5), use_container_width=True, hide_index=True)

elif page == "Subjects":
    st.title("📚 Learning Subjects")
    chosen = st.selectbox("Select a subject", list(SUBJECTS))
    info = SUBJECTS[chosen]
    st.subheader(f'{info["icon"]} {chosen}')
    st.write(info["description"])
    st.markdown("### Topics to cover")
    for topic in info["topics"]:
        st.checkbox(topic, key=f"topic_{chosen}_{topic}")
    st.link_button("Open official learning resource ↗", info["url"])
    st.caption("Topic checkboxes are session-only in this version.")

elif page == "Quiz":
    st.title("📝 Python Programming Quiz")
    st.write("Answer all questions and submit to see your score.")
    with st.form("quiz_form"):
        answers = []
        for i,item in enumerate(QUESTIONS):
            st.markdown(f"**Question {i+1} of {len(QUESTIONS)}**")
            st.write(item["q"])
            answers.append(st.radio("Choose an answer", item["options"], index=None, key=f"answer_{i}", horizontal=True))
            st.divider()
        submitted = st.form_submit_button("Submit quiz", type="primary", use_container_width=True)
    if submitted:
        score = sum(answers[i] == item["answer"] for i,item in enumerate(QUESTIONS))
        pct = score * 100 / len(QUESTIONS)
        save_quiz(student_name, score, len(QUESTIONS))
        st.success("Your result has been saved on this computer.")
        x,y,z = st.columns(3)
        x.metric("Correct answers", f"{score}/{len(QUESTIONS)}")
        y.metric("Score", f"{pct:.0f}%")
        z.metric("Feedback", "Excellent" if pct >= 80 else "Good progress" if pct >= 60 else "Keep practicing")
        st.progress(pct/100)
        with st.expander("Review answers and explanations", expanded=True):
            for i,item in enumerate(QUESTIONS):
                st.markdown(f'**{i+1}. {item["q"]}**')
                st.write(f"Your answer: {answers[i] or 'Not answered'}")
                st.write(f'Correct answer: {item["answer"]}')
                st.caption(item["why"])
                st.write("✅ Correct" if answers[i] == item["answer"] else "❌ Needs review")
                st.divider()

elif page == "AI Mentor":
    st.title("🤖 AI Mentor")
    st.write("Ask about Python, ML, data science, or study habits.")
    st.warning("This version uses a built-in FAQ, not a connected generative AI model.")
    question = st.text_input("Your question", placeholder="Example: What is a Python list?")
    if st.button("Get explanation", type="primary"):
        q = question.lower().strip()
        faq = [
            (["list"], "A Python list is an ordered, mutable collection. Example: `numbers = [1, 2, 3]`. Use `append()` to add an item."),
            (["tuple"], "A tuple is ordered and cannot be changed after creation. Example: `point = (3, 5)`."),
            (["dictionary","dict","key-value"], "A dictionary stores key-value pairs. Example: `student = {'name': 'Asha'}`. Access the value using `student['name']`."),
            (["set"], "A set stores unique values. Example: `unique = {1, 2, 3}`. Duplicate values are removed."),
            (["loop","for loop","while loop"], "A for loop iterates over an iterable. A while loop repeats while its condition is true."),
            (["function","def"], "A function is reusable code. Define one using `def greet():` and indent its body."),
            (["machine learning"," ml"], "Machine learning finds patterns in data. Typical steps: prepare data, split train/test, train a model, evaluate it."),
            (["variable"], "A variable is a name referring to a value. Example: `score = 85`."),
            (["condition","if statement"], "An if statement runs code when a condition is true. Use elif for another condition and else as a fallback."),
            (["study","focus","plan"], "Try 25 minutes of focused study, a 5-minute break, then practice questions. Review mistakes.")
        ]
        found = next((ans for keys,ans in faq if any(k in q for k in keys)), None)
        if not q:
            st.warning("Please enter a question.")
        elif found:
            st.markdown(found)
        else:
            st.info("Try asking about Python lists, tuples, dictionaries, sets, loops, functions, variables, conditions, machine learning, or study planning.")

elif page == "Progress":
    st.title("📈 Learning Analytics")
    attempts, logs = get_df("quiz_attempts"), get_df("study_logs")
    mins = int(logs["minutes"].sum()) if not logs.empty else 0
    a,b,c = st.columns(3)
    a.metric("Quiz attempts", len(attempts))
    b.metric("Study sessions", len(logs))
    c.metric("Total study time", f"{mins} minutes")
    if not attempts.empty:
        st.subheader("Quiz score history")
        st.line_chart(attempts.iloc[::-1].set_index("attempted_at")["percentage"])
        st.dataframe(attempts[["quiz_name","score","total","percentage","attempted_at"]], use_container_width=True, hide_index=True)
    else:
        st.info("Complete the quiz to see score history.")
    if not logs.empty:
        st.subheader("Study time by subject")
        st.bar_chart(logs.groupby("subject")["minutes"].sum())
        st.dataframe(logs[["subject","minutes","note","logged_at"]], use_container_width=True, hide_index=True)
    else:
        st.info("Add a session in Study Planner to track study time.")

elif page == "Study Planner":
    st.title("🗓️ Study Planner")
    st.write("Save study sessions in the local SQLite database.")
    with st.form("study_form"):
        subject = st.selectbox("Subject", list(SUBJECTS))
        minutes = st.number_input("Duration (minutes)", min_value=1, max_value=1440, value=30, step=5)
        note = st.text_area("What did you study?", placeholder="Example: Practiced Python loops.")
        save = st.form_submit_button("Save study session", type="primary")
    if save:
        save_study(subject, int(minutes), note)
        st.success("Study session saved.")
        st.rerun()
    logs = get_df("study_logs")
    if not logs.empty:
        st.subheader("Recent sessions")
        st.dataframe(logs[["subject","minutes","note","logged_at"]].head(10), use_container_width=True, hide_index=True)

elif page == "Profile":
    st.title("👤 Student Profile")
    current = get_profile()
    with st.form("profile_form"):
        name = st.text_input("Your name", value=current["name"])
        goal = st.text_area("Learning goal", value=current["goal"])
        save = st.form_submit_button("Save profile", type="primary")
    if save:
        save_profile(name, goal)
        st.success("Profile saved.")
        st.rerun()
    st.caption("Profile is saved locally in studypilot.db.")

st.divider()
st.caption("StudyPilot AI • Student Learning Support MVP • Local data stays on this computer.")
