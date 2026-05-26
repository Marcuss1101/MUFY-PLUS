import streamlit as st
from datetime import datetime, timedelta, date
import random
import time

# ---------------------------
# GEMINI AI SETUP
# ---------------------------
AI_ENABLED = True

try:
    from google import genai

    # PASTE YOUR GEMINI API KEY HERE
    API_KEY = "AIzaSyDxJjfH6aq6FVX5W-nPeu5mSNis105KzdA"

    client = genai.Client(api_key=API_KEY)

except Exception:
    AI_ENABLED = False


# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(
    page_title="StudyHub AI",
    page_icon="📚",
    layout="wide"
)

# ---------------------------
# SESSION STATE
# ---------------------------
if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "subjects" not in st.session_state:
    st.session_state.subjects = ["General"]

if "notes" not in st.session_state:
    st.session_state.notes = ""

if "study_streak" not in st.session_state:
    st.session_state.study_streak = 0

if "last_study_date" not in st.session_state:
    st.session_state.last_study_date = None

if "exams" not in st.session_state:
    st.session_state.exams = []

if "timer_running" not in st.session_state:
    st.session_state.timer_running = False

if "timer_seconds" not in st.session_state:
    st.session_state.timer_seconds = 25 * 60


# ---------------------------
# QUOTES
# ---------------------------
quotes = [
    "Success is the sum of small efforts repeated daily.",
    "Study hard, your future self will thank you.",
    "Discipline beats motivation.",
    "Dream big, start small.",
    "One chapter at a time.",
    "Progress, not perfection."
]

daily_quote = random.choice(quotes)

# ---------------------------
# GEMINI FUNCTIONS
# ---------------------------
def ask_gemini(prompt):
    if not AI_ENABLED:
        return "⚠️ Gemini AI not available."

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:
        return f"⚠️ Gemini Error:\n{str(e)}"


# ---------------------------
# STREAK FUNCTION
# ---------------------------
def update_streak():
    today = date.today()

    if st.session_state.last_study_date:
        diff = (today - st.session_state.last_study_date).days

        if diff == 1:
            st.session_state.study_streak += 1
        elif diff > 1:
            st.session_state.study_streak = 1
    else:
        st.session_state.study_streak = 1

    st.session_state.last_study_date = today


# ---------------------------
# SIDEBAR
# ---------------------------
st.sidebar.title("📚 StudyHub")

# Focus Timer
st.sidebar.subheader("⏰ Focus Timer")

minutes = st.sidebar.slider(
    "Focus Time (minutes)",
    5,
    60,
    25
)

if st.sidebar.button("Start Timer"):
    st.session_state.timer_running = True
    st.session_state.timer_seconds = minutes * 60

if st.session_state.timer_running:
    timer_placeholder = st.sidebar.empty()

    while st.session_state.timer_seconds > 0:
        mins, secs = divmod(
            st.session_state.timer_seconds, 60
        )

        timer_placeholder.metric(
            "Time Left",
            f"{mins:02}:{secs:02}"
        )

        time.sleep(1)
        st.session_state.timer_seconds -= 1

    st.sidebar.success("🎉 Session Complete!")
    st.sidebar.info("💧 Drink water")
    st.sidebar.info("🧍 Stretch your body")
    st.sidebar.info("👀 Rest your eyes")

    st.session_state.timer_running = False


st.sidebar.divider()

# Study streak
st.sidebar.subheader("🔥 Study Streak")
st.sidebar.metric(
    "Days",
    st.session_state.study_streak
)

if st.sidebar.button("Mark Today Studied"):
    update_streak()

st.sidebar.divider()

# Quote
st.sidebar.subheader("💬 Quote of the Day")
st.sidebar.info(daily_quote)

# ---------------------------
# MAIN PAGE
# ---------------------------
st.title("📚 StudyHub Dashboard")

col1, col2 = st.columns([2, 1])

# ---------------------------
# TASKS
# ---------------------------
with col1:
    st.header("✅ Tasks")

    task_name = st.text_input("Task")

    subject = st.selectbox(
        "Subject",
        st.session_state.subjects
    )

    deadline = st.date_input("Deadline")

    if st.button("Add Task"):
        if task_name:
            st.session_state.tasks.append({
                "task": task_name,
                "subject": subject,
                "deadline": str(deadline),
                "completed": False
            })

    st.subheader("Task List")

    for i, task in enumerate(
            st.session_state.tasks):

        cols = st.columns([4, 2, 2, 1])

        with cols[0]:
            st.write(task["task"])

        with cols[1]:
            st.write(task["subject"])

        with cols[2]:
            st.write(task["deadline"])

        with cols[3]:
            done = st.checkbox(
                "Done",
                value=task["completed"],
                key=f"task_{i}"
            )

            st.session_state.tasks[i][
                "completed"
            ] = done


# ---------------------------
# SUBJECTS
# ---------------------------
with col2:
    st.header("📖 Subjects")

    new_subject = st.text_input(
        "Add Subject"
    )

    if st.button("Add Subject"):
        if new_subject:
            st.session_state.subjects.append(
                new_subject
            )

    st.write(
        st.session_state.subjects
    )

# ---------------------------
# NOTES
# ---------------------------
st.divider()

st.header("📝 Quick Notes")

st.session_state.notes = st.text_area(
    "Write notes here",
    value=st.session_state.notes,
    height=150
)

# ---------------------------
# EXAM COUNTDOWN
# ---------------------------
st.divider()

st.header("📆 Exam Countdown")

exam_name = st.text_input(
    "Exam Name"
)

exam_date = st.date_input(
    "Exam Date",
    key="exam_date"
)

if st.button("Add Exam"):
    st.session_state.exams.append({
        "name": exam_name,
        "date": exam_date
    })

for exam in st.session_state.exams:
    days_left = (
        exam["date"] - date.today()
    ).days

    st.info(
        f"📌 {exam['name']} "
        f"- {days_left} days left"
    )

# ---------------------------
# GEMINI AI
# ---------------------------
st.divider()

st.header("🤖 Gemini Study Assistant")

if AI_ENABLED:

    ai_option = st.selectbox(
        "Choose AI Feature",
        [
            "Study Advice",
            "Summarize Notes",
            "What Should I Study Next?"
        ]
    )

    if st.button("Ask Gemini"):

        if ai_option == "Study Advice":
            prompt = """
            Give me short study tips
            for productivity.
            """

        elif ai_option == "Summarize Notes":
            prompt = f"""
            Summarize this into
            concise study notes:

            {st.session_state.notes}
            """

        else:
            prompt = f"""
            Based on these tasks:

            {st.session_state.tasks}

            Tell me what I should
            study next.
            """

        with st.spinner("Thinking..."):
            response = ask_gemini(prompt)

        st.success(response)

else:
    st.warning(
        "Gemini AI unavailable."
    )

st.caption(
    "StudyHub AI • Built with Streamlit + Gemini"
)