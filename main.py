import os
import json
import datetime
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Projeto Nexo Sanctuary Master API",
    description="API Longitudinal de Alta Performance para Preparação Medicina UEL — Python 3",
    version="6.8.0"
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
    return {"notes": [], "telemetry": []}

def _save_local_db(data: Dict[str, Any]) -> None:
    with open(LOCAL_DB, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

CONTEUDOS_CLAREZA = [
    {
        "texto": "O Senhor é o meu pastor; nada me faltará.",
        "referencia": "Salmos 23:1",
        "imagem": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e"
    },
    {
        "texto": "Lâmpada para os meus pés é a tua palavra e luz para o meu caminho.",
        "referencia": "Salmos 119:105",
        "imagem": "https://images.unsplash.com/photo-1519681393784-d120267933ba"
    },
    {
        "texto": "Tudo posso naquele que me fortalece.",
        "referencia": "Filipenses 4:13",
        "imagem": "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05"
    },
    {
        "texto": "Confie no Senhor de todo o seu coração e não se apoie em sua própria inteligência.",
        "referencia": "Provérbios 3:5",
        "imagem": "https://images.unsplash.com/photo-1506744038136-46273834b3fb"
    },
    {
        "texto": "Ainda que eu caminhe pelo vale da sombra da morte, não temerei mal nenhum, pois tu estás comigo.",
        "referencia": "Salmos 23:4",
        "imagem": "https://images.unsplash.com/photo-1426604966848-d7adac902bff"
    }
]

@app.get("/api/v1/quotes")
def get_quotes():
    return {"quotes": CONTEUDOS_CLAREZA}

class NotePayload(BaseModel):
    id: Optional[int] = None
    title: str = ""
    content: str
    category: str = "geral"

@app.get("/api/v1/notes")
def list_notes():
    db = _load_local_db()
    return {"notes": db.get("notes", [])}

@app.post("/api/v1/notes")
def save_note(payload: NotePayload):
    db = _load_local_db()
    notes = db.get("notes", [])
    if payload.id:
        for n in notes:
            if n["id"] == payload.id:
                n["title"] = payload.title
                n["content"] = payload.content
                n["category"] = payload.category
                n["updated_at"] = datetime.datetime.utcnow().isoformat() + "Z"
                _save_local_db(db)
                return {"status": "updated", "note": n}
    
    new_note = {
        "id": len(notes) + 1 if not notes else max(n["id"] for n in notes) + 1,
        "title": payload.title,
        "content": payload.content,
        "category": payload.category,
        "created_at": datetime.datetime.utcnow().isoformat() + "Z",
    }
    notes.append(new_note)
    db["notes"] = notes
    _save_local_db(db)
    return {"status": "created", "note": new_note}

@app.delete("/api/v1/notes/{note_id}")
def delete_note(note_id: int):
    db = _load_local_db()
    notes = db.get("notes", [])
    filtered = [n for n in notes if n["id"] != note_id]
    if len(filtered) == len(notes):
        raise HTTPException(status_code=404, detail="Nota não encontrada.")
    db["notes"] = filtered
    _save_local_db(db)
    return {"status": "deleted", "id": note_id}

@app.get("/api/v1/telemetry")
def get_telemetry():
    db = _load_local_db()
    telemetry = db.get("telemetry", [])
    if not telemetry:
        telemetry = [
            {"label": "Sim 1", "score": 49.5},
            {"label": "Sim 2", "score": 57.0},
            {"label": "Sim 3", "score": 63.5},
            {"label": "Sim 4", "score": 70.0},
            {"label": "Sim 5 (Atual)", "score": 76.5}
        ]
        db["telemetry"] = telemetry
        _save_local_db(db)
    
    scores = [t["score"] for t in telemetry]
    stats = {
        "count": len(scores),
        "mean": round(sum(scores) / len(scores), 2) if scores else 0,
        "min": min(scores) if scores else 0,
        "max": max(scores) if scores else 0,
        "projection": 86.0,
        "corte_uel": 78.0
    }
    return {"telemetry": telemetry, "stats": stats}

@app.get("/api/v1/blocks/daily")
def get_daily_block():
    return {
        "total_questions": 20,
        "discipline": "Biologia / Química / Física (Foco Medicina UEL)",
        "status": "ready",
        "questoes": [
            {"id": 1, "enunciado": "Questão 1: Sobre citoesqueleto e transporte axonal...", "gabarito": "Letra C"},
            {"id": 2, "enunciado": "Questão 2: Termoquímica aplicada a ciclos metabólicos...", "gabarito": "Letra A"}
        ]
    }

@app.get("/api/v1/recompositions/{attempt_id}")
def get_recomposition(attempt_id: int):
    return {
        "attempt_id": attempt_id,
        "discipline": "Biologia Celular",
        "learning_gap": "Dificuldade na fosforilação oxidativa e rendimento de ATP nas cristas mitocondriais.",
        "micro_revisao": "A cadeia transportadora de elétrons localiza-se nas cristas mitocondriais, gerando gradiente de prótons.",
        "exercicio_validacao": "Qual o papel direto da ATP sintase no gradiente eletroquímico?"
    }

class AcknowledgePayload(BaseModel):
    command: str

@app.post("/api/v1/recompositions/{attempt_id}/acknowledge")
def acknowledge_recomposition(attempt_id: int, payload: AcknowledgePayload):
    return {"status": "success", "command_received": payload.command, "mensagem": "Recomposição assimilada com sucesso."}

@app.get("/api/v1/simulated/full")
def get_full_simulated():
    return {
        "total_questions": 60,
        "questions": [
            {"id": 1, "discipline": "Biologia", "enunciado": "Explique detalhadamente a fosforilação oxidativa e o balanço energético."},
            {"id": 2, "discipline": "Química", "enunciado": "Determine a constante de equilíbrio para o sistema gasoso em condições fisiológicas."}
        ]
    }

class SimulatedSubmitPayload(BaseModel):
    answers: Dict[str, Any]

@app.post("/api/v1/simulated/submit")
def submit_simulated(payload: SimulatedSubmitPayload):
    return {"status": "evaluated", "score_estimated": 82.5, "mensagem": "Simulado avaliado com sucesso perante os critérios COPS-UEL."}

class DiscursiveSubmitPayload(BaseModel):
    title: str
    proposal_content: str
    student_answer: str

@app.post("/api/v1/discursive/submit")
def submit_discursive(payload: DiscursiveSubmitPayload):
    return {"status": "audited", "estimated_score": 9.2, "feedback": "Excelente fundamentação teórica e clareza na argumentação discursiva."}

@app.get("/", response_class=HTMLResponse)
def read_root():
    for caminho in ["index.html", "app/index.html", "../index.html"]:
        if os.path.exists(caminho):
            with open(caminho, "r", encoding="utf-8") as f:
                return f.read()
    return "<h1>index.html não encontrado</h1>"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
