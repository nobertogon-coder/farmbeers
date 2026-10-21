# -*- coding: utf-8 -*-
"""
FarmBeers Backend API - Servidor Principal FastAPI + PostgreSQL
Com Auto-Migrador de Colunas e Persistência Garantida
"""
import os
import io
import re
import hashlib
import datetime
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import pdfplumber
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Float, ForeignKey, desc, func, text
from sqlalchemy.orm import declarative_base, sessionmaker, Session, relationship

import clinical_rules

# ==============================================================================
# BANCO DE DADOS POSTGRESQL (PERSISTENTE E AUTO-MIGRADO)
# ==============================================================================
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./farmbeers.db")
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,
    pool_recycle=300
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def hash_password(password: str) -> str:
    salt = "FB_CLINICAL_SALT_2026"
    return hashlib.sha256((password + salt).encode("utf-8")).hexdigest()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password = Column(String(100), nullable=False)
    role = Column(String(20), default="pharmacist")
    is_active = Column(Boolean, default=True)
    last_ping = Column(DateTime, default=datetime.datetime.utcnow)

class ScreeningRecord(Base):
    __tablename__ = "screenings"
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    pharmacist_username = Column(String(50), default="admin", nullable=True)
    sector = Column(String(50), default="UPI (Enfermaria)", nullable=True)
    patient_age = Column(Integer, default=70, nullable=True)
    crcl_ml_min = Column(Float, nullable=True)
    acb_score = Column(Integer, default=0, nullable=True)
    total_alerts = Column(Integer, default=0, nullable=True)
    alerts = relationship("ScreeningAlertRecord", back_populates="screening", cascade="all, delete-orphan")

class ScreeningAlertRecord(Base):
    __tablename__ = "screening_alerts"
    id = Column(Integer, primary_key=True, index=True)
    screening_id = Column(Integer, ForeignKey("screenings.id", ondelete="CASCADE"), nullable=True)
    drug_name = Column(String(150), nullable=False, default="Medicamento")
    axis = Column(String(100), nullable=False, default="AGS Beers 2023")
    recommendation = Column(String(1000), nullable=False, default="Reavaliar prescrição.")
    outcome = Column(String(30), default="pending", nullable=True)
    screening = relationship("ScreeningRecord", back_populates="alerts")

Base.metadata.create_all(bind=engine)

# Auto-migrador: adiciona colunas que possam faltar em bancos já existentes
def run_auto_migrations():
    with engine.connect() as conn:
        try:
            if not DATABASE_URL.startswith("sqlite"):
                conn.execute(text("ALTER TABLE screening_alerts ADD COLUMN IF NOT EXISTS outcome VARCHAR(30) DEFAULT 'pending';"))
                conn.execute(text("ALTER TABLE screenings ADD COLUMN IF NOT EXISTS total_alerts INTEGER DEFAULT 0;"))
                conn.execute(text("ALTER TABLE screenings ADD COLUMN IF NOT EXISTS acb_score INTEGER DEFAULT 0;"))
                conn.execute(text("ALTER TABLE screenings ADD COLUMN IF NOT EXISTS crcl_ml_min DOUBLE PRECISION;"))
                conn.commit()
        except Exception as e:
            print(f"Aviso na auto-migração: {e}")

run_auto_migrations()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_default_users():
    db = SessionLocal()
    try:
        defaults = [
            ("admin", "admin123", "admin"),
            ("farmaceutico", "farm123", "pharmacist"),
            ("Teste", "teste123", "pharmacist")
        ]
        for u, p, r in defaults:
            user = db.query(User).filter(User.username == u).first()
            if not user:
                new_user = User(
                    username=u,
                    password=hash_password(p),
                    role=r,
                    is_active=True,
                    last_ping=datetime.datetime.utcnow()
                )
                db.add(new_user)
            else:
                if user.password == p:
                    user.password = hash_password(p)
        db.commit()
    except Exception:
        db.rollback()
    finally:
        db.close()

init_default_users()

# ==============================================================================
# FASTAPI APP
# ==============================================================================
app = FastAPI(title="FarmBeers System API", version="8.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginRequest(BaseModel):
    username: str
    password: str

class PingRequest(BaseModel):
    username: str

class CreateUserRequest(BaseModel):
    username: str
    password: str
    role: str

class OutcomeRequest(BaseModel):
    outcome: str

class MedicationInput(BaseModel):
    name: str
    dose: Optional[str] = ""
    route: Optional[str] = "VO (Oral)"
    frequency: Optional[str] = ""
    is_sos: Optional[bool] = False

class ScreeningPayload(BaseModel):
    age: Optional[int] = 70
    sector: Optional[str] = "UPI (Enfermaria)"
    fall_risk: Optional[bool] = False
    conditions: Optional[List[str]] = []
    crcl_ml_min: Optional[float] = None
    crcl_notes: Optional[str] = ""
    medications: List[MedicationInput] = []

# ==============================================================================
# AUTENTICAÇÃO
# ==============================================================================
@app.post("/api/v1/auth/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    pwd_h = hash_password(payload.password)
    user = db.query(User).filter(User.username == payload.username).first()

    if not user:
        raise HTTPException(status_code=401, detail="Usuário ou senha incorretos.")

    if user.password != pwd_h and user.password != payload.password:
        raise HTTPException(status_code=401, detail="Usuário ou senha incorretos.")

    if user.password == payload.password:
        user.password = pwd_h

    if not user.is_active:
        raise HTTPException(status_code=403, detail="Acesso bloqueado pela administração.")

    user.last_ping = datetime.datetime.utcnow()
    db.commit()
    return {"status": "ok", "user": {"id": user.id, "username": user.username, "role": user.role}}

@app.post("/api/v1/auth/ping")
def ping_user(payload: PingRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == payload.username).first()
    if user:
        user.last_ping = datetime.datetime.utcnow()
        db.commit()
    return {"status": "alive"}

@app.post("/api/v1/auth/logout")
def logout_user(payload: PingRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == payload.username).first()
    if user:
        user.last_ping = datetime.datetime.utcnow() - datetime.timedelta(minutes=10)
        db.commit()
    return {"status": "logged_out"}

# ==============================================================================
# GESTÃO DE USUÁRIOS
# ==============================================================================
@app.get("/api/v1/admin/users")
def list_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    now = datetime.datetime.utcnow()
    res = []
    for u in users:
        is_online = bool(u.last_ping and (now - u.last_ping).total_seconds() <= 60)
        res.append({
            "id": u.id,
            "username": u.username,
            "role": u.role,
            "is_active": u.is_active,
            "is_online": is_online
        })
    return res

@app.post("/api/v1/admin/users")
def create_user(payload: CreateUserRequest, db: Session = Depends(get_db)):
    exists = db.query(User).filter(User.username == payload.username).first()
    if exists:
        raise HTTPException(status_code=400, detail="Nome de usuário já cadastrado.")
    new_u = User(
        username=payload.username,
        password=hash_password(payload.password),
        role=payload.role,
        is_active=True,
        last_ping=datetime.datetime.utcnow()
    )
    db.add(new_u)
    db.commit()
    return {"status": "created"}

@app.patch("/api/v1/admin/users/{user_id}/toggle-status")
def toggle_user_status(user_id: int, db: Session = Depends(get_db)):
    u = db.query(User).filter(User.id == user_id).first()
    if not u:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    if u.username == "admin":
        raise HTTPException(status_code=400, detail="Não é permitido bloquear o administrador padrão.")
    u.is_active = not u.is_active
    db.commit()
    return {"status": "updated", "is_active": u.is_active}

@app.delete("/api/v1/admin/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    u = db.query(User).filter(User.id == user_id).first()
    if not u:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    if u.username == "admin":
        raise HTTPException(status_code=400, detail="Não é permitido excluir o administrador padrão.")
    db.delete(u)
    db.commit()
    return {"status": "deleted"}

# ==============================================================================
# ROTA DE MÉTRICAS DA CFT - TOTALMENTE ROBUSTA
# ==============================================================================
@app.get("/api/v1/admin/metrics")
def get_metrics(
    year: Optional[str] = None,
    month: Optional[str] = None,
    day: Optional[str] = None,
    db: Session = Depends(get_db)
):
    try:
        all_screenings = db.query(ScreeningRecord).order_by(desc(ScreeningRecord.created_at)).all()
        
        screenings = []
        for s in all_screenings:
            dt = s.created_at
            if dt and year and year.strip().isdigit() and int(year.strip()) > 2000:
                if dt.year != int(year.strip()):
                    continue
            if dt and month and month.strip().isdigit() and 1 <= int(month.strip()) <= 12:
                if dt.month != int(month.strip()):
                    continue
            if dt and day and day.strip().isdigit() and 1 <= int(day.strip()) <= 31:
                if dt.day != int(day.strip()):
                    continue
            screenings.append(s)

        total_patients = len(screenings)
        count_uti = sum(1 for s in screenings if "uti" in (s.sector or "").lower())
        count_upi = total_patients - count_uti

        s_ids = [s.id for s in screenings]
        total_alerts = 0
        accepted_count = 0
        top_5 = []

        if s_ids:
            alerts = db.query(ScreeningAlertRecord).filter(ScreeningAlertRecord.screening_id.in_(s_ids)).all()
            total_alerts = len(alerts)
            accepted_count = sum(1 for a in alerts if a.outcome == "accepted")

            counts = {}
            for a in alerts:
                d_name = a.drug_name or "Medicamento"
                counts[d_name] = counts.get(d_name, 0) + 1
            sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:5]
            top_5 = [{"drug": k, "count": v} for k, v in sorted_counts]
        else:
            total_alerts = sum((s.total_alerts or 0) for s in screenings)

        acceptance_rate = round((accepted_count / total_alerts * 100), 1) if total_alerts > 0 else 0.0

        return {
            "total_patients": total_patients,
            "count_upi": count_upi,
            "count_uti": count_uti,
            "total_beers_alerts": total_alerts,
            "accepted_interventions": accepted_count,
            "acceptance_rate": acceptance_rate,
            "top_5_beers": top_5
        }
    except Exception as e:
        print(f"Erro em metrics: {e}")
        return {
            "total_patients": 0,
            "count_upi": 0,
            "count_uti": 0,
            "total_beers_alerts": 0,
            "accepted_interventions": 0,
            "acceptance_rate": 0.0,
            "top_5_beers": []
        }

# ==============================================================================
# AUDITORIA E ATUALIZAÇÃO DO DESFECHO DA INTERVENÇÃO
# ==============================================================================
@app.patch("/api/v1/alerts/{alert_id}/outcome")
def update_alert_outcome(alert_id: int, payload: OutcomeRequest, db: Session = Depends(get_db)):
    try:
        alert_rec = db.query(ScreeningAlertRecord).filter(ScreeningAlertRecord.id == alert_id).first()
        if not alert_rec:
            return {"status": "not_found", "alert_id": alert_id}
        alert_rec.outcome = payload.outcome
        db.commit()
        return {"status": "updated", "alert_id": alert_id, "outcome": alert_rec.outcome}
    except Exception as e:
        db.rollback()
        return {"status": "error", "detail": str(e)}

# ==============================================================================
# MOTOR DE TRIAGEM COM PERSISTÊNCIA COMPLETA E IMEDIATA
# ==============================================================================
@app.post("/api/v1/screen")
def process_screening(payload: ScreeningPayload, db: Session = Depends(get_db)):
    patient_age = payload.age if (payload.age and payload.age > 0) else 70
    med_dicts = [m.model_dump() for m in payload.medications]

    alerts_raw, acb_total, acb_text, med_tag_map = clinical_rules.evaluate_patient_beers(
        medications=med_dicts,
        age=patient_age,
        fall_risk=bool(payload.fall_risk),
        conditions=payload.conditions or [],
        crcl=payload.crcl_ml_min
    )

    persisted_records = []
    if payload.medications:
        try:
            sec_val = str(payload.sector) if payload.sector else "UPI (Enfermaria)"
            crcl_val = float(payload.crcl_ml_min) if payload.crcl_ml_min is not None else None

            record = ScreeningRecord(
                pharmacist_username="admin",
                sector=sec_val,
                patient_age=int(patient_age),
                crcl_ml_min=crcl_val,
                acb_score=int(acb_total),
                total_alerts=len(alerts_raw),
                created_at=datetime.datetime.utcnow()
            )
            db.add(record)
            db.commit()
            db.refresh(record)

            for a in alerts_raw:
                d_name = str(a.get("drug") or a.get("drug_name") or "Medicamento")
                alert_rec = ScreeningAlertRecord(
                    screening_id=record.id,
                    drug_name=d_name,
                    axis=str(a.get("axis", "AGS Beers 2023")),
                    recommendation=str(a.get("recommendation", "Reavaliar prescrição.")),
                    outcome="pending"
                )
                db.add(alert_rec)
                db.commit()
                db.refresh(alert_rec)
                pers
