import streamlit as st
from datetime import datetime, date, timedelta
import random

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(page_title="StudyHub", layout="wide")

# ----------------------------
# SESSION STATE INIT
# ----------------------------
if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "subjects" not in st.session_state:
    st.session_state.subjects = ["General"]

if "notes" not in st.session_state:
    st.session_state.notes = ""

if "streak" not in st.session_state:
    st.session_state.streak = 0

if "last_active" not in st.session_state:
    st.session_state.last_active = None

if "exams" not in st.session_state:
    st.session_state.exams = []

if "timer_running" not in st.session_state:
    st.session_state.timer_running = False

if "timer_end" not in st.session_state:
    st.session_state.timer_end = None


# ----------------------------
# QUOTES
# ----------------------------
QUOTES = [
    "Small progress is still progress.",
    "Discipline beats motivation.",
    "You don’t have to be perfect, just consistent.",
    "Study now, shine later.",
    "One day or day one—you decide.",
]


def update_streak():
    today = date.today()
    last = st.session_state.last_active

    if last is None:
        st.session_state.streak = 1
    else:
        diff = (today - last).days
        if diff == 1:
            st.session_state.streak += 1
        elif diff > 1:
            st.session_state.streak = 1

    st.session_state.last_active = today


# ----------------------------
# SIDEBAR
# ----------------------------
st.sidebar.title("🧠 StudyHub")

# Focus Timer
st.sidebar.subheader("⏰ Focus Timer (25 min)")

if st.sidebar.button("Start Focus Session"):
    st.session_state.timer_running = True
    st.session_state.timer_end = datetime.now() + timedelta(minutes=25)

if st.session_state.timer_running:
    remaining = st.session_state.timer_end - datetime.now()
    if remaining.total_seconds() > 0:
        st.sidebar.success(f"Time left: {remaining.seconds // 60}m {remaining.seconds % 60}s")
    else:
        st.session_state.timer_running = False
        st.sidebar.warning("Session done! Take a break 💆")

st.sidebar.divider()

# Reminders
st.sidebar.subheader("💡 Break Reminders")
reminders = [
    "💧 Drink water",
    "🧍 Stretch your body",
    "👀 Rest your eyes (20-20-20 rule)",
    "🌿 Take a deep breath",
]
st.sidebar.info(random.choice(reminders))

st.sidebar.divider()

# Streak
st.sidebar.subheader("🔥 Study Streak")
st.sidebar.metric("Days", st.session_state.streak)

if st.sidebar.button("Mark Today as Studied"):
    update_streak()

st.sidebar.divider()

# Quote
st.sidebar.subheader("💬 Quote of the Day")
st.sidebar.write(random.choice(QUOTES))


# ----------------------------
# MAIN LAYOUT
# ----------------------------
st.title("📚 StudyHub Dashboard")

col1, col2 = st.columns(2)


# ----------------------------
# SUBJECTS
# ----------------------------
with col1:
    st.subheader("📘 Subjects")

    new_subject = st.text_input("Add subject")
    if st.button("Add Subject"):
        if new_subject and new_subject not in st.session_state.subjects:
            st.session_state.subjects.append(new_subject)

    st.write("Current subjects:")
    st.write(st.session_state.subjects)


# ----------------------------
# TASKS
# ----------------------------
with col2:
    st.subheader("📌 Add Task")

    task_title = st.text_input("Task title")

    subject = st.selectbox("Subject", st.session_state.subjects)

    deadline = st.date_input("Deadline")

    if st.button("Add Task"):
        if task_title:
            st.session_state.tasks.append({
                "title": task_title,
                "subject": subject,
                "deadline": deadline,
                "done": False
            })

# Task list
st.subheader("📋 Tasks")

for i, task in enumerate(st.session_state.tasks):
    colA, colB, colC, colD = st.columns([3, 2, 2, 1])

    with colA:
        st.write(f"**{task['title']}**")

    with colB:
        st.write(task["subject"])

    with colC:
        days_left = (task["deadline"] - date.today()).days
        if days_left < 0:
            st.error(f"Overdue by {abs(days_left)} days")
        else:
            st.info(f"{days_left} days left")

    with colD:
        if st.button("✔", key=f"done_{i}"):
            st.session_state.tasks[i]["done"] = True

    if task["done"]:
        st.success("Completed ✔")


# ----------------------------
# EXAMS
# ----------------------------
st.subheader("📆 Exam Countdown")

exam_name = st.text_input("Exam name")
exam_date = st.date_input("Exam date", key="exam_date")

if st.button("Add Exam"):
    st.session_state.exams.append({
        "name": exam_name,
        "date": exam_date
    })

for exam in st.session_state.exams:
    days = (exam["date"] - date.today()).days
    st.write(f"📌 {exam['name']} — {days} days left")


# ----------------------------
# NOTES
# ----------------------------
st.subheader("📝 Mini Notes")
st.session_state.notes = st.text_area("Write notes here...", st.session_state.notes)


# ----------------------------
# FOOTER
# ----------------------------
st.caption("Built for focused studying 🚀")