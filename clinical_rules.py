# =====================================================================
# 3. MOTOR CLÍNICO: AVALIAÇÃO BEERS E ACB SCORE
# =====================================================================
def evaluate_patient_beers(medications, age, fall_risk=False, conditions=None, crcl=None):
    alerts = []
    acb_total = 0
    med_tag_map = {}
    
    if conditions is None:
        conditions = []

    # Se a idade for inferior a 65 anos, as regras geriátricas estritas não se aplicam
    if age < 65:
        return alerts, acb_total, "Idade inferior a 65 anos. Triagem geriátrica não aplicável.", med_tag_map

    # Listas para verificar interações (Tabela 4)
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

        # 2. Regras da Tabela 2 (Evitar na maioria dos idosos)
        
        # --- AQUI ESTÁ A CORREÇÃO DA FENITOÍNA ---
        if canonical == "fenitoina":
            alerts.append({
                "drug": canonical.capitalize(),
                "axis": "AGS Beers 2023 - Tabela 2 / Janela Estreita",
                "recommendation": "Evitar uso. Risco elevado de toxicidade neurológica central (ataxia, nistagmo, declínio cognitivo e encefalopatia).",
                "rationale": "Farmacocinética não linear e alta ligação proteica dependente de albumina. Altamente tóxico em idosos desnutridos.",
                "tapering": "Avaliar substituição por Levetiracetam ou Lamotrigina se indicado. Monitorar nível sérico livre se uso compulsório.",
                "is_sos": is_sos
            })
            med_tag_map[canonical] = "Tox. Neurológica"
        # ----------------------------------------

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
                "rationale": "Falência dos mecanismos contrarreguladores adrenérgicos no idoso (hipoglicemia assintomática).",
                "tapering": "Substituir por Inibidor de DPP-4 (ex: Linagliptina) ou esquema de insulina seguro.",
                "is_sos": is_sos
            })
            med_tag_map[canonical] = "Risco Hipoglicemia"

        if canonical in ["cetoprofeno", "diclofenaco", "ibuprofeno", "naproxeno", "nimesulida", "cetorolaco", "meloxicam"]:
            nsaids.append(canonical)
            alerts.append({
                "drug": canonical.capitalize(),
                "axis": "AGS Beers 2023 - Tabela 2",
                "recommendation": "Evitar uso. Risco de Hemorragia Digestiva e Lesão Renal Aguda.",
                "rationale": "Inibição de prostaglandinas induz constrição da arteríola aferente (isquemia glomerular).",
                "tapering": "Suspender. Substituir por Dipirona/Paracetamol fixo ou opioides fracos (Tramadol).",
                "is_sos": is_sos
            })
            med_tag_map[canonical] = "Risco Renal/Gástrico"

        # 3. Regras da Tabela 6 (Ajuste por Função Renal)
        if crcl is not None:
            if canonical == "enoxaparina" and crcl < 30:
                anticoagulants.append(canonical)
                alerts.append({
                    "drug": canonical.capitalize(),
                    "axis": "AGS Beers 2023 - Tabela 6 (Renal)",
                    "recommendation": f"Função renal comprometida (CrCl {crcl} mL/min). Reduzir dose profilática para 20mg/dia.",
                    "rationale": "Eliminação glomerular estrita. Risco de hemorragia grave por acúmulo de fator anti-Xa.",
                    "tapering": "Adequar dose baseada na taxa de filtração.",
                    "is_sos": is_sos
                })
                med_tag_map[canonical] = "Ajuste Renal"

            if canonical == "espironolactona" and crcl < 30:
                alerts.append({
                    "drug": canonical.capitalize(),
                    "axis": "AGS Beers 2023 - Tabela 6 (Renal)",
                    "recommendation": f"Evitar uso com CrCl {crcl} mL/min. Risco elevado de hipercalemia fatal.",
                    "rationale": "Inibição da excreção de potássio tubular sem capacidade de depuração glomerular.",
                    "tapering": "Suspender prescrição e monitorar potássio sérico.",
                    "is_sos": is_sos
                })
                med_tag_map[canonical] = "Ajuste Renal"

            if canonical == "morfina" and crcl < 30:
                alerts.append({
                    "drug": canonical.capitalize(),
                    "axis": "AGS Beers 2023 - Tabela 6 (Renal)",
                    "recommendation": f"Evitar uso com CrCl {crcl} mL/min. Substituir analgésico.",
                    "rationale": "Acúmulo de M3G e M6G causa neurotoxicidade (mioclonias) e depressão respiratória.",
                    "tapering": "Substituir por Fentanila ou Metadona (metabolismo hepático em metabólitos inativos).",
                    "is_sos": is_sos
                })
                med_tag_map[canonical] = "Ajuste Renal"

        if canonical in ["varfarina"]:
            anticoagulants.append(canonical)

    # 4. Regras da Tabela 4 (Interações Sinérgicas Geriátricas)
    if len(snc_depressants) >= 2:
        alerts.append({
            "drug": "Múltiplos Depressores do SNC",
            "axis": "AGS Beers 2023 - Tabela 4",
            "recommendation": f"Prescrição simultânea de 2 ou mais drogas no SNC: {', '.join(snc_depressants)}.",
            "rationale": "Efeito sinérgico exponencial no risco de quedas e colapso respiratório.",
            "tapering": "Eleger o medicamento menos essencial para desmame imediato.",
            "is_sos": False
        })
    
    if len(nsaids) > 0 and len(anticoagulants) > 0:
        alerts.append({
            "drug": "AINE + Anticoagulante",
            "axis": "AGS Beers 2023 - Tabela 4",
            "recommendation": "Uso concomitante aumenta severamente risco de sangramento.",
            "rationale": "Inibição plaquetária somada à depleção da mucosa gástrica e bloqueio da cascata de coagulação.",
            "tapering": "Suspender AINE imediatamente.",
            "is_sos": False
        })

    # Interpretação do Escore ACB
    acb_text = "Carga Nula ou Leve. Risco controlado."
    if acb_total >= 3:
        acb_text = f"ALTO RISCO (Score {acb_total}). Probabilidade severa de declínio cognitivo, delirium hospitalar e retenção periférica."
    elif acb_total in [1, 2]:
        acb_text = f"Carga Moderada (Score {acb_total}). Vigiar retenção urinária e confusão mental."

    return alerts, acb_total, acb_text, med_tag_map
