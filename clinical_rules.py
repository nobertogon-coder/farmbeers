# -*- coding: utf-8 -*-
"""
FarmBeers - Motor Clínico AGS Beers 2023
Mapeamento Canônico com Reconhecimento Inteligente por Expressões Regulares
"""
import re
import unicodedata
from typing import List, Dict, Any, Optional

def normalize_text(text: str) -> str:
    if not text:
        return ""
    text = unicodedata.normalize("NFD", text.lower())
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return " ".join(text.split())

BEERS_RULES = {
    # --------------------------------------------------------------------------
    # ANTI-HISTAMÍNICOS DE 1ª GERAÇÃO (TABELA 2)
    # --------------------------------------------------------------------------
    "dexclorfeniramina": {
        "drug": "Dexclorfeniramina",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar)",
        "recommendation": "Evitar o uso rotineiro em idosos. Suspender e substituir por anti-histamínico de 2ª geração ou corticoide nasal.",
        "rationale": "Potente ação anticolinérgica central e periférica. Causa sedação pronunciada, boca seca, constipação intestinal severa, retenção urinária e elevação crítica do risco de declínio cognitivo agudo e quedas.",
        "tapering": "Pode ser descontinuada diretamente na ausência de anafilaxia aguda. Substituir por Loratadina 10mg/dia ou Cetirizina 5-10mg/dia se houver rinite/alergia ativa."
    },
    "hidroxizina": {
        "drug": "Hidroxizina",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar)",
        "recommendation": "Evitar o uso em geriatria.",
        "rationale": "Efeito anticolinérgico intenso e sedação residual prolongada com prejuízo cognitivo e psicomotor.",
        "tapering": "Suspensão direta; avaliar uso de emolientes tópicos ou anti-histamínicos não sedativos para prurido."
    },
    "prometazina": {
        "drug": "Prometazina",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar)",
        "recommendation": "Evitar o uso rotineiro como antialérgico, antiemético ou sedativo.",
        "rationale": "Fenotiazina com bloqueio colinérgico, dopaminérgico e alfa-adrenérgico potente. Risco de hipotensão severa, sedação profunda e sintomas extrapiramidais.",
        "tapering": "Descontinuar e utilizar Ondansetrona ou anti-histamínicos modernos conforme a indicação clínica."
    },
    "dimenidrinato": {
        "drug": "Dimenidrinato",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar)",
        "recommendation": "Evitar o uso frequente para náuseas, vômitos ou vertigem em idosos.",
        "rationale": "Alta atividade anticolinérgica associada a delirium e lentificação psicomotora em ambiente hospitalar.",
        "tapering": "Substituir por antieméticos de menor impacto neurológico central (ex.: Ondansetrona)."
    },
    "difenidramina": {
        "drug": "Difenidramina",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar)",
        "recommendation": "Evitar o uso profilático ou como hipnótico.",
        "rationale": "Elevada carga anticolinérgica com comprovado risco de confusão mental aguda e desorientação espacial.",
        "tapering": "Interrupção imediata."
    },

    # --------------------------------------------------------------------------
    # ANTICOLINÉRGICOS E ANTIESPASMÓDICOS DIVERSOS
    # --------------------------------------------------------------------------
    "escopolamina": {
        "drug": "Escopolamina",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar)",
        "recommendation": "Evitar o uso rotineiro para cólicas ou desconforto abdominal em idosos.",
        "rationale": "Alcaloide com potente bloqueio colinérgico muscarínico. Provoca confusão mental, agitação paradoxal, taquicardia e retenção urinária aguda.",
        "tapering": "Substituir por medidas não farmacológicas ou analgésicos simples quando apropriado."
    },
    "biperideno": {
        "drug": "Biperideno",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar)",
        "recommendation": "Evitar na prevenção e manejo de sintomas extrapiramidais em idosos.",
        "rationale": "Anticolinérgico de ação central com alto potencial para desencadear delírio, alucinações e perda de memória.",
        "tapering": "Reduzir 50% da dose a cada 3 a 5 dias antes da suspensão definitiva para evitar efeito colinérgico rebote."
    },
    "oxibutinina": {
        "drug": "Oxibutinina",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar)",
        "recommendation": "Evitar para incontinência urinária em idosos.",
        "rationale": "Potente bloqueador muscarínico. Agrava constipação e piora o declínio cognitivo pré-existente.",
        "tapering": "Desprescrever gradualmente; considerar fisioterapia uroginecológica ou agonista beta-3 (Mirabegrona)."
    },

    # --------------------------------------------------------------------------
    # BENZODIAZEPÍNICOS E HIPNÓTICOS (TABELAS 2 E 3)
    # --------------------------------------------------------------------------
    "diazepam": {
        "drug": "Diazepam",
        "axis": "AGS Beers 2023 - Tabela 2 e 3 (Evitar)",
        "recommendation": "Evitar o uso crônico ou agudo em enfermarias e UTIs geriátricas.",
        "rationale": "Meia-vida muito longa e acúmulo de metabólitos ativos (desmetildiazepam). Risco extremo de sonolência diurna, ataxia, quedas com fraturas e delirium.",
        "tapering": "Desmame lento: diminuir 25% da dose a cada 1 a 2 semanas sob supervisão médica/farmacêutica para prevenir crise de abstinência e convulsões."
    },
    "clonazepam": {
        "drug": "Clonazepam",
        "axis": "AGS Beers 2023 - Tabela 2 e 3 (Evitar)",
        "recommendation": "Evitar o uso crônico para insônia ou ansiedade.",
        "rationale": "Sensibilidade cerebral aumentada a agonistas GABAérgicos no idoso, causando lentificação psicomotora e quedas.",
        "tapering": "Reduzir progressivamente (ex.: 0,25mg a cada 7 a 14 dias) até o desmame total."
    },
    "lorazepam": {
        "drug": "Lorazepam",
        "axis": "AGS Beers 2023 - Tabela 2 e 3 (Evitar)",
        "recommendation": "Evitar a manutenção crônica.",
        "rationale": "Apesar do metabolismo por conjugação direta, preserva alto risco de dependência física, tolerância, sedação e traumas físicos.",
        "tapering": "Desmame gradual ao longo de 2 a 4 semanas."
    },
    "alprazolam": {
        "drug": "Alprazolam",
        "axis": "AGS Beers 2023 - Tabela 2 e 3 (Evitar)",
        "recommendation": "Evitar em idosos.",
        "rationale": "Rápida absorção e alta afinidade, associado a sintomas severos de rebote e dependência rápida.",
        "tapering": "Reduzir 0,25mg semanalmente sob vigilância de sintomas de ansiedade de rebote."
    },
    "midazolam": {
        "drug": "Midazolam",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar exceto procedimentos)",
        "recommendation": "Evitar como sedativo/indutor de sono em enfermarias clínicas.",
        "rationale": "Sedação profunda, amnésia anterógrada e piora imediata de quadros confusionais agudos em internamento.",
        "tapering": "Restringir estritamente a sedação processual ou descontinuar."
    },
    "zolpidem": {
        "drug": "Zolpidem",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar)",
        "recommendation": "Evitar o uso para insônia em idosos.",
        "rationale": "Mecanismo semelhante aos benzodiazepínicos. Eleva taxa de quedas noturnas, fraturas e comportamentos complexos do sono.",
        "tapering": "Reduzir para 5mg/noite por 1 semana e suspender, priorizando higiene do sono não farmacológica."
    },
    "zopiclona": {
        "drug": "Zopiclona",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar)",
        "recommendation": "Evitar em idosos.",
        "rationale": "Droga Z com sedação residual diurna, tontura e perda de reflexos posturais.",
        "tapering": "Desmame em 7 a 10 dias."
    },

    # --------------------------------------------------------------------------
    # NEUROLÉPTICOS E ANTIDEPRESSIVOS TRICÍCLICOS
    # --------------------------------------------------------------------------
    "amitriptilina": {
        "drug": "Amitriptilina",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar)",
        "recommendation": "Evitar para depressão, dor crônica ou insônia.",
        "rationale": "Altamente anticolinérgica, sedativa e indutora de hipotensão postural e arritmias cardíacas por bloqueio de condução.",
        "tapering": "Reduzir 10mg a cada semana. Substituir por Duloxetina ou Gabapentinoide para dor neuropática."
    },
    "nortriptilina": {
        "drug": "Nortriptilina",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar na 1ª linha)",
        "recommendation": "Evitar na primeira linha terapêutica.",
        "rationale": "Menor bloqueio que a amitriptilina, mas mantém risco significativo de efeitos anticolinérgicos e cardiovasculares.",
        "tapering": "Desmame paulatino."
    },
    "clomipramina": {
        "drug": "Clomipramina",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar)",
        "recommendation": "Evitar em idosos.",
        "rationale": "Forte ação anticolinérgica e arritmogênica.",
        "tapering": "Desmame gradual ao longo de 2 a 4 semanas."
    },
    "haloperidol": {
        "drug": "Haloperidol",
        "axis": "AGS Beers 2023 - Tabela 2 e 3 (Evitar com ressalvas)",
        "recommendation": "Evitar o uso como controle comportamental não psicótico em idosos com demência.",
        "rationale": "Risco aumentado de eventos cerebrovasculares, parkinsonismo secundário medicamentoso e mortalidade global em demência.",
        "tapering": "Restringir apenas a delírio hiperativo grave com risco iminente de dano; descontinuar assim que estabilizado."
    },
    "clorpromazina": {
        "drug": "Clorpromazina",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar)",
        "recommendation": "Evitar em geriatria.",
        "rationale": "Sedação severa, bloqueio alfa-1 com síncope postural e propriedades anticolinérgicas intensas.",
        "tapering": "Desmame progressivo sob avaliação psiquiátrica."
    },
    "levomepromazina": {
        "drug": "Levomepromazina",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar)",
        "recommendation": "Evitar em idosos.",
        "rationale": "Hipotensão severa, sonolência profunda e risco exacerbado de quedas hospitalares.",
        "tapering": "Descontinuação progressiva."
    },
    "quetiapina": {
        "drug": "Quetiapina",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar sem indicação precisa)",
        "recommendation": "Evitar o uso rotineiro como hipnótico simples ou para agitação isolada.",
        "rationale": "Risco de hipotensão postural e eventos vasculares em idosos demenciados.",
        "tapering": "Reduzir a dose gradualmente até suspensão se utilizada unicamente para sono."
    },
    "olanzapina": {
        "drug": "Olanzapina",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar)",
        "recommendation": "Evitar em idosos, exceto psicose ou transtorno bipolar refratário.",
        "rationale": "Ação anticolinérgica considerável, ganho ponderal, síndrome metabólica e eventos vasculares em demência.",
        "tapering": "Redução quinzenal da dose."
    },
    "risperidona": {
        "drug": "Risperidona",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar com ressalvas)",
        "recommendation": "Evitar para controle de agitação sem sintomas psicóticos graves.",
        "rationale": "Sintomas extrapiramidais dose-dependentes e risco aumentado de AVC e mortalidade em demência.",
        "tapering": "Usar a menor dose eficaz e limitar a duração ao menor tempo possível."
    },

    # --------------------------------------------------------------------------
    # GASTROINTESTINAIS E MOTILIDADE
    # --------------------------------------------------------------------------
    "metoclopramida": {
        "drug": "Metoclopramida",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar)",
        "recommendation": "Evitar o uso crônico ou profilático desnecessário.",
        "rationale": "Antagonismo D2 central. Causa discinesia tardia frequentemente irreversível, acatisia e parkinsonismo medicamentoso.",
        "tapering": "Substituir por Ondansetrona ou Domperidona por curto período com monitoramento eletrocardiográfico."
    },
    "omeprazol": {
        "drug": "Omeprazol",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar uso > 8 semanas)",
        "recommendation": "Evitar uso contínuo por mais de 8 semanas sem indicação clínica formal.",
        "rationale": "O bloqueio ácido crônico favorece infecção por Clostridioides difficile, desmineralização óssea com fraturas, hipomagnesemia e má absorção de B12.",
        "tapering": "Reduzir para dose em dias alternados por 2 semanas antes da suspensão, associando antiácidos se houver pirose de rebote."
    },
    "pantoprazol": {
        "drug": "Pantoprazol",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar uso > 8 semanas)",
        "recommendation": "Reavaliar necessidade de manutenção prolongada além de 8 semanas.",
        "rationale": "Mesmos riscos associados à classe dos IBPs na população geriátrica.",
        "tapering": "Desmame gradual para evitar hipersecreção ácida rebote."
    },
    "oleo mineral": {
        "drug": "Óleo Mineral",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar VO)",
        "recommendation": "Evitar a administração por via oral.",
        "rationale": "Risco de aspiração traqueobrônquica inadvertida e desenvolvimento de pneumonia lipoídica grave em idosos acamados ou disfágicos.",
        "tapering": "Substituir por laxantes osmóticos seguros (ex.: Lactulose ou Macrogol / PEG)."
    },

    # --------------------------------------------------------------------------
    # RELAXANTES MUSCULARES
    # --------------------------------------------------------------------------
    "ciclobenzaprina": {
        "drug": "Ciclobenzaprina",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar)",
        "recommendation": "Evitar o uso em idosos.",
        "rationale": "Homologia estrutural com tricíclicos; alta ação anticolinérgica, sedação excessiva, tontura e risco elevado de quedas.",
        "tapering": "Suspensão direta; aplicar medidas fisioterápicas e analgésicos simples."
    },
    "carisoprodol": {
        "drug": "Carisoprodol",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar)",
        "recommendation": "Evitar em idosos.",
        "rationale": "Biotransformado em meprobamato, com elevado perfil de sedação, tolerância e dependência química.",
        "tapering": "Descontinuação progressiva em poucos dias."
    },
    "orfenadrina": {
        "drug": "Orfenadrina",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar)",
        "recommendation": "Evitar em idosos.",
        "rationale": "Anticolinérgico potente presente em analgésicos combinados; desencadeia boca seca, retenção urinária e desorientação.",
        "tapering": "Substituir por dipirona ou paracetamol isolados."
    },

    # --------------------------------------------------------------------------
    # AINES
    # --------------------------------------------------------------------------
    "diclofenaco": {
        "drug": "Diclofenaco",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar uso crônico)",
        "recommendation": "Evitar uso crônico ou rotineiro.",
        "rationale": "Risco de hemorragia gastrointestinal alta, lesão renal aguda, retenção hidrossalina e descompensação de insuficiência cardíaca e hipertensão.",
        "tapering": "Suspender e transicionar para analgesia escalonada segura (Dipirona, Paracetamol ou opioide fraco por curto período)."
    },
    "ibuprofeno": {
        "drug": "Ibuprofeno",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar uso crônico)",
        "recommendation": "Evitar o uso frequente em idosos.",
        "rationale": "Nefrotoxicidade aguda e risco ulcerogênico elevado no trato digestivo.",
        "tapering": "Suspensão direta."
    },
    "cetoprofeno": {
        "drug": "Cetoprofeno",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar)",
        "recommendation": "Evitar prescrição rotineira em pacientes internados idosos.",
        "rationale": "Inibição de prostaglandinas gástricas e renais protetoras com rápida deterioração da função renal.",
        "tapering": "Suspensão imediata."
    },
    "cetorolaco": {
        "drug": "Cetorolaco",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar)",
        "recommendation": "Evitar em idosos.",
        "rationale": "AINE de altíssima potência associado a taxas desproporcionais de sangramento gástrico e falência renal aguda.",
        "tapering": "Suspensão imediata."
    },
    "nimesulida": {
        "drug": "Nimesulida",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar)",
        "recommendation": "Evitar terminantemente.",
        "rationale": "Hepatotoxicidade grave e nefrotoxicidade em pacientes geriátricos.",
        "tapering": "Interrupção imediata."
    },
    "meloxicam": {
        "drug": "Meloxicam",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar)",
        "recommendation": "Evitar em idosos.",
        "rationale": "Mantém risco cardiovascular e renal em idosos hospitalizados.",
        "tapering": "Interromper e reavaliar analgesia."
    },
    "piroxicam": {
        "drug": "Piroxicam",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar)",
        "recommendation": "Evitar absolutamente.",
        "rationale": "Meia-vida biológica superior a 50 horas com máxima taxa de sangramentos e reações adversas cutâneas graves.",
        "tapering": "Suspensão imediata."
    },

    # --------------------------------------------------------------------------
    # CARDIOVASCULARES
    # --------------------------------------------------------------------------
    "digoxina": {
        "drug": "Digoxina",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar como 1ª linha / Dose > 0.125mg)",
        "recommendation": "Evitar na primeira linha para fibrilação atrial ou insuficiência cardíaca; se imprescindível, nunca exceder 0,125 mg/dia.",
        "rationale": "Faixa terapêutica estreita e eliminação renal reduzida no envelhecimento; altíssimo risco de intoxicação digitálica com arritmias fatais e distúrbios neurológicos/visuais.",
        "tapering": "Monitorar digoxinemia e função renal; ajustar ou transicionar para betabloqueador seguro."
    },
    "amiodarona": {
        "drug": "Amiodarona",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar como 1ª linha para FA)",
        "recommendation": "Evitar como terapia inicial de FA, exceto em IC grave com disfunção de VE se outros agentes forem contraindicados.",
        "rationale": "Múltiplas toxicidades cumulativas a longo prazo (tireoidiana, pulmonar com fibrose, hepática e prolongamento do intervalo QT).",
        "tapering": "Desprescrição sob monitoramento do ritmo cardíaco conjunto com a cardiologia."
    },
    "espironolactona": {
        "drug": "Espironolactona",
        "axis": "AGS Beers 2023 - Tabela 2 e 6 (Evitar se dose > 25mg ou CrCl < 30)",
        "recommendation": "Evitar doses > 25 mg/dia na IC ou evitar o uso se o Clearance de Creatinina for < 30 mL/min.",
        "rationale": "Risco crítico de hipercalemia potencialmente letal, especialmente associado a IECA/BRA.",
        "tapering": "Monitorar rigorosamente potássio sérico e creatinina; suspender se CrCl < 30 mL/min."
    },
    "clonidina": {
        "drug": "Clonidina",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar para HAS de rotina)",
        "recommendation": "Evitar como anti-hipertensivo rotineiro em idosos.",
        "rationale": "Agonista alfa-2 central. Causa sedação acentuada, boca seca, bradicardia sinusal, hipotensão ortostática com quedas e crise hipertensiva severa de rebote.",
        "tapering": "Nunca suspender abruptamente. Reduzir a dose gradualmente ao longo de vários dias introduzindo anti-hipertensivo de primeira linha."
    },
    "metildopa": {
        "drug": "Metildopa",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar)",
        "recommendation": "Evitar em geriatria.",
        "rationale": "Depressão do SNC, bradicardia e risco imunológico de anemia hemolítica e lesão hepática.",
        "tapering": "Desmame gradual associado à transição para bloqueador de canal de cálcio ou IECA/BRA."
    },
    "nifedipino": {
        "drug": "Nifedipino (Liberação Rápida)",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar liberação imediata)",
        "recommendation": "Evitar cápsulas de liberação imediata ou via sublingual.",
        "rationale": "Queda abrupta da pressão arterial desencadeando taquicardia reflexa com isquemia miocárdica ou cerebral aguda.",
        "tapering": "Substituir por bloqueador de canal de cálcio de liberação prolongada ou anlodipino."
    },
    "doxazosina": {
        "drug": "Doxazosina",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar como anti-hipertensivo)",
        "recommendation": "Evitar como monoterapia ou agente primário para hipertensão.",
        "rationale": "Bloqueador alfa-1 periférico com alta incidência de hipotensão ortostática severa e síncope.",
        "tapering": "Se utilizada para HPB, manter monitoramento pressórico sentado/em pé rigoroso."
    },

    # --------------------------------------------------------------------------
    # HIPOGLICEMIANTES
    # --------------------------------------------------------------------------
    "glibenclamida": {
        "drug": "Glibenclamida",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar)",
        "recommendation": "Evitar terminantemente em pacientes geriátricos.",
        "rationale": "Sulfonilureia de ação prolongada e metabólitos ativos que se acumulam no idoso; alto risco de hipoglicemia severa, prolongada e dano neurológico irreversível.",
        "tapering": "Substituir imediatamente por Gliclazida MR, inibidor de DPP-4 (ex.: Linagliptina) ou esquema de insulina basal ajustada."
    },
    "glimepirida": {
        "drug": "Glimepirida",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar)",
        "recommendation": "Evitar em idosos.",
        "rationale": "Risco aumentado de hipoglicemias prolongadas em relação a outras opções antidiabéticas.",
        "tapering": "Transicionar para opções com menor risco de hipoglicemia."
    },

    # --------------------------------------------------------------------------
    # OPIOIDES E DIVERSOS
    # --------------------------------------------------------------------------
    "tramadol": {
        "drug": "Tramadol",
        "axis": "AGS Beers 2023 - Tabela 2 e 5 (Evitar / Risco de SIADH e Síndrome Serotoninérgica)",
        "recommendation": "Evitar o uso rotineiro ou associado a psicotrópicos.",
        "rationale": "Pode precipitar hiponatremia grave por SIADH, reduzir limiar epiléptico e causar Síndrome Serotoninérgica quando combinado com antidepressivos.",
        "tapering": "Reduzir 25-50% da dose a cada 3 dias antes da descontinuação."
    },
    "codeina": {
        "drug": "Codeína",
        "axis": "AGS Beers 2023 - Tabela 2 (Cautela / Constipação severa)",
        "recommendation": "Evitar uso prolongado; se necessário, prescrever laxativo profilático obrigatório.",
        "rationale": "Metabolismo variável via CYP2D6 e altíssima prevalência de constipação refratária e retenção urinária.",
        "tapering": "Desmame rápido e substituição por analgésicos não opioides."
    },
    "morfina": {
        "drug": "Morfina",
        "axis": "AGS Beers 2023 - Tabela 6 (Ajuste por Função Renal)",
        "recommendation": "Evitar se Clearance de Creatinina < 30 mL/min.",
        "rationale": "Retenção de metabólitos ativos neurotóxicos (M3G e M6G) levando a mioclonias, delírio e depressão respiratória grave.",
        "tapering": "Em caso de falência renal, substituir por Fentanila ou Metadona sob titulação rigorosa."
    },
    "meperidina": {
        "drug": "Meperidina",
        "axis": "AGS Beers 2023 - Tabela 2 (Evitar absolutamente)",
        "recommendation": "Evitar em qualquer cenário na geriatria.",
        "rationale": "O metabólito normeperidina possui meia-vida longa, excreção renal e neurotoxicidade extrema com convulsões e alucinações.",
        "tapering": "Substituição imediata por outro analgésico."
    }
}

SYNONYM_MAP = {
    # Dexclorfeniramina e sinônimos
    "dexclorfeniramina": "dexclorfeniramina",
    "maleato de dexclorfeniramina": "dexclorfeniramina",
    "polaramine": "dexclorfeniramina",
    "polararen": "dexclorfeniramina",
    "polaren": "dexclorfeniramina",
    "clorfeniramina": "dexclorfeniramina",
    "coristina": "dexclorfeniramina",

    # Anti-histamínicos
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

    # Anticolinérgicos
    "escopolamina": "escopolamina",
    "buscopan": "escopolamina",
    "hioscina": "escopolamina",
    "butilbrometo de escopolamina": "escopolamina",
    "biperideno": "biperideno",
    "akineton": "biperideno",
    "oxibutinina": "oxibutinina",
    "retemic": "oxibutinina",

    # Benzodiazepínicos e Sedativos
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

    # Neuropáticos / Antidepressivos / Antipsicóticos
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

    # GI e Motilidade
    "metoclopramida": "metoclopramida",
    "plasil": "metoclopramida",
    "omeprazol": "omeprazol",
    "losec": "omeprazol",
    "pantoprazol": "pantoprazol",
    "pantocal": "pantoprazol",
    "oleo mineral": "oleo mineral",
    "nujol": "oleo mineral",

    # Relaxantes Musculares
    "ciclobenzaprina": "ciclobenzaprina",
    "miosan": "ciclobenzaprina",
    "musculare": "ciclobenzaprina",
    "carisoprodol": "carisoprodol",
    "tandrilax": "carisoprodol",
    "torsilax": "carisoprodol",
    "orfenadrina": "orfenadrina",
    "dorflex": "orfenadrina",

    # AINEs
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

    # Cardiovasculares
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

    # Hipoglicemiantes
    "glibenclamida": "glibenclamida",
    "daonil": "glibenclamida",
    "glimepirida": "glimepirida",
    "amaryl": "glimepirida",

    # Opioides
    "tramadol": "tramadol",
    "tramal": "tramadol",
    "codeina": "codeina",
    "tylex": "codeina",
    "morfina": "morfina",
    "dimorf": "morfina",
    "meperidina": "meperidina",
    "petidina": "meperidina",
    "dolantina": "meperidina"
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

def lookup_hospital_drug(name: str) -> Optional[str]:
    return identify_drug_canonical(name)

def evaluate_patient_beers(
    medications: List[str],
    age: int,
    fall_risk: bool = False,
    conditions: Optional[List[str]] = None,
    crcl: Optional[float] = None
) -> List[Dict[str, Any]]:
    alerts = []
    conditions = conditions or []

    if age < 65:
        return alerts

    processed = set()

    for raw in medications:
        canonical = identify_drug_canonical(raw)
        if not canonical:
            continue

        if canonical in processed:
            continue
        processed.add(canonical)

        if canonical in BEERS_RULES:
            r = BEERS_RULES[canonical]
            rec = r["recommendation"]
            rat = r["rationale"]
            tap = r.get("tapering", "")

            if fall_risk and canonical in [
                "dexclorfeniramina", "hidroxizina", "difenidramina", "prometazina",
                "diazepam", "clonazepam", "lorazepam", "alprazolam", "midazolam",
                "zolpidem", "zopiclona", "amitriptilina", "quetiapina", "risperidona",
                "olanzapina", "haloperidol", "clonidina", "tramadol"
            ]:
                rec += " [ALERTA DE QUEDAS]: Paciente com alto risco de quedas documentado; este fármaco eleva significativamente a ocorrência de fraturas ortopédicas e traumatismo cranioencefálico."

            if crcl is not None:
                if canonical == "espironolactona" and crcl < 30:
                    rec += f" [AJUSTE RENAL CrCl={crcl} mL/min]: Evitar uso pelo risco iminente de hipercalemia refratária."
                elif canonical == "morfina" and crcl < 30:
                    rec += f" [AJUSTE RENAL CrCl={crcl} mL/min]: Evitar uso em TFG < 30 mL/min devido ao acúmulo de metabólitos neurotóxicos."

            alerts.append({
                "drug": r["drug"],
                "axis": r["axis"],
                "recommendation": rec,
                "rationale": rat,
                "tapering": tap
            })

    return alerts
