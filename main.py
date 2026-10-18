import os
import io
import gspread
from google.oauth2.service_account import Credentials
from google import genai
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any

load_dotenv()

app = FastAPI(
    title="Projeto Nexo Sanctuary Master API",
    description="API Longitudinal para Preparação Medicina UEL",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SCOPES_SHEETS = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
CREDENTIALS_FILE = "credentials.json"
SPREADSHEET_ID = os.getenv("GOOGLE_SHEET_ID")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client_ai = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None

def conectar_servicos():
    creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES_SHEETS)
    gc = gspread.authorize(creds)
    sheet = gc.open_by_key(SPREADSHEET_ID)
    drive_service = build('drive', 'v3', credentials=creds)
    return sheet, drive_service

# --- ROTA PRINCIPAL: Serve a Interface Gráfica do index.html ---
@app.get("/", response_class=HTMLResponse)
def read_root():
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return """
        <html>
            <head><title>Projeto Nexo</title></head>
            <body style="font-family:sans-serif; background:#060911; color:#fff; text-align:center; padding-top:50px;">
                <h1>Projeto Nexo Sanctuary Master API</h1>
                <p>O arquivo <b>index.html</b> não foi encontrado na raiz do projeto. Por favor, envie-o para o repositório.</p>
            </body>
        </html>
        """

# --- ROTAS DA API ---
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
    return {
        "status": "success",
        "attempt_id": attempt_id,
        "command_received": payload.command,
        "message": "Leitura consolidada com sucesso."
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
                "alternatives": ["Alt A", "Alt B", "Alt C", "Alt D"]
            }
        ]
    }

class SimulatedSubmitPayload(BaseModel):
    answers: Dict[str, Any]

@app.post("/api/v1/simulated/submit")
def submit_simulated(payload: SimulatedSubmitPayload):
    return {
        "status": "evaluated",
        "score_estimated": 78.5,
        "feedback": "Simulado avaliado com sucesso sob os critérios COPS/UEL."
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
        "feedback": "Argumentação científica coerente com o padrão UEL."
    }
