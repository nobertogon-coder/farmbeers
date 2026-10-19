# -*- coding: utf-8 -*-
"""
FarmBeers Backend API - FastAPI + PostgreSQL Permanente
Compatibilidade estrita com o index.html oficial (PDF review modal, auth e persistência)
"""
import os
import io
import datetime
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import pdfplumber
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Float, ForeignKey, desc, func
from sqlalchemy.orm import declarative_base, sessionmaker, Session, relationship

import clinical_rules

# ==============================================================================
# BANCO DE DADOS POSTGRESQL (PERSISTÊNCIA PERMANENTE NO RENDER)
# ==============================================================================
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./farmbeers.db")

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

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
    pharmacist_username = Column(String(50), nullable=False)
    sector = Column(String(50), nullable=False)
    patient_age = Column(Integer, nullable=False)
    crcl_ml_min = Column(Float, nullable=True)
    total_alerts = Column(Integer, default=0)
    alerts = relationship("ScreeningAlertRecord", back_populates="screening", cascade="all, delete-orphan")

class ScreeningAlertRecord(Base):
    __tablename__ = "screening_alerts"
    id = Column(Integer, primary_key=True, index=True)
    screening_id = Column(Integer, ForeignKey("screenings.id"))
    drug_name = Column(String(100), nullable=False)
    axis = Column(String(100), nullable=False)
    recommendation = Column(String(1000), nullable=False)
    screening = relationship("ScreeningRecord", back_populates="alerts")

Base.metadata.create_all(bind=engine)

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
            exists = db.query(User).filter(User.username == u).first()
            if not exists:
                user = User(username=u, password=p, role=r, is_active=True, last_ping=datetime.datetime.utcnow())
                db.add(user)
        db.commit()
    finally:
        db.close()

init_default_users()

# ==============================================================================
# FASTAPI APP
# ==============================================================================
app = FastAPI(title="FarmBeers System API", version="3.2.0")

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

class MedicationInput(BaseModel):
    name: str
    dose: Optional[str] = ""
    route: Optional[str] = "VO (Oral)"
    frequency: Optional[str] = ""

class ScreeningPayload(BaseModel):
    age: int
    sector: str = "UPI (Enfermaria)"
    fall_risk: bool = False
    conditions: List[str] = []
    crcl_ml_min: Optional[float] = None
    crcl_notes: Optional[str] = ""
    medications: List[MedicationInput]

# ==============================================================================
# AUTENTICAÇÃO E PRESENÇA
# ==============================================================================
@app.post("/api/v1/auth/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == payload.username, User.password == payload.password).first()
    if not user:
        raise HTTPException(status_code=401, detail="Usuário ou senha incorretos.")
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
        is_online = False
        if u.last_ping:
            diff = (now - u.last_ping).total_seconds()
            if diff <= 60:
                is_online = True
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
        password=payload.password,
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
# INDICADORES CLÍNICOS CFT
# ==============================================================================
@app.get("/api/v1/admin/metrics")
def get_metrics(year: int = 2026, month: Optional[int] = None, day: Optional[int] = None, db: Session = Depends(get_db)):
    q = db.query(ScreeningRecord).filter(func.extract('year', ScreeningRecord.created_at) == year)
    if month:
        q = q.filter(func.extract('month', ScreeningRecord.created_at) == month)
    if day:
        q = q.filter(func.extract('day', ScreeningRecord.created_at) == day)
    
    screenings = q.all()
    total_patients = len(screenings)
    count_upi = sum(1 for s in screenings if s.sector == "UPI (Enfermaria)")
    count_uti = sum(1 for s in screenings if s.sector == "UTI")
    total_beers_alerts = sum(s.total_alerts for s in screenings)

    s_ids = [s.id for s in screenings]
    top_5 = []
    if s_ids:
        rows = (
            db.query(ScreeningAlertRecord.drug_name, func.count(ScreeningAlertRecord.id).label("total"))
            .filter(ScreeningAlertRecord.screening_id.in_(s_ids))
            .group_by(ScreeningAlertRecord.drug_name)
            .order_by(desc("total"))
            .limit(5)
            .all()
        )
        top_5 = [{"drug": r[0], "count": r[1]} for r in rows]

    return {
        "total_patients": total_patients,
        "count_upi": count_upi,
        "count_uti": count_uti,
        "total_beers_alerts": total_beers_alerts,
        "top_5_beers": top_5
    }

# ==============================================================================
# MOTOR DE TRIAGEM FARMBEERS
# ==============================================================================
@app.post("/api/v1/screen")
def process_screening(payload: ScreeningPayload, db: Session = Depends(get_db)):
    med_names = [m.name for m in payload.medications]
    
    alerts = clinical_rules.evaluate_patient_beers(
        medications=med_names,
        age=payload.age,
        fall_risk=payload.fall_risk,
        conditions=payload.conditions,
        crcl=payload.crcl_ml_min
    )

    alert_by_canonical = {a["drug"].strip().lower(): a for a in alerts}
    
    med_rows = []
    for m in payload.medications:
        canonical = clinical_rules.identify_drug_canonical(m.name)
        matched = None
        if canonical:
            c_key = canonical.strip().lower()
            if c_key in alert_by_canonical:
                matched = alert_by_canonical[c_key]
            else:
                for k, v in alert_by_canonical.items():
                    if k in c_key or c_key in k:
                        matched = v
                        break

        dose_text = f"{m.dose} {m.route} {m.frequency}".strip()
        if matched:
            med_rows.append({
                "name": m.name,
                "dose_route": dose_text or "VO (Oral)",
                "is_beers": True,
                "alert_tag": matched.get("axis", "AGS Beers 2023")
            })
        else:
            med_rows.append({
                "name": m.name,
                "dose_route": dose_text or "VO (Oral)",
                "is_beers": False,
                "alert_tag": ""
            })

    # Gravação permanente no PostgreSQL
    record = ScreeningRecord(
        pharmacist_username="admin",
        sector=payload.sector,
        patient_age=payload.age,
        crcl_ml_min=payload.crcl_ml_min,
        total_alerts=len(alerts)
    )
    db.add(record)
    db.flush()

    for a in alerts:
        alert_rec = ScreeningAlertRecord(
            screening_id=record.id,
            drug_name=a.get("drug", "Medicamento"),
            axis=a.get("axis", "Beers"),
            recommendation=a.get("recommendation", "")
        )
        db.add(alert_rec)
    db.commit()

    return {
        "total_beers_alerts": len(alerts),
        "alerts": alerts,
        "medication_rows": med_rows
    }

# ==============================================================================
# EXTRAÇÃO DE PRESCRIÇÃO HOSPITALAR (PDF)
# ==============================================================================
@app.post("/api/v1/prescription/extract-pdf")
async def extract_pdf(file: UploadFile = File(...)):
    contents = await file.read()
    found_drugs = set()
    try:
        with pdfplumber.open(io.BytesIO(contents)) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if not text:
                    continue
                lines = text.split("\n")
                for line in lines:
                    line_clean = line.strip()
                    if not line_clean:
                        continue
                    matched = clinical_rules.identify_drug_canonical(line_clean)
                    if matched:
                        found_drugs.add(matched.capitalize())
                    else:
                        for w in line_clean.split():
                            w_clean = w.strip(".,;:()[]{}")
                            if len(w_clean) >= 4:
                                m_word = clinical_rules.identify_drug_canonical(w_clean)
                                if m_word:
                                    found_drugs.add(m_word.capitalize())
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao processar PDF: {str(e)}")

    drug_list = sorted(list(found_drugs))

    # Retorna tanto em 'medications' quanto em 'drugs' para casamento perfeito com o script
    return {
        "medications": drug_list,
        "drugs": drug_list
    }

# ==============================================================================
# SERVIR O INDEX.HTML
# ==============================================================================
@app.get("/", response_class=HTMLResponse)
def read_root():
    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>FarmBeers Online. Arquivo index.html não localizado.</h1>"
