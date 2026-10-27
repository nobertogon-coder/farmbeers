# -*- coding: utf-8 -*-
import re
import unicodedata

# =====================================================================
# 1. DICIONÁRIO MESTRE DE DROGAS (AGS Beers 2023 + ACB)
# Total: 49 Princípios Ativos de Alto Risco mapeados.
# =====================================================================
BEERS_DRUGS = {
    # 1. SNC e Anticonvulsivantes
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

    # 2. Anticolinérgicos e Anti-histamínicos
    "prometazina": ["prometazina", "fenergan"],
    "dimenidrinato": ["dimenidrinato", "dramin", "nausicalm"],
    "dexclorfeniramina": ["dexclorfeniramina", "polaramine", "histamin"],
    "hidroxizina": ["hidroxizina", "hixizine"],
    "escopolamina": ["escopolamina", "hioscina", "buscopan", "hyoscine"],
    "amitriptilina": ["amitriptilina", "tryptanol", "amytril"],
    "nortriptilina": ["nortriptilina", "pamelor"],

    # 3. Analgésicos, Opioides e Relaxantes Musculares
    "ciclobenzaprina": ["ciclobenzaprina", "miosan", "musculare"],
    "orfenadrina": ["orfenadrina", "dorflex"],
    "carisoprodol": ["carisoprodol", "torsilax", "tandrilax"],
    "morfina": ["morfina", "dimorf"],
    "tramadol": ["tramadol", "tramal", "sylador"],
    "codeina": ["codeina", "tylex", "paco"],

    # 4. AINEs
    "cetoprofeno": ["cetoprofeno", "profenid", "biprofenid"],
    "diclofenaco": ["diclofenaco", "voltaren", "cataflam", "flotac"],
    "ibuprofeno": ["ibuprofeno", "alivium", "advil"],
    "naproxeno": ["naproxeno", "flanax"],
    "nimesulida": ["nimesulida", "nisulid", "cimelide"],
    "cetorolaco": ["cetorolaco", "toragesic", "trometamol"],
    "meloxicam": ["meloxicam", "bioflex", "movatec"],

    # 5. Cardiovasculares e Renais
    "clonidina": ["clonidina", "atensina"],
    "doxazosina": ["doxazosina", "cardura"],
    "metildopa": ["metildopa", "aldomet"],
    "amiodarona": ["amiodarona", "ancoron", "atlansil"],
    "digoxina": ["digoxina", "lanoxin"],
    "espironolactona": ["espironolactona", "aldactone", "diempax"],
    "enoxaparina": ["enoxaparina", "clexane", "versa"],
    "varfarina": ["varfarina", "marevan", "coumadin"],

    # 6. Endocrinologia e TGI
    "glibenclamida": ["glibenclamida", "daonil"],
    "glimepirida": ["glimepirida", "amaryl"],
    "metoclopramida": ["metoclopramida", "plasil"],
    "oleo mineral": ["oleo mineral", "nujol"],
    "omeprazol": ["omeprazol", "losec", "peptazol"],
    "pantoprazol": ["pantoprazol", "pantocal"],

    # 7. Antipsicóticos
    "risperidona": ["risperidona", "risperdal"],
    "quetiapina": ["quetiapina", "seroquel"],
    "haloperidol": ["haloperidol", "haldol"],
    "olanzapina": ["olanzapina", "zyprexa"],
    "clorpromazina": ["clorpromazina", "amplictil"]
}

# =====================================================================
# ESCORE ACB (Gera pontuação paralela independente)
# =====================================================================
ACB_SCORES = {
    "amitriptilina": 3, "prometazina": 3, "escopolamina": 3, "dimenidrinato": 3,
    "dexclorfeniramina": 3, "hidroxizina": 3, "clorpromazina": 3, "olanzapina": 3,
    "nortriptilina": 3, "carbamazepina": 2, "ciclobenzaprina": 2, "orfenadrina": 2,
    "risperidona": 1, "quetiapina": 1, "haloperidol": 1, "diazepam": 1, "alprazolam": 1
}

# =====================================================================
# FUNÇÕES DE PROCESSAMENTO
# =====================================================================
def normalize_text(text: str) -> str:
    if not text: return ""
    nfkd_form = unicodedata.normalize('NFKD', text)
    return nfkd_form.encode('ASCII', 'ignore').decode('utf-8').lower()

def identify_drug_canonical(drug_name: str) -> str:
    if not drug_name: return ""
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
# 3. MOTOR CLÍNICO: MAPA EXAUSTIVO DAS 49 DROGAS (BLINDADO)
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

        # PARTE A: GERAÇÃO DO ESCORE ACB (Se aplicável)
        if canonical in ACB_SCORES:
            score = ACB_SCORES[canonical]
            acb_total += score
            alerts.append({
                "drug": canonical.capitalize(),
                "axis": "ACB Score (Carga Anticolinérgica)",
                "recommendation": f"Pontua {score} no Escore ACB. Risco de delirium, boca seca e retenção urinária.",
                "rationale": "A depleção colinérgica está ligada ao declínio cognitivo agudo e crônico.",
                "tapering": "Considerar desprescrição ou substituição.",
                "is_sos": is_sos,
                "acb_score": score
            })

        # PARTE B: REGRAS ESTRITAS DE BEERS (Garante que as 49 drogas disparem alerta)
        
        # GRUPO 1: ANTICOLINÉRGICOS FORTES (Tabela 2)
        if canonical in ["prometazina", "dimenidrinato", "dexclorfeniramina", "hidroxizina", "escopolamina", "amitriptilina", "nortriptilina"]:
            alerts.append({
                "drug": canonical.capitalize(),
                "axis": "AGS Beers 2023 - Tabela 2",
                "recommendation": "Altamente Anticolinérgico. Evitar uso.",
                "rationale": "Comprometimento do clearance renal do idoso potencializa toxicidade no SNC (delirium e alucinações).",
                "tapering": "Substituir por anti-histamínicos de 2ª geração ou suspender.",
                "is_sos": is_sos
            })
            med_tag_map[canonical] = "Alto Risco Anticolinérgico"

        # GRUPO 2: BENZODIAZEPÍNICOS, DROGAS Z E BARBITÚRICOS
        elif canonical in ["diazepam", "clonazepam", "lorazepam", "midazolam", "alprazolam", "zolpidem", "fenobarbital"]:
            snc_depressants.append(canonical)
            alerts.append({
                "drug": canonical.capitalize(),
                "axis": "AGS Beers 2023 - Tabela 2",
                "recommendation": "Evitar prescrição. Elevado risco de ataxia, síncope e fratura de fêmur.",
                "rationale": "Hipersensibilidade de receptores GABA e aumento da meia-vida em tecido adiposo.",
                "tapering": "Redução gradual de 25% da dose a cada 7-14 dias. Não suspender abruptamente.",
                "is_sos": is_sos
            })
            med_tag_map[canonical] = "Risco Queda/SNC"

        # GRUPO 3: FENITOÍNA
        elif canonical == "fenitoina":
            alerts.append({
                "drug": canonical.capitalize(),
                "axis": "AGS Beers 2023 - Tabela 2 / Janela Estreita",
                "recommendation": "Evitar uso se houver alternativa. Risco elevado de toxicidade neurológica central.",
                "rationale": "Idosos têm menor albumina sérica; a fração livre e tóxica da fenitoína aumenta drasticamente.",
                "tapering": "Monitorar nível sérico livre. Avaliar transição para Levetiracetam.",
                "is_sos": is_sos
            })
            med_tag_map[canonical] = "Tox. Neurológica"

        # GRUPO 4: OUTROS ANTICONVULSIVANTES E ESTABILIZADORES
        elif canonical in ["carbamazepina", "acido valproico"]:
            snc_depressants.append(canonical)
            alerts.append({
                "drug": canonical.capitalize(),
                "axis": "AGS Beers 2023 - Alerta Geriátrico",
                "recommendation": "Usar com cautela. Monitorar interações hepáticas severas e quedas.",
                "rationale": "Risco de SIADH (hiponatremia induzida), tremor e parkinsonismo secundário.",
                "tapering": "Dosar sódio sérico e evitar polifarmácia concomitante.",
                "is_sos": is_sos
            })
            med_tag_map[canonical] = "Risco SNC/SIADH"

        # GRUPO 5: RELAXANTES MUSCULARES
        elif canonical in ["ciclobenzaprina", "orfenadrina", "carisoprodol"]:
            alerts.append({
                "drug": canonical.capitalize(),
                "axis": "AGS Beers 2023 - Tabela 2",
                "recommendation": "Evitar. Tolerabilidade extremamente pobre em geriatria.",
                "rationale": "Efeitos adversos anticolinérgicos e sedativos profundos superam a analgesia.",
                "tapering": "Suspender. Preferir analgesia simples ou compressas.",
                "is_sos": is_sos
            })
            med_tag_map[canonical] = "Relaxante Muscular Inadequado"

        # GRUPO 6: AINEs
        elif canonical in ["cetoprofeno", "diclofenaco", "ibuprofeno", "naproxeno", "nimesulida", "cetorolaco", "meloxicam"]:
            nsaids.append(canonical)
            alerts.append({
                "drug": canonical.capitalize(),
                "axis": "AGS Beers 2023 - Tabela 2",
                "recommendation": "Evitar uso, principalmente crônico. Risco grave de HDA e Lesão Renal Aguda.",
                "rationale": "Inibição de COX afeta diretamente a barreira mucosa e a perfusão glomerular.",
                "tapering": "Suspender imediatamente. Substituir por Paracetamol ou opioide fraco.",
                "is_sos": is_sos
            })
            med_tag_map[canonical] = "Risco Renal/HDA"

        # GRUPO 7: OPIOIDES (Inclui alerta obrigatório de renal para morfina)
        elif canonical in ["morfina", "tramadol", "codeina"]:
            snc_depressants.append(canonical)
            if canonical == "morfina":
                if crcl is not None and crcl < 30:
                    alerts.append({
                        "drug": canonical.capitalize(),
                        "axis": "AGS Beers 2023 - Tabela 6 (Renal Crítico)",
                        "recommendation": f"Suspender ou Evitar. CrCl {crcl} mL/min. Risco de coma.",
                        "rationale": "Acúmulo de M3G/M6G por falha renal causa neurotoxicidade e depressão respiratória.",
                        "tapering": "Substituir por Fentanila ou Metadona (metabolismo hepático).",
                        "is_sos": is_sos
                    })
                    med_tag_map[canonical] = "Ajuste Renal Crítico"
                else:
                    alerts.append({
                        "drug": canonical.capitalize(),
                        "axis": "Atenção Geriátrica - Função Renal",
                        "recommendation": "Exige monitoramento renal estrito. Droga neurotóxica se CrCl < 30.",
                        "rationale": "Metabólitos ativos acumulam-se rapidamente na disfunção renal do idoso.",
                        "tapering": "Se CrCl desconhecido, solicitar exame antes da manutenção da droga.",
                        "is_sos": is_sos
                    })
                    med_tag_map[canonical] = "Risco Opioide/Renal"
            else:
                alerts.append({
                    "drug": canonical.capitalize(),
                    "axis": "Atenção Geriátrica - Opioide",
                    "recommendation": "Monitorar sedação, tontura e garantir protocolo de constipação.",
                    "rationale": "Queda da motilidade intestinal e limiar rebaixado para confusão mental.",
                    "tapering": "Usar a menor dose possível. Associar macrogol se uso regular.",
                    "is_sos": is_sos
                })
                med_tag_map[canonical] = "Opioide/SNC"

        # GRUPO 8: ALFA-AGONISTAS E CARDIO
        elif canonical in ["clonidina", "doxazosina", "metildopa"]:
            alerts.append({
                "drug": canonical.capitalize(),
                "axis": "AGS Beers 2023 - Tabela 2",
                "recommendation": "Evitar como anti-hipertensivo de rotina.",
                "rationale": "Alto risco de hipotensão ortostática grave, bradicardia e síncope.",
                "tapering": "Desmame progressivo (Clonidina pode causar rebote fatal se parada subitamente).",
                "is_sos": is_sos
            })
            med_tag_map[canonical] = "Risco Ortostático"

        elif canonical == "amiodarona":
            alerts.append({
                "drug": canonical.capitalize(),
                "axis": "AGS Beers 2023 - Tabela 2",
                "recommendation": "Evitar como 1ª linha para Fibrilação Atrial.",
                "rationale": "Toxicidade orgânica múltipla (pulmão, tireoide, fígado) e meia-vida de meses.",
                "tapering": "Avaliar controle de frequência no lugar de ritmo.",
                "is_sos": is_sos
            })
            med_tag_map[canonical] = "Tox. Cumulativa"

        elif canonical == "digoxina":
            alerts.append({
                "drug": canonical.capitalize(),
                "axis": "AGS Beers 2023 - Tabela 2",
                "recommendation": "Evitar uso de doses maiores que 0,125 mg/dia.",
                "rationale": "Janela terapêutica super estreita associada a menor clearance renal geriátrico.",
                "tapering": "Monitorar função renal e K+.",
                "is_sos": is_sos
            })
            med_tag_map[canonical] = "Janela Estreita"

        # GRUPO 9: RENAL EXCLUSIVO (Espironolactona e Enoxaparina)
        elif canonical == "espironolactona":
            if crcl is not None and crcl < 30:
                alerts.append({
                    "drug": canonical.capitalize(),
                    "axis": "AGS Beers 2023 - Tabela 6 (Renal)",
                    "recommendation": f"Evitar uso com CrCl {crcl} mL/min. Risco de parada cardíaca por hipercalemia.",
                    "rationale": "Inibição de K+ tubular sem depuração glomerular agrava hipercalemia rapidamente.",
                    "tapering": "Suspender droga imediatamente.",
                    "is_sos": is_sos
                })
                med_tag_map[canonical] = "Ajuste Renal Crítico"
            else:
                alerts.append({
                    "drug": canonical.capitalize(),
                    "axis": "Alerta Geriátrico - Risco Renal",
                    "recommendation": "Uso condicionado ao Clearance de Creatinina (Evitar se CrCl < 30).",
                    "rationale": "Medicamento fatal se houver declínio renal agudo despercebido.",
                    "tapering": "Garantir medição de eletrólitos antes da dose.",
                    "is_sos": is_sos
                })
                med_tag_map[canonical] = "Risco Hipercalemia"

        elif canonical == "enoxaparina":
            anticoagulants.append(canonical)
            if crcl is not None and crcl < 30:
                alerts.append({
                    "drug": canonical.capitalize(),
                    "axis": "AGS Beers 2023 - Tabela 6 (Renal)",
                    "recommendation": f"Disfunção renal (CrCl {crcl}). Ajuste obrigatório (Ex: Profilaxia para 20mg/dia).",
                    "rationale": "Sem filtração glomerular, o fármaco acumula no sangue gerando hemorragia maciça.",
                    "tapering": "Ajustar dose ou transicionar para Heparina Não Fracionada (HNF).",
                    "is_sos": is_sos
                })
                med_tag_map[canonical] = "Ajuste Renal Crítico"
            else:
                alerts.append({
                    "drug": canonical.capitalize(),
                    "axis": "Alerta Geriátrico - Risco Renal",
                    "recommendation": "Uso condicionado ao Clearance. Exige ajuste se CrCl < 30.",
                    "rationale": "Sem função renal confirmada, a heparina acumula no idoso.",
                    "tapering": "Garantir o cálculo Cockcroft-Gault antes de manter prescrição plena.",
                    "is_sos": is_sos
                })
                med_tag_map[canonical] = "Ajuste Renal"

        elif canonical == "varfarina":
            anticoagulants.append(canonical)
            alerts.append({
                "drug": canonical.capitalize(),
                "axis": "Janela Estreita / Interações",
                "recommendation": "Alto risco hemorrágico em idosos polimedicados e desnutridos.",
                "rationale": "Sofre interferência direta de hipoalbuminemia e inibidores da CYP450.",
                "tapering": "Controle estrito de RNI (INR).",
                "is_sos": is_sos
            })
            med_tag_map[canonical] = "Risco Hemorragia"

        # GRUPO 10: ENDÓCRINO E TGI
        elif canonical in ["glibenclamida", "glimepirida"]:
            alerts.append({
                "drug": canonical.capitalize(),
                "axis": "AGS Beers 2023 - Tabela 2",
                "recommendation": "Evitar prescrição. Risco de hipoglicemia severa e letal.",
                "rationale": "Ação prolongada associada à falha da resposta adrenérgica no idoso (hipoglicemia não sentida).",
                "tapering": "Substituir por Inibidor de DPP-4 (ex: Linagliptina).",
                "is_sos": is_sos
            })
            med_tag_map[canonical] = "Risco Hipoglicemia"

        elif canonical == "metoclopramida":
            alerts.append({
                "drug": canonical.capitalize(),
                "axis": "AGS Beers 2023 - Tabela 2",
                "recommendation": "Evitar, especialmente uso contínuo.",
                "rationale": "Forte penetração no SNC causando parkinsonismo medicamentoso e discinesia tardia.",
                "tapering": "Trocar por Ondansetrona ou Domperidona (menor penetração central).",
                "is_sos": is_sos
            })
            med_tag_map[canonical] = "Risco Extrapiramidal"

        elif canonical == "oleo mineral":
            alerts.append({
                "drug": canonical.capitalize(),
                "axis": "AGS Beers 2023 - Tabela 2",
                "recommendation": "Evitar uso oral para constipação.",
                "rationale": "Elevado risco de pneumonia lipoídica silenciosa por microaspiração.",
                "tapering": "Substituir por laxantes osmóticos (Macrogol ou Lactulose).",
                "is_sos": is_sos
            })
            med_tag_map[canonical] = "Risco Aspiração"

        elif canonical in ["omeprazol", "pantoprazol"]:
            alerts.append({
                "drug": canonical.capitalize(),
                "axis": "AGS Beers 2023 - Tabela 2",
                "recommendation": "Evitar uso > 8 semanas sem justificativa formal (HDA prévia, esofagite grave).",
                "rationale": "Supressão ácida causa fraturas osteoporóticas, deficiência de B12 e infecção por C. difficile.",
                "tapering": "Reduzir 50% da dose ou espaçar para dias alternados até suspensão.",
                "is_sos": is_sos
            })
            med_tag_map[canonical] = "Uso Crônico Indevido"

        # GRUPO 11: ANTIPSICÓTICOS
        elif canonical in ["risperidona", "quetiapina", "haloperidol", "olanzapina", "clorpromazina"]:
            snc_depressants.append(canonical)
            alerts.append({
                "drug": canonical.capitalize(),
                "axis": "AGS Beers 2023 - Tabela 2 (Antipsicóticos)",
                "recommendation": "Evitar como rotina para insônia ou agitação demencial leve.",
                "rationale": "Black Box Warning: triplica risco de AVC isquêmico e morte súbita em idosos com demência.",
                "tapering": "Usar apenas no delirium grave (menor dose/tempo). Desmamar o quanto antes.",
                "is_sos": is_sos
            })
            med_tag_map[canonical] = "Risco AVC/Mortalidade"

    # PARTE C: AVALIAÇÃO DE INTERAÇÕES SINÉRGICAS (Tabela 4)
    if len(snc_depressants) >= 2:
        alerts.append({
            "drug": "Múltiplos Depressores do SNC",
            "axis": "AGS Beers 2023 - Tabela 4",
            "recommendation": f"Uso simultâneo de {len(snc_depressants)} sedativos ({', '.join(snc_depressants)}).",
            "rationale": "O efeito central se multiplica, gerando parada respiratória, quedas e delirium irreversível.",
            "tapering": "Escolher a droga de menor prioridade e iniciar desprescrição imediata.",
            "is_sos": False
        })
    
    if len(nsaids) > 0 and len(anticoagulants) > 0:
        alerts.append({
            "drug": "AINE + Anticoagulante",
            "axis": "AGS Beers 2023 - Tabela 4",
            "recommendation": "ALERTA CRÍTICO: Uso concomitante aumenta severamente risco de sangramento.",
            "rationale": "Inibição de plaquetas (AINE) e bloqueio da coagulação somam-se à corrosão gástrica.",
            "tapering": "Suspender AINE imediatamente.",
            "is_sos": False
        })

    # PARTE D: FECHAMENTO ACB
    acb_text = "Carga Nula ou Leve. Risco controlado."
    if acb_total >= 3:
        acb_text = f"ALTO RISCO (Score {acb_total}). Probabilidade severa de declínio cognitivo, delirium e retenção periférica."
    elif acb_total in [1, 2]:
        acb_text = f"Carga Moderada (Score {acb_total}). Vigiar queixas de constipação e confusão mental."

    return alerts, acb_total, acb_text, med_tag_map
