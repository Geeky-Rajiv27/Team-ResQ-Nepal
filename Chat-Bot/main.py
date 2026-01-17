#NOTE : IMporting all libraries, packages that we want like fastapi since we are using fastapi, 
from fastapi import FastAPI, HTTPException  #HTTPexception is for raising request related errors
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai
import os

# her i loading info from environmnet variables
load_dotenv()

# Retriving API key from the .env file in a variable
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY is missing")

# Here we gonna initializing the gemini's client using built in functions , methods
client = genai.Client(api_key=API_KEY)

# telling our bot / giving refrence of our document where we have written all the possible questions and answer that our client can ask to our bot 
try:
    with open("project_docs.txt", "r", encoding="utf-8") as f:
        PROJECT_DOCS = f.read()
except FileNotFoundError:
    raise RuntimeError("project_docs.txt not found")    # raising errors

# making our fastapi app
app = FastAPI(title="Project Q&A Bot")

#Creating pydantic models for questions
class UserQuestion(BaseModel):
    question: str

@app.post("/ask")   #endpoints for asking the bot to assist 
async def ask_bot(data: UserQuestion):
    prompt = f"""
You are an AI assistant for our application.

STRICT RULES:
- Answer ONLY using the project documentation below.
- If the answer is not found, reply:
  "Sorry, this information is not available in the app documentation."

PROJECT DOCUMENTATION:
{PROJECT_DOCS}  # this stores list of possible quesitions and answers

USER QUESTION:
{data.question}

ANSWER:
"""
    #jsut handling errors 
    try:
        # Here we are generating response from bot to users using new Gemini client
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt
        )

        if not response.text:
            raise ValueError("Empty response from model")

        return {"answer": response.text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
