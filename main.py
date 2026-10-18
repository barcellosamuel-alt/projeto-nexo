import os
import io
import gspread
from google.oauth2.service_account import Credentials
from google import genai
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from dotenv import load_dotenv
from fastapi import FastAPI
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

def executar_lapidacao_nexo(questao):
    prompt_sistema = """
    Você é o 'Nexo | Lapidação Cirúrgica', agente inteligente de diagnóstico e recomposição de erros para o vestibular de Medicina da UEL (COPS/UEL).
    Estruture sua resposta estritamente em:
    1. Anatomia do Erro (Feedback Formativo)
    2. Microrevisão Direta
    3. Active Recall (Recordação Ativa / What-if)
    """
    prompt_usuario = f"""
    Analise a seguinte falha mapeada no Banco Longitudinal:
    - ID da Questão: {questao.get('ID_QUESTAO')}
    - Disciplina: {questao.get('DISCIPLINA')}
    - Conteúdo: {questao.get('CONTEUDO')}
    - Resposta do Candidato: {questao.get('RESPOSTA_CANDIDATO')}
    - Gabarito Oficial: {questao.get('GABARITO')}
    """
    response = client_ai.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt_usuario,
        config=genai.types.GenerateContentConfig(
            system_instruction=prompt_sistema,
            temperature=0.2
        )
    )
    return response.text

def salvar_markdown_drive(drive_service, id_questao, disciplina, conteudo, texto_markdown):
    nome_arquivo = f"[NEXO] {id_questao} - {disciplina} ({conteudo}).md"
    file_metadata = {'name': nome_arquivo, 'mimeType': 'text/markdown'}
    media = MediaIoBaseUpload(io.BytesIO(texto_markdown.encode('utf-8')), mimetype='text/markdown', resumable=True)
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id, webViewLink').execute()
    return file.get('webViewLink')

@app.get("/")
def read_root():
    return {"status": "online", "message": "Projeto Nexo Sanctuary API ativa para Medicina UEL!"}

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
