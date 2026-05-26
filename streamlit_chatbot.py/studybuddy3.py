import streamlit as st
from datetime import date
from openai import OpenAI
import json

# ----------------------------
# OPENAI SETUP (INLINE KEY)
# ----------------------------
client = OpenAI(api_key="")


# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(page_title="StudyHub AI (OpenAI)", layout="wide")


# ----------------------------
# SESSION STATE
# ----------------------------
if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "subjects" not in st.session_state:
    st.session_state.subjects = ["General"]

if "notes" not in st.session_state:
    st.session_state.notes = ""

if "exams" not in st.session_state:
    st.session_state.exams = []

if "streak" not in st.session_state:
    st.session_state.streak = 0

if "last_done" not in st.session_state:
    st.session_state.last_done = None


# ----------------------------
# AI FUNCTION
# ----------------------------
def ask_ai(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful study assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI Error: {str(e)}"


# ----------------------------
# STREAK SYSTEM
# ----------------------------
def update_streak():
    today = date.today()

    if st.session_state.last_done is None:
        st.session_state.streak = 1
    else:
        diff = (today - st.session_state.last_done).days
        if diff == 1:
            st.session_state.streak += 1
        elif diff > 1:
            st.session_state.streak = 1

    st.session_state.last_done = today


# ----------------------------
# SIDEBAR
# ----------------------------
st.sidebar.title("🧠 StudyHub AI (OpenAI)")

st.sidebar.metric("🔥 Streak", st.session_state.streak)

if st.sidebar.button("Mark Today as Studied"):
    update_streak()

st.sidebar.divider()

st.sidebar.subheader("💬 AI Quote")
st.sidebar.info(
    ask_ai("Give a short motivational quote for studying (max 15 words).")
)

if st.sidebar.button("📊 Study Plan"):
    prompt = f"""
    Create a structured study plan.

    Tasks:
    {json.dumps(st.session_state.tasks, default=str)}

    Exams:
    {json.dumps(st.session_state.exams, default=str)}
    """
    st.sidebar.success(ask_ai(prompt))

if st.sidebar.button("🧠 What should I study next?"):
    prompt = f"""
    Based on tasks:
    {st.session_state.tasks}

    Suggest ONLY ONE task to do next and explain briefly.
    """
    st.sidebar.info(ask_ai(prompt))


# ----------------------------
# MAIN UI
# ----------------------------
st.title("📚 StudyHub AI (Powered by OpenAI)")


# ----------------------------
# SUBJECTS
# ----------------------------
st.subheader("📘 Subjects")

new_subject = st.text_input("Add Subject")

if st.button("Add Subject"):
    if new_subject and new_subject not in st.session_state.subjects:
        st.session_state.subjects.append(new_subject)

st.write(st.session_state.subjects)


# ----------------------------
# TASKS
# ----------------------------
st.subheader("📌 Add Task")

col1, col2, col3 = st.columns(3)

with col1:
    task_title = st.text_input("Task Title")

with col2:
    subject = st.selectbox("Subject", st.session_state.subjects)

with col3:
    deadline = st.date_input("Deadline")

if st.button("Add Task"):
    if task_title:
        st.session_state.tasks.append({
            "title": task_title,
            "subject": subject,
            "deadline": str(deadline),
            "done": False
        })


st.subheader("📋 Tasks")

for i, task in enumerate(st.session_state.tasks):
    colA, colB, colC, colD = st.columns([4, 2, 2, 1])

    with colA:
        st.write(task["title"])

    with colB:
        st.write(task["subject"])

    with colC:
        st.write(task["deadline"])

    with colD:
        if st.button("✔", key=f"done_{i}"):
            st.session_state.tasks[i]["done"] = True
            update_streak()

    if task["done"]:
        st.success("Completed ✔")


# ----------------------------
# EXAMS
# ----------------------------
st.subheader("📆 Exams")

exam_name = st.text_input("Exam Name")
exam_date = st.date_input("Exam Date", key="exam")

if st.button("Add Exam"):
    if exam_name:
        st.session_state.exams.append({
            "name": exam_name,
            "date": str(exam_date)
        })

for exam in st.session_state.exams:
    st.write(f"📌 {exam['name']} → {exam['date']}")


# ----------------------------
# NOTES + AI SUMMARY
# ----------------------------
st.subheader("📝 Notes")

st.session_state.notes = st.text_area("Write notes here...", st.session_state.notes)

if st.button("🧠 Summarize Notes"):
    st.info(
        ask_ai(f"Summarize these notes into bullet points:\n\n{st.session_state.notes}")
    )


# ----------------------------
# INSIGHT
# ----------------------------
st.subheader("📊 AI Insight")

if st.button("Analyze Progress"):
    prompt = f"""
    Tasks: {st.session_state.tasks}
    Exams: {st.session_state.exams}
    Streak: {st.session_state.streak}

    Give short feedback and improvement tips.
    """
    st.success(ask_ai(prompt))


st.caption("🚀 StudyHub AI — OpenAI Version")