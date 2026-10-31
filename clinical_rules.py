# -*- coding: utf-8 -*-
import re
import unicodedata

# =====================================================================
# 1. DICIONÁRIO MESTRE DE DROGAS (Radar Beers - AGS 2023 + ACB)
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

ACB_SCORES = {
    "amitriptilina": 3, "prometazina": 3, "escopolamina": 3, "dimenidrinato": 3,
    "dexclorfeniramina": 3, "hidroxizina": 3, "clorpromazina": 3, "olanzapina": 3,
    "nortriptilina": 3, "carbamazepina": 2, "ciclobenzaprina": 2, "orfenadrina": 2,
    "risperidona": 1, "quetiapina": 1, "haloperidol": 1, "diazepam": 1, "alprazolam": 1
}

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
# 3. MOTOR CLÍNICO: SEPARAÇÃO ENTRE USO CONTÍNUO VS. SN/QN
# =====================================================================
def evaluate_patient_beers(medications, age, fall_risk=False, conditions=None, crcl=None):
    alerts = []
    acb_continuous = 0
    acb_sos_potential = 0
    med_tag_map = {}

    if conditions is None:
        conditions = []
    if age < 65:
        return alerts, 0, "Idade inferior a 65 anos. Triagem geriátrica não aplicável.", med_tag_map

    snc_depressants_fixed = []
    snc_depressants_sos = []
    nsaids = []
    anticoagulants = []

    for med in medications:
        raw_name = med.get("name", "")
        canonical = identify_drug_canonical(raw_name)
        if not canonical:
            continue

        freq_str = str(med.get("frequency", "")).lower()
        dose_str = str(med.get("dose", "")).lower()
        is_sos = bool(med.get("is_sos", False)) or any(k in freq_str or k in dose_str for k in ["sn", "qn", "sos", "necessario", "necessário", "acm"])

        # PARTE A: ESCORE ACB (Separa uso fixo de uso SN/QN)
        if canonical in ACB_SCORES:
            score = ACB_SCORES[canonical]
            if is_sos:
                acb_sos_potential += score
                alerts.append({
                    "drug": canonical.capitalize(),
                    "axis": "ACB Score Potencial (Prescrito SN/QN)",
                    "recommendation": f"Paciente não faz uso contínuo (prescrito SN/QN). Se administrado, soma +{score} ponto(s) de carga anticolinérgica.",
                    "rationale": "Mesmo em doses isoladas de resgate, anticolinérgicos fortes precipitam delirium agudo, retenção urinária (bexigoma) e quedas noturnas.",
                    "tapering": "Não requer desmame. Verificar se houve administração nas últimas 24h e sugerir substituição preventiva do resgate.",
                    "is_sos": True,
                    "acb_score": score
                })
            else:
                acb_continuous += score
                alerts.append({
                    "drug": canonical.capitalize(),
                    "axis": "ACB Score (Carga Anticolinérgica Ativa)",
                    "recommendation": f"Uso contínuo pontua {score} no Escore ACB. Alto risco de delirium, boca seca, constipação e bexigoma.",
                    "rationale": "A depleção colinérgica cumulativa está diretamente associada ao declínio cognitivo em idosos.",
                    "tapering": "Avaliar desprescrição ou substituição por fármaco sem efeito anticolinérgico.",
                    "is_sos": False,
                    "acb_score": score
                })
            med_tag_map[canonical] = "Carga Anticolinérgica (SN/QN)" if is_sos else "Carga Anticolinérgica"

        # PARTE B: REGRAS DE BEERS (49 DROGAS)
        base_alert = None

        if canonical in ["prometazina", "dimenidrinato", "dexclorfeniramina", "hidroxizina", "escopolamina", "amitriptilina", "nortriptilina"]:
            base_alert = {
                "drug": canonical.capitalize(),
                "axis": "AGS Beers 2023 - Tabela 2",
                "recommendation": "Fármaco altamente anticolinérgico. Evitar uso em idosos.",
                "rationale": "Redução da depuração no idoso potencializa confusão mental, sedação residual e retenção urinária.",
                "tapering": "Substituir por opção segura (ex: Ondansetrona para náusea; Loratadina para alergia; Dipirona para dor)."
            }
            med_tag_map[canonical] = "Alto Risco Anticolinérgico"

        elif canonical in ["diazepam", "clonazepam", "lorazepam", "midazolam", "alprazolam", "zolpidem", "fenobarbital"]:
            if is_sos:
                snc_depressants_sos.append(canonical)
            else:
                snc_depressants_fixed.append(canonical)
            base_alert = {
                "drug": canonical.capitalize(),
                "axis": "AGS Beers 2023 - Tabela 2",
                "recommendation": "Evitar prescrição. Elevado risco de sedação excessiva, ataxia, síncope e fratura de fêmur.",
                "rationale": "Hipersensibilidade de receptores GABA e aumento da meia-vida de eliminação em idosos.",
                "tapering": "Redução gradual de 25% da dose a cada 7 a 14 dias (não suspender abruptamente se uso crônico)."
            }
            med_tag_map[canonical] = "Risco Queda/SNC"

        elif canonical == "fenitoina":
            base_alert = {
                "drug": canonical.capitalize(),
                "axis": "AGS Beers 2023 - Tabela 2 / Janela Estreita",
                "recommendation": "Evitar uso se houver alternativa mais segura. Alto risco de toxicidade neurológica central (nistagmo, ataxia).",
                "rationale": "Cinética de saturação (Michaelis-Menten) e forte ligação à albumina; em idosos hipoalbuminêmicos a fração livre tóxica dispara.",
                "tapering": "Monitorar nível sérico corrigido pela albumina ou avaliar transição gradual para Levetiracetam/Lamotrigina."
            }
            med_tag_map[canonical] = "Tox. Neurológica"

        elif canonical in ["carbamazepina", "acido valproico"]:
            if is_sos:
                snc_depressants_sos.append(canonical)
            else:
                snc_depressants_fixed.append(canonical)
            base_alert = {
                "drug": canonical.capitalize(),
                "axis": "AGS Beers 2023 - Alerta Geriátrico",
                "recommendation": "Usar com cautela. Vigiar hiponatremia (SIADH), sedação e interações medicamentosas.",
                "rationale": "Potencial indutor/inibidor enzimático hepático e risco de instabilidade postural no idoso.",
                "tapering": "Monitorar sódio sérico periodicamente e revisar fármacos concomitantes."
            }
            med_tag_map[canonical] = "Risco SNC/SIADH"

        elif canonical in ["ciclobenzaprina", "orfenadrina", "carisoprodol"]:
            base_alert = {
                "drug": canonical.capitalize(),
                "axis": "AGS Beers 2023 - Tabela 2",
                "recommendation": "Evitar relaxantes musculares em idosos.",
                "rationale": "Pouca eficácia clínica nas doses toleradas e alto índice de sedação, fraqueza muscular e quedas.",
                "tapering": "Suspender e priorizar analgesia simples (Dipirona/Paracetamol) e medidas físicas locais."
            }
            med_tag_map[canonical] = "Relaxante Muscular Inadequado"

        elif canonical in ["cetoprofeno", "diclofenaco", "ibuprofeno", "naproxeno", "nimesulida", "cetorolaco", "meloxicam"]:
            nsaids.append(canonical)
            base_alert = {
                "drug": canonical.capitalize(),
                "axis": "AGS Beers 2023 - Tabela 2",
                "recommendation": "Evitar uso. Risco elevado de Lesão Renal Aguda (LRA) e Hemorragia Digestiva Alta (HDA).",
                "rationale": "O bloqueio de prostaglandinas causa vasoconstrição da arteríola aferente glomerular e isquemia renal.",
                "tapering": "Suspender imediatamente e substituir por Dipirona ou Paracetamol."
            }
            med_tag_map[canonical] = "Risco Renal/HDA"

        elif canonical in ["morfina", "tramadol", "codeina"]:
            if is_sos:
                snc_depressants_sos.append(canonical)
            else:
                snc_depressants_fixed.append(canonical)
            if canonical == "morfina":
                if crcl is not None and crcl < 30:
                    base_alert = {
                        "drug": canonical.capitalize(),
                        "axis": "AGS Beers 2023 - Tabela 6 (Renal Crítico)",
                        "recommendation": f"Evitar uso com CrCl {crcl} mL/min. Risco de neurotoxicidade e depressão respiratória.",
                        "rationale": "Acúmulo renal dos metabólitos ativos M3G e M6G.",
                        "tapering": "Substituir por Fentanila ou Metadona (metabolização hepática)."
                    }
                    med_tag_map[canonical] = "Ajuste Renal Crítico"
                else:
                    base_alert = {
                        "drug": canonical.capitalize(),
                        "axis": "Atenção Geriátrica - Opioide Forte",
                        "recommendation": "Exige monitoramento da função renal (evitar se CrCl < 30 mL/min) e prevenção de constipação.",
                        "rationale": "Metabólitos ativos dependem de excreção renal; risco de retenção urinária e sedação.",
                        "tapering": "Titular menor dose eficaz e associar laxante osmótico se uso regular."
                    }
                    med_tag_map[canonical] = "Risco Opioide/Renal"
            else:
                base_alert = {
                    "drug": canonical.capitalize(),
                    "axis": "AGS Beers 2023 - Opioide / SNC",
                    "recommendation": "Usar com cautela. Risco de tontura, obstipação intestinal, SIADH (Tramadol) e quedas.",
                    "rationale": "Limiar reduzido para confusão mental e lentificação do trânsito gastrointestinal.",
                    "tapering": "Manter pelo menor tempo necessário; se uso contínuo, prescrever laxante profilático."
                }
                med_tag_map[canonical] = "Opioide/SNC"

        elif canonical in ["clonidina", "doxazosina", "metildopa"]:
            base_alert = {
                "drug": canonical.capitalize(),
                "axis": "AGS Beers 2023 - Tabela 2",
                "recommendation": "Evitar como anti-hipertensivo de rotina no idoso.",
                "rationale": "Alto risco de hipotensão ortostática severa, bradicardia, síncope e efeitos depressores centrais.",
                "tapering": "Desmame gradual obrigatório (suspensão abrupta de Clonidina causa hipertensão rebote)."
            }
            med_tag_map[canonical] = "Risco Ortostático"

        elif canonical == "amiodarona":
            base_alert = {
                "drug": canonical.capitalize(),
                "axis": "AGS Beers 2023 - Tabela 2",
                "recommendation": "Evitar como terapia de 1ª linha para Fibrilação Atrial (salvo em IC ou hipertrofia ventricular importante).",
                "rationale": "Meia-vida extremamente longa (semanas a meses) e toxicidade cumulativa tireoidiana, pulmonar e hepática.",
                "tapering": "Discutir estratégia de controle de frequência (betabloqueador) em vez de controle de ritmo."
            }
            med_tag_map[canonical] = "Tox. Cumulativa"

        elif canonical == "digoxina":
            base_alert = {
                "drug": canonical.capitalize(),
                "axis": "AGS Beers 2023 - Tabela 2",
                "recommendation": "Evitar doses superiores a 0,125 mg/dia e evitar como 1ª linha em Fibrilação Atrial ou IC.",
                "rationale": "Sarcopenia reduz o volume de distribuição e a queda da TFG promove intoxicação digitálica precoce.",
                "tapering": "Garantir dose <= 0,125 mg/dia e monitorar potássio, magnésio e função renal."
            }
            med_tag_map[canonical] = "Janela Estreita"

        elif canonical == "espironolactona":
            if crcl is not None and crcl < 30:
                base_alert = {
                    "drug": canonical.capitalize(),
                    "axis": "AGS Beers 2023 - Tabela 6 (Renal Crítico)",
                    "recommendation": f"Contraindicado com CrCl {crcl} mL/min (< 30 mL/min). Risco grave de hipercalemia fatal.",
                    "rationale": "Retenção tubular de potássio somada à incapacidade de filtração glomerular.",
                    "tapering": "Suspender prescrição e monitorar potássio sérico e ECG."
                }
                med_tag_map[canonical] = "Ajuste Renal Crítico"
            else:
                base_alert = {
                    "drug": canonical.capitalize(),
                    "axis": "AGS Beers 2023 - Tabela 6 (Vigilância Renal)",
                    "recommendation": "Monitorar função renal e Potássio sérico (Evitar se CrCl < 30 mL/min ou doses > 25 mg/dia).",
                    "rationale": "Idosos apresentam menor reserva tubular para excreção de potássio, especialmente se associados a IECA/BRA.",
                    "tapering": "Confirmar Clearance de Creatinina e K+ sérico."
                }
                med_tag_map[canonical] = "Risco Hipercalemia"

        elif canonical == "enoxaparina":
            anticoagulants.append(canonical)
            if crcl is not None and crcl < 30:
                base_alert = {
                    "drug": canonical.capitalize(),
                    "axis": "AGS Beers 2023 - Tabela 6 (Renal Crítico)",
                    "recommendation": f"Ajuste renal obrigatório (CrCl {crcl} mL/min < 30). Reduzir profilaxia para 20 mg/dia ou 1 mg/kg 1x/dia se terapêutica.",
                    "rationale": "Eliminação estritamente renal; acúmulo do fator anti-Xa eleva drasticamente o risco de sangramento maior.",
                    "tapering": "Ajustar posologia imediatamente ou substituir por Heparina Não Fracionada (HNF)."
                }
                med_tag_map[canonical] = "Ajuste Renal Crítico"
            else:
                base_alert = {
                    "drug": canonical.capitalize(),
                    "axis": "AGS Beers 2023 - Tabela 6 (Vigilância Renal)",
                    "recommendation": "Verificar Clearance de Creatinina corrigido para sarcopenia (Exige redução de dose se CrCl < 30 mL/min).",
                    "rationale": "Creatinina sérica falsamente normal em idosos sarcopênicos pode mascarar ClCr < 30 mL/min e causar sangramento.",
                    "tapering": "Preencher Peso, Idade e Creatinina na calculadora ao lado para validar a dose."
                }
                med_tag_map[canonical] = "Ajuste Renal"

        elif canonical == "varfarina":
            anticoagulants.append(canonical)
            base_alert = {
                "drug": canonical.capitalize(),
                "axis": "AGS Beers 2023 - Risco Hemorrágico",
                "recommendation": "Vigilância rigorosa de RNI (INR) e interações medicamentosas.",
                "rationale": "Maior risco de sangramento intracraniano e gastrointestinal em idosos, agravado por hipoalbuminemia.",
                "tapering": "Monitorar RNI frequentemente e avaliar possibilidade de DOAC ajustado à função renal."
            }
            med_tag_map[canonical] = "Risco Hemorragia"

        elif canonical in ["glibenclamida", "glimepirida"]:
            base_alert = {
                "drug": canonical.capitalize(),
                "axis": "AGS Beers 2023 - Tabela 2",
                "recommendation": "Evitar sulfonilureias em idosos. Alto risco de hipoglicemia severa e prolongada.",
                "rationale": "Meia-vida longa e perda dos sinais autonômicos de alerta (hipoglicemia silenciosa provocando síncope/isquemia).",
                "tapering": "Suspender e substituir por Inibidor de DPP-4 (Linagliptina), Metformina (se TFG > 30) ou insulina basal segura."
            }
            med_tag_map[canonical] = "Risco Hipoglicemia"

        elif canonical == "metoclopramida":
            base_alert = {
                "drug": canonical.capitalize(),
                "axis": "AGS Beers 2023 - Tabela 2",
                "recommendation": "Evitar uso (salvo gastroparesia documentada, por no máximo 12 semanas).",
                "rationale": "Atravessa a barreira hematoencefálica bloqueando receptores D2, causando parkinsonismo e discinesia tardia.",
                "tapering": "Substituir antiemético por Ondansetrona (4-8 mg) ou pró-cinético por Domperidona."
            }
            med_tag_map[canonical] = "Risco Extrapiramidal"

        elif canonical == "oleo mineral":
            base_alert = {
                "drug": canonical.capitalize(),
                "axis": "AGS Beers 2023 - Tabela 2",
                "recommendation": "Evitar uso por via oral.",
                "rationale": "Risco elevado de microaspiração silenciosa e pneumonia lipoídica grave em idosos.",
                "tapering": "Substituir por laxante osmótico seguro (Lactulose ou Macrogol/PEG 4000)."
            }
            med_tag_map[canonical] = "Risco Aspiração"

        elif canonical in ["omeprazol", "pantoprazol"]:
            base_alert = {
                "drug": canonical.capitalize(),
                "axis": "AGS Beers 2023 - Tabela 2",
                "recommendation": "Evitar uso contínuo por mais de 8 semanas sem indicação estrita (HDA, esofagite erosiva, uso de AINE).",
                "rationale": "Associação com infecção por Clostridioides difficile, perda óssea/fraturas e hipomagnesemia.",
                "tapering": "Desmame reduzindo a dose em 50% por 2 semanas ou uso sob demanda antes de suspender."
            }
            med_tag_map[canonical] = "Uso Crônico Indevido"

        elif canonical in ["risperidona", "quetiapina", "haloperidol", "olanzapina", "clorpromazina"]:
            if is_sos:
                snc_depressants_sos.append(canonical)
            else:
                snc_depressants_fixed.append(canonical)
            base_alert = {
                "drug": canonical.capitalize(),
                "axis": "AGS Beers 2023 - Tabela 2 (Antipsicóticos)",
                "recommendation": "Evitar para sintomas comportamentais da demência ou insônia hospitalar.",
                "rationale": "Aumenta o risco de Acidente Vascular Cerebral (AVC), declínio cognitivo acelerado e mortalidade (Black Box Warning).",
                "tapering": "Reservar apenas para delirium hiperativo grave com risco físico. Realizar desmame assim que estabilizado."
            }
            med_tag_map[canonical] = "Risco AVC/Mortalidade"

        # APLICAÇÃO DA REGRA SN/QN (SE NECESSÁRIO) VS. CONTÍNUO
        if base_alert:
            if is_sos:
                base_alert["axis"] = f"{base_alert['axis']} [Prescrito SN/QN]"
                base_alert["recommendation"] = (
                    f"[PACIENTE SEM USO CONTÍNUO - APENAS SN/QN]: {base_alert['recommendation']} "
                    f"Como está prescrito apenas 'Se Necessário', o risco ocorre se a dose for administrada."
                )
                base_alert["tapering"] = (
                    "Não requer desmame (uso não contínuo). Verificar na checagem da enfermagem se houve administração "
                    "nas últimas 24h. Se não utilizado, sugerir exclusão da prescrição ou troca preventiva por resgate seguro."
                )
                base_alert["is_sos"] = True
                if canonical in med_tag_map and "(SN/QN)" not in med_tag_map[canonical]:
                    med_tag_map[canonical] = f"{med_tag_map[canonical]} [SN/QN]"
            else:
                base_alert["is_sos"] = False

            alerts.append(base_alert)

    # PARTE C: INTERAÇÕES SINÉRGICAS (Tabela 4)
    total_snc = snc_depressants_fixed + snc_depressants_sos
    if len(total_snc) >= 2:
        if len(snc_depressants_fixed) >= 2:
            alerts.append({
                "drug": "Múltiplos Depressores do SNC (Uso Contínuo)",
                "axis": "AGS Beers 2023 - Tabela 4",
                "recommendation": f"Uso simultâneo fixo de {len(snc_depressants_fixed)} fármacos ativos no SNC ({', '.join(snc_depressants_fixed)}).",
                "rationale": "Sinergismo depressor central que multiplica o risco de quedas graves, fraturas e depressão respiratória.",
                "tapering": "Priorizar o desmame de um dos sedativos imediatamente.",
                "is_sos": False
            })
        else:
            alerts.append({
                "drug": "Associação Potencial no SNC (Fixo + SN/QN)",
                "axis": "AGS Beers 2023 - Tabela 4 [Alerta Preventivo]",
                "recommendation": f"Prescrição combina depressores do SNC entre uso fixo e resgate SN/QN ({', '.join(total_snc)}).",
                "rationale": "Caso o medicamento SN/QN seja administrado no plantão, haverá somação de efeito sedativo e risco agudo de queda.",
                "tapering": "Orientar a equipe a evitar a administração do resgate sedativo ou substituí-lo preventivamente.",
                "is_sos": True
            })

    if len(nsaids) > 0 and len(anticoagulants) > 0:
        alerts.append({
            "drug": "AINE + Anticoagulante",
            "axis": "AGS Beers 2023 - Tabela 4",
            "recommendation": "ALERTA CRÍTICO: Associação eleva severamente o risco de sangramento gastrointestinal.",
            "rationale": "Efeito antiplaquetário e lesão de mucosa do AINE somados à anticoagulação sistêmica.",
            "tapering": "Suspender o AINE imediatamente (mesmo se prescrito SN/QN).",
            "is_sos": False
        })

    # PARTE D: TEXTO EXPLICATIVO DO ACB SCORE (Diferenciando Fixo vs. SN/QN)
    if acb_continuous >= 3:
        acb_text = f"ALTO RISCO CONTÍNUO (Score Fixo: {acb_continuous}). Forte probabilidade de delirium hospitalar, declínio cognitivo e retenção urinária."
    elif acb_continuous in [1, 2]:
        acb_text = f"Carga Contínua Moderada (Score Fixo: {acb_continuous}). Vigiar constipação, boca seca e confusão mental."
    else:
        acb_text = "Carga Contínua Nula (Score Fixo: 0). Sem sobrecarga anticolinérgica de uso diário."

    if acb_sos_potential > 0:
        acb_text += f" | ATENÇÃO SN/QN: Há +{acb_sos_potential} pt(s) prescrito(s) 'Se Necessário' (só pontuam se administrados)."

    return alerts, acb_continuous, acb_text, med_tag_map
