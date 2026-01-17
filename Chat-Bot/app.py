# app.py
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from google import genai

# okay so basically i need to create the client here for gemini
# honestly took me a while to figure this out but you gotta use genai.Client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def get_gemini_response(question):
    # this function is for getting response from gemini api
    # i'm using gemini-2.5-flash-lite because it's faster i think
    # TODO: maybe try other models later?
    resp = client.models.generate_content(
        model="gemini-2.5-flash-lite", 
        contents=question
    )
    return resp.text

# setting up the page config stuff
# honestly not sure if page_title does much but keeping it anyway
st.set_page_config(page_title="Q&A Demo")
st.header("Gemini Q&A Demo (Using gemini-2.5-flash-lite)")

# initialize chat history if it doesn't exist yet
# this part is important otherwise you'll get errors when trying to access it
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# input box where user types their question
input_from_user = st.text_input("Ask your question:")

# when the user clicks the ask button, we process the question
# added the "and input_from_user" check so it doesn't crash if they click with empty input
if st.button("Ask") and input_from_user:
    # get the answer from gemini
    bot_answer = get_gemini_response(input_from_user)
    
    # adding both the question and answer to chat history
    # using tuples here like ("You", question) and ("Bot", answer)
    st.session_state['chat_history'].append(("You", input_from_user))
    st.session_state['chat_history'].append(("Bot", bot_answer))

# display all the chat history below
# this loops through everything and shows it
st.subheader("Chat History")
for user_role, message_text in st.session_state['chat_history']:
    st.write(f"{user_role}: {message_text}")


# Note to self: maybe add a clear history button later?
# also could make the UI look better with some styling