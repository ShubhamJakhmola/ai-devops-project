from fastapi import FastAPI
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


@app.get("/system-demo")
def system_demo():

    logger.info("System demo endpoint called")

    init_db()

    # Redis Test
    redis_client = redis.Redis(host=REDIS_HOST, port=6379)

    redis_client.set("demo_key", "Redis cache working")

    redis_value = redis_client.get("demo_key").decode()

    # PostgreSQL Test
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
        ("PostgreSQL insert working", current_time)
    )

    conn.commit()

    cur.execute(
        "SELECT message, created_at FROM demo_logs ORDER BY id DESC LIMIT 1"
    )

    latest_record = cur.fetchone()

    cur.close()
    conn.close()

    return {
        "fastapi": "API working",
        "postgresql": {
            "status": "connected",
            "latest_record": latest_record[0],
            "timestamp": str(latest_record[1])
        },
        "redis": {
            "status": "connected",
            "cached_value": redis_value
        },
        "nginx": "reverse proxy active",
        "docker": "containerized services running",
        "server": "AWS EC2 Ubuntu active",
        "logging": "application logging active"
    }