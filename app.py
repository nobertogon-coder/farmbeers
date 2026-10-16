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

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./farmabeers.db")
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="pharmacist")
    is_active = Column(Boolean, default=True)
    is_logged_in = Column(Boolean, default=False)
    last_ping = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)


class ScreeningLog(Base):
    __tablename__ = "screening_logs"
    id = Column(Integer, primary_key=True, index=True)
    patient_age = Column(Integer, nullable=False)
    sector = Column(String, nullable=False)
    crcl_ml_min = Column(Float, nullable=True)
    medications = Column(JSON, nullable=False)
    conditions = Column(JSON, nullable=True)
    beers_alerts = Column(JSON, nullable=False)
    total_alerts = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 100000)
    return f"{salt}${key.hex()}"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        salt, expected_hash = hashed_password.split("$")
        key = hashlib.pbkdf2_hmac("sha256", plain_password.encode("utf-8"), salt.encode("utf-8"), 100000)
        return secrets.compare_digest(key.hex(), expected_hash)
    except Exception:
        return False


# Seed Admin
db_seed = SessionLocal()
try:
    admin = db_seed.query(User).filter(User.username == "admin").first()
    if not admin:
        db_seed.add(User(
            username="admin",
            hashed_password=hash_password("admin123"),
            role="admin",
            is_active=True,
            is_logged_in=False
        ))
        db_seed.commit()
finally:
    db_seed.close()


def _norm(text: str) -> str:
    if not text:
        return ""
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join([c for c in nfkd if not unicodedata.combining(c)]).strip().lower()


# =============================================================================
# REGRAS BEERS 2023 COM PLANOS PRÁTICOS DE DESPRESCRIÇÃO (TAPERING)
# =============================================================================
TABLE_2_GENERAL = [
    {
        "drug": "Diazepam", "cat": "Benzodiazepínico",
        "rec": "Evitar. Risco elevado de sedação excessiva, delirium e quedas.",
        "rat": "Meia-vida cumulativa muito prolongada (> 100h em idosos).",
        "tapering": "Desmame Gradual: Reduzir a dose diária em 25% a cada 1-2 semanas. Não suspender abruptamente pelo risco de convulsões e abstinência."
    },
    {
        "drug": "Clonazepam", "cat": "Benzodiazepínico",
        "rec": "Evitar no idoso.",
        "rat": "Sedação diurna residual e prejuízo psicomotor cumulativo.",
        "tapering": "Desmame Gradual: Reduzir 0,25 mg a 0,5 mg a cada 2 semanas. Monitorar rebote de ansiedade e insônia."
    },
    {
        "drug": "Lorazepam", "cat": "Benzodiazepínico",
        "rec": "Evitar.",
        "rat": "Sensibilidade farmacodinâmica exacerbada em idosos, induzindo ataxia.",
        "tapering": "Desmame: Redução de 25% a 50% da dose a cada 7-14 dias até descontinuação."
    },
    {
        "drug": "Alprazolam", "cat": "Benzodiazepínico",
        "rec": "Evitar.",
        "rat": "Pico plasmático rápido, dependência precoce e abstinência interdose.",
        "tapering": "Desmame: Se em dose alta, avaliar conversão temporária para meia-vida intermediária ou redução fracionada semanal."
    },
    {
        "drug": "Zolpidem", "cat": "Drogas Z",
        "rec": "Evitar.",
        "rat": "Risco de amnésia, sonambulismo e fraturas idêntico aos benzodiazepínicos com ganho clínico marginal.",
        "tapering": "Desmame: Reduzir para 5 mg por 1 semana, depois dias alternados por 1 semana antes de suspender. Instituir higiene do sono."
    },
    {
        "drug": "Haloperidol", "cat": "Antipsicótico Típico",
        "rec": "Evitar em demência/sedação rotineira.",
        "rat": "Aumento documentado de mortalidade e AVC em demência; elevado índice de parkinsonismo medicamentoso.",
        "tapering": "Desmame: Reduzir 25% a 50% a cada 1-2 semanas se o quadro que motivou o uso agudo tiver remitido."
    },
    {
        "drug": "Quetiapina", "cat": "Antipsicótico Atípico",
        "rec": "Evitar uso exclusivo para insônia.",
        "rat": "Hipotensão postural acentuada e ganho de peso sem evidência formal como hipnótico primário.",
        "tapering": "Desmame: Titular dose para baixo (ex.: 25 mg para 12,5 mg) antes da retirada total."
    },
    {
        "drug": "Amitriptilina", "cat": "Antidepressivo Tricíclico",
        "rec": "Evitar.",
        "rat": "Altíssima carga anticolinérgica: hipotensão ortostática, boca seca, retenção vesical e arritmias cardíacas.",
        "tapering": "Desmame: Reduzir 25 mg/semana. Se necessário para dor neuropática, preferir gabapentinoide com ajuste renal ou duloxetina."
    },
    {
        "drug": "Nortriptilina", "cat": "Antidepressivo Tricíclico",
        "rec": "Evitar.",
        "rat": "Risco de hipotensão postural e carga anticolinérgica em geriatria.",
        "tapering": "Desmame: Redução gradual ao longo de 2 a 4 semanas."
    },
    {
        "drug": "Diclofenaco", "cat": "AINE",
        "rec": "Evitar uso contínuo.",
        "rat": "Hemorragia digestiva alta, nefrite intersticial/lesão renal aguda e descompensação de IC.",
        "tapering": "Desprescrição: Interrupção direta para dor crônica; substituir por Dipirona/Paracetamol ou AINE tópico."
    },
    {
        "drug": "Ibuprofeno", "cat": "AINE",
        "rec": "Evitar uso regular/prolongado.",
        "rat": "Nefrotoxicidade hemodinâmica e antagonismo do efeito antiplaquetário do AAS.",
        "tapering": "Desprescrição: Limitar o uso agudo a no máximo 48h com IBP co-prescrito."
    },
    {
        "drug": "Cetoprofeno", "cat": "AINE",
        "rec": "Evitar uso crônico.",
        "rat": "Ulceração péptica grave e retenção hidrossalina.",
        "tapering": "Desprescrição: Substituição imediata por analgésico simples."
    },
    {
        "drug": "Meloxicam", "cat": "AINE",
        "rec": "Evitar uso crônico.",
        "rat": "Em doses terapêuticas perde a seletividade COX-2 e exibe risco hemorrágico e renal.",
        "tapering": "Desprescrição: Interromper uso rotineiro."
    },
    {
        "drug": "Ciclobenzaprina", "cat": "Relaxante Muscular",
        "rec": "Evitar.",
        "rat": "Ação anticolinérgica potente e sedação diurna com elevado risco de quedas.",
        "tapering": "Desprescrição: Descontinuação direta em cursos curtos ou redução em 3 a 5 dias."
    },
    {
        "drug": "Carisoprodol", "cat": "Relaxante Muscular",
        "rec": "Evitar.",
        "rat": "Metabolizado em meprobamato. Sedação profunda, dependência física e hipotensão.",
        "tapering": "Desprescrição: Descontinuação gradual em 1 semana para evitar síndrome de retirada."
    },
    {
        "drug": "Glibenclamida", "cat": "Sulfonilureia",
        "rec": "Evitar estritamente.",
        "rat": "Elevadíssimo risco de hipoglicemia severa e prolongada com dano cerebral.",
        "tapering": "Substituição: Trocar de imediato por Gliclazida MR ou inibidor de SGLT2/DPP-4 sob monitorização glicêmica."
    },
    {
        "drug": "Metoclopramida", "cat": "Procinético",
        "rec": "Evitar uso > 12 semanas.",
        "rat": "Efeitos extrapiramidais e discinesia tardia frequentemente irreversível.",
        "tapering": "Desprescrição: Suspender ou substituir por Domperidona/Ondansetrona conforme a indicação clínica."
    },
    {
        "drug": "Omeprazol", "cat": "IBP",
        "rec": "Evitar uso > 8 semanas sem indicação clínica formal.",
        "rat": "Risco de colite por C. difficile, fraturas osteoporóticas e hipomagnesemia.",
        "tapering": "Desmame de IBP: Reduzir para dose padrão por 2 semanas, depois dose em dias alternados por 2 semanas antes de suspender (evita hipersecreção ácida rebote)."
    },
    {
        "drug": "Dexclorfeniramina", "cat": "Anti-histamínico 1ª Geração",
        "rec": "Evitar.",
        "rat": "Anticolinérgico intenso: retenção urinária aguda em homens e confusão mental.",
        "tapering": "Substituição: Substituir por anti-histamínico de 2ª geração (Loratadina, Cetirizina ou Fexofenadina)."
    },
    {
        "drug": "Prometazina", "cat": "Anti-histamínico 1ª Geração",
        "rec": "Evitar.",
        "rat": "Sedação profunda, hipotensão ortostática e efeito anticolinérgico.",
        "tapering": "Substituição: Suspender e utilizar alternativas não sedativas."
    },
    {
        "drug": "Digoxina", "cat": "Digitálico",
        "rec": "Evitar dose > 0,125 mg/dia.",
        "rat": "Janela terapêutica estreita com risco de arritmias letais por acúmulo renal.",
        "tapering": "Ajuste: Reduzir imediatamente para <= 0,125 mg/dia e monitorar digoxinemia e potássio sérico."
    }
]

TABLE_3_DISEASE = [
    {
        "cond": "Insuficiência Cardíaca", "drug": "Diclofenaco", "rec": "Evitar.",
        "rat": "Retenção de sódio e vasoconstrição renal descompensam agudamente a IC.",
        "tapering": "Substituição analgésica imediata por Paracetamol/Dipirona."
    },
    {
        "cond": "Insuficiência Cardíaca", "drug": "Ibuprofeno", "rec": "Evitar.",
        "rat": "Descompensação hemodinâmica e anulação de diuréticos de alça.",
        "tapering": "Suspensão imediata."
    },
    {
        "cond": "Insuficiência Cardíaca", "drug": "Cetoprofeno", "rec": "Evitar.",
        "rat": "Retenção hídrica com exacerbação de insuficiência cardíaca.",
        "tapering": "Suspensão imediata."
    },
    {
        "cond": "Doença de Parkinson", "drug": "Haloperidol", "rec": "Evitar estritamente.",
        "rat": "Bloqueio D2 estriatal precipita acinesia severa e rigidez motora aguda.",
        "tapering": "Substituição: Se antipsicótico for indispensável em Parkinson, utilizar apenas Quetiapina ou Clozapina."
    },
    {
        "cond": "Doença de Parkinson", "drug": "Metoclopramida", "rec": "Evitar.",
        "rat": "Bloqueio dopaminérgico central agrava os sintomas motores.",
        "tapering": "Substituir por Ondansetrona para controle de náuseas."
    },
    {
        "cond": "Histórico de Quedas", "drug": "Diazepam", "rec": "Evitar.",
        "rat": "Ataxia motora e lentificação de reflexos precipitam novas quedas graves.",
        "tapering": "Iniciar protocolo gradual de desmame conforme Tabela 2."
    },
    {
        "cond": "Histórico de Quedas", "drug": "Clonazepam", "rec": "Evitar.",
        "rat": "Prejuízo motor cumulativo com risco elevado de traumatismo craniano e fratura de fêmur.",
        "tapering": "Iniciar protocolo gradual de desmame conforme Tabela 2."
    },
    {
        "cond": "Histórico de Quedas", "drug": "Zolpidem", "rec": "Evitar.",
        "rat": "Incoordenação motora e sonambulismo noturno.",
        "tapering": "Desmame escalonado em 2 semanas."
    },
    {
        "cond": "Demência", "drug": "Amitriptilina", "rec": "Evitar.",
        "rat": "Ação anticolinérgica potente neutraliza anticolinesterásicos e acelera declínio cognitivo.",
        "tapering": "Descontinuação progressiva em 2 a 3 semanas."
    }
]

TABLE_4_CAUTION = [
    {
        "drug": "Ácido Acetilsalicílico", "rec": "Usar com cautela em prevenção primária >= 70 anos.",
        "rat": "Risco de hemorragia gastrointestinal maior sem comprovação de sobrevida primária líquida.",
        "tapering": "Reavaliação: Se não houver histórico de IAM/AVC (prevenção primária), avaliar suspensão após discussão clínica."
    },
    {
        "drug": "Sertralina", "rec": "Monitorar sódio sérico.",
        "rat": "Risco de hiponatremia grave por SIADH em pacientes idosos.",
        "tapering": "Conduta: Dosar sódio antes e 2 semanas após início/titulação."
    },
    {
        "drug": "Fluoxetina", "rec": "Monitorar sódio sérico.",
        "rat": "Risco substancial de hiponatremia por SIADH e meia-vida muito prolongada.",
        "tapering": "Conduta: Monitorar eletrólitos séricos com atenção redobrada se associado a diurético."
    }
]

TABLE_5_INTERACTIONS = [
    {
        "d1": "Morfina", "d2": "Diazepam", "rec": "Evitar associação.",
        "rat": "Depressão respiratória bulbar profunda sinérgica e sedação extrema com risco de morte.",
        "tapering": "Conduta: Se não for protocolo de cuidados paliativos terminais, suspender o benzodiazepínico."
    },
    {
        "d1": "Tramadol", "d2": "Clonazepam", "rec": "Evitar associação.",
        "rat": "Depressão do SNC cumulativa e rebaixamento de nível de consciência.",
        "tapering": "Conduta: Reavaliar estratégia analgésica multimodal."
    },
    {
        "d1": "Diclofenaco", "d2": "Varfarina", "rec": "Evitar associação.",
        "rat": "Aumento drástico no risco de hemorragia digestiva alta volumosa.",
        "tapering": "Conduta: Suspender o AINE de imediato."
    },
    {
        "d1": "Ibuprofeno", "d2": "Rivaroxabana", "rec": "Evitar associação.",
        "rat": "Lesão direta de mucosa gástrica associada à inibição do fator Xa.",
        "tapering": "Conduta: Suspender o AINE de imediato."
    }
]

TABLE_6_RENAL = [
    {
        "drug": "Pregabalina", "limit": 60.0, "rec": "Reduzir dose se ClCr < 60 mL/min.",
        "rat": "Excreção renal inalterada; acúmulo provoca sonolência incapacitante, mioclonias e ataxia.",
        "tapering": "Ajuste de Dose: ClCr 30-60: máx 150 mg/dia; ClCr 15-30: máx 75 mg/dia; ClCr < 15: máx 25-50 mg/dia."
    },
    {
        "drug": "Gabapentina", "limit": 60.0, "rec": "Reduzir dose se ClCr < 60 mL/min.",
        "rat": "Depuração exclusivamente renal; acúmulo sérico causa neurotoxicidade.",
        "tapering": "Ajuste de Dose: ClCr 30-59: máx 700 mg/dia; ClCr 15-29: máx 300 mg/dia; ClCr < 15: máx 300 mg a cada 48h."
    },
    {
        "drug": "Ciprofloxacino", "limit": 30.0, "rec": "Ajustar dose se ClCr < 50; evitar se < 30 mL/min.",
        "rat": "Acúmulo com risco de encefalopatia, confusão mental e prolongamento do intervalo QTc.",
        "tapering": "Ajuste de Dose: ClCr 30-50: 250-500 mg 12/12h; ClCr < 30: 250-500 mg 24/24h."
    },
    {
        "drug": "Espironolactona", "limit": 30.0, "rec": "Evitar se ClCr < 30 mL/min.",
        "rat": "Incapacidade de excreção de potássio resulta em hipercalemia potencialmente fatal.",
        "tapering": "Conduta: Suspender a droga e monitorar calemia de urgência."
    }
]


# =============================================================================
# MODELOS DE DADOS E ENGINE CLÍNICA
# =============================================================================
class MedicationItem(BaseModel):
    name: str
    dose: Optional[str] = None
    route: Optional[str] = "VO (Oral)"
    frequency: Optional[str] = None


class ScreeningPayload(BaseModel):
    age: int
    sector: str = "UPI (Enfermaria)"
    fall_risk: Optional[bool] = False
    conditions: Optional[List[str]] = []
    crcl_ml_min: Optional[float] = None
    crcl_notes: Optional[str] = None
    medications: List[MedicationItem]


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


def evaluate_beers(payload: ScreeningPayload) -> ScreeningResult:
    alerts: List[BeersAlert] = []
    norm_meds = [_norm(m.name) for m in payload.medications]
    norm_conds = [_norm(c) for c in (payload.conditions or [])]
    if payload.fall_risk:
        norm_conds.append("historico de quedas")

    rows: List[ScreenedMedicationRow] = []

    for med, nmed in zip(payload.medications, norm_meds):
        row_alerts = []

        # Tabela 2
        for r in TABLE_2_GENERAL:
            if _norm(r["drug"]) in nmed or nmed in _norm(r["drug"]):
                alert = BeersAlert(
                    axis="Tabela 2 (MPI Geral)",
                    drug=med.name,
                    category=r["cat"],
                    recommendation=r["rec"],
                    rationale=r["rat"],
                    tapering=r.get("tapering"),
                    severity="Alta"
                )
                alerts.append(alert)
                row_alerts.append(alert)

        # Tabela 4
        for r in TABLE_4_CAUTION:
            if _norm(r["drug"]) in nmed or nmed in _norm(r["drug"]):
                alert = BeersAlert(
                    axis="Tabela 4 (Cautela)",
                    drug=med.name,
                    category="Uso Cauteloso",
                    recommendation=r["rec"],
                    rationale=r["rat"],
                    tapering=r.get("tapering"),
                    severity="Moderada"
                )
                alerts.append(alert)
                row_alerts.append(alert)

        # Tabela 6
        if payload.crcl_ml_min is not None:
            for r in TABLE_6_RENAL:
                if (_norm(r["drug"]) in nmed or nmed in _norm(r["drug"])) and payload.crcl_ml_min < r["limit"]:
                    alert = BeersAlert(
                        axis="Tabela 6 (Ajuste Renal)",
                        drug=f"{med.name} (ClCr: {payload.crcl_ml_min} mL/min)",
                        category="Disfunção Renal",
                        recommendation=r["rec"],
                        rationale=r["rat"],
                        tapering=r.get("tapering"),
                        severity="Alta"
                    )
                    alerts.append(alert)
                    row_alerts.append(alert)

        # Tabela 3
        for r in TABLE_3_DISEASE:
            rc = _norm(r["cond"])
            if any(rc in c or c in rc for c in norm_conds):
                if _norm(r["drug"]) in nmed or nmed in _norm(r["drug"]):
                    alert = BeersAlert(
                        axis="Tabela 3 (Fármaco-Doença)",
                        drug=f"{med.name} na presença de {r['cond']}",
                        category="Interação Doença",
                        recommendation=r["rec"],
                        rationale=r["rat"],
                        tapering=r.get("tapering"),
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

    # Tabela 5
    for r in TABLE_5_INTERACTIONS:
        d1, d2 = _norm(r["d1"]), _norm(r["d2"])
        if any(d1 in nm or nm in d1 for nm in norm_meds) and any(d2 in nm or nm in d2 for nm in norm_meds):
            alerts.append(BeersAlert(
                axis="Tabela 5 (Interação Não Segura)",
                drug=f"{r['d1']} + {r['d2']}",
                category="Interação Medicamentosa",
                recommendation=r["rec"],
                rationale=r["rat"],
                tapering=r.get("tapering"),
                severity="Crítica"
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


app = FastAPI(title="FarmBeers - Triagem Farmacêutica")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LoginPayload(BaseModel):
    username: str
    password: str


class CreateUserPayload(BaseModel):
    username: str
    password: str
    role: str = "pharmacist"


@app.get("/")
def serve_home():
    return FileResponse("index.html")


@app.post("/api/v1/auth/login")
def login(creds: LoginPayload, db: Session = Depends(get_db)):
    u = creds.username.strip().lower()
    user = db.query(User).filter(User.username == u).first()
    if not user or not verify_password(creds.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos.")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Este usuário está bloqueado pelo administrador.")

    user.is_logged_in = True
    user.last_ping = datetime.utcnow()
    db.commit()

    return {
        "user": {
            "username": user.username,
            "role": user.role
        }
    }


@app.post("/api/v1/auth/logout")
def logout(payload: dict, db: Session = Depends(get_db)):
    uname = payload.get("username", "").strip().lower()
    if uname:
        user = db.query(User).filter(User.username == uname).first()
        if user:
            user.is_logged_in = False
            db.commit()
    return {"status": "logged_out"}


@app.post("/api/v1/auth/ping")
def ping_activity(payload: dict, db: Session = Depends(get_db)):
    uname = payload.get("username", "").strip().lower()
    if uname:
        user = db.query(User).filter(User.username == uname).first()
        if user:
            user.is_logged_in = True
            user.last_ping = datetime.utcnow()
            db.commit()
    return {"status": "active"}


@app.get("/api/v1/admin/users")
def get_users_list(db: Session = Depends(get_db)):
    users = db.query(User).all()
    now = datetime.utcnow()
    result = []
    for u in users:
        is_online = bool(
            u.is_logged_in and u.last_ping and (now - u.last_ping <= timedelta(seconds=60))
        )
        if not is_online and u.is_logged_in:
            u.is_logged_in = False
            db.commit()

        result.append({
            "id": u.id,
            "username": u.username,
            "role": u.role,
            "is_active": u.is_active,
            "is_online": is_online,
            "created_at": u.created_at.strftime("%d/%m/%Y")
        })
    return result


@app.post("/api/v1/admin/users", status_code=status.HTTP_201_CREATED)
def create_new_user(payload: CreateUserPayload, db: Session = Depends(get_db)):
    uname = payload.username.strip().lower()
    if not uname or not payload.password.strip():
        raise HTTPException(status_code=400, detail="Usuário e senha são obrigatórios.")

    if db.query(User).filter(User.username == uname).first():
        raise HTTPException(status_code=400, detail="Nome de usuário já existe.")

    new_u = User(
        username=uname,
        hashed_password=hash_password(payload.password.strip()),
        role=payload.role,
        is_active=True,
        is_logged_in=False,
        last_ping=None
    )
    db.add(new_u)
    db.commit()
    return {"message": "Usuário cadastrado com sucesso!"}


@app.patch("/api/v1/admin/users/{user_id}/toggle-status")
def toggle_user_active(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    if user.username == "admin":
        raise HTTPException(status_code=400, detail="Não é permitido bloquear o administrador principal.")

    user.is_active = not user.is_active
    if not user.is_active:
        user.is_logged_in = False
    db.commit()
    return {"id": user.id, "is_active": user.is_active}


@app.delete("/api/v1/admin/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    if user.username == "admin":
        raise HTTPException(status_code=400, detail="Não é permitido excluir o administrador principal.")

    db.delete(user)
    db.commit()
    return {"message": "Usuário excluído com sucesso."}


@app.get("/api/v1/admin/metrics")
def get_metrics_by_period(
    year: int = Query(default=datetime.utcnow().year),
    month: Optional[int] = Query(default=None),
    day: Optional[int] = Query(default=None),
    db: Session = Depends(get_db)
):
    query = db.query(ScreeningLog).filter(func.extract("year", ScreeningLog.created_at) == year)
    if month:
        query = query.filter(func.extract("month", ScreeningLog.created_at) == month)
    if day:
        query = query.filter(func.extract("day", ScreeningLog.created_at) == day)

    records = query.all()
    total_patients = len(records)
    total_beers_alerts = sum(r.total_alerts for r in records)

    count_upi = sum(1 for r in records if r.sector == "UPI (Enfermaria)")
    count_uti = sum(1 for r in records if r.sector == "UTI")

    beers_counter = {}
    for r in records:
        if r.beers_alerts:
            for item in r.beers_alerts:
                drug_name = item.get("drug", "").split(" (")[0].split(" na presença")[0]
                beers_counter[drug_name] = beers_counter.get(drug_name, 0) + 1

    sorted_top = sorted(beers_counter.items(), key=lambda x: x[1], reverse=True)[:5]
    top_5_list = [{"drug": k, "count": v} for k, v in sorted_top]

    period_desc = f"{year}"
    if month:
        period_desc = f"{month:02d}/{year}"
    if day and month:
        period_desc = f"{day:02d}/{month:02d}/{year}"

    return {
        "period": period_desc,
        "total_patients": total_patients,
        "count_upi": count_upi,
        "count_uti": count_uti,
        "total_beers_alerts": total_beers_alerts,
        "top_5_beers": top_5_list
    }


@app.post("/api/v1/screen", response_model=ScreeningResult)
def run_screening_endpoint(payload: ScreeningPayload, db: Session = Depends(get_db)):
    result = evaluate_beers(payload)
    db.add(ScreeningLog(
        patient_age=payload.age,
        sector=payload.sector,
        crcl_ml_min=payload.crcl_ml_min,
        medications=[m.name for m in payload.medications],
        conditions=payload.conditions,
        beers_alerts=[{"drug": a.drug, "axis": a.axis} for a in result.alerts],
        total_alerts=result.total_beers_alerts
    ))
    db.commit()
    return result


# =============================================================================
# EXTRAÇÃO DE PDF SEGURA (FILTRA FRASES DE NEGAÇÃO E HISTÓRICO PASSADO)
# =============================================================================
NEGATION_PATTERNS = [
    r"nega\s+(uso\s+de\s+)?",
    r"sem\s+uso\s+de\s+",
    r"não\s+faz\s+uso\s+de\s+",
    r"suspenso\s+(o\s+)?",
    r"suspensa\s+(a\s+)?",
    r"alergia\s+(a|ao)\s+",
    r"alérgico\s+(a|ao)\s+"
]


@app.post("/api/v1/prescription/extract-pdf")
async def extract_pdf(file: UploadFile = File(...)):
    contents = await file.read()
    lines_list = []
    with pdfplumber.open(io.BytesIO(contents)) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                lines_list.extend(t.splitlines())

    vocab = set([r["drug"] for r in TABLE_2_GENERAL] + [r["drug"] for r in TABLE_6_RENAL])
    found = set()

    for line in lines_list:
        line_clean = line.strip().lower()
        if not line_clean:
            continue

        # Se a linha contiver qualquer padrão de negação, ignora
        has_negation = any(re.search(pat, line_clean) for pat in NEGATION_PATTERNS)
        if has_negation:
            continue

        for drug in vocab:
            if re.search(r"\b" + re.escape(drug.lower()) + r"\b", line_clean):
                found.add(drug)

    return {"medications": sorted(list(found))}