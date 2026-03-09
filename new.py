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

@app.get("/monthly-stats/{month}")
def get_month(month : str):
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT * FROM monthly_chart WHERE \"Month\" = :month LIMIT 10"),
            {"month": month}
        )

        row = result.fetchall()


    if row is None:
        raise HTTPException(status_code=404, detail="Month not found")
    
    return row


def process_items(prices: dict[str, float]):
    for item_name,item_price in prices.items():
        print(item_name)
        print(item_price)

