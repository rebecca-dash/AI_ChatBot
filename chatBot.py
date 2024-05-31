from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai

#configure API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

#function to load gemini pro model and get response
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])
context = "Assess the users personality by asking them questions based on the Myers Brigg's assessments"
def get_gemini_response(input):
    response = chat.send_message(input, stream=True)
    return response

#initilize streamlit app
st.set_page_config(page_title="AI Personality Test Demo")
st.header("Gemini Pro Personality Test")

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

input = st.text_input("Input: ", key="input")
submit = st.button("Ask Gemini")

if submit and input:
    response = get_gemini_response(input)
    #Add user query and resposne to session and chat history
    st.session_state['chat_history'].append(("You: ", input))
    st.subheader("Gemini says: ")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Gemini: ",chunk.text))

st.subheader("Chat History")

for role,text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")


