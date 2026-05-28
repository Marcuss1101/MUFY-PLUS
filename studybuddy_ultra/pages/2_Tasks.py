import streamlit as st
from utils_storage import load, save
from utils_ultra import add_xp, add_badge, update_streak

FILE = "data/tasks.json"

st.title("📅 Tasks")

tasks = load(FILE)

task = st.text_input("Add Task")

if st.button("Add"):
    tasks.append({"task": task, "done": False})
    save(FILE, tasks)

for i, t in enumerate(tasks):

    col1, col2 = st.columns([4, 1])

    with col1:
        st.write(("✔" if t["done"] else "❌"), t["task"])

    with col2:
        if not t["done"] and st.button("Complete", key=i):

            tasks[i]["done"] = True
            save(FILE, tasks)

            add_xp(25)
            update_streak()

            if len(tasks) >= 5:
                add_badge("Task Master 🏆")

            st.success("+25 XP 🔥")