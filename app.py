# -*- coding: utf-8 -*-
"""
FarmBeers Backend API - Servidor Principal FastAPI + PostgreSQL
Parser Avançado com Regex de Doses/Vias/Posologia (SN/QN/SOS) e Criptografia SHA-256
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
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Float, ForeignKey, desc, func
from sqlalchemy.orm import declarative_base, sessionmaker, Session, relationship

import clinical_rules

# ==============================================================================
# BANCO DE DADOS POSTGRESQL (PERSISTÊNCIA PERMANENTE)
# ==============================================================================
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./farmbeers.db")
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def hash_password(password: str) -> str:
    salt = "FB_CLINICAL_SALT_2026"
    return hashlib.sha256((password + salt).encode("utf-8")).hexdigest()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(100), nullable=False)
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
                user = User(
                    username=u,
                    password_hash=hash_password(p),
                    role=r,
                    is_active=True,
                    last_ping=datetime.datetime.utcnow()
                )
                db.add(user)
        db.commit()
    finally:
        db.close()

init_default_users()

# ==============================================================================
# FASTAPI CONFIGURAÇÃO
# ==============================================================================
app = FastAPI(title="FarmBeers System API", version="3.6.0")

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
# AUTENTICAÇÃO COM HASH SHA-256
# ==============================================================================
@app.post("/api/v1/auth/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    pwd_h = hash_password(payload.password)
    user = db.query(User).filter(User.username == payload.username, User.password_hash == pwd_h).first()
    
    # Retrocompatibilidade automática se o banco ainda tiver senhas em texto puro
    if not user:
        legacy_user = db.query(User).filter(User.username == payload.username, User.password_hash == payload.password).first()
        if legacy_user:
            legacy_user.password_hash = pwd_h
            db.commit()
            user = legacy_user

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
# GESTÃO DE USUÁRIOS & INDICADORES CFT
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
        password_hash=hash_password(payload.password),
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
# MOTOR DE TRIAGEM COM ESTRATIFICAÇÃO SN/QN/SOS E VIGILÂNCIA RENAL
# ==============================================================================
@app.post("/api/v1/screen")
def process_screening(payload: ScreeningPayload, db: Session = Depends(get_db)):
    patient_age = payload.age if (payload.age and payload.age > 0) else 70
    med_dicts = [m.model_dump() for m in payload.medications]
    
    alerts_raw = clinical_rules.evaluate_patient_beers(
        medications=med_dicts,
        age=patient_age,
        fall_risk=bool(payload.fall_risk),
        conditions=payload.conditions or [],
        crcl=payload.crcl_ml_min
    )

    alerts_complete = []
    for a in alerts_raw:
        alerts_complete.append({
            "drug": a.get("drug", "Medicamento"),
            "axis": a.get("axis", "AGS Beers 2023"),
            "recommendation": a.get("recommendation", "Reavaliar prescrição."),
            "rationale": a.get("rationale", "Medicamento potencialmente inapropriado para idosos."),
            "tapering": a.get("tapering", ""),
            "is_sos": a.get("is_sos", False)
        })

    alert_by_canonical = {a["drug"].strip().lower(): a for a in alerts_complete}
    
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

        parts = [p for p in [m.dose, m.route, m.frequency] if p and p.strip()]
        dose_route_str = " ".join(parts) if parts else "VO (Oral)"
        
        # Indica visualmente se é SN / QN
        is_sn_flag = bool(m.is_sos) or any(t in dose_route_str.lower() for t in ["sn", "qn", "sos"])
        if is_sn_flag and "[SN/QN]" not in dose_route_str:
            dose_route_str = f"{dose_route_str} [SN/QN]"

        if matched:
            med_rows.append({
                "name": m.name,
                "dose_route": dose_route_str,
                "is_beers": True,
                "is_sos": is_sn_flag,
                "alert_tag": matched.get("axis", "AGS Beers 2023")
            })
        else:
            med_rows.append({
                "name": m.name,
                "dose_route": dose_route_str,
                "is_beers": False,
                "is_sos": is_sn_flag,
                "alert_tag": ""
            })

    if payload.medications:
        try:
            record = ScreeningRecord(
                pharmacist_username="admin",
                sector=payload.sector or "UPI (Enfermaria)",
                patient_age=patient_age,
                crcl_ml_min=payload.crcl_ml_min,
                total_alerts=len(alerts_complete)
            )
            db.add(record)
            db.flush()

            for a in alerts_complete:
                alert_rec = ScreeningAlertRecord(
                    screening_id=record.id,
                    drug_name=a["drug"],
                    axis=a["axis"],
                    recommendation=a["recommendation"]
                )
                db.add(alert_rec)
            db.commit()
        except Exception:
            db.rollback()

    return {
        "total_beers_alerts": len(alerts_complete),
        "alerts": alerts_complete,
        "medication_rows": med_rows
    }

# ==============================================================================
# EXTRAÇÃO DE PDF HOSPITALAR INTELIGENTE (REGEX DE DOSE, VIA E SN/QN)
# ==============================================================================
def extract_posology_details(line: str):
    dose = ""
    route = "VO (Oral)"
    freq = ""
    is_sn = False

    # Regex de Dosagem (ex: 4mg, 500mg, 1g, 20 gotas, 1 amp, 2 cp)
    m_dose = re.search(r'(\b\d+[\.,]?\d*\s*(?:mg|g|mcg|ml|gotas|gota|ampola|amp|cp|comp|frasco)\b)', line, re.I)
    if m_dose:
        dose = m_dose.group(1).strip()

    # Regex de Via de Administração Hospitalar
    if re.search(r'\b(iv|ev|endovenos[ao]|intravenos[ao])\b', line, re.I):
        route = "IV (Endovenoso)"
    elif re.search(r'\b(im|intramuscular)\b', line, re.I):
        route = "IM (Intramuscular)"
    elif re.search(r'\b(sc|subcutane[ao])\b', line, re.I):
        route = "SC (Subcutâneo)"
    elif re.search(r'\b(inalat[oó]ri[ao]|neb|inal)\b', line, re.I):
        route = "Inalatório"
    elif re.search(r'\b(t[oó]pic[ao]|creme|pomada)\b', line, re.I):
        route = "Tópico"
    elif re.search(r'\b(vo|oral)\b', line, re.I):
        route = "VO (Oral)"

    # Regex de Frequência e Indicadores SN / QN / SOS
    if re.search(r'\b(sn|qn|sos|se\s+necess[aá]rio|quando\s+necess[aá]rio|a\s+crit[eé]rio\s+m[eé]dico|acm)\b', line, re.I):
        is_sn = True
        freq = "SN (Se Necessário)"
    else:
        m_freq = re.search(r'(\b\d{1,2}\s*/\s*\d{1,2}\s*h|\b\d{1,2}\s*em\s*\d{1,2}\s*h|\b\d{1,2}x\s*/\s*dia|\b\d{1,2}x\s*ao\s*dia|\b1x\b|\b2x\b|\b3x\b|\b4x\b|\bmanh[aã]\b|\bnoite\b|\b12/12h\b|\b8/8h\b|\b6/6h\b|\b24/24h\b)', line, re.I)
        if m_freq:
            freq = m_freq.group(1).strip()

    return dose, route, freq, is_sn

@app.post("/api/v1/prescription/extract-pdf")
async def extract_pdf(file: UploadFile = File(...)):
    contents = await file.read()
    extracted_items = []
    seen = set()
    try:
        with pdfplumber.open(io.BytesIO(contents)) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if not text:
                    continue
                for line in text.split("\n"):
                    line_clean = line.strip()
                    if not line_clean:
                        continue
                    matched = clinical_rules.identify_drug_canonical(line_clean)
                    if matched and matched not in seen:
                        seen.add(matched)
                        dose, route, freq, is_sn = extract_posology_details(line_clean)
                        extracted_items.append({
                            "name": matched.capitalize(),
                            "dose": dose,
                            "route": route,
                            "frequency": freq,
                            "is_sos": is_sn
                        })
                    else:
                        for w in line_clean.split():
                            w_clean = w.strip(".,;:()[]{}")
                            if len(w_clean) >= 4:
                                m_word = clinical_rules.identify_drug_canonical(w_clean)
                                if m_word and m_word not in seen:
                                    seen.add(m_word)
                                    dose, route, freq, is_sn = extract_posology_details(line_clean)
                                    extracted_items.append({
                                        "name": m_word.capitalize(),
                                        "dose": dose,
                                        "route": route,
                                        "frequency": freq,
                                        "is_sos": is_sn
                                    })
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao ler PDF: {str(e)}")

    drug_names = [it["name"] for it in extracted_items]
    return {
        "medications": drug_names,
        "drugs": drug_names,
        "items": extracted_items
    }

# ==============================================================================
# SERVIR PÁGINA PRINCIPAL
# ==============================================================================
@app.get("/", response_class=HTMLResponse)
def read_root():
    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>FarmBeers Online. Arquivo index.html não localizado.</h1>"
