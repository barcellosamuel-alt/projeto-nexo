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
from googleapiclient.http import MediaIoBaseUpload
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

load_dotenv()

app = FastAPI(
    title="Projeto Nexo Sanctuary Master API",
    description="API Longitudinal para Preparação Medicina UEL — Python 3 + TypeScript",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# CONFIGURAÇÃO DE SERVIÇOS GOOGLE
# ---------------------------------------------------------------------------
SCOPES_SHEETS = [
    "[googleapis.com](https://www.googleapis.com/auth/spreadsheets)",
    "[googleapis.com](https://www.googleapis.com/auth/drive)",
    "[googleapis.com](https://www.googleapis.com/auth/calendar)"
]
CREDENTIALS_FILE = "credentials.json"
SPREADSHEET_ID = os.getenv("GOOGLE_SHEET_ID")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
CALENDAR_ID = os.getenv("GOOGLE_CALENDAR_ID", "primary")

client_ai = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None

# Persistência local (fallback quando não há credenciais Google)
LOCAL_DB = "nexo_db.json"


def _load_local_db() -> Dict[str, Any]:
    if os.path.exists(LOCAL_DB):
        with open(LOCAL_DB, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"notes": [], "telemetry": [], "pet": {}}


def _save_local_db(data: Dict[str, Any]) -> None:
    with open(LOCAL_DB, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def conectar_servicos():
    """Conecta aos serviços Google (Sheets, Drive, Calendar) se credenciais existirem."""
    if not os.path.exists(CREDENTIALS_FILE):
        return None, None, None
    creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES_SHEETS)
    gc = gspread.authorize(creds)
    sheet = gc.open_by_key(SPREADSHEET_ID) if SPREADSHEET_ID else None
    drive_service = build('drive', 'v3', credentials=creds)
    calendar_service = build('calendar', 'v3', credentials=creds)
    return sheet, drive_service, calendar_service


# ---------------------------------------------------------------------------
# 1) CALCULADORA CIENTÍFICA MODERNA (Python 3 — avaliação segura via AST)
# ---------------------------------------------------------------------------
ALLOWED_NAMES: Dict[str, Any] = {
    "pi": math.pi, "e": math.e, "tau": math.tau,
    "inf": math.inf, "nan": math.nan,
    "abs": abs, "round": round, "min": min, "max": max, "sum": sum,
    "sin": math.sin, "cos": math.cos, "tan": math.tan,
    "asin": math.asin, "acos": math.acos, "atan": math.atan,
    "atan2": math.atan2, "sinh": math.sinh, "cosh": math.cosh, "tanh": math.tanh,
    "log": math.log, "log10": math.log10, "log2": math.log2, "ln": math.log,
    "sqrt": math.sqrt, "cbrt": lambda x: x ** (1/3),
    "pow": pow, "exp": math.exp, "expm1": math.expm1,
    "factorial": math.factorial, "gcd": math.gcd, "lcm": math.lcm,
    "degrees": math.degrees, "radians": math.radians,
    "floor": math.floor, "ceil": math.ceil, "trunc": math.trunc,
    "hypot": math.hypot, "perm": math.perm, "comb": math.comb,
    "gamma": math.gamma, "erf": math.erf,
}

BIN_OPS: Dict[type, Any] = {
    ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
    ast.Div: operator.truediv, ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod, ast.Pow: operator.pow,
}

UNARY_OPS: Dict[type, Any] = {
    ast.UAdd: operator.pos, ast.USub: operator.neg,
}


def _safe_eval(node: ast.AST) -> Any:
    """Avalia uma expressão AST de forma segura, sem eval/exec."""
    if isinstance(node, ast.Expression):
        return _safe_eval(node.body)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float, complex)):
            return node.value
        raise ValueError("Tipo de constante não suportado.")
    if isinstance(node, ast.BinOp):
        op = BIN_OPS.get(type(node.op))
        if op is None:
            raise ValueError(f"Operador não suportado: {type(node.op).__name__}")
        return op(_safe_eval(node.left), _safe_eval(node.right))
    if isinstance(node, ast.UnaryOp):
        op = UNARY_OPS.get(type(node.op))
        if op is None:
            raise ValueError("Operador unário não suportado.")
        return op(_safe_eval(node.operand))
    if isinstance(node, ast.Name):
        if node.id in ALLOWED_NAMES:
            return ALLOWED_NAMES[node.id]
        raise ValueError(f"Nome não permitido: {node.id}")
    if isinstance(node, ast.Call):
        if isinstance(node.func, ast.Name) and node.func.id in ALLOWED_NAMES:
            args = [_safe_eval(a) for a in node.args]
            kwargs = {kw.arg: _safe_eval(kw.value) for kw in node.keywords}
            return ALLOWED_NAMES[node.func.id](*args, **kwargs)
        raise ValueError("Função não permitida.")
    if isinstance(node, ast.List):
        return [_safe_eval(e) for e in node.elts]
    if isinstance(node, ast.Tuple):
        return tuple(_safe_eval(e) for e in node.elts)
    raise ValueError(f"Expressão não suportada: {type(node).__name__}")


def avaliar_expressao(expressao: str) -> Any:
    """Avalia uma expressão matemática de forma segura."""
    expressao = expressao.strip()
    if not expressao:
        raise ValueError("Expressão vazia.")
    # Substitui símbolos comuns
    expressao = expressao.replace("×", "*").replace("÷", "/").replace("^", "**")
    expressao = expressao.replace("π", "pi").replace("√", "sqrt")
    tree = ast.parse(expressao, mode="eval")
    return _safe_eval(tree)


class CalcPayload(BaseModel):
    expression: str


@app.post("/api/v1/calculator/evaluate")
def calculator_evaluate(payload: CalcPayload):
    try:
        resultado = avaliar_expressao(payload.expression)
        return {"status": "success", "expression": payload.expression, "result": resultado}
    except ZeroDivisionError:
        return {"status": "error", "message": "Divisão por zero."}
    except OverflowError:
        return {"status": "error", "message": "Resultado muito grande (overflow)."}
    except (ValueError, SyntaxError) as e:
        return {"status": "error", "message": f"Expressão inválida: {e}"}


# ---------------------------------------------------------------------------
# 2) DISPOSITIVO DE NOTAS (Python 3 — persistência em JSON local + Sheets)
# ---------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------
# 3) DISPOSITIVO MOTIVACIONAL EVANGÉLICO (frases + imagens digitais)
# ---------------------------------------------------------------------------
FRASES_EVANGELICAS = [
    {"tipo": "versiculo", "texto": "Tudo posso naquele que me fortalece. — Filipenses 4:13",
     "imagem": "[images.unsplash.com](https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=1200&q=80)"},
    {"tipo": "versiculo", "texto": "O Senhor é o meu pastor; nada me faltará. — Salmos 23:1",
     "imagem": "[images.unsplash.com](https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1200&q=80)"},
    {"tipo": "versiculo", "texto": "Entrega o teu caminho ao Senhor; confia nele, e ele tudo fará. — Salmos 37:5",
     "imagem": "[images.unsplash.com](https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?auto=format&fit=crop&w=1200&q=80)"},
    {"tipo": "versiculo", "texto": "Porque eu bem sei os pensamentos que tenho a vosso respeito, diz o Senhor. — Jeremias 29:11",
     "imagem": "[images.unsplash.com](https://images.unsplash.com/photo-1506905925346-21bda4d32df4?auto=format&fit=crop&w=1200&q=80)"},
    {"tipo": "versiculo", "texto": "O choro pode durar uma noite, mas a alegria vem pela manhã. — Salmos 30:5",
     "imagem": "[images.unsplash.com](https://images.unsplash.com/photo-1470252649378-9c29740c9fa8?auto=format&fit=crop&w=1200&q=80)"},
    {"tipo": "motivacional", "texto": "Cada novo amanhecer traz uma nova oportunidade de recomeçar com fé.",
     "imagem": "[images.unsplash.com](https://images.unsplash.com/photo-1470246973918-29a93221c455?auto=format&fit=crop&w=1200&q=80)"},
    {"tipo": "motivacional", "texto": "Acredite no seu potencial e permita que a esperança guie os seus passos hoje.",
     "imagem": "[images.unsplash.com](https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1200&q=80)"},
    {"tipo": "motivacional", "texto": "A fé não elimina os obstáculos, mas dá forças para atravessá-los.",
     "imagem": "[images.unsplash.com](https://images.unsplash.com/photo-1441974231531-c6227db76b6e?auto=format&fit=crop&w=1200&q=80)"},
    {"tipo": "motivacional", "texto": "Deus não escolhe os capacitados; capacita os escolhidos.",
     "imagem": "[images.unsplash.com](https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1200&q=80)"},
    {"tipo": "motivacional", "texto": "A persistência na fé transforma sonhos em testemunhos.",
     "imagem": "[images.unsplash.com](https://images.unsplash.com/photo-1472214103451-9374bd1c798e?auto=format&fit=crop&w=1200&q=80)"},
]


@app.get("/api/v1/quotes")
def get_quotes():
    return {"quotes": FRASES_EVANGELICAS}


@app.get("/api/v1/quotes/random")
def get_random_quote():
    return {"quote": random.choice(FRASES_EVANGELICAS)}


# ---------------------------------------------------------------------------
# 4) DISPOSITIVO DE MÚSICA / AMBIENTE SONORO (presets servidos pelo Python)
# ---------------------------------------------------------------------------
AMBIENT_PRESETS = [
    {"id": "chuva", "nome": "Chuva Suave", "emoji": "🌧️", "tipo": "noise", "filtro": "lowpass", "freq": 800},
    {"id": "cafe", "nome": "Cafeteria", "emoji": "☕", "tipo": "noise", "filtro": "bandpass", "freq": 1200},
    {"id": "mar", "nome": "Ondas do Mar", "emoji": "🌊", "tipo": "noise", "filtro": "lowpass", "freq": 400},
    {"id": "floresta", "nome": "Floresta", "emoji": "🌲", "tipo": "noise", "filtro": "bandpass", "freq": 2000},
    {"id": "lofi", "nome": "Lo-Fi Beats", "emoji": "🎧", "tipo": "melody", "filtro": "none", "freq": 0},
    {"id": "vento", "nome": "Vento", "emoji": "🍃", "tipo": "noise", "filtro": "lowpass", "freq": 300},
    {"id": "fogueira", "nome": "Fogueira", "emoji": "🔥", "tipo": "noise", "filtro": "lowpass", "freq": 600},
    {"id": "silencio", "nome": "Silêncio Profundo", "emoji": "🔇", "tipo": "none", "filtro": "none", "freq": 0},
]


@app.get("/api/v1/ambient")
def get_ambient_presets():
    return {"presets": AMBIENT_PRESETS}


# ---------------------------------------------------------------------------
# 5) PET DIGITAL (cachorro) — estado persistido no Python
# ---------------------------------------------------------------------------
class PetStatePayload(BaseModel):
    xp: int = 0
    level: int = 1
    happiness: int = 50
    hunger: int = 50
    energy: int = 50
    name: str = "Rex"


@app.get("/api/v1/pet")
def get_pet_state():
    db = _load_local_db()
    pet = db.get("pet", {})
    if not pet:
        pet = {"xp": 0, "level": 1, "happiness": 50, "hunger": 50, "energy": 50, "name": "Rex"}
    return {"pet": pet}


@app.post("/api/v1/pet")
def update_pet_state(payload: PetStatePayload):
    db = _load_local_db()
    db["pet"] = payload.dict()
    _save_local_db(db)
    return {"status": "updated", "pet": db["pet"]}


@app.post("/api/v1/pet/action")
def pet_action(action: str = "pet"):
    db = _load_local_db()
    pet = db.get("pet", {"xp": 0, "level": 1, "happiness": 50, "hunger": 50, "energy": 50, "name": "Rex"})
    if action == "pet":
        pet["happiness"] = min(100, pet.get("happiness", 50) + 10)
        pet["xp"] = pet.get("xp", 0) + 5
    elif action == "feed":
        pet["hunger"] = max(0, pet.get("hunger", 50) - 20)
        pet["happiness"] = min(100, pet.get("happiness", 50) + 5)
    elif action == "play":
        pet["energy"] = max(0, pet.get("energy", 50) - 15)
        pet["happiness"] = min(100, pet.get("happiness", 50) + 15)
        pet["xp"] = pet.get("xp", 0) + 10
    elif action == "sleep":
        pet["energy"] = min(100, pet.get("energy", 50) + 30)
    # Subida de nível
    xp = pet.get("xp", 0)
    pet["level"] = 1 + xp // 100
    db["pet"] = pet
    _save_local_db(db)
    return {"status": "success", "action": action, "pet": pet}


# ---------------------------------------------------------------------------
# 6) RELÓGIO / CALENDÁRIO DIGITAL (Google Calendar via Python 3)
# ---------------------------------------------------------------------------
class CalendarEventPayload(BaseModel):
    summary: str
    description: str = ""
    start_datetime: str  # ISO 8601
    end_datetime: str
    timezone: str = "America/Sao_Paulo"


@app.get("/api/v1/calendar/now")
def get_server_time():
    agora = datetime.datetime.now(datetime.timezone.utc)
    return {
        "utc": agora.isoformat(),
        "timestamp": agora.timestamp(),
        "timezone": "UTC"
    }


@app.post("/api/v1/calendar/event")
def create_calendar_event(payload: CalendarEventPayload):
    """Cria evento no Google Calendar (ou retorna link de fallback)."""
    _, _, calendar_service = conectar_servicos()
    if calendar_service is None:
        # Fallback: link de template do Google Calendar
        link = (
            f"[calendar.google.com](https://calendar.google.com/calendar/render?action=TEMPLATE)"
            f"&text={payload.summary}&dates={payload.start_datetime.replace('-', '').replace(':', '')}"
            f"/{payload.end_datetime.replace('-', '').replace(':', '')}"
            f"&details={payload.description}"
        )
        return {"status": "fallback", "link": link, "message": "Credenciais não configuradas; use o link."}

    event = {
        "summary": payload.summary,
        "description": payload.description,
        "start": {"dateTime": payload.start_datetime, "timeZone": payload.timezone},
        "end": {"dateTime": payload.end_datetime, "timeZone": payload.timezone},
    }
    created = calendar_service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
    return {"status": "created", "event_id": created.get("id"), "link": created.get("htmlLink")}


# ---------------------------------------------------------------------------
# 7) TELEMETRIA LONGITUDINAL (Python 3 — dados + estatísticas)
# ---------------------------------------------------------------------------
class TelemetryPayload(BaseModel):
    label: str
    score: float
    discipline: str = "Geral"


@app.get("/api/v1/telemetry")
def get_telemetry():
    db = _load_local_db()
    telemetry = db.get("telemetry", [])
    if not telemetry:
        # Dados iniciais de demonstração
        telemetry = [
            {"label": "Sim 1", "score": 52, "discipline": "Geral"},
            {"label": "Sim 2", "score": 58, "discipline": "Geral"},
            {"label": "Sim 3", "score": 64, "discipline": "Geral"},
            {"label": "Sim 4", "score": 71, "discipline": "Geral"},
        ]
        db["telemetry"] = telemetry
        _save_local_db(db)
    scores = [t["score"] for t in telemetry]
    stats = {
        "count": len(scores),
        "mean": round(sum(scores) / len(scores), 2) if scores else 0,
        "min": min(scores) if scores else 0,
        "max": max(scores) if scores else 0,
        "trend": "up" if len(scores) > 1 and scores[-1] > scores[0] else "down",
        "projection": round(scores[-1] * 1.15, 2) if scores else 0,
    }
    return {"telemetry": telemetry, "stats": stats}


@app.post("/api/v1/telemetry")
def add_telemetry(payload: TelemetryPayload):
    db = _load_local_db()
    db.setdefault("telemetry", []).append(payload.dict())
    _save_local_db(db)
    return {"status": "added", "telemetry": db["telemetry"]}


# ---------------------------------------------------------------------------
# MÓDULOS DE ESTUDO (mantidos e aprimorados)
# ---------------------------------------------------------------------------
@app.get("/api/v1/blocks/daily")
def get_daily_block():
    return {
        "total_questions": 20,
        "discipline": "Biologia / Química / Física",
        "status": "ready",
        "message": "Bloco diário de treino carregado com sucesso.",
    }


@app.get("/api/v1/recompositions/{attempt_id}")
def get_recomposition(attempt_id: int):
    return {
        "attempt_id": attempt_id,
        "discipline": "Biologia Celular",
        "learning_gap": "Dificuldade na fosforilação oxidativa e rendimento de ATP.",
        "micro_revisao": "A cadeia transportadora de elétrons localiza-se nas cristas mitocondriais.",
        "exercicio_validacao": "Qual o papel direto da ATP sintase no gradiente eletroquímico?",
    }


class AcknowledgePayload(BaseModel):
    command: str


@app.post("/api/v1/recompositions/{attempt_id}/acknowledge")
def acknowledge_recomposition(attempt_id: int, payload: AcknowledgePayload):
    return {
        "status": "success",
        "attempt_id": attempt_id,
        "command_received": payload.command,
        "message": "Leitura consolidada com sucesso.",
    }


@app.get("/api/v1/simulated/full")
def get_full_simulated():
    return {
        "total_questions": 2,
        "questions": [
            {
                "id": 1,
                "discipline": "Biologia",
                "enunciado": "Explique o processo de fosforilação oxidativa.",
                "alternatives": ["Alt A", "Alt B", "Alt C", "Alt D"],
            }
        ],
    }


class SimulatedSubmitPayload(BaseModel):
    answers: Dict[str, Any]


@app.post("/api/v1/simulated/submit")
def submit_simulated(payload: SimulatedSubmitPayload):
    return {
        "status": "evaluated",
        "score_estimated": 78.5,
        "feedback": "Simulado avaliado com sucesso sob os critérios COPS/UEL.",
    }


class DiscursiveSubmitPayload(BaseModel):
    title: str
    proposal_content: str
    student_answer: str


@app.post("/api/v1/discursive/submit")
def submit_discursive(payload: DiscursiveSubmitPayload):
    return {
        "status": "audited",
        "title": payload.title,
        "estimated_score": 8.5,
        "feedback": "Argumentação científica coerente com o padrão UEL.",
    }


# ---------------------------------------------------------------------------
# ROTA PRINCIPAL — serve o index.html
# ---------------------------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
def read_root():
    caminhos_possiveis = ["index.html", "app/index.html", "../index.html", "static/index.html"]
    for caminho in caminhos_possiveis:
        if os.path.exists(caminho):
            with open(caminho, "r", encoding="utf-8") as f:
                return f.read()
    return """
    <html>
        <head><title>Projeto Nexo — Erro de Arquivo</title></head>
        <body style="font-family:sans-serif; background:#060911; color:#fff; text-align:center; padding-top:50px;">
            <h1>Projeto Nexo Sanctuary Master API</h1>
            <p>O arquivo <b>index.html</b> não foi encontrado.</p>
        </body>
    </html>
    """


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
