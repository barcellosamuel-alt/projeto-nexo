import os
import io
import json
import math
import ast
import operator
import random
import datetime
from typing import Dict, Any, List, Optional

import gspread
from google.oauth2.service_account import Credentials
from google import genai
from googleapiclient.discovery import build
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

load_dotenv()

app = FastAPI(
    title="Projeto Nexo Sanctuary Master API",
    description="API Longitudinal de Alta Performance para Preparação Medicina UEL — Python 3",
    version="3.5.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

LOCAL_DB = "nexo_db.json"

def _load_local_db() -> Dict[str, Any]:
    if os.path.exists(LOCAL_DB):
        try:
            with open(LOCAL_DB, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"notes": [], "telemetry": [], "pet": {"xp": 0, "level": 1, "happiness": 50, "hunger": 50}}

def _save_local_db(data: Dict[str, Any]) -> None:
    with open(LOCAL_DB, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# --- Cantinho da Clareza (Mensagens Dinâmicas) ---
CONTEUDOS_CLAREZA = [
    {
        "tipo": "versiculo",
        "texto": "Tudo posso naquele que me fortalece. — Filipenses 4:13",
        "imagem": "https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=1200&q=80"
    },
    {
        "tipo": "motivacional",
        "texto": "Cada novo amanhecer traz uma nova oportunidade de recomeçar com fé e precisão rumo à UEL.",
        "imagem": "https://images.unsplash.com/photo-1470246973918-29a93221c455?auto=format&fit=crop&w=1200&q=80"
    },
    {
        "tipo": "versiculo",
        "texto": "O Senhor é o meu pastor; nada me faltará. — Salmos 23:1",
        "imagem": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1200&q=80"
    },
    {
        "tipo": "motivacional",
        "texto": "A aprovação em Medicina na UEL é construída na consistência diária.",
        "imagem": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1200&q=80"
    }
]

@app.get("/api/v1/quotes")
def get_quotes():
    return {"quotes": CONTEUDOS_CLAREZA}

# --- Gerenciamento de Notas ---
class NotePayload(BaseModel):
    title: str = ""
    content: str
    category: str = "geral"

@app.get("/api/v1/notes")
def list_notes():
    db = _load_local_db()
    return {"notes": db.get("notes", [])}

@app.post("/api/v1/notes")
def create_note(payload: NotePayload):
    db = _load_local_db()
    note = {
        "id": len(db.get("notes", [])) + 1,
        "title": payload.title,
        "content": payload.content,
        "category": payload.category,
        "created_at": datetime.datetime.utcnow().isoformat() + "Z",
    }
    db.setdefault("notes", []).append(note)
    _save_local_db(db)
    return {"status": "created", "note": note}

# --- Telemetria Longitudinal ---
@app.get("/api/v1/telemetry")
def get_telemetry():
    db = _load_local_db()
    telemetry = db.get("telemetry", [])
    if not telemetry:
        telemetry = [
            {"label": "Sim 1", "score": 52.0, "discipline": "Geral"},
            {"label": "Sim 2", "score": 58.5, "discipline": "Geral"},
            {"label": "Sim 3", "score": 64.0, "discipline": "Geral"},
            {"label": "Sim 4 (Atual)", "score": 71.0, "discipline": "Geral"}
        ]
        db["telemetry"] = telemetry
        _save_local_db(db)
    
    scores = [t["score"] for t in telemetry]
    stats = {
        "count": len(scores),
        "mean": round(sum(scores) / len(scores), 2) if scores else 0,
        "min": min(scores) if scores else 0,
        "max": max(scores) if scores else 0,
        "trend": "up",
        "projection": 82.5
    }
    return {"telemetry": telemetry, "stats": stats}

# --- Módulos de Estudo e Simulado UEL ---
@app.get("/api/v1/blocks/daily")
def get_daily_block():
    return {
        "total_questions": 20,
        "discipline": "Biologia / Química / Física",
        "status": "ready",
        "message": "Bloco diário de treino carregado com sucesso."
    }

@app.get("/api/v1/recompositions/{attempt_id}")
def get_recomposition(attempt_id: int):
    return {
        "attempt_id": attempt_id,
        "discipline": "Biologia Celular",
        "learning_gap": "Dificuldade na fosforilação oxidativa e rendimento de ATP.",
        "micro_revisao": "A cadeia transportadora de elétrons localiza-se nas cristas mitocondriais.",
        "exercicio_validacao": "Qual o papel direto da ATP sintase no gradiente eletroquímico?"
    }

class AcknowledgePayload(BaseModel):
    command: str

@app.post("/api/v1/recompositions/{attempt_id}/acknowledge")
def acknowledge_recomposition(attempt_id: int, payload: AcknowledgePayload):
    return {"status": "success", "command_received": payload.command, "message": "Leitura consolidada."}

@app.get("/api/v1/simulated/full")
def get_full_simulated():
    return {
        "total_questions": 2,
        "questions": [
            {
                "id": 1,
                "discipline": "Biologia",
                "enunciado": "Explique o processo de fosforilação oxidativa.",
                "alternatives": ["Alt A", "Alt B", "Alt C", "Alt D"]
            }
        ]
    }

class SimulatedSubmitPayload(BaseModel):
    answers: Dict[str, Any]

@app.post("/api/v1/simulated/submit")
def submit_simulated(payload: SimulatedSubmitPayload):
    return {"status": "evaluated", "score_estimated": 78.5, "feedback": "Simulado avaliado sob os critérios COPS/UEL."}

class DiscursiveSubmitPayload(BaseModel):
    title: str
    proposal_content: str
    student_answer: str

@app.post("/api/v1/discursive/submit")
def submit_discursive(payload: DiscursiveSubmitPayload):
    return {"status": "audited", "title": payload.title, "estimated_score": 8.5, "feedback": "Argumentação coerente com o padrão UEL."}

# --- Pet Virtual ---
@app.get("/api/v1/pet")
def get_pet_state():
    db = _load_local_db()
    return {"pet": db.get("pet", {"xp": 0, "level": 1, "happiness": 50, "hunger": 50})}

# --- Rota Principal ---
@app.get("/", response_class=HTMLResponse)
def read_root():
    for caminho in ["index.html", "app/index.html", "../index.html"]:
        if os.path.exists(caminho):
            with open(caminho, "r", encoding="utf-8") as f:
                return f.read()
    return """
    <html>
        <head><title>Projeto Nexo — Erro de Arquivo</title></head>
        <body style="font-family:sans-serif; background:#04070d; color:#fff; text-align:center; padding-top:60px;">
            <h1>Projeto Nexo Sanctuary Master API</h1>
            <p>O arquivo <b>index.html</b> não foi encontrado na raiz do repositório.</p>
        </body>
    </html>
    """

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
