# importing all essential modules we need
import os
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from google import genai
import base64
from PIL import Image
import io

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))# fetching API key from .env file that 
#i have stored already

def generate_image(prompt):# this will generate the image based on the user's prompt requirement
    response = client.models.generate_content(
        model="gemini-2.5-flash-image-lite", #This is smaller free-tier image model since we are using this for our hackathon
        contents=prompt,
        config={
            "response_modalities": ["IMAGE"],
        }
    )
    # here we are extracting the bytes of images 
    for part in response.parts:
        if part.inline_data and part.inline_data.image:
            return part.inline_data.image
    return None

st.set_page_config(page_title="Vision Demo")
st.header("Gemini Vision App")

prompt = st.text_input("Describe the image you want:")

if st.button("Generate Image") and prompt:
    image_b64 = generate_image(prompt)
    if image_b64:
        image_bytes = base64.b64decode(image_b64)
        img = Image.open(io.BytesIO(image_bytes))
        st.image(img, use_column_width=True)
