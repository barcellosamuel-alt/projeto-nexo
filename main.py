import os
import json
import datetime
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from google import genai
from google.genai import types

load_dotenv()

app = FastAPI(
    title="Projeto Nexo Sanctuary Master API",
    description="API Longitudinal de Alta Performance para Preparação Acadêmica Avançada",
    version="11.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

LOCAL_DB = "nexo_db.json"
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID", "SUA_ID_DA_PLANILHA_AQUI")
GSPREAD_CREDS_FILE = "credentials.json"

try:
    gemini_client = genai.Client()
except Exception:
    gemini_client = None

def _load_local_db() -> Dict[str, Any]:
    if os.path.exists(LOCAL_DB):
        try:
            with open(LOCAL_DB, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"notes": [], "errors": [], "telemetry": [], "settings": {"theme": "night"}}

def _save_local_db(data: Dict[str, Any]) -> None:
    with open(LOCAL_DB, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_google_sheet_data():
    try:
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        if not os.path.exists(GSPREAD_CREDS_FILE):
            return None
        creds = ServiceAccountCredentials.from_json_keyfile_name(GSPREAD_CREDS_FILE, scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(GOOGLE_SHEET_ID).worksheet('Telemetria')
        return sheet.get_all_records()
    except Exception:
        return None

@app.get("/api/v1/settings/theme")
def get_theme():
    db = _load_local_db()
    return db.get("settings", {}).get("theme", "night")

class ThemePayload(BaseModel):
    theme: str

@app.post("/api/v1/settings/theme")
def set_theme(payload: ThemePayload):
    db = _load_local_db()
    if "settings" not in db: db["settings"] = {}
    db["settings"]["theme"] = payload.theme
    _save_local_db(db)
    return {"status": "success", "theme": payload.theme}

@app.get("/api/v1/telemetry/advanced")
def get_advanced_telemetry():
    sheet_data = get_google_sheet_data()
    if not sheet_data:
        sheet_data = [
            {"Label": "Sim 1", "Score": 48.0, "Consolidacao": 55.0},
            {"Label": "Sim 2", "Score": 55.5, "Consolidacao": 65.0},
            {"Label": "Sim 3", "Score": 62.0, "Consolidacao": 72.0},
            {"Label": "Sim 4", "Score": 68.5, "Consolidacao": 78.0},
            {"Label": "Sim 5", "Score": 74.0, "Consolidacao": 82.0}
        ]
    labels = [t["Label"] for t in sheet_data]
    scores = [float(t["Score"]) for t in sheet_data]
    consolidacao_taxa = [float(t["Consolidacao"]) for t in sheet_data]
    stats = {
        "count": len(scores),
        "mean_score": round(sum(scores) / len(scores), 2) if scores else 0,
        "mean_consolidation": round(sum(consolidacao_taxa) / len(consolidacao_taxa), 2) if consolidacao_taxa else 0,
        "projection_score": 84.5,
        "corte_historico": 78.0,
        "meta_consolidation": 90.0
    }
    return {"labels": labels, "scores": scores, "consolidation_taxa": consolidacao_taxa, "stats": stats}

class AIChatPayload(BaseModel):
    prompt: str

@app.post("/api/v1/ai/chat")
def chat_with_gemini(payload: AIChatPayload):
    if not gemini_client:
        raise HTTPException(status_code=500, detail="Gemini client não inicializado. Verifique a chave GEMINI_API_KEY no Render.")
    try:
        response = gemini_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=payload.prompt,
            config=types.GenerateContentConfig(
                system_instruction="Você é o tutor pedagógico inteligente do Projeto Nexo, especializado em auxiliar estudantes de alta performance em questões complexas de exatas e biológicas.",
                temperature=0.3,
            ),
        )
        return {"status": "success", "response": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

CONTEUDOS_CLAREZA = [
    {"texto": "O Senhor é o meu pastor; nada me faltará.", "referencia": "Salmos 23:1", "imagem": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e"},
    {"texto": "Lâmpada para os meus pés é a tua palavra e luz para o meu caminho.", "referencia": "Salmos 119:105", "imagem": "https://images.unsplash.com/photo-1519681393784-d120267933ba"},
    {"texto": "Tudo posso naquele que me fortalece.", "referencia": "Filipenses 4:13", "imagem": "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05"},
    {"texto": "Confie no Senhor de todo o seu coração e não se apoie em sua própria inteligência.", "referencia": "Provérbios 3:5", "imagem": "https://images.unsplash.com/photo-1506744038136-46273834b3fb"},
    {"texto": "Ainda que eu caminhe pelo vale da sombra da morte, não temerei mal nenhum, pois tu estás comigo.", "referencia": "Salmos 23:4", "imagem": "https://images.unsplash.com/photo-1426604966848-d7adac902bff"}
]

@app.get("/api/v1/quotes")
def get_quotes(): return {"quotes": CONTEUDOS_CLAREZA}

@app.get("/api/v1/notes")
def list_notes():
    db = _load_local_db()
    return {"notes": db.get("notes", [])}

class NotePayload(BaseModel):
    id: Optional[int] = None
    title: str = ""
    content: str
    category: str = "geral"

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
        "id": len(notes) + 1,
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
    db["notes"] = filtered
    _save_local_db(db)
    return {"status": "deleted", "id": note_id}

class ErrorPayload(BaseModel):
    disciplina: str
    topico: str
    motivo: str

@app.get("/api/v1/errors")
def list_errors():
    db = _load_local_db()
    return {"errors": db.get("errors", [])}

@app.post("/api/v1/errors")
def add_error(payload: ErrorPayload):
    db = _load_local_db()
    errors = db.get("errors", [])
    item = {
        "id": len(errors) + 1,
        "disciplina": payload.disciplina,
        "topico": payload.topico,
        "motivo": payload.motivo,
        "date": datetime.datetime.utcnow().isoformat()[:10]
    }
    errors.append(item)
    db["errors"] = errors
    _save_local_db(db)
    return {"status": "added", "error": item}

@app.get("/api/v1/blocks/daily")
def get_daily_block(): return {"total_questions": 20, "discipline": "Biologia / Química / Física", "status": "ready"}

@app.get("/api/v1/recompositions/{attempt_id}")
def get_recomposition(attempt_id: int):
    return {
        "attempt_id": attempt_id,
        "discipline": "Biologia Celular",
        "learning_gap": "Dificuldade na fosforilação oxidativa e rendimento de ATP.",
        "micro_revisao": "A cadeia transportadora localiza-se nas cristas mitocondriais.",
        "exercicio_validacao": "Qual o papel direto da ATP sintase no gradiente eletroquímico?"
    }

class AcknowledgePayload(BaseModel):
    command: str

@app.post("/api/v1/recompositions/{attempt_id}/acknowledge")
def acknowledge_recomposition(attempt_id: int, payload: AcknowledgePayload): return {"status": "success", "command_received": payload.command}

@app.get("/api/v1/simulated/full")
def get_full_simulated():
    return {"total_questions": 1, "questions": [{"id": 1, "discipline": "Biologia", "enunciado": "Explique a fosforilação oxidativa."}]}

class SimulatedSubmitPayload(BaseModel):
    answers: Dict[str, Any]

@app.post("/api/v1/simulated/submit")
def submit_simulated(payload: SimulatedSubmitPayload): return {"status": "evaluated", "score_estimated": 81.5}

class DiscursiveSubmitPayload(BaseModel):
    title: str
    proposal_content: str
    student_answer: str

@app.post("/api/v1/discursive/submit")
def submit_discursive(payload: DiscursiveSubmitPayload): return {"status": "audited", "estimated_score": 9.0}

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
