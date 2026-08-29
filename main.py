import os, re, json, sqlite3, uuid
from datetime import datetime, timezone
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

APP_NAME = "JobAgent AI"
DB = os.getenv("DATABASE_PATH", "jobagent.db")

app = FastAPI(title=APP_NAME, version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

def conn():
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    return c

def init_db():
    c = conn()
    c.executescript("""
    CREATE TABLE IF NOT EXISTS profiles(
        user_id TEXT PRIMARY KEY,
        name TEXT,
        email TEXT,
        role TEXT,
        mode TEXT,
        salary INTEGER,
        skills TEXT,
        hours INTEGER,
        cv_text TEXT
    );

    CREATE TABLE IF NOT EXISTS jobs(
        id TEXT PRIMARY KEY,
        title TEXT,
        company TEXT,
        url TEXT,
        description TEXT,
        source TEXT,
        created_at TEXT
    );

    CREATE TABLE IF NOT EXISTS matches(
        id TEXT PRIMARY KEY,
        user_id TEXT,
        job_id TEXT,
        score REAL,
        reasons TEXT,
        created_at TEXT
    );

    CREATE TABLE IF NOT EXISTS applications(
        id TEXT PRIMARY KEY,
        user_id TEXT,
        job_id TEXT,
        status TEXT,
        resume_text TEXT,
        cover_letter TEXT,
        created_at TEXT
    );
    """)
    c.commit()
    c.close()

init_db()
@app.get("/")
def inicio():
    return {"mensaje": "🤖 Agente de empleo-IA funcionando correctamente"}
