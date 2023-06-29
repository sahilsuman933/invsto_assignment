from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import csv
import psycopg2
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db_conn = {
    "host": "localhost",
    "database": "invsto",
    "user": "postgres",
}

class StockData(BaseModel):
    datetime: str
    close: float
    high: float
    low: float
    open: float
    volume: int
    instrument: str


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        content = await file.read()
        decoded_content = content.decode("utf-8").splitlines()
        insert_query = """
             INSERT INTO stock_data (datetime, close, high, low, open, volume, instrument)
             VALUES (%s, %s, %s, %s, %s, %s, %s)
         """

        reader = csv.DictReader(decoded_content)
        with psycopg2.connect(**db_conn) as conn:
            with conn.cursor() as cursor:
                for row in reader:
                    stock_data = StockData(**row)
                    cursor.execute(
                        "INSERT INTO stock_data (datetime, close, high, low, open, volume, instrument) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                        (stock_data.datetime, stock_data.close, stock_data.high, stock_data.low, stock_data.open,
                         stock_data.volume, stock_data.instrument)
                    )

        return JSONResponse({"message": "Data uploaded successfully"})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


@app.get("/data")
def get_data():
    try:
        with psycopg2.connect(**db_conn) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM stock_data")
                rows = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                data = []
                for row in rows:
                    data.append(dict(zip(columns, row)))

        return {"data": data}
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
