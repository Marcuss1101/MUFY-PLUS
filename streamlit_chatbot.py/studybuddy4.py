import streamlit as st
from datetime import date

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(page_title="StudyHub", layout="wide")


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
st.sidebar.title("📚 StudyHub")

st.sidebar.metric("🔥 Study Streak", st.session_state.streak)

if st.sidebar.button("Mark Today as Studied"):
    update_streak()

st.sidebar.divider()

st.sidebar.subheader("💡 Motivation")
st.sidebar.info("Small progress every day leads to big results.")


# ----------------------------
# MAIN UI
# ----------------------------
st.title("📚 StudyHub Dashboard (No AI)")


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
st.subheader("📆 Exam Countdown")

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
# NOTES
# ----------------------------
st.subheader("📝 Notes")

st.session_state.notes = st.text_area("Write your notes here...", st.session_state.notes)


# ----------------------------
# FOOTER
# ----------------------------
st.caption("🚀 StudyHub — Simple, clean, no AI, no errors")