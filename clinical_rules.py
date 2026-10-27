# -*- coding: utf-8 -*-
import re
import unicodedata

# =====================================================================
# 1. DICIONÁRIO MESTRE DE DROGAS (AGS Beers 2023 + ACB)
# =====================================================================
BEERS_DRUGS = {
    # --- SNC e Anticonvulsivantes ---
    "fenobarbital": ["fenobarbital", "gardenal", "fenocris", "edhanol"],
    "fenitoina": ["fenitoina", "hidantal", "epamin"],
    "diazepam": ["diazepam", "valium", "compaz", "diazepax"],
    "clonazepam": ["clonazepam", "rivotril", "clonotril"],
    "lorazepam": ["lorazepam", "lorax", "mesmerin"],
    "midazolam": ["midazolam", "dormonid"],
    "alprazolam": ["alprazolam", "frontal", "apraz"],
    "zolpidem": ["zolpidem", "stilnox", "patz", "turner"],
    "carbamazepina": ["carbamazepina", "tegretol"],
    "acido valproico": ["acido valproico", "valproato", "depakene", "depakote"],

    # --- Anticolinérgicos e Anti-histamínicos ---
    "prometazina": ["prometazina", "fenergan"],
    "dimenidrinato": ["dimenidrinato", "dramin", "nausicalm"],
    "dexclorfeniramina": ["dexclorfeniramina", "polaramine", "histamin"],
    "hidroxizina": ["hidroxizina", "hixizine"],
    "escopolamina": ["escopolamina", "hioscina", "buscopan", "hyoscine"],
    "amitriptilina": ["amitriptilina", "tryptanol", "amytril"],
    "nortriptilina": ["nortriptilina", "pamelor"],

    # --- Analgésicos, Opioides e Relaxantes Musculares ---
    "ciclobenzaprina": ["ciclobenzaprina", "miosan", "musculare"],
    "orfenadrina": ["orfenadrina", "dorflex"],
    "carisoprodol": ["carisoprodol", "torsilax", "tandrilax"],
    "morfina": ["morfina", "dimorf"],
    "tramadol": ["tramadol", "tramal", "sylador"],
    "codeina": ["codeina", "tylex", "paco"],

    # --- AINEs ---
    "cetoprofeno": ["cetoprofeno", "profenid", "biprofenid"],
    "diclofenaco": ["diclofenaco", "voltaren", "cataflam", "flotac"],
    "ibuprofeno": ["ibuprofeno", "alivium", "advil"],
    "naproxeno": ["naproxeno", "flanax"],
    "nimesulida": ["nimesulida", "nisulid", "cimelide"],
    "cetorolaco": ["cetorolaco", "toragesic", "trometamol"],
    "meloxicam": ["meloxicam", "bioflex", "movatec"],

    # --- Cardiovasculares e Renais ---
    "clonidina": ["clonidina", "atensina"],
    "doxazosina": ["doxazosina", "cardura"],
    "metildopa": ["metildopa", "aldomet"],
    "amiodarona": ["amiodarona", "ancoron", "atlansil"],
    "digoxina": ["digoxina", "lanoxin"],
    "espironolactona": ["espironolactona", "aldactone", "diempax"],
    "enoxaparina": ["enoxaparina", "clexane", "versa"],
    "varfarina": ["varfarina", "marevan", "coumadin"],

    # --- Endocrinologia e TGI ---
    "glibenclamida": ["glibenclamida", "daonil"],
    "glimepirida": ["glimepirida", "amaryl"],
    "metoclopramida": ["metoclopramida", "plasil"],
    "oleo mineral": ["oleo mineral", "nujol"],
    "omeprazol": ["omeprazol", "losec", "peptazol"],
    "pantoprazol": ["pantoprazol", "pantocal"],

    # --- Antipsicóticos ---
    "risperidona": ["risperidona", "risperdal"],
    "quetiapina": ["quetiapina", "seroquel"],
    "haloperidol": ["haloperidol", "haldol"],
    "olanzapina": ["olanzapina", "zyprexa"],
    "clorpromazina": ["clorpromazina", "amplictil"]
}

# Dicionário ACB Score
ACB_SCORES = {
    "amitriptilina": 3, "prometazina": 3, "escopolamina": 3, "dimenidrinato": 3,
    "dexclorfeniramina": 3, "hidroxizina": 3, "clorpromazina": 3, "olanzapina": 3,
    "nortriptilina": 3, "carbamazepina": 2, "ciclobenzaprina": 2, "orfenadrina": 2,
    "risperidona": 1, "quetiapina": 1, "haloperidol": 1, "diazepam": 1, "alprazolam": 1
}

# =====================================================================
# 2. FUNÇÕES DE PROCESSAMENTO
# =====================================================================
def normalize_text(text: str) -> str:
    if not text:
        return ""
    nfkd_form = unicodedata.normalize('NFKD', text)
    return nfkd_form.encode('ASCII', 'ignore').decode('utf-8').lower()

def identify_drug_canonical(drug_name: str) -> str:
    if not drug_name:
        return ""
    normalized_input = normalize_text(drug_name)
    for generic, synonyms in BEERS_DRUGS.items():
        for syn in synonyms:
            if normalize_text(syn) in normalized_input:
                return generic
    return ""

def detect_drugs_in_prescription(prescription_text: str) -> list:
    detected_drugs = []
    normalized_text = normalize_text(prescription_text)
    for generic_name, synonyms in BEERS_DRUGS.items():
        for synonym in synonyms:
            if normalize_text(synonym) in normalized_text:
                detected_drugs.append(generic_name)
                break
    return detected_drugs

# =====================================================================
# 3. MOTOR CLÍNICO: TODAS AS DROGAS MAPEADAS
# =====================================================================
def evaluate_patient_beers(medications, age, fall_risk=False, conditions=None, crcl=None):
    alerts = []
    acb_total = 0
    med_tag_map = {}
    
    if conditions is None: conditions = []

    if age < 65:
        return alerts, acb_total, "Idade inferior a 65 anos. Triagem geriátrica não aplicável.", med_tag_map

    snc_depressants = []
    nsaids = []
    anticoagulants = []

    for med in medications:
        raw_name = med.get("name", "")
        canonical = identify_drug_canonical(raw_name)
        if not canonical:
            continue

        is_sos = med.get("is_sos", False)

        # 1. ESCORE ACB (Calcula pontos e avisa)
        if canonical in ACB_SCORES:
            score = ACB_SCORES[canonical]
            acb_total += score
            alerts.append({
                "drug": canonical.capitalize(),
                "axis": "ACB Score (Carga Anticolinérgica)",
                "recommendation": f"Pontua {score} no ACB Score. Risco de delirium, boca seca e bexigoma.",
                "rationale": "Depleção colinérgica agrava o declínio cognitivo em idosos.",
                "tapering": "Considerar desprescrição ou substituição.",
                "is_sos": is_sos,
                "acb_score": score
            })
            med_tag_map[canonical] = "Carga Anticolinérgica"

        # 2. SISTEMA NERVOSO CENTRAL E ANTICONVULSIVANTES
        if canonical in ["diazepam", "clonazepam", "lorazepam", "midazolam", "alprazolam", "zolpidem", "fenobarbital"]:
            snc_depressants.append(canonical)
            alerts.append({
                "drug": canonical.capitalize(),
                "axis": "AGS Beers 2023 - Tabela 2",
                "recommendation": "Evitar uso. Elevado risco de sedação prolongada, quedas e fraturas.",
                "rationale": "Idosos têm hipersensibilidade GABAérgica e meia-vida prolongada.",
                "tapering": "Redução gradual (25% a cada 7-14 dias).",
                "is_sos": is_sos
            })
            med_tag_map[canonical] = "Risco Queda/SNC"

        elif canonical == "fenitoina":
            alerts.append({
                "drug": canonical.capitalize(),
                "axis": "AGS Beers 2023 - Tabela 2 / Janela Estreita",
                "recommendation": "Evitar uso. Risco elevado de ataxia e toxicidade neurológica.",
                "rationale": "Cinética não linear e forte dependência de albumina sérica.",
                "tapering": "Avaliar substituição. Monitorar nível sérico livre se uso obrigatório.",
                "is_sos": is_sos
            })
            med_tag_map[canonical] = "Tox. Neurológica"

        elif canonical in ["carbamazepina", "acido valproico"]:
            snc_depressants.append(canonical)
            alerts.append({
                "drug": canonical.capitalize(),
                "axis": "AGS Beers 2023 - SNC / Psiquiatria",
                "recommendation": "Usar com extrema cautela. Risco de hiponatremia (SIADH) e quedas.",
                "rationale": "Fármacos com interações hepáticas complexas e potencial sedativo.",
                "tapering": "Monitorar sódio sérico e reflexos motores.",
                "is_sos": is_sos
            })
            med_tag_map[canonical] = "Risco SNC/SIADH"

        # 3. RELAXANTES MUSCULARES FORTES
        elif canonical in ["ciclobenzaprina", "orfenadrina", "carisoprodol"]:
            alerts.append({
                "drug": canonical.capitalize(),
                "axis": "AGS Beers 2023 - Tabela 2",
                "recommendation": "Evitar. Risco severo de toxicidade anticolinérgica e sedação.",
                "rationale": "Baixa tolerabilidade em idosos (fraqueza, delirium e quedas).",
                "tapering": "Suspender. Preferir analgesia simples (Dipirona/Paracetamol).",
                "is_sos": is_sos
            })
            med_tag_map[canonical] = "Relaxante Muscular Inadequado"

        # 4. AINES E OPIOIDES
        elif canonical in ["cetoprofeno", "diclofenaco", "ibuprofeno", "naproxeno", "nimesulida", "cetorolaco", "meloxicam"]:
            nsaids.append(canonical)
            alerts.append({
                "drug": canonical.capitalize(),
                "axis": "AGS Beers 2023 - Tabela 2",
                "recommendation": "Evitar. Risco de Lesão Renal Aguda e Hemorragia Digestiva.",
                "rationale": "A inibição de prostaglandinas gera vasoconstrição da arteríola aferente renal.",
                "tapering": "Suspender imediatamente.",
                "is_sos": is_sos
            })
            med_tag_map[canonical] = "Risco Renal/HDA"

        elif canonical in ["tramadol", "codeina"]:
            snc_depressants.append(canonical)
            alerts.append({
                "drug": canonical.capitalize(),
                "axis": "Alerta Geriátrico - SNC",
                "recommendation": "Usar com cautela. Pode causar constipação severa, tontura e delirium.",
                "rationale": "Idosos são mais sensíveis aos efeitos centrais e gastrointestinais dos opioides.",
                "tapering": "Usar menor dose efetiva e prescrever laxante profilático se contínuo.",
                "is_sos": is_sos
            })
            med_tag_map[canonical] = "Opioide/SNC"

        # 5. CARDIOVASCULARES
        elif canonical in ["clonidina", "metildopa", "doxazosina"]:
            alerts.append({
                "drug": canonical.capitalize(),
                "axis": "AGS Beers 2023 - Tabela 2",
                "recommendation": "Evitar uso como anti-hipertensivo de rotina.",
                "rationale": "Alto risco de hipotensão ortostática, bradicardia e síncope ao levantar-se.",
                "tapering": "Desmame gradual (Clonidina causa rebote hipertensivo se suspensa subitamente).",
                "is_sos": is_sos
            })
            med_tag_map[canonical] = "Risco Ortostático"

        elif canonical == "amiodarona":
            alerts.append({
                "drug": canonical.capitalize(),
                "axis": "AGS Beers 2023 - Tabela 2",
                "recommendation": "Evitar como 1ª linha para Fibrilação Atrial.",
                "rationale": "Alta toxicidade pulmonar, tireoidiana e tempo de meia-vida extremamente longo.",
                "tapering": "Reavaliar necessidade de controle de ritmo vs. controle de frequência.",
                "is_sos": is_sos
            })
            med_tag_map[canonical] = "Tox. Cumulativa"

        elif canonical == "digoxina":
            alerts.append({
                "drug": canonical.capitalize(),
                "axis": "AGS Beers 2023 - Tabela 2",
                "recommendation": "Evitar doses > 0,125 mg/dia.",
                "rationale": "Redução do volume de distribuição (sarcopenia) e da depuração renal causam intoxicação fácil.",
                "tapering": "Monitorar função renal, potássio e nível sérico.",
                "is_sos": is_sos
            })
            med_tag_map[canonical] = "Janela Estreita"

        # 6. ANTIPSICÓTICOS
        elif canonical in ["risperidona", "quetiapina", "haloperidol", "olanzapina", "clorpromazina"]:
            snc_depressants.append(canonical)
            alerts.append({
                "drug": canonical.capitalize(),
                "axis": "AGS Beers 2023 - Tabela 2 (Antipsicóticos)",
                "recommendation": "Evitar uso para problemas comportamentais em demência (se não houver risco físico).",
                "rationale": "Aumenta risco de AVC, declínio cognitivo e mortalidade (Black Box Warning).",
                "tapering": "Desmame gradual. Usar doses mínimas apenas no delirium hiperativo grave.",
                "is_sos": is_sos
            })
            med_tag_map[canonical] = "Risco AVC/Mortalidade"

        # 7. GASTROINTESTINAL E ENDOCRINO
        elif canonical == "metoclopramida":
            alerts.append({
                "drug": canonical.capitalize(),
                "axis": "AGS Beers 2023 - Tabela 2",
                "recommendation": "Evitar uso, especialmente crônico.",
                "rationale": "Risco elevado de efeitos extrapiramidais (parkinsonismo medicamentoso) e discinesia tardia.",
                "tapering": "Substituir por Ondansetrona ou Domperidona.",
                "is_sos": is_sos
            })
            med_tag_map[canonical] = "Risco Extrapiramidal"

        elif canonical == "oleo mineral":
            alerts.append({
                "drug": canonical.capitalize(),
                "axis": "AGS Beers 2023 - Tabela 2",
                "recommendation": "Evitar uso como laxante.",
                "rationale": "Alto risco de aspiração e pneumonia lipoídica em idosos com disfagia.",
                "tapering": "Substituir por Macrogol (PEG 4000) ou Lactulose.",
                "is_sos": is_sos
            })
            med_tag_map[canonical] = "Risco Aspiração"

        elif canonical in ["omeprazol", "pantoprazol"]:
            alerts.append({
                "drug": canonical.capitalize(),
                "axis": "AGS Beers 2023 - Tabela 2",
                "recommendation": "Evitar uso ininterrupto por > 8 semanas sem indicação clara (ex: HDA, esôfago de Barrett).",
                "rationale": "Risco de infecção por C. difficile, perda óssea e má absorção de vitamina B12/Magnésio.",
                "tapering": "Reduzir dose em 50% ou passar para dias alternados até suspender.",
                "is_sos": is_sos
            })
            med_tag_map[canonical] = "Uso Crônico Indevido"

        # 8. AJUSTES RENAIS ESTABELECIDOS (Tabela 6)
        if crcl is not None:
            if canonical == "enoxaparina" and crcl < 30:
                anticoagulants.append(canonical)
                alerts.append({
                    "drug": canonical.capitalize(),
                    "axis": "AGS Beers 2023 - Tabela 6 (Renal)",
                    "recommendation": f"Função renal comprometida (CrCl {crcl} mL/min). Reduzir profilaxia para 20mg/dia.",
                    "rationale": "Risco de sangramento por acúmulo de fator anti-Xa.",
                    "tapering": "Adequar à taxa de filtração.",
                    "is_sos": is_sos
                })
                med_tag_map[canonical] = "Ajuste Renal"

            if canonical == "espironolactona" and crcl < 30:
                alerts.append({
                    "drug": canonical.capitalize(),
                    "axis": "AGS Beers 2023 - Tabela 6 (Renal)",
                    "recommendation": f"Evitar uso com CrCl {crcl} mL/min.",
                    "rationale": "Risco iminente de hipercalemia fatal.",
                    "tapering": "Suspender e monitorar K+ sérico.",
                    "is_sos": is_sos
                })
                med_tag_map[canonical] = "Ajuste Renal"

            if canonical == "morfina" and crcl < 30:
                alerts.append({
                    "drug": canonical.capitalize(),
                    "axis": "AGS Beers 2023 - Tabela 6 (Renal)",
                    "recommendation": f"Evitar uso com CrCl {crcl} mL/min.",
                    "rationale": "Acúmulo de neurotoxinas (M3G/M6G) causa mioclonias e coma.",
                    "tapering": "Substituir por Fentanila.",
                    "is_sos": is_sos
                })
                med_tag_map[canonical] = "Ajuste Renal"

        if canonical == "varfarina":
            anticoagulants.append(canonical)
            alerts.append({
                "drug": canonical.capitalize(),
                "axis": "Janela Estreita / Sangramento",
                "recommendation": "Vigilância extrema de RNI.",
                "rationale": "Hipoalbuminemia aumenta fração livre e eleva risco hemorrágico.",
                "tapering": "Garantir interações avaliadas.",
                "is_sos": is_sos
            })
            med_tag_map[canonical] = "Risco Sangramento"

    # 9. REGRAS DE INTERAÇÃO (Tabela 4)
    if len(snc_depressants) >= 2:
        alerts.append({
            "drug": "Múltiplos Depressores do SNC",
            "axis": "AGS Beers 2023 - Tabela 4",
            "recommendation": f"Prescrição simultânea de 2 ou mais sedativos: {', '.join(snc_depressants)}.",
            "rationale": "Efeito sinérgico letal (quedas, depressão respiratória e delirium).",
            "tapering": "Desprescrever o menos essencial.",
            "is_sos": False
        })
    
    if len(nsaids) > 0 and len(anticoagulants) > 0:
        alerts.append({
            "drug": "AINE + Anticoagulante",
            "axis": "AGS Beers 2023 - Tabela 4",
            "recommendation": "Uso concomitante severamente contraindicado.",
            "rationale": "Risco catastrófico de Hemorragia Digestiva.",
            "tapering": "Suspender AINE.",
            "is_sos": False
        })

    # Interpretação ACB
    acb_text = "Carga Nula ou Leve. Risco controlado."
    if acb_total >= 3:
        acb_text = f"ALTO RISCO (Score {acb_total}). Probabilidade severa de declínio cognitivo e delirium."
    elif acb_total in [1, 2]:
        acb_text = f"Carga Moderada (Score {acb_total}). Vigiar retenção urinária e confusão mental."

    return alerts, acb_total, acb_text, med_tag_map
