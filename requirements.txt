import os
import random
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any

load_dotenv()

app = FastAPI(
    title="Projeto Nexo Sanctuary Master API",
    description="API Longitudinal Avançada para Preparação Medicina UEL & Painel Cantinho da Clareza",
    version="3.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base de conteúdos dinâmicos para o Cantinho da Clareza (Item 5)
CONTEUDOS_CLAREZA = [
    {
        "tipo": "versiculo",
        "texto": "Tudo posso naquele que me fortalece. — Filipenses 4:13",
        "imagem": "https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=1200&q=80"
    },
    {
        "tipo": "motivacional",
        "texto": "Cada novo amanhecer traz uma nova oportunidade de recomeçar com fé e precisão cirúrgica rumo à UEL.",
        "imagem": "https://images.unsplash.com/photo-1470246973918-29a93221c455?auto=format&fit=crop&w=1200&q=80"
    },
    {
        "tipo": "versiculo",
        "texto": "O Senhor é o meu pastor; nada me faltará. — Salmos 23:1",
        "imagem": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1200&q=80"
    },
    {
        "tipo": "motivacional",
        "texto": "A aprovação em Medicina na UEL é construída na consistência diária e na superação de cada lacuna de conhecimento.",
        "imagem": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1200&q=80"
    }
]

@app.get("/", response_class=HTMLResponse)
def read_root():
    caminhos_possiveis = ["index.html", "app/index.html", "../index.html"]
    for caminho in caminhos_possiveis:
        if os.path.exists(caminho):
            try:
                with open(caminho, "r", encoding="utf-8") as f:
                    return f.read()
            except Exception as e:
                return f"<h1>Erro ao ler o index.html: {str(e)}</h1>"
    return """
    <html>
        <head><title>Projeto Nexo — Erro de Arquivo</title></head>
        <body style="font-family:sans-serif; background:#060911; color:#fff; text-align:center; padding-top:50px;">
            <h1>Projeto Nexo Sanctuary Master API</h1>
            <p>O arquivo <b>index.html</b> não foi encontrado nos diretórios verificados.</p>
        </body>
    </html>
    """

@app.get("/api/conteudo")
def get_conteudo():
    return CONTEUDOS_CLAREZA

@app.get("/api/v1/blocks/daily")
def get_daily_block():
    return {
        "total_questions": 20,
        "discipline": "Biologia / Química / Física",
        "status": "ready",
        "message": "Bloco diário de treino tático carregado com sucesso."
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

# --- Item 8: Telemetria Longitudinal Otimizada via Python 3 (Pandas/NumPy) ---
@app.get("/api/v1/telemetry/longitudinal")
def get_longitudinal_telemetry():
    dados_brutos = {
        "simulado": ["Sim 1", "Sim 2", "Sim 3", "Sim 4 (Atual)", "Projeção UEL"],
        "pontuacao": [52.0, 58.5, 64.0, 71.0, 82.5],
        "acertos_pct": [52, 58, 64, 71, 82.5]
    }
    df = pd.DataFrame(dados_brutos)
    
    media = float(df["pontuacao"].mean())
    desvio_padrao = float(df["pontuacao"].std(ddof=0))
    taxa_crescimento = float(df["pontuacao"].pct_change().mean() * 100)
    
    return {
        "status": "success",
        "labels": df["simulado"].tolist(),
        "scores": df["pontuacao"].tolist(),
        "analytics": {
            "media_geral": round(media, 2),
            "desvio_padrao": round(desvio_padrao, 2),
            "taxa_crescimento_media_pct": round(taxa_crescimento, 2),
            "status_preparacao": "Evolução acelerada compatível com corte UEL Medicina"
        }
    }
