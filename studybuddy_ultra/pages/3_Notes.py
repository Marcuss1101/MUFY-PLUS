import streamlit as st

st.title("📝 Notes")

if "notes" not in st.session_state:
    st.session_state.notes = []

note = st.text_area("Write note")

if st.button("Save Note"):
    st.session_state.notes.append(note)

for n in st.session_state.notes:
    st.write("📌", n)