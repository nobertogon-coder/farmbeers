import os
import io
import re
import hashlib
import secrets
import unicodedata
from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import FastAPI, HTTPException, UploadFile, File, Depends, status, Query
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, JSON, Boolean, func
from sqlalchemy.orm import declarative_base, sessionmaker, Session
import pdfplumber

# Importação da base farmacológica
from clinical_rules import TABLE_2_GENERAL, TABLE_6_RENAL, TABLE_3_DISEASE_DRUG, TABLE_5_INTERACTIONS

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./farmabeers.db")
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# =========================================================================
# MODELOS DE DADOS
# =========================================================================
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    salt = Column(String(64), nullable=False)
    password_hash = Column(String(64), nullable=False)
    role = Column(String(20), default="pharmacist", nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    last_ping = Column(DateTime, default=datetime.utcnow, nullable=False)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    operator_username = Column(String(50), nullable=False)
    patient_age = Column(Integer, nullable=False)
    sector = Column(String(50), nullable=False)
    crcl_calculated = Column(Float, nullable=True)
    total_medications = Column(Integer, nullable=False)
    total_beers_alerts = Column(Integer, nullable=False)
    identified_drugs = Column(JSON, nullable=False)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def _hash_password(password: str, salt: str) -> str:
    return hashlib.sha256((salt + password).encode("utf-8")).hexdigest()

def init_default_users():
    """Garante a existência dos três usuários: admin, farmaceutico e Teste."""
    db = SessionLocal()
    try:
        users_to_seed = [
            ("admin", "admin123", "admin"),
            ("farmaceutico", "farm123", "pharmacist"),
            ("Teste", "12345", "pharmacist")
        ]
        for uname, pwd, rle in users_to_seed:
            existing = db.query(User).filter(User.username == uname).first()
            if not existing:
                s = secrets.token_hex(16)
                h = _hash_password(pwd, s)
                db.add(User(username=uname, salt=s, password_hash=h, role=rle, is_active=True))
        db.commit()
    finally:
        db.close()

init_default_users()

# =========================================================================
# SCHEMAS PYDANTIC
# =========================================================================
class LoginRequest(BaseModel):
    username: str
    password: str

class UserCreateRequest(BaseModel):
    username: str
    password: str
    role: str = "pharmacist"

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

class BeersAlert(BaseModel):
    axis: str
    drug: str
    category: str
    recommendation: str
    rationale: str
    tapering: Optional[str] = None
    severity: str

class ScreenedMedicationRow(BaseModel):
    name: str
    dose_route: str
    is_beers: bool
    alert_tag: Optional[str] = None
    recommendation: Optional[str] = None
    rationale: Optional[str] = None
    tapering: Optional[str] = None

class ScreeningResult(BaseModel):
    patient_age: int
    sector: str
    crcl_ml_min: Optional[float]
    crcl_notes: Optional[str]
    total_medications: int
    total_beers_alerts: int
    medication_rows: List[ScreenedMedicationRow]
    alerts: List[BeersAlert]

# =========================================================================
# MOTOR CLÍNICO DE AVALIAÇÃO DE BEERS 2023
# =========================================================================
def _norm(text: str) -> str:
    if not text:
        return ""
    nfkd = unicodedata.normalize("NFKD", text)
    clean = "".join([c for c in nfkd if not unicodedata.combining(c)])
    return clean.lower().strip()

def _match_drug(text_norm: str, drug_name: str, aliases: list) -> bool:
    """Verifica correspondência por fronteiras de palavra exatas (\b)."""
    targets = [drug_name.lower()] + [a.lower() for a in aliases]
    for target in targets:
        pattern = r'\b' + re.escape(target) + r'\b'
        if re.search(pattern, text_norm):
            return True
    return False

def evaluate_beers(payload: ScreeningPayload) -> ScreeningResult:
    alerts: List[BeersAlert] = []
    rows: List[ScreenedMedicationRow] = []

    norm_conditions = [_norm(c) for c in (payload.conditions or [])]
    if payload.fall_risk:
        norm_conditions.append("queda")
        norm_conditions.append("risco de queda")

    for med in payload.medications:
        nmed = _norm(med.name)
        row_alerts = []

        # Tabela 2: Inapropriados Gerais
        for item in TABLE_2_GENERAL:
            if _match_drug(nmed, item["drug"], item.get("aliases", [])):
                alert = BeersAlert(
                    axis="Tabela 2 (MPI Geral)",
                    drug=item["drug"],
                    category=item["cat"],
                    recommendation=item["rec"],
                    rationale=item["rat"],
                    tapering=item.get("tapering"),
                    severity="Alta"
                )
                alerts.append(alert)
                row_alerts.append(alert)

        # Tabela 6: Ajuste Renal
        for item in TABLE_6_RENAL:
            if _match_drug(nmed, item["drug"], item.get("aliases", [])):
                cutoff = item.get("cutoff_clcr", 60.0)
                if payload.crcl_ml_min is not None and payload.crcl_ml_min < cutoff:
                    alert = BeersAlert(
                        axis="Tabela 6 (Ajuste Renal)",
                        drug=f"{item['drug']} (ClCr: {payload.crcl_ml_min} mL/min)",
                        category=item["cat"],
                        recommendation=item["rec"],
                        rationale=f"{item['rat']} Guia: {item['guideline']}",
                        tapering=item.get("guideline"),
                        severity="Alta"
                    )
                    alerts.append(alert)
                    row_alerts.append(alert)

        # Tabela 3: Cruzamento Fármaco-Doença
        for rule in TABLE_3_DISEASE_DRUG:
            matched_cond = any(any(c_term in cond for c_term in rule["conditions"]) for cond in norm_conditions)
            if matched_cond:
                matched_drug = any(re.search(r'\b' + re.escape(d) + r'\b', nmed) for d in rule["drugs"])
                if matched_drug:
                    alert = BeersAlert(
                        axis="Tabela 3 (Fármaco-Doença)",
                        drug=f"{med.name} - {rule['title']}",
                        category="Condição Clínica Associada",
                        recommendation=rule["rec"],
                        rationale=rule["rat"],
                        tapering="Revisar prescrição considerando o histórico do paciente.",
                        severity="Alta"
                    )
                    alerts.append(alert)
                    row_alerts.append(alert)

        dose_info = f"{med.dose or ''} {med.route or ''} {med.frequency or ''}".strip()
        if row_alerts:
            primary = row_alerts[0]
            rows.append(ScreenedMedicationRow(
                name=med.name,
                dose_route=dose_info or "--",
                is_beers=True,
                alert_tag=primary.axis,
                recommendation=primary.recommendation,
                rationale=primary.rationale,
                tapering=primary.tapering
            ))
        else:
            rows.append(ScreenedMedicationRow(
                name=med.name,
                dose_route=dose_info or "--",
                is_beers=False,
                alert_tag=None,
                recommendation=None,
                rationale=None,
                tapering=None
            ))

    # Tabela 5: Interações Críticas Duplas
    all_meds_text = [_norm(m.name) for m in payload.medications]
    for inter in TABLE_5_INTERACTIONS:
        group_a, group_b = inter["pair"]
        has_a = any(any(re.search(r'\b' + re.escape(term) + r'\b', m) for term in group_a) for m in all_meds_text)
        has_b = any(any(re.search(r'\b' + re.escape(term) + r'\b', m) for term in group_b) for m in all_meds_text)

        if has_a and has_b:
            alerts.append(BeersAlert(
                axis="Tabela 5 (Interação Crítica)",
                drug=inter["alert"],
                category="Interação Medicamentosa",
                recommendation=inter["rec"],
                rationale=inter["rat"],
                tapering="Substituir ao menos um dos agentes por alternativa de menor risco respiratório/hemorrágico.",
                severity="Alta"
            ))

    return ScreeningResult(
        patient_age=payload.age,
        sector=payload.sector,
        crcl_ml_min=payload.crcl_ml_min,
        crcl_notes=payload.crcl_notes,
        total_medications=len(payload.medications),
        total_beers_alerts=len(alerts),
        medication_rows=rows,
        alerts=alerts
    )

# =========================================================================
# APLICAÇÃO FASTAPI
# =========================================================================
app = FastAPI(title="FarmBeers - Triagem Hospitalar AGS Beers 2023", version="2.3.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def get_index():
    if os.path.exists("index.html"):
        return FileResponse("index.html")
    return {"message": "FarmBeers API ativa. Carregue o arquivo index.html."}

# --- AUTENTICAÇÃO E SESSÃO ---
@app.post("/api/v1/auth/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == req.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não encontrado.")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Conta desativada pelo administrador.")
    
    if _hash_password(req.password, user.salt) != user.password_hash:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Senha incorreta.")
    
    user.last_ping = datetime.utcnow()
    db.commit()
    return {
        "status": "success",
        "user": {
            "id": user.id,
            "username": user.username,
            "role": user.role
        }
    }

@app.post("/api/v1/auth/ping")
def ping_user(payload: dict, db: Session = Depends(get_db)):
    uname = payload.get("username")
    if uname:
        u = db.query(User).filter(User.username == uname).first()
        if u:
            u.last_ping = datetime.utcnow()
            db.commit()
    return {"status": "ok"}

@app.post("/api/v1/auth/logout")
def logout_user(payload: dict, db: Session = Depends(get_db)):
    uname = payload.get("username")
    if uname:
        u = db.query(User).filter(User.username == uname).first()
        if u:
            u.last_ping = datetime.utcnow() - timedelta(minutes=5)
            db.commit()
    return {"status": "logged_out"}

# --- GESTÃO DE USUÁRIOS (ADMIN) ---
@app.get("/api/v1/admin/users")
def list_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    now = datetime.utcnow()
    res = []
    for u in users:
        is_online = (now - u.last_ping) < timedelta(seconds=60)
        res.append({
            "id": u.id,
            "username": u.username,
            "role": u.role,
            "is_active": u.is_active,
            "is_online": is_online
        })
    return res

@app.post("/api/v1/admin/users")
def create_user(req: UserCreateRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == req.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Nome de usuário já cadastrado.")
    s = secrets.token_hex(16)
    h = _hash_password(req.password, s)
    new_user = User(username=req.username, salt=s, password_hash=h, role=req.role, is_active=True)
    db.add(new_user)
    db.commit()
    return {"message": f"Usuário {req.username} criado com sucesso."}

@app.patch("/api/v1/admin/users/{user_id}/toggle-status")
def toggle_status(user_id: int, db: Session = Depends(get_db)):
    u = db.query(User).filter(User.id == user_id).first()
    if not u:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    if u.username == "admin":
        raise HTTPException(status_code=400, detail="Não é permitido desativar o administrador padrão.")
    u.is_active = not u.is_active
    db.commit()
    return {"message": "Status atualizado.", "is_active": u.is_active}

@app.delete("/api/v1/admin/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    u = db.query(User).filter(User.id == user_id).first()
    if not u:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    if u.username == "admin":
        raise HTTPException(status_code=400, detail="Não é permitido excluir o administrador principal.")
    db.delete(u)
    db.commit()
    return {"message": "Usuário excluído com sucesso."}

# --- TRIAGEM CLÍNICA E EXTRAÇÃO DE PDF ---
@app.post("/api/v1/screen", response_model=ScreeningResult)
def screen_prescription(payload: ScreeningPayload, db: Session = Depends(get_db)):
    result = evaluate_beers(payload)
    
    identified = [a.drug for a in result.alerts]
    log_entry = AuditLog(
        operator_username="farmaceutico",
        patient_age=payload.age,
        sector=payload.sector,
        crcl_calculated=payload.crcl_ml_min,
        total_medications=len(payload.medications),
        total_beers_alerts=result.total_beers_alerts,
        identified_drugs=identified
    )
    db.add(log_entry)
    db.commit()
    return result

@app.post("/api/v1/prescription/extract-pdf")
async def extract_prescription_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Apenas arquivos PDF são aceitos.")
    
    content = await file.read()
    extracted_text = ""
    try:
        with pdfplumber.open(io.BytesIO(content)) as pdf:
            for page in pdf.pages:
                extracted_text += (page.extract_text() or "") + "\n"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar PDF: {str(e)}")

    lines = extracted_text.splitlines()
    detected_medications = []

    targets = []
    for item in TABLE_2_GENERAL:
        targets.append(item["drug"])
        targets.extend(item.get("aliases", []))
    for item in TABLE_6_RENAL:
        targets.append(item["drug"])
        targets.extend(item.get("aliases", []))

    for line in lines:
        nline = _norm(line)
        if any(neg in nline for neg in ["nega uso", "sem uso de", "alergia a", "nao faz uso", "suspenso"]):
            continue
        
        for t in targets:
            if re.search(r'\b' + re.escape(t.lower()) + r'\b', nline):
                title_med = t.capitalize()
                if title_med not in detected_medications:
                    detected_medications.append(title_med)

    return {"medications": detected_medications}

# --- INDICADORES CFT (ADMIN) ---
@app.get("/api/v1/admin/metrics")
def get_metrics(
    year: int = Query(2026),
    month: Optional[int] = Query(None),
    day: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(AuditLog)
    query = query.filter(func.extract("year", AuditLog.timestamp) == year)
    if month:
        query = query.filter(func.extract("month", AuditLog.timestamp) == month)
    if day:
        query = query.filter(func.extract("day", AuditLog.timestamp) == day)

    logs = query.all()
    total_patients = len(logs)
    count_upi = sum(1 for l in logs if "UPI" in l.sector)
    count_uti = sum(1 for l in logs if "UTI" in l.sector)
    total_alerts = sum(l.total_beers_alerts for l in logs)

    drug_counts = {}
    for l in logs:
        if isinstance(l.identified_drugs, list):
            for d in l.identified_drugs:
                drug_counts[d] = drug_counts.get(d, 0) + 1

    sorted_drugs = sorted(drug_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    top_5 = [{"drug": k, "count": v} for k, v in sorted_drugs]

    return {
        "total_patients": total_patients,
        "count_upi": count_upi,
        "count_uti": count_uti,
        "total_beers_alerts": total_alerts,
        "top_5_beers": top_5
    }
