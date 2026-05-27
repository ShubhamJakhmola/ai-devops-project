from fastapi import FastAPI
import os
import redis
import psycopg2
import logging

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "db")

@app.get("/")
def root():
    logger.info("Root endpoint called")
    return {"message": "AI Backend Running"}

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