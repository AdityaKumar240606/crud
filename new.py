from pydantic import BaseModel, EmailStr
from fastapi import FastAPI,HTTPException
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
app = FastAPI()

connection_url = URL.create(
    drivername="postgresql",
    username="postgres",
    password="Aditya@123",
    host="localhost",
    port=5432,
    database="gc_data"
)
engine  = create_engine(connection_url)

@app.get("/channel/{channel_name}")
def get_channel_data(channel_name: str):
    with engine.connect() as conn:
        result = conn.execute(
            text('SELECT * FROM "channel-wise-publishing" WHERE \"Channels\" = :channel_name'),
            {"channel_name":channel_name}
        )
        row = result.fetchone()
    return dict(row._mapping)



VALID_PLATFORMS = ["Facebook", "Instagram", "Linkedin", "Reels", "Shorts", "X", "Youtube", "Threads"]

@app.put("/channel/update/{channel_name}/{platform}/{new_count}")
def update_channel_count(channel_name: str, platform: str, new_count: int):

    with engine.begin() as conn:
        result = conn.execute(
            text(f'UPDATE "channel-wise-publishing" SET "{platform}" = :new_count WHERE "Channels" = :channel_name'),
            {"new_count": new_count, "channel_name": channel_name}
        )

    return {"message": f"{platform} count updated for channel {channel_name} to {new_count}"}

@app.delete("/channel/{channel_name}")
def delete_channel(channel_name:str):
    with engine.begin() as conn:
        result = conn.execute(text('DELETE FROM "channel-wise-publishing" WHERE "Channels" = :channel_name'),
            {"channel_name": channel_name})

    return {"message": f"Deleted channel {channel_name}"}


