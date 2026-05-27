from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import os
import redis
import psycopg2
import logging

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "db")


class DemoData(BaseModel):
    message: str


def init_db():
    conn = psycopg2.connect(
        host=POSTGRES_HOST,
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )

    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS demo_logs (
            id SERIAL PRIMARY KEY,
            message TEXT,
            created_at TIMESTAMP
        )
    """)

    conn.commit()

    cur.close()
    conn.close()


@app.get("/")
def root():

    logger.info("Root endpoint called")

    return {
        "message": "AI Backend Running"
    }


@app.get("/health")
def health_check():

    logger.info("Health check endpoint called")

    redis_status = "connected"
    db_status = "connected"

    try:
        r = redis.Redis(host=REDIS_HOST, port=6379)
        r.ping()

    except Exception:
        redis_status = "failed"

    try:
        conn = psycopg2.connect(
            host=POSTGRES_HOST,
            database=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD")
        )

        conn.close()

    except Exception:
        db_status = "failed"

    return {
        "app": "running",
        "redis": redis_status,
        "database": db_status
    }


@app.post("/generate")
def generate():

    logger.info("Generate endpoint called")

    return {
        "response": "AI response generated successfully"
    }


@app.post("/store-data")
def store_data(data: DemoData):

    logger.info("Store data endpoint called")

    init_db()

    redis_client = redis.Redis(host=REDIS_HOST, port=6379)

    redis_client.set("latest_message", data.message)

    conn = psycopg2.connect(
        host=POSTGRES_HOST,
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )

    cur = conn.cursor()

    current_time = datetime.now()

    cur.execute(
        "INSERT INTO demo_logs (message, created_at) VALUES (%s, %s)",
        (data.message, current_time)
    )

    conn.commit()

    cur.close()
    conn.close()

    return {
        "status": "success",
        "message": "Data stored successfully",
        "stored_data": data.message,
        "postgresql": "updated",
        "redis": "cache updated",
        "timestamp": str(current_time)
    }


@app.get("/fetch-data")
def fetch_data():

    logger.info("Fetch data endpoint called")

    init_db()

    redis_client = redis.Redis(host=REDIS_HOST, port=6379)

    redis_value = redis_client.get("latest_message")

    if redis_value:
        redis_value = redis_value.decode()

    else:
        redis_value = "No cache found"

    conn = psycopg2.connect(
        host=POSTGRES_HOST,
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )

    cur = conn.cursor()

    cur.execute(
        "SELECT message, created_at FROM demo_logs ORDER BY id DESC LIMIT 1"
    )

    latest_record = cur.fetchone()

    cur.close()
    conn.close()

    if latest_record:
        db_message = latest_record[0]
        db_time = str(latest_record[1])

    else:
        db_message = "No records found"
        db_time = "N/A"

    return {
        "project": "AI DevOps Infrastructure Demo",

        "postgresql": {
            "status": "connected",
            "latest_message": db_message,
            "timestamp": db_time
        },

        "redis": {
            "status": "connected",
            "cached_message": redis_value
        },

        "services": {
            "fastapi": "running",
            "nginx": "active",
            "docker": "operational",
            "aws_ec2": "running",
            "ci_cd": "GitHub Actions active",
            "security": "Fail2Ban enabled"
        }
    }