#NOTE : importing necessary models 
import os
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from google import genai    #importing genai from google this is built in 

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY")) #retriving api key from .env file

def get_gemini_response(question):
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",  # more lite and have free limited request chances
        contents=question
    )
    return response.text

st.set_page_config(page_title="Q&A Chatbot")
st.header("Gemini Q&A Chatbot (gemini-2.5-flash-lite)")

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

user_input = st.text_input("Your question:")

if st.button("Ask") and user_input:
    answer = get_gemini_response(user_input)
    st.session_state['chat_history'].append(("You", user_input))
    st.session_state['chat_history'].append(("Bot", answer))

st.subheader("Chat History")
for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")
