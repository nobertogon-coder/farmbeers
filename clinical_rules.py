# -*- coding: utf-8 -*-
"""
FarmBeers - Motor Clínico Oficial (AGS Beers 2023)
Integrado com:
- Tabela 2 (Medicamentos a evitar em idosos)
- Tabela 4 (Interações medicamentosas de alto risco AGS Beers 2023)
- Tabela 6 (Ajuste por função renal)
- Carga Anticolinérgica Cumulativa (ACB Score)
- Modulação Posológica SN/QN/SOS
"""
import re
import unicodedata
from typing import List, Dict, Any, Optional, Tuple

def normalize_text(text: str) -> str:
    if not text:
        return ""
    text = unicodedata.normalize("NFD", text.lower())
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return " ".join(text.split())

ACB_SCORE_MAP = {
    "dexclorfeniramina": 3,
    "hidroxizina": 3,
    "prometazina": 3,
    "dimenidrinato": 3,
    "difenidramina": 3,
    "escopolamina": 3,
    "biperideno": 3,
    "oxibutinina": 3,
    "amitriptilina": 3,
    "clomipramina": 3,
    "nortriptilina": 3,
    "clorpromazina": 3,
    "levomepromazina": 3,
    "orfenadrina": 3,
    "ciclobenzaprina": 2,
    "carisoprodol": 2,
    "diazepam": 1,
    "clonazepam": 1,
    "lorazepam": 1,
    "alprazolam": 1,
    "haloperidol": 1,
    "risperidona": 1,
    "quetiapina": 1,
    "olanzapina": 1,
    "metoclopramida": 1,
    "clonidina": 1
}

BEERS_RULES = {
    "dexclorfeniramina": {
        "drug": "Dexclorfeniramina",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar)",
        "renal_dependent": False,
        "recommendation": "Evitar o uso rotineiro em idosos. Suspender e substituir por anti-histamínico de 2ª geração ou corticoide nasal.",
        "rationale": "Potente ação anticolinérgica central e periférica. Causa sedação pronunciada, boca seca, constipação severa, retenção urinária e elevação crítica do risco de declínio cognitivo e quedas.",
        "tapering": "Pode ser descontinuada diretamente. Substituir por Loratadina 10mg/dia ou Cetirizina 5-10mg/dia se houver rinite/alergia ativa.",
        "sos_note": "Prescrição identificada como SN/QN: Uso pontual para crise alérgica aguda tolerado. Não administrar em esquema fixo e monitorar sonolência e retenção urinária."
    },
    "hidroxizina": {
        "drug": "Hidroxizina",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar)",
        "renal_dependent": False,
        "recommendation": "Evitar o uso em geriatria.",
        "rationale": "Efeito anticolinérgico intenso e sedação residual prolongada com prejuízo cognitivo e psicomotor.",
        "tapering": "Suspensão direta; avaliar uso de emolientes tópicos ou anti-histamínicos não sedativos para prurido.",
        "sos_note": "Uso como resgate SN/QN: Evitar doses repetidas; preferir anti-histamínico de 2ª geração mesmo no alívio de sintomas agudos."
    },
    "prometazina": {
        "drug": "Prometazina",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar)",
        "renal_dependent": False,
        "recommendation": "Evitar o uso rotineiro como antialérgico, antiemético ou sedativo.",
        "rationale": "Fenotiazina com bloqueio colinérgico, dopaminérgico e alfa-adrenérgico potente. Risco de hipotensão severa, sedação profunda e sintomas extrapiramidais.",
        "tapering": "Descontinuar e utilizar Ondansetrona ou anti-histamínicos modernos conforme a indicação clínica.",
        "sos_note": "Uso pontual em anafilaxia ou profilaxia transfusional aceito. Evitar o uso como antiemético ou sedativo de rotina."
    },
    "dimenidrinato": {
        "drug": "Dimenidrinato",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar)",
        "renal_dependent": False,
        "recommendation": "Evitar o uso frequente para náuseas, vômitos ou vertigem em idosos.",
        "rationale": "Alta atividade anticolinérgica associada a delirium e lentificação psicomotora em ambiente hospitalar.",
        "tapering": "Substituir por antieméticos de menor impacto neurológico central (ex.: Ondansetrona).",
        "sos_note": "Prescrito como resgate SN/QN para êmese: Limitar a doses isoladas estritamente necessárias. Se vômitos persistentes, migrar para ondansetrona."
    },
    "difenidramina": {
        "drug": "Difenidramina",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar)",
        "renal_dependent": False,
        "recommendation": "Evitar o uso profilático ou como hipnótico.",
        "rationale": "Elevada carga anticolinérgica com comprovado risco de confusão mental aguda e desorientação espacial.",
        "tapering": "Interrupção imediata.",
        "sos_note": "Aceito apenas em esquemas pré-quimioterápicos ou manejo imediato de anafilaxia."
    },
    "escopolamina": {
        "drug": "Escopolamina",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar)",
        "renal_dependent": False,
        "recommendation": "Evitar o uso rotineiro para cólicas ou desconforto abdominal em idosos.",
        "rationale": "Alcaloide com potente bloqueio colinérgico muscarínico. Provoca confusão mental, agitação paradoxal, taquicardia e retenção urinária aguda.",
        "tapering": "Substituir por medidas não farmacológicas ou analgésicos simples quando apropriado.",
        "sos_note": "Uso como antiespasmódico pontual de resgate SN/QN: Reavaliar a necessidade caso a dor abdominal persista; vigiar globo vesical."
    },
    "biperideno": {
        "drug": "Biperideno",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar)",
        "renal_dependent": False,
        "recommendation": "Evitar na prevenção e manejo de sintomas extrapiramidais em idosos.",
        "rationale": "Anticolinérgico de ação central com alto potencial para desencadear delírio, alucinações e perda de memória.",
        "tapering": "Reduzir 50% da dose a cada 3 a 5 dias antes da suspensão definitiva para evitar efeito colinérgico rebote.",
        "sos_note": "Não recomendado em esquema de resgate rotineiro."
    },
    "oxibutinina": {
        "drug": "Oxibutinina",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar)",
        "renal_dependent": False,
        "recommendation": "Evitar para incontinência urinária em idosos.",
        "rationale": "Potente bloqueador muscarínico. Agrava constipação e piora o declínio cognitivo pré-existente.",
        "tapering": "Desprescrever gradualmente; considerar fisioterapia uroginecológica ou agonista beta-3 (Mirabegrona).",
        "sos_note": "Medicamento de ação contínua; não possui indicação posológica de resgate."
    },
    "diazepam": {
        "drug": "Diazepam",
        "axis": "AGS Beers 2023 - Tabela 2 e 3 (Evitar)",
        "renal_dependent": False,
        "recommendation": "Evitar o uso crônico ou agudo em enfermarias e UTIs geriátricas.",
        "rationale": "Meia-vida longa e acúmulo de metabólitos ativos. Risco extremo de sonolência diurna, ataxia, quedas com fraturas e delirium.",
        "tapering": "Desmame lento: diminuir 25% da dose a cada 1 a 2 semanas sob supervisão médica/farmacêutica para prevenir crise de abstinência.",
        "sos_note": "Se prescrito em crise convulsiva aguda, o uso é justificado. Para agitação ou insônia pontual, evitar devido ao risco de perda do equilíbrio postural."
    },
    "clonazepam": {
        "drug": "Clonazepam",
        "axis": "AGS Beers 2023 - Tabela 2 e 3 (Evitar)",
        "renal_dependent": False,
        "recommendation": "Evitar o uso crônico para insônia ou ansiedade.",
        "rationale": "Sensibilidade cerebral aumentada a agonistas GABAérgicos no idoso, causando lentificação psicomotora e quedas.",
        "tapering": "Reduzir progressivamente (ex.: 0,25mg a cada 7 a 14 dias) até o desmame total.",
        "sos_note": "Evitar doses de resgate noturno SN/QN para insônia hospitalar; aplicar higiene do sono não farmacológica."
    },
    "lorazepam": {
        "drug": "Lorazepam",
        "axis": "AGS Beers 2023 - Tabela 2 e 3 (Evitar)",
        "renal_dependent": False,
        "recommendation": "Evitar a manutenção crônica.",
        "rationale": "Apesar do metabolismo por conjugação direta, preserva alto risco de dependência física, tolerância, sedação e traumas físicos.",
        "tapering": "Desmame gradual ao longo de 2 a 4 semanas.",
        "sos_note": "Uso em crise aguda de ansiedade/agitação deve ser restrito e monitorado de perto."
    },
    "alprazolam": {
        "drug": "Alprazolam",
        "axis": "AGS Beers 2023 - Tabela 2 e 3 (Evitar)",
        "renal_dependent": False,
        "recommendation": "Evitar em idosos.",
        "rationale": "Rápida absorção e alta afinidade, associado a sintomas severos de rebote e dependência rápida.",
        "tapering": "Reduzir 0,25mg semanalmente sob vigilância de sintomas de ansiedade de rebote.",
        "sos_note": "Alto potencial de indução de efeito rebote nas horas seguintes."
    },
    "midazolam": {
        "drug": "Midazolam",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar exceto procedimentos)",
        "renal_dependent": False,
        "recommendation": "Evitar como sedativo/indutor de sono em enfermarias clínicas.",
        "rationale": "Sedação profunda, amnésia anterógrada e piora de quadros confusionais agudos em internamento.",
        "tapering": "Restringir estritamente a sedação processual ou descontinuar.",
        "sos_note": "Justificado para procedimentos ou contenção de emergência em UTI. Evitar como indutor de sono rotineiro."
    },
    "zolpidem": {
        "drug": "Zolpidem",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar)",
        "renal_dependent": False,
        "recommendation": "Evitar o uso para insônia em idosos.",
        "rationale": "Mecanismo semelhante aos benzodiazepínicos. Eleva taxa de quedas noturnas, fraturas e comportamentos complexos do sono.",
        "tapering": "Reduzir para 5mg/noite por 1 semana e suspender, priorizando higiene do sono não farmacológica.",
        "sos_note": "Evitar prescrever como 'se necessário (SN) para dormir' em ambiente hospitalar."
    },
    "zopiclona": {
        "drug": "Zopiclona",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar)",
        "renal_dependent": False,
        "recommendation": "Evitar em idosos.",
        "rationale": "Droga Z com sedação residual diurna, tontura e perda de reflexos posturais.",
        "tapering": "Desmame em 7 a 10 dias.",
        "sos_note": "Risco de sonolência residual matinal e acidentes ao levantar."
    },
    "amitriptilina": {
        "drug": "Amitriptilina",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar)",
        "renal_dependent": False,
        "recommendation": "Evitar para depressão, dor crônica ou insônia.",
        "rationale": "Altamente anticolinérgica, sedativa e indutora de hipotensão postural e arritmias cardíacas.",
        "tapering": "Reduzir 10mg a cada semana. Substituir por Duloxetina ou Gabapentinoide para dor neuropática.",
        "sos_note": "Fármaco de uso estritamente contínuo; posologias pontuais indicam erro de aprazamento."
    },
    "nortriptilina": {
        "drug": "Nortriptilina",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar na 1ª linha)",
        "renal_dependent": False,
        "recommendation": "Evitar na primeira linha terapêutica.",
        "rationale": "Menor bloqueio que a amitriptilina, mas mantém risco significativo de efeitos anticolinérgicos e cardiovasculares.",
        "tapering": "Desmame paulatino.",
        "sos_note": "Uso crônico; não indicado como resgate."
    },
    "clomipramina": {
        "drug": "Clomipramina",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar)",
        "renal_dependent": False,
        "recommendation": "Evitar em idosos.",
        "rationale": "Forte ação anticolinérgica e arritmogênica.",
        "tapering": "Desmame gradual ao longo de 2 a 4 semanas.",
        "sos_note": "Uso de manutenção exclusivo."
    },
    "haloperidol": {
        "drug": "Haloperidol",
        "axis": "AGS Beers 2023 - Tabela 2 e 3 (Evitar com ressalvas)",
        "renal_dependent": False,
        "recommendation": "Evitar o uso como controle comportamental não psicótico em idosos com demência.",
        "rationale": "Risco aumentado de eventos cerebrovasculares, parkinsonismo secundário medicamentoso e mortalidade global em demência.",
        "tapering": "Restringir apenas a delírio hiperativo grave com risco iminente de dano; descontinuar assim que estabilizado.",
        "sos_note": "Se prescrito SN/QN para Delirium Hiperativo grave com agitação psicomotora: Administrar a menor dose (0,5 a 1mg) e monitorar intervalo QTc e sinais extrapiramidais."
    },
    "clorpromazina": {
        "drug": "Clorpromazina",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar)",
        "renal_dependent": False,
        "recommendation": "Evitar em geriatria.",
        "rationale": "Sedação severa, bloqueio alfa-1 com síncope postural e propriedades anticolinérgicas intensas.",
        "tapering": "Desmame progressivo sob avaliação psiquiátrica.",
        "sos_note": "Alto risco de precipitar hipotensão ortostática fulminante ao ser administrado como dose de resgate."
    },
    "levomepromazina": {
        "drug": "Levomepromazina",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar)",
        "renal_dependent": False,
        "recommendation": "Evitar em idosos.",
        "rationale": "Hipotensão severa, sonolência profunda e risco exacerbado de quedas hospitalares.",
        "tapering": "Descontinuação progressiva.",
        "sos_note": "Sedação excessiva associada a perda de reflexos de proteção das vias aéreas."
    },
    "quetiapina": {
        "drug": "Quetiapina",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar sem indicação precisa)",
        "renal_dependent": False,
        "recommendation": "Evitar o uso rotineiro como hipnótico simples ou para agitação isolada.",
        "rationale": "Risco de hipotensão postural e eventos vasculares em idosos demenciados.",
        "tapering": "Reduzir a dose gradualmente até suspensão se utilizada unicamente para sono.",
        "sos_note": "Evitar administração como hipnótico pontual se houver demência associada."
    },
    "olanzapina": {
        "drug": "Olanzapina",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar)",
        "renal_dependent": False,
        "recommendation": "Evitar em idosos, exceto psicose ou transtorno bipolar refratário.",
        "rationale": "Ação anticolinérgica considerável, ganho ponderal, síndrome metabólica e eventos vasculares em demência.",
        "tapering": "Redução quinzenal da dose.",
        "sos_note": "Se utilizada para náuseas refratárias em oncologia ou delírio grave, reavaliar término pós-crise."
    },
    "risperidona": {
        "drug": "Risperidona",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar com ressalvas)",
        "renal_dependent": False,
        "recommendation": "Evitar para controle de agitação sem sintomas psicóticos graves.",
        "rationale": "Sintomas extrapiramidais dose-dependentes e risco aumentado de AVC e mortalidade em demência.",
        "tapering": "Usar a menor dose eficaz e limitar a duração ao menor tempo possível.",
        "sos_note": "Limitar a episódios agudos refratários de delírio e evitar manutenção contínua inadvertida."
    },
    "metoclopramida": {
        "drug": "Metoclopramida",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar)",
        "renal_dependent": False,
        "recommendation": "Evitar o uso crônico ou profilático desnecessário.",
        "rationale": "Antagonismo D2 central. Causa discinesia tardia frequentemente irreversível, acatisia e parkinsonismo medicamentoso.",
        "tapering": "Substituir por Ondansetrona ou Domperidona por curto período com monitoramento eletrocardiográfico.",
        "sos_note": "Uso SN/QN para náuseas agudas: Preferir ondansetrona; se administrada, não exceder 12 semanas cumulativas e vigiar sintomas extrapiramidais."
    },
    "omeprazol": {
        "drug": "Omeprazol",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar uso > 8 semanas)",
        "renal_dependent": False,
        "recommendation": "Evitar uso contínuo por mais de 8 semanas sem indicação clínica formal.",
        "rationale": "O bloqueio ácido crônico favorece infecção por Clostridioides difficile, desmineralização óssea com fraturas, hipomagnesemia e má absorção de B12.",
        "tapering": "Reduzir para dose em dias alternados por 2 semanas antes da suspensão, associando antiácidos se houver pirose de rebote.",
        "sos_note": "Em caso de queimação episódica, preferir antiácidos tópicos pontuais a iniciar IBP contínuo."
    },
    "pantoprazol": {
        "drug": "Pantoprazol",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar uso > 8 semanas)",
        "renal_dependent": False,
        "recommendation": "Reavaliar necessidade de manutenção prolongada além de 8 semanas.",
        "rationale": "Mesmos riscos associados à classe dos IBPs na população geriátrica.",
        "tapering": "Desmame gradual para evitar hipersecreção ácida rebote.",
        "sos_note": "Gastroproteção aguda em hemorragia digestiva alta é justificada; reavaliar após estabilização."
    },
    "oleo mineral": {
        "drug": "Óleo Mineral",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar VO)",
        "renal_dependent": False,
        "recommendation": "Evitar a administração por via oral.",
        "rationale": "Risco de aspiração traqueobrônquica inadvertida e pneumonia lipoídica grave em idosos acamados ou disfágicos.",
        "tapering": "Substituir por laxantes osmóticos seguros (ex.: Lactulose ou Macrogol / PEG).",
        "sos_note": "Mesmo em doses únicas para constipação aguda, a via oral deve ser evitada se houver risco de engasgo."
    },
    "ciclobenzaprina": {
        "drug": "Ciclobenzaprina",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar)",
        "renal_dependent": False,
        "recommendation": "Evitar o uso em idosos.",
        "rationale": "Homologia estrutural com tricíclicos; alta ação anticolinérgica, sedação excessiva, tontura e risco elevado de quedas.",
        "tapering": "Suspensão direta; aplicar medidas fisioterápicas e analgésicos simples.",
        "sos_note": "Dose única para lombalgia: Monitorar sedação e risco imediato de perda do equilíbrio ao deambular."
    },
    "carisoprodol": {
        "drug": "Carisoprodol",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar)",
        "renal_dependent": False,
        "recommendation": "Evitar em idosos.",
        "rationale": "Biotransformado em meprobamato, com elevado perfil de sedação, tolerância e dependência química.",
        "tapering": "Descontinuação progressiva em poucos dias.",
        "sos_note": "Evitar o uso mesmo em formulações combinadas de resgate para dor."
    },
    "orfenadrina": {
        "drug": "Orfenadrina",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar)",
        "renal_dependent": False,
        "recommendation": "Evitar em idosos.",
        "rationale": "Anticolinérgico potente presente em analgésicos combinados; desencadeia boca seca, retenção urinária e desorientação.",
        "tapering": "Substituir por dipirona ou paracetamol isolados.",
        "sos_note": "Muito comum em analgésicos de resgate (ex.: Dorflex). Recomenda-se prescrever dipirona pura no lugar."
    },
    "diclofenaco": {
        "drug": "Diclofenaco",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar uso crônico)",
        "renal_dependent": True,
        "recommendation": "Evitar uso crônico ou rotineiro.",
        "rationale": "Risco de hemorragia gastrointestinal alta, lesão renal aguda, retenção hidrossalina e descompensação de IC e HAS.",
        "tapering": "Suspender e transicionar para analgesia escalonada segura (Dipirona, Paracetamol ou opioide fraco).",
        "sos_note": "Prescrito como resgate SN/QN para dor: Se estritamente necessário, limitar ao menor tempo possível (< 3 dias) associado a IBP se houver risco gástrico."
    },
    "ibuprofeno": {
        "drug": "Ibuprofeno",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar uso crônico)",
        "renal_dependent": True,
        "recommendation": "Evitar o uso frequente em idosos.",
        "rationale": "Nefrotoxicidade aguda e risco ulcerogênico elevado no trato digestivo.",
        "tapering": "Suspensão direta.",
        "sos_note": "Uso pontual para dor/febre: Preferir paracetamol ou dipirona como antipirético de escolha."
    },
    "cetoprofeno": {
        "drug": "Cetoprofeno",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar)",
        "renal_dependent": True,
        "recommendation": "Evitar prescrição rotineira em pacientes internados idosos.",
        "rationale": "Inibição de prostaglandinas gástricas e renais protetoras com rápida deterioração da função renal.",
        "tapering": "Suspensão imediata.",
        "sos_note": "Comum em prescrições hospitalares de resgate SN/QN: Substituir por dipirona 1g IV."
    },
    "cetorolaco": {
        "drug": "Cetorolaco",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar)",
        "renal_dependent": True,
        "recommendation": "Evitar em idosos.",
        "rationale": "AINE de altíssima potência associado a taxas desproporcionais de sangramento gástrico e falência renal aguda.",
        "tapering": "Suspensão imediata.",
        "sos_note": "Contraindicado mesmo em doses isoladas de resgate pós-operatório em idosos frágeis."
    },
    "nimesulida": {
        "drug": "Nimesulida",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar)",
        "renal_dependent": True,
        "recommendation": "Evitar terminantemente.",
        "rationale": "Hepatotoxicidade grave e nefrotoxicidade em pacientes geriátricos.",
        "tapering": "Interrupção imediata.",
        "sos_note": "Evitar sob qualquer forma posológica."
    },
    "meloxicam": {
        "drug": "Meloxicam",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar)",
        "renal_dependent": True,
        "recommendation": "Evitar em idosos.",
        "rationale": "Mantém risco cardiovascular e renal em idosos hospitalizados.",
        "tapering": "Interromper e reavaliar analgesia.",
        "sos_note": "Ação seletiva COX-2 parcial não isenta nefrotoxicidade em idosos desidratados."
    },
    "piroxicam": {
        "drug": "Piroxicam",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar)",
        "renal_dependent": True,
        "recommendation": "Evitar absolutamente.",
        "rationale": "Meia-vida biológica superior a 50 horas com máxima taxa de sangramentos e reações adversas cutâneas graves.",
        "tapering": "Suspensão imediata.",
        "sos_note": "Contraindicado em regime crônico ou pontual."
    },
    "digoxina": {
        "drug": "Digoxina",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar como 1ª linha / Dose > 0.125mg)",
        "renal_dependent": True,
        "recommendation": "Evitar na primeira linha para FA ou IC; se imprescindível, nunca exceder 0,125 mg/dia.",
        "rationale": "Faixa terapêutica estreita e eliminação renal reduzida no envelhecimento; alto risco de intoxicação com arritmias fatais.",
        "tapering": "Monitorar digoxinemia e função renal; ajustar ou transicionar para betabloqueador seguro.",
        "sos_note": "Fármaco de uso contínuo monitorado."
    },
    "amiodarona": {
        "drug": "Amiodarona",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar como 1ª linha para FA)",
        "renal_dependent": False,
        "recommendation": "Evitar como terapia inicial de FA, exceto em IC grave com disfunção de VE se outros agentes forem contraindicados.",
        "rationale": "Toxicidades cumulativas (tireoidiana, pulmonar com fibrose, hepática e prolongamento do intervalo QT).",
        "tapering": "Desprescrição sob monitoramento conjunto com a cardiologia.",
        "sos_note": "Se utilizada para reversão aguda de arritmia em emergência/UTI, o uso pontual é respaldado."
    },
    "espironolactona": {
        "drug": "Espironolactona",
        "axis": "AGS Beers 2023 - Tabela 2 e 6 (Evitar se dose > 25mg ou CrCl < 30)",
        "renal_dependent": True,
        "recommendation": "Evitar doses > 25 mg/dia na IC ou evitar o uso se o Clearance de Creatinina for < 30 mL/min.",
        "rationale": "Risco crítico de hipercalemia potencialmente letal, especialmente associado a IECA/BRA.",
        "tapering": "Monitorar potássio sérico e creatinina; suspender se CrCl < 30 mL/min.",
        "sos_note": "Uso crônico; não se aplica como medicação de resgate."
    },
    "clonidina": {
        "drug": "Clonidina",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar para HAS de rotina)",
        "renal_dependent": False,
        "recommendation": "Evitar como anti-hipertensivo rotineiro em idosos.",
        "rationale": "Agonista alfa-2 central. Provoca sedação acentuada, boca seca, bradicardia sinusal, hipotensão ortostática e crise hipertensiva de rebote.",
        "tapering": "Nunca suspender abruptamente. Reduzir a dose gradualmente ao introduzir anti-hipertensivo de primeira linha.",
        "sos_note": "Se prescrita SN/QN para picos pressóricos: Evitar o uso indiscriminado pelo risco de hipotensão súbita seguida de efeito rebote."
    },
    "metildopa": {
        "drug": "Metildopa",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar)",
        "renal_dependent": False,
        "recommendation": "Evitar em geriatria.",
        "rationale": "Depressão do SNC, bradicardia e risco imunológico de anemia hemolítica e lesão hepática.",
        "tapering": "Desmame gradual associado à transição para bloqueador de canal de cálcio ou IECA/BRA.",
        "sos_note": "Fármaco de uso fixo."
    },
    "nifedipino": {
        "drug": "Nifedipino (Liberação Rápida)",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar liberação imediata)",
        "renal_dependent": False,
        "recommendation": "Evitar cápsulas de liberação imediata ou via sublingual.",
        "rationale": "Queda abrupta da pressão arterial desencadeando taquicardia reflexa com isquemia miocárdica ou cerebral aguda.",
        "tapering": "Substituir por bloqueador de canal de cálcio de liberação prolongada ou anlodipino.",
        "sos_note": "Proibido em urgências hipertensivas por via sublingual/cápsula mordida."
    },
    "doxazosina": {
        "drug": "Doxazosina",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar como anti-hipertensivo)",
        "renal_dependent": False,
        "recommendation": "Evitar como monoterapia ou agente primário para hipertensão.",
        "rationale": "Bloqueador alfa-1 periférico com alta incidência de hipotensão ortostática severa e síncope.",
        "tapering": "Se utilizada para HPB, manter monitoramento pressórico sentado/em pé rigoroso.",
        "sos_note": "Uso noturno fixo recomendado para minimizar risco de quedas ortostáticas."
    },
    "glibenclamida": {
        "drug": "Glibenclamida",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar)",
        "renal_dependent": True,
        "recommendation": "Evitar terminantemente em pacientes geriátricos.",
        "rationale": "Sulfonilureia de ação prolongada e metabólitos ativos que se acumulam no idoso; alto risco de hipoglicemia severa e prolongada.",
        "tapering": "Substituir imediatamente por Gliclazida MR, inibidor de DPP-4 (ex.: Linagliptina) ou esquema de insulina basal.",
        "sos_note": "Medicamento de uso fixo; contraindicado."
    },
    "glimepirida": {
        "drug": "Glimepirida",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar)",
        "renal_dependent": True,
        "recommendation": "Evitar em idosos.",
        "rationale": "Risco aumentado de hipoglicemias prolongadas.",
        "tapering": "Transicionar para opções com menor risco de hipoglicemia.",
        "sos_note": "Uso de manutenção diário."
    },
    "tramadol": {
        "drug": "Tramadol",
        "axis": "AGS Beers 2023 - Tabela 2 e 5 (Evitar / Risco de SIADH e Síndrome Serotoninérgica)",
        "renal_dependent": True,
        "recommendation": "Evitar o uso rotineiro ou associado a psicotrópicos.",
        "rationale": "Pode precipitar hiponatremia grave por SIADH, reduzir limiar epiléptico e causar Síndrome Serotoninérgica quando combinado com antidepressivos.",
        "tapering": "Reduzir 25-50% da dose a cada 3 dias antes da descontinuação.",
        "sos_note": "Prescrito SN/QN para dor moderada/grave: Limitar dose diária; prescrever laxativo preventivo e vigiar nível de consciência."
    },
    "codeina": {
        "drug": "Codeína",
        "axis": "AGS Beers 2023 - Tabela 2 (Cautela / Constipação severa)",
        "renal_dependent": True,
        "recommendation": "Evitar uso prolongado; se necessário, prescrever laxativo profilático obrigatório.",
        "rationale": "Metabolismo variável via CYP2D6 e altíssima prevalência de constipação refratária e retenção urinária.",
        "tapering": "Desmame rápido e substituição por analgésicos não opioides.",
        "sos_note": "Uso pontual: Manter hidratação e vigiar hábito intestinal."
    },
    "morfina": {
        "drug": "Morfina",
        "axis": "AGS Beers 2023 - Tabela 6 (Ajuste por Função Renal)",
        "renal_dependent": True,
        "recommendation": "Evitar se Clearance de Creatinina < 30 mL/min.",
        "rationale": "Retenção de metabólitos neurotóxicos (M3G e M6G) levando a mioclonias, delírio e depressão respiratória grave.",
        "tapering": "Em caso de falência renal, substituir por Fentanila sob titulação rigorosa.",
        "sos_note": "Resgate SN/QN para dor oncológica ou pós-operatória: Titular com cautela se houver insuficiência renal documentada."
    },
    "meperidina": {
        "drug": "Meperidina",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar absolutamente)",
        "renal_dependent": True,
        "recommendation": "Evitar em qualquer cenário na geriatria.",
        "rationale": "O metabólito normeperidina possui meia-vida longa, excreção renal e neurotoxicidade extrema com convulsões e alucinações.",
        "tapering": "Substituição imediata por outro analgésico.",
        "sos_note": "Contraindicado mesmo em dose única de resgate para tremores pós-anestésicos."
    }
}

SYNONYM_MAP = {
    "dexclorfeniramina": "dexclorfeniramina",
    "maleato de dexclorfeniramina": "dexclorfeniramina",
    "polaramine": "dexclorfeniramina",
    "polararen": "dexclorfeniramina",
    "polaren": "dexclorfeniramina",
    "clorfeniramina": "dexclorfeniramina",
    "coristina": "dexclorfeniramina",
    "hidroxizina": "hidroxizina",
    "hixizine": "hidroxizina",
    "prurizin": "hidroxizina",
    "prometazina": "prometazina",
    "fenergan": "prometazina",
    "dimenidrinato": "dimenidrinato",
    "dramin": "dimenidrinato",
    "dramin b6": "dimenidrinato",
    "difenidramina": "difenidramina",
    "benadryl": "difenidramina",
    "escopolamina": "escopolamina",
    "buscopan": "escopolamina",
    "hioscina": "escopolamina",
    "butilbrometo de escopolamina": "escopolamina",
    "biperideno": "biperideno",
    "akineton": "biperideno",
    "oxibutinina": "oxibutinina",
    "retemic": "oxibutinina",
    "diazepam": "diazepam",
    "valium": "diazepam",
    "clonazepam": "clonazepam",
    "rivotril": "clonazepam",
    "lorazepam": "lorazepam",
    "lorax": "lorazepam",
    "alprazolam": "alprazolam",
    "frontin": "alprazolam",
    "midazolam": "midazolam",
    "dormonid": "midazolam",
    "zolpidem": "zolpidem",
    "stilnox": "zolpidem",
    "patz": "zolpidem",
    "zopiclona": "zopiclona",
    "imovane": "zopiclona",
    "amitriptilina": "amitriptilina",
    "tryptanol": "amitriptilina",
    "amytril": "amitriptilina",
    "nortriptilina": "nortriptilina",
    "pamelor": "nortriptilina",
    "clomipramina": "clomipramina",
    "anafranil": "clomipramina",
    "haloperidol": "haloperidol",
    "haldol": "haloperidol",
    "clorpromazina": "clorpromazina",
    "amplictil": "clorpromazina",
    "levomepromazina": "levomepromazina",
    "neozine": "levomepromazina",
    "quetiapina": "quetiapina",
    "seroquel": "quetiapina",
    "olanzapina": "olanzapina",
    "zyprexa": "olanzapina",
    "risperidona": "risperidona",
    "risperdal": "risperidona",
    "metoclopramida": "metoclopramida",
    "plasil": "metoclopramida",
    "omeprazol": "omeprazol",
    "losec": "omeprazol",
    "pantoprazol": "pantoprazol",
    "pantocal": "pantoprazol",
    "oleo mineral": "oleo mineral",
    "nujol": "oleo mineral",
    "ciclobenzaprina": "ciclobenzaprina",
    "miosan": "ciclobenzaprina",
    "musculare": "ciclobenzaprina",
    "carisoprodol": "carisoprodol",
    "tandrilax": "carisoprodol",
    "torsilax": "carisoprodol",
    "orfenadrina": "orfenadrina",
    "dorflex": "orfenadrina",
    "diclofenaco": "diclofenaco",
    "voltaren": "diclofenaco",
    "cataflam": "diclofenaco",
    "ibuprofeno": "ibuprofeno",
    "advil": "ibuprofeno",
    "cetoprofeno": "cetoprofeno",
    "profenid": "cetoprofeno",
    "cetorolaco": "cetorolaco",
    "toradol": "cetorolaco",
    "nimesulida": "nimesulida",
    "nisulid": "nimesulida",
    "meloxicam": "meloxicam",
    "piroxicam": "piroxicam",
    "digoxina": "digoxina",
    "digox": "digoxina",
    "lanoxin": "digoxina",
    "amiodarona": "amiodarona",
    "ancoron": "amiodarona",
    "espironolactona": "espironolactona",
    "aldactone": "espironolactona",
    "clonidina": "clonidina",
    "atensina": "clonidina",
    "metildopa": "metildopa",
    "aldomet": "metildopa",
    "nifedipino": "nifedipino",
    "adalat": "nifedipino",
    "doxazosina": "doxazosina",
    "carduran": "doxazosina",
    "glibenclamida": "glibenclamida",
    "daonil": "glibenclamida",
    "glimepirida": "glimepirida",
    "amaryl": "glimepirida",
    "tramadol": "tramadol",
    "tramal": "tramadol",
    "codeina": "codeina",
    "tylex": "codeina",
    "morfina": "morfina",
    "dimorf": "morfina",
    "meperidina": "meperidina",
    "petidina": "meperidina",
    "dolantina": "meperidina",

    # Fármacos adicionais mapeados para Interações da Tabela 4
    "losartana": "losartana",
    "enalapril": "enalapril",
    "captopril": "captopril",
    "ramipril": "ramipril",
    "valsartana": "valsartana",
    "candesartana": "candesartana",
    "varfarina": "varfarina",
    "marevan": "varfarina",
    "coumadin": "varfarina",
    "rivaroxabana": "rivaroxabana",
    "xarelto": "rivaroxabana",
    "apixabana": "apixabana",
    "eliquis": "apixabana",
    "dabigatrana": "dabigatrana",
    "pradaxa": "dabigatrana",
    "enoxaparina": "enoxaparina",
    "clexane": "enoxaparina",
    "heparina": "heparina"
}

def identify_drug_canonical(input_text: str) -> Optional[str]:
    if not input_text:
        return None

    cleaned = normalize_text(input_text)
    if cleaned in SYNONYM_MAP:
        return SYNONYM_MAP[cleaned]

    sorted_synonyms = sorted(SYNONYM_MAP.keys(), key=lambda x: len(x), reverse=True)
    for syn in sorted_synonyms:
        pattern = r"\b" + re.escape(syn) + r"\b"
        if re.search(pattern, cleaned):
            return SYNONYM_MAP[syn]

    for syn, canonical in SYNONYM_MAP.items():
        if len(syn) >= 5 and syn in cleaned:
            return canonical

    return None

# ==============================================================================
# DETECTOR DA TABELA 4 DE BEERS (INTERAÇÕES MEDICAMENTOSAS DE ALTO RISCO)
# ==============================================================================
def check_beers_table_4_interactions(active_canonicals: List[str]) -> List[Dict[str, Any]]:
    table_4_alerts = []
    meds = set(active_canonicals)

    opioids = {"tramadol", "codeina", "morfina", "meperidina"}
    bzds_and_z = {"diazepam", "clonazepam", "lorazepam", "alprazolam", "midazolam", "zolpidem", "zopiclona"}
    ras_inhibitors = {"losartana", "enalapril", "captopril", "ramipril", "valsartana", "candesartana"}
    nsaids = {"diclofenaco", "ibuprofeno", "cetoprofeno", "cetorolaco", "nimesulida", "meloxicam", "piroxicam"}
    anticoagulants = {"varfarina", "rivaroxabana", "apixabana", "dabigatrana", "enoxaparina", "heparina"}
    cns_drugs = opioids | bzds_and_z | {"haloperidol", "quetiapina", "olanzapina", "risperidona", "amitriptilina", "nortriptilina", "clomipramina"}

    # Interação 1: Opioide + Benzodiazepínico / Droga Z
    found_op = meds.intersection(opioids)
    found_bzd = meds.intersection(bzds_and_z)
    if found_op and found_bzd:
        table_4_alerts.append({
            "drug": f"{', '.join([o.capitalize() for o in found_op])} + {', '.join([b.capitalize() for b in found_bzd])}",
            "drug_name": "Associação Opioide + Benzodiazepínico/Z",
            "axis": "AGS Beers 2023 - Tabela 4 (Interação Crítica)",
            "recommendation": "Evitar uso concomitante. Alto risco de sedação sinérgica grave, depressão respiratória fatal e coma.",
            "rationale": "A FDA e a AGS Beers contraindicam a prescrição combinada rotineira em idosos devido à potencialização letal no SNC.",
            "tapering": "Se a analgesia for necessária, priorizar analgésicos não opioides e iniciar desmame gradual do sedativo.",
            "is_sos": False,
            "acb_score": 0
        })

    # Interação 2: IECA/BRA + Espironolactona
    found_ras = meds.intersection(ras_inhibitors)
    if found_ras and "espironolactona" in meds:
        table_4_alerts.append({
            "drug": f"{', '.join([r.capitalize() for r in found_ras])} + Espironolactona",
            "drug_name": "Associação IECA/BRA + Espironolactona",
            "axis": "AGS Beers 2023 - Tabela 4 (Interação Crítica)",
            "recommendation": "Monitorar rigorosamente potássio sérico e função renal. Evitar doses de espironolactona > 25mg/dia.",
            "rationale": "Bloqueio duplo do sistema renina-angiotensina-aldosterona gerando hipercalemia grave e arritmias cardíacas em idosos.",
            "tapering": "Avaliar dosagem de eletrólitos a cada 48h no internamento; suspender se K+ > 5,0 mEq/L.",
            "is_sos": False,
            "acb_score": 0
        })

    # Interação 3: Anticoagulante + AINE
    found_anticoag = meds.intersection(anticoagulants)
    found_nsaid = meds.intersection(nsaids)
    if found_anticoag and found_nsaid:
        table_4_alerts.append({
            "drug": f"{', '.join([a.capitalize() for a in found_anticoag])} + {', '.join([n.capitalize() for n in found_nsaid])}",
            "drug_name": "Associação Anticoagulante + AINE",
            "axis": "AGS Beers 2023 - Tabela 4 (Interação Crítica)",
            "recommendation": "Evitar categoricamente o uso concomitante. Alto risco de hemorragia gastrointestinal fulminante.",
            "rationale": "Sinergismo entre inibição de fatores de coagulação e erosão ulcerativa da mucosa gástrica provocada pelo AINE.",
            "tapering": "Suspender imediatamente o AINE e prescrever Dipirona ou Paracetamol como analgésico seguro.",
            "is_sos": False,
            "acb_score": 0
        })

    # Interação 4: 3 ou mais agentes ativos no SNC (Polifarmácia Psicotrópica)
    found_cns = meds.intersection(cns_drugs)
    if len(found_cns) >= 3:
        table_4_alerts.append({
            "drug": f"Polifarmácia SNC ({', '.join([c.capitalize() for c in found_cns])})",
            "drug_name": "Associação de ≥ 3 Medicamentos do SNC",
            "axis": "AGS Beers 2023 - Tabela 4 (Risco Extremo de Quedas)",
            "recommendation": "Reduzir o número total de fármacos que atuam no SNC. Minimizar doses e evitar duplicidades terapêuticas.",
            "rationale": "Uso de 3 ou mais agentes psicoativos eleva substancialmente o risco de fraturas por quedas, ataxia e declínio cognitivo agudo.",
            "tapering": "Eleger o medicamento com menor indicação clínica para iniciar desmame (*tapering*) escalonado.",
            "is_sos": False,
            "acb_score": 0
        })

    return table_4_alerts

# ==============================================================================
# MOTOR CONSOLIDADO DE AVALIAÇÃO DE BEERS 2023
# ==============================================================================
def evaluate_patient_beers(
    medications: List[Dict[str, Any]],
    age: int,
    fall_risk: bool = False,
    conditions: Optional[List[str]] = None,
    crcl: Optional[float] = None
) -> Tuple[List[Dict[str, Any]], int, str]:
    alerts = []
    conditions = conditions or []
    total_acb_score = 0

    if age < 65:
        return alerts, 0, "Idade inferior a 65 anos. Avaliação de Beers não aplicável por critério etário."

    processed = set()
    canonicals_list = []

    for med in medications:
        med_name = med.get("name", "")
        is_sos = bool(med.get("is_sos", False)) or any(
            t in med.get("frequency", "").lower() for t in ["sn", "qn", "sos", "necessario"]
        )

        canonical = identify_drug_canonical(med_name)
        if not canonical:
            continue

        canonicals_list.append(canonical)

        if canonical in processed:
            continue
        processed.add(canonical)

        acb_pts = ACB_SCORE_MAP.get(canonical, 0)
        total_acb_score += acb_pts

        if canonical in BEERS_RULES:
            r = BEERS_RULES[canonical]
            rec = r.get("recommendation", "Reavaliar uso em idosos.")
            rat = r.get("rationale", "Medicamento potencialmente inapropriado.")
            tap = r.get("tapering", "")

            if is_sos:
                rec = f"PRESCRIÇÃO SN/QN (RESGATE): {r.get('sos_note', rec)}"

            if fall_risk and canonical in [
                "dexclorfeniramina", "hidroxizina", "difenidramina", "prometazina",
                "diazepam", "clonazepam", "lorazepam", "alprazolam", "midazolam",
                "zolpidem", "zopiclona", "amitriptilina", "quetiapina", "risperidona",
                "olanzapina", "haloperidol", "clonidina", "tramadol"
            ]:
                rec += " [ALERTA DE QUEDAS]: Paciente com risco elevado documentado; este fármaco aumenta expressivamente quedas e fraturas."

            if r.get("renal_dependent", False):
                if crcl is not None:
                    if canonical in ["espironolactona", "morfina"] and crcl < 30:
                        rec += f" [CONTRAINDICAÇÃO RENAL CrCl={crcl} mL/min]: Eliminação prejudicada com acúmulo de toxicidade letal. Suspender ou substituir."
                    elif canonical == "glibenclamida" and crcl < 50:
                        rec += f" [ALERTA RENAL CrCl={crcl} mL/min]: Alto risco de hipoglicemia prolongada refratária."
                else:
                    rec += " [ATENÇÃO DE VIGILÂNCIA RENAL]: A depuração deste fármaco depende da filtração glomerular. Recomenda-se inserir creatinina sérica para assegurar CrCl > 30 mL/min."

            alerts.append({
                "drug": r.get("drug", canonical.capitalize()),
                "drug_name": r.get("drug", canonical.capitalize()),
                "axis": r.get("axis", "AGS Beers 2023"),
                "recommendation": rec,
                "rationale": rat,
                "tapering": tap,
                "is_sos": is_sos,
                "acb_score": acb_pts
            })

    # Adiciona as Interações de Alto Risco da Tabela 4
    table_4_alerts = check_beers_table_4_interactions(canonicals_list)
    alerts.extend(table_4_alerts)

    if total_acb_score >= 3:
        acb_interpretation = f"Carga Crítica ({total_acb_score} pontos) — Elevado risco de precipitação de delirium hospitalar, declínio cognitivo e retenção urinária aguda nas próximas 24-48h."
    elif total_acb_score in [1, 2]:
        acb_interpretation = f"Carga Moderada ({total_acb_score} ponto{'s' if total_acb_score > 1 else ''}) — Monitorar queixas de boca seca, constipação e sonolência."
    else:
        acb_interpretation = "Carga Anticolinérgica Neutra (0 pontos) — Sem medicamentos anticolinérgicos identificados."

    return alerts, total_acb_score, acb_interpretation
