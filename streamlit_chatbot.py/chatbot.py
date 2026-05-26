import streamlit as st 
import pandas as pd

st.title("Chatbot")
st.header("Ask anything")

st.write("type your questions below")

def initialize_session_state():
    if "message" not in st.session_state:
        st.session_state.message = []

def main():
    st.title("Simple Chatbot")

    initialize_session_state()

    for message in st.session_state.message:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if prompt := st.chat_input("What's on your mind?"):
        with st.chat_message("user"):
             st.write(prompt)

        st.session_state.message.append({
            "role":"user",
            "content":prompt})   

        response =f"You said:{prompt}"

        with st.chat_message("assistant"):
            st.write(response)

        st.session_state.message.append({
            "role":"assistant",
            "content":response})

if __name__ == "__main__":
    main()


df = pd.DataFrame({
    'Month':['January','February','March','Apri','May','June','July','August','September','October','November','December','January'],
    'Price':[1000,1500,2000,2500,3000,3500,4000,4500,5000,5500,6000,6500,1200]
})

st.sidebar.header("Filters")

selected_month = st.sidebar.selectbox(
    "Selected Month",
    options=df['Month'].unique()
)

price_range = st.sidebar.slider(
    "Selected Price Range",
    min_value=0,
    max_value=6500,
    value=(0,6500)
)

import streamlit as st
import google.generativeai as genai

GOOGLE_API_KEY = ""
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []

def get_gemini_response(prompt):
    response = model.generate_content(prompt)
    return response.text

def main():
    st.title("Gemini AI Chatbot")
    
    initialize_session_state()

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if prompt := st.chat_input("Chat with Gemini"):
    with st.chat_message("user"):
        st.write(prompt)

     st.session_state.messages.append({"role": "user", "content": prompt})

    
     response = get_gemini_response(prompt)

     with st.chat_message("assistant"):
        st.write(response)

        st.session_state.messages.append({"role": "assistant", "content": response})
        
        def get_gemini_response(prompt):
            try:
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(prompt)
                return response.text

            except Exception as e:
                 return f"Error: {str(e)}"
        
        with st.chat_message("assistant"):
            st.write(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})

 def get_gemini_response(prompt):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"Error: {str(e)}"
if __name__ == "__main__":
    main()
