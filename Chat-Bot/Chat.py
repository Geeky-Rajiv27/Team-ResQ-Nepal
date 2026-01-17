# NOTE : importing os module along with dotenv which we gonna use below 
import os
from dotenv import load_dotenv
load_dotenv()   # initializing the dotenv() so that we can load info from .env

import streamlit as st  #this is for streaming 
from google import genai    #this is latest one 

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))  # retriving api key
#from .env

def get_gemini_response(question):  #
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",  #using gemini-2.5-flash-lite since it provide tokens so that we can check or provide users more tokens to chat with our bot
        contents=question
    )
    return response.text

st.set_page_config(page_title="Chatbot Demo")   # setting the page title
st.header("Gemini Chatbot")

if 'chat_history' not in st.session_state:  # this is for chat history like currently we are not using this in our project but if we want we can also use this to see the history of chats that user do with our bot 
    st.session_state['chat_history'] = []

user_input = st.text_input("Ask your question:")

if st.button("Ask") and user_input:
    answer = get_gemini_response(user_input)
    st.session_state['chat_history'].append(("You", user_input))
    st.session_state['chat_history'].append(("Bot", answer))

st.subheader("Chat History")
for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")
