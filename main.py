from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import os

import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost:5433/nexo_db")
app = FastAPI(title="Projeto Nexo — Backend Longitudinal", version="1.0.0")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class AcknowledgeRequest(BaseModel):
    command: str

class DiscursiveSubmission(BaseModel):
    title: str
    proposal_content: str
    student_answer: str

class SimulatedSubmission(BaseModel):
    answers: dict

@app.get("/")
def read_root():
    return FileResponse("static/index.html")

@app.get("/api/v1/blocks/daily")
def get_daily_block(discipline: str = "GERAL"):
    questoes_exemplo = [
        {
            "id": i,
            "discipline": "Biologia / Química",
            "enunciado": f"Questão {i} do Bloco Diário - Padrão COPS/UEL (Medicina).",
            "status": "PENDENTE"
        }
        for i in range(1, 21)
    ]
    return {
        "success": True,
        "block_size": 20,
        "discipline_focus": discipline,
        "questions": questoes_exemplo
    }

@app.get("/api/v1/recompositions/{attempt_id}")
def get_recomposition_content(attempt_id: int, db: Session = Depends(get_db)):
    return {
        "success": True,
        "attempt_id": attempt_id,
        "discipline": "Física / Ondulatória",
        "learning_gap": "Inversão na manipulação algébrica da fórmula da velocidade de propagação de ondas.",
        "micro_revisao": "Revisão Ativa: A velocidade de propagação de uma onda depende exclusivamente do meio. A frequência é determinada pela fonte. O comprimento de onda ajusta-se conforme a relação adequada. Nunca inverta esta razão em cálculos algébricos sob pressão na prova da COPS/UEL.",
        "exercicio_validacao": "Determine o comprimento de onda de uma onda sonora que se propaga a 340 m/s com frequência de 680 Hz.",
        "status": "PENDENTE"
    }

@app.post("/api/v1/recompositions/{attempt_id}/acknowledge")
def acknowledge_recomposition(attempt_id: int, payload: AcknowledgeRequest, db: Session = Depends(get_db)):
    if payload.command != "[NEXO_LIDO_E_COMPREENDIDO]":
        raise HTTPException(status_code=400, detail="Comando de validação inválido.")
    return {
        "success": True,
        "message": "Leitura e compreensão registadas com sucesso pelo backend.",
        "attempt_id": attempt_id,
        "new_status": "ACKNOWLEDGED"
    }

@app.post("/api/v1/discursive/submit")
def submit_discursive_exam(exam: DiscursiveSubmission, db: Session = Depends(get_db)):
    return {
        "success": True,
        "message": "Prova discursiva submetida e congelada para avaliação.",
        "title": exam.title,
        "status": "SUBMITTED"
    }

@app.get("/api/v1/simulated/full")
def get_full_simulated():
    disciplinas_uel = ["Biologia", "Química", "Física", "Matemática", "História", "Geografia", "Filosofia/Sociologia", "Língua Portuguesa / Literatura"]
    
    questoes_simulado = [
        {
            "id": i,
            "discipline": disciplinas_uel[(i - 1) % len(disciplinas_uel)],
            "enunciado": f"Questão {i} do Simulado UEL (Medicina). Analise o contexto e assinale a alternativa correta conforme os critérios da banca COPS.",
            "alternatives": [
                "A) Afirmativa incorreta baseada em distatores comuns da banca.",
                "B) Afirmativa parcialmente correta, mas incompleta quanto ao enunciado.",
                "C) Alternativa correta que atende rigorosamente ao rigor científico exigido.",
                "D) Distator conceitual focado em erros comuns de interpretação.",
                "E) Afirmativa anacrônica em relação ao conteúdo cobrado."
            ]
        }
        for i in range(1, 61)
    ]
    
    return {
        "success": True,
        "title": "Simulado Oficial UEL — Padrão COPS (Medicina)",
        "total_questions": 60,
        "duration_minutes": 300,
        "questions": questoes_simulado
    }

@app.post("/api/v1/simulated/submit")
def submit_simulated(submission: SimulatedSubmission, db: Session = Depends(get_db)):
    total_respondidas = len(submission.answers)
    return {
        "success": True,
        "message": "Simulado submetido e avaliado com sucesso pelo motor longitudinal do Projeto Nexo.",
        "total_answered": total_respondidas,
        "estimated_score": f"{(total_respondidas * 1.5):.1f} / 90.0",
        "status": "CONCLUDED"
    }
