from fastapi import FastAPI
from pydantic import BaseModel
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_google_genai import ChatGoogleGenerativeAI

import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")

db = SQLDatabase.from_uri(DATABASE_URL)

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-lite", temperature=0)

agent = create_sql_agent(llm=llm, db=db, verbose=True)

app = FastAPI()

class Question(BaseModel):
    question: str

@app.post("/query")
def query(body: Question):
    result = agent.invoke({"input": body.question})
    return {"answer": result["output"]}