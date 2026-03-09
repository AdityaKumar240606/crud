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


class ChannelCreate(BaseModel):
    channel_name: str
    Facebook: int = 0
    Instagram: int = 0
    Linkedin: int = 0
    Reels: int = 0
    Shorts: int = 0
    X: int = 0
    Youtube: int = 0
    Threads: int = 0

@app.post("/channel")
def create_channel(channel: ChannelCreate):
    with engine.begin() as conn:
        existing = conn.execute(text('SELECT 1 FROM "channel-wise-publishing" WHERE "Channels" = :name'),
            {"name": channel.channel_name}).fetchone()
        
        conn.execute(text('''INSERT INTO "channel-wise-publishing" ("Channels", "Facebook", "Instagram", "Linkedin", "Reels", "Shorts", "X", "Youtube", "Threads")
            VALUES (:channel_name, :Facebook, :Instagram, :Linkedin, :Reels, :Shorts, :X, :Youtube, :Threads)
        '''), channel.model_dump(exclude={"channel_name"}) | {"channel_name": channel.channel_name})

    return {"message":  f"Channel '{channel.channel_name}' created   "}


