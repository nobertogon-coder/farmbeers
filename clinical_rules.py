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

    # --- Anticolinérgicos e Anti-histamínicos (ACB Score Alto) ---
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

    # --- Anti-inflamatórios Não Esteroides (AINEs) ---
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

    # --- Endocrinologia e Trato Gastrointestinal ---
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

# Dicionário de Pontuação de Carga Anticolinérgica (ACB Score)
ACB_SCORES = {
    "amitriptilina": 3, "prometazina": 3, "escopolamina": 3, "dimenidrinato": 3,
    "dexclorfeniramina": 3, "hidroxizina": 3, "clorpromazina": 3, "olanzapina": 3,
    "nortriptilina": 3, "carbamazepina": 2, "ciclobenzaprina": 2,
    "risperidona": 1, "quetiapina": 1, "haloperidol": 1, "diazepam": 1, "alprazolam": 1
}

# =====================================================================
# 2. FUNÇÕES DE PROCESSAMENTO TEXTUAL E IDENTIFICAÇÃO
# =====================================================================
def normalize_text(text: str) -> str:
    """Remove acentos e converte para minúsculo"""
    if not text:
        return ""
    nfkd_form = unicodedata.normalize('NFKD', text)
    return nfkd_form.encode('ASCII', 'ignore').decode('utf-8').lower()

def identify_drug_canonical(drug_name: str) -> str:
    """Identifica o nome genérico a partir de qualquer sinônimo ou nome comercial."""
    if not drug_name:
        return ""
    normalized_input = normalize_text(drug_name)
    for generic, synonyms in BEERS_DRUGS.items():
        for syn in synonyms:
            if normalize_text(syn) in normalized_input:
                return generic
    return ""

# =====================================================================
# 3. MOTOR CLÍNICO: AVALIAÇÃO BEERS E ACB SCORE
# =====================================================================
def evaluate_patient_beers(medications, age, fall_risk=False, conditions=None, crcl=None):
    alerts = []
    acb_total = 0
    med_tag_map = {}
    
    if conditions is None:
        conditions = []

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

        # 1. Cálculo da Carga Anticolinérgica (ACB)
        if canonical in ACB_SCORES:
            score = ACB_SCORES[canonical]
            acb_total += score
            alerts.append({
                "drug": canonical.capitalize(),
                "axis": "ACB Score (Carga Anticolinérgica)",
                "recommendation": f"Pontua {score} no ACB Score. Risco de delirium, boca seca, bexigoma e quedas.",
                "rationale": "A depleção colinérgica agrava o declínio cognitivo em idosos.",
                "tapering": "Considerar desprescrição ou substituição por alternativa não anticolinérgica.",
                "is_sos": is_sos,
                "acb_score": score
            })
            med_tag_map[canonical] = "Carga Anticolinérgica"

        # 2. Regras da Tabela 2
        if canonical == "fenitoina":
            alerts.append({
                "drug": canonical.capitalize(),
                "axis": "AGS Beers 2023 - Tabela 2 / Janela Estreita",
                "recommendation": "Evitar uso. Risco elevado de toxicidade neurológica central (ataxia, nistagmo).",
                "rationale": "Farmacocinética não linear e alta ligação proteica dependente de albumina.",
                "tapering": "Avaliar substituição. Monitorar nível sérico livre se uso compulsório.",
                "is_sos": is_sos
            })
            med_tag_map[canonical] = "Tox. Neurológica"

        if canonical in ["diazepam", "clonazepam", "lorazepam", "midazolam", "alprazolam", "zolpidem", "fenobarbital"]:
            snc_depressants.append(canonical)
            alerts.append({
                "drug": canonical.capitalize(),
                "axis": "AGS Beers 2023 - Tabela 2",
                "recommendation": "Evitar prescrição. Elevado risco de ataxia, síncope e fratura de fêmur.",
                "rationale": "Hipersensibilidade de receptores GABA e aumento da meia-vida (fármaco lipofílico).",
                "tapering": "Redução gradual de 25% da dose a cada 7 a 14 dias para evitar crise de abstinência.",
                "is_sos": is_sos
            })
            med_tag_map[canonical] = "Risco Queda/SNC"

        if canonical in ["glibenclamida", "glimepirida"]:
            alerts.append({
                "drug": canonical.capitalize(),
                "axis": "AGS Beers 2023 - Tabela 2",
                "recommendation": "Evitar prescrição. Risco de hipoglicemia severa e prolongada.",
                "rationale": "Falência dos mecanismos contrarreguladores adrenérgicos no idoso.",
                "tapering": "Substituir por Inibidor de DPP-4 (ex: Linagliptina) ou insulina segura.",
                "is_sos": is_sos
            })
            med_tag_map[canonical] = "Risco Hipoglicemia"

        if canonical in ["cetoprofeno", "diclofenaco", "ibuprofeno", "naproxeno", "nimesulida", "cetorolaco", "meloxicam"]:
            nsaids.append(canonical)
            alerts.append({
                "drug": canonical.capitalize(),
                "axis": "AGS Beers 2023 - Tabela 2",
                "recommendation": "Evitar uso. Risco de Hemorragia Digestiva e Lesão Renal Aguda.",
                "rationale": "Inibição de prostaglandinas induz isquemia glomerular.",
                "tapering": "Suspender. Substituir por Dipirona/Paracetamol fixo ou opioides fracos.",
                "is_sos": is_sos
            })
            med_tag_map[canonical] = "Risco Renal/Gástrico"

        # 3. Regras da Tabela 6 (Ajuste Renal)
        if crcl is not None:
            if canonical == "enoxaparina" and crcl < 30:
                anticoagulants.append(canonical)
                alerts.append({
                    "drug": canonical.capitalize(),
                    "axis": "AGS Beers 2023 - Tabela 6 (Renal)",
                    "recommendation": f"Função renal comprometida (CrCl {crcl} mL/min). Reduzir dose profilática para 20mg/dia.",
                    "rationale": "Eliminação glomerular estrita. Risco de hemorragia grave.",
                    "tapering": "Adequar dose baseada na taxa de filtração.",
                    "is_sos": is_sos
                })
                med_tag_map[canonical] = "Ajuste Renal"

            if canonical == "espironolactona" and crcl < 30:
                alerts.append({
                    "drug": canonical.capitalize(),
                    "axis": "AGS Beers 2023 - Tabela 6 (Renal)",
                    "recommendation": f"Evitar uso com CrCl {crcl} mL/min. Risco elevado de hipercalemia.",
                    "rationale": "Inibição da excreção de potássio tubular sem depuração glomerular.",
                    "tapering": "Suspender prescrição e monitorar potássio sérico.",
                    "is_sos": is_sos
                })
                med_tag_map[canonical] = "Ajuste Renal"

            if canonical == "morfina" and crcl < 30:
                alerts.append({
                    "drug": canonical.capitalize(),
                    "axis": "AGS Beers 2023 - Tabela 6 (Renal)",
                    "recommendation": f"Evitar uso com CrCl {crcl} mL/min. Substituir analgésico.",
                    "rationale": "Acúmulo de M3G e M6G causa neurotoxicidade e depressão respiratória.",
                    "tapering": "Substituir por Fentanila ou Metadona.",
                    "is_sos": is_sos
                })
                med_tag_map[canonical] = "Ajuste Renal"

        if canonical in ["varfarina"]:
            anticoagulants.append(canonical)

    # 4. Regras da Tabela 4 (Interações)
    if len(snc_depressants) >= 2:
        alerts.append({
            "drug": "Múltiplos Depressores do SNC",
            "axis": "AGS Beers 2023 - Tabela 4",
            "recommendation": f"Prescrição simultânea de 2 ou mais drogas no SNC: {', '.join(snc_depressants)}.",
            "rationale": "Efeito sinérgico exponencial no risco de quedas e colapso respiratório.",
            "tapering": "Eleger o medicamento menos essencial para desmame.",
            "is_sos": False
        })
    
    if len(nsaids) > 0 and len(anticoagulants) > 0:
        alerts.append({
            "drug": "AINE + Anticoagulante",
            "axis": "AGS Beers 2023 - Tabela 4",
            "recommendation": "Uso concomitante aumenta severamente risco de sangramento.",
            "rationale": "Inibição plaquetária somada ao bloqueio da cascata de coagulação.",
            "tapering": "Suspender AINE imediatamente.",
            "is_sos": False
        })

    acb_text = "Carga Nula ou Leve. Risco controlado."
    if acb_total >= 3:
        acb_text = f"ALTO RISCO (Score {acb_total}). Probabilidade severa de declínio cognitivo e delirium."
    elif acb_total in [1, 2]:
        acb_text = f"Carga Moderada (Score {acb_total}). Vigiar retenção urinária e confusão mental."

    return alerts, acb_total, acb_text, med_tag_map
