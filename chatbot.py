from fastapi import FastAPI
from pydantic import BaseModel
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_groq import ChatGroq

import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")

system_prompt = system_prompt = system_prompt = system_prompt = """
You are a PostgreSQL expert. You ONLY query the "channel-wise-publishing" table.

STRICT RULES:
1. ONLY query the "channel-wise-publishing" table. No other tables.
2. ALWAYS wrap the table name in double quotes: "channel-wise-publishing"
3. ALWAYS wrap column names in double quotes.
4. ALWAYS add LIMIT 10 to every SELECT query.
5. NEVER use INSERT, UPDATE, DELETE, DROP, or any data-modifying statement.
6. ONLY generate SELECT queries.
7. Do NOT call list_tables or describe any other table or schema.
8. ALWAYS execute the query using the sql_db_query tool and return the actual data results.
9. NEVER return the SQL query as your final answer. Always run it and return the data.
10. ALWAYS return the final answer as a JSON array of objects. Example:
    [{{"Channels": "A", "Facebook": 100, "Instagram": 7}}]
    No extra text, no explanation, just the JSON array.
"""
db = SQLDatabase.from_uri(
    DATABASE_URL,
    include_tables=["channel-wise-publishing"],
    sample_rows_in_table_info=2
)

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    max_tokens=500,
    request_timeout=30
)

agent = create_sql_agent(
    llm=llm,
    db=db,
    verbose=True,
    agent_type="tool-calling",
    prefix=system_prompt,
    max_execution_time=60
)

app = FastAPI()

class Question(BaseModel):
    question: str

@app.post("/query")
def query(body: Question):
    result = agent.invoke({"input": body.question})
    return {"answer": result["output"]}