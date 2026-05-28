import streamlit as st
from datetime import date

st.title("🎯 Exam Countdown")

exam_date = st.date_input("Exam Date")

days_left = (exam_date - date.today()).days

st.metric("Days Left", days_left)