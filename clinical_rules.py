# -*- coding: utf-8 -*-
"""
FarmBeers - Motor de Regras Clínicas (AGS Beers Criteria 2023)
Mapeamento dos 72 Fármacos Hospitalares Brasileiros Padronizados
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

# ==============================================================================
# BASE DE CONHECIMENTO DE FÁRMACOS E REGRAS DE BEERS 2023 (TABELAS 2, 3, 5 E 6)
# ==============================================================================

# Regras Clínicas por Princípio Ativo Canônico
BEERS_RULES = {
    # --------------------------------------------------------------------------
    # ANTI-HISTAMÍNICOS DE 1ª GERAÇÃO (AÇÃO ANTICOLINÉRGICA POTENTE - TABELA 2)
    # --------------------------------------------------------------------------
    "dexclorfeniramina": {
        "drug": "Dexclorfeniramina",
        "axis": "Critério de Beers - Tabela 2 (Evitar)",
        "recommendation": "Anti-histamínico de 1ª geração com potente ação anticolinérgica. Alto risco de sedação excessiva, confusão mental, boca seca, constipação e retenção urinária. Risco acentuado de quedas e fraturas em idosos. Recomendação: Evitar o uso. Alternativas: Corticoides nasais tópicos ou anti-histamínicos de 2ª geração (ex.: cetirizina, loratadina, fexofenadina)."
    },
    "hidroxizina": {
        "drug": "Hidroxizina",
        "axis": "Critério de Beers - Tabela 2 (Evitar)",
        "recommendation": "Potente ação anticolinérgica e sedativa. Risco elevado de sedação, delírio, quedas e retenção urinária. Evitar o uso em idosos."
    },
    "difenidramina": {
        "drug": "Difenidramina",
        "axis": "Critério de Beers - Tabela 2 (Evitar)",
        "recommendation": "Anticolinérgico potente. Evitar o uso como antialérgico ou hipnótico. Alto risco de declínio cognitivo agudo e acidentes."
    },
    "dimenidrinato": {
        "drug": "Dimenidrinato",
        "axis": "Critério de Beers - Tabela 2 (Evitar)",
        "recommendation": "Alta atividade anticolinérgica e depressora do SNC. Evitar o uso para náuseas/êmese crônica ou vertigem em idosos. Preferir alternativas com menor perfil anticolinérgico (ex.: ondansetrona)."
    },
    "prometazina": {
        "drug": "Prometazina",
        "axis": "Critério de Beers - Tabela 2 (Evitar)",
        "recommendation": "Fenotiazina com propriedades anticolinérgicas e antidopaminérgicas intensas. Alto risco de sedação prolongada, hipotensão ortostática, sintomas extrapiramidais e delírio. Evitar."
    },
    "ciproeptadina": {
        "drug": "Ciproeptadina",
        "axis": "Critério de Beers - Tabela 2 (Evitar)",
        "recommendation": "Ação anticolinérgica potente. Evitar estimulantes de apetite ou antialérgicos dessa classe em idosos."
    },

    # --------------------------------------------------------------------------
    # ANTIPARKINSONIANOS ANTICOLINÉRGICOS / ESPASMOLÍTICOS URINÁRIOS
    # --------------------------------------------------------------------------
    "biperideno": {
        "drug": "Biperideno",
        "axis": "Critério de Beers - Tabela 2 (Evitar)",
        "recommendation": "Anticolinérgico de ação central. Alto risco de delírio, alucinações e retenção urinária aguda. Evitar na prevenção ou tratamento de sintomas extrapiramidais."
    },
    "oxibutinina": {
        "drug": "Oxibutinina",
        "axis": "Critério de Beers - Tabela 2 (Evitar)",
        "recommendation": "Espasmolítico urinário com forte bloqueio anticolinérgico sistêmico e central. Risco de piora cognitiva e constipação grave. Preferir fisioterapia pélvica ou mirabegrona."
    },
    "escopolamina": {
        "drug": "Escopolamina",
        "axis": "Critério de Beers - Tabela 2 (Evitar)",
        "recommendation": "Alcaloide da beladona com pronunciada ação anticolinérgica. Causa confusão mental, agitação paradoxal e retenção urinária. Evitar em idosos."
    },

    # --------------------------------------------------------------------------
    # BENZODIAZEPÍNICOS E HIPNÓTICOS SEDATIVOS (TABELA 2 E TABELA 3)
    # --------------------------------------------------------------------------
    "diazepam": {
        "drug": "Diazepam",
        "axis": "Critério de Beers - Tabela 2 (Evitar)",
        "recommendation": "Benzodiazepínico de longa ação com metabólitos ativos acumulativos. Risco acentuado de sedação excessiva, quedas, fraturas e acidentes automobilísticos. Evitar."
    },
    "clonazepam": {
        "drug": "Clonazepam",
        "axis": "Critério de Beers - Tabela 2 (Evitar)",
        "recommendation": "Alta sensibilidade em idosos, meia-vida longa. Risco significativo de comprometimento cognitivo, sedação diurna e quedas. Evitar o uso crônico."
    },
    "lorazepam": {
        "drug": "Lorazepam",
        "axis": "Critério de Beers - Tabela 2 (Evitar)",
        "recommendation": "Benzodiazepínico. Embora de meia-vida intermediária, mantém risco elevado de ataxia, delírio, dependência e quedas em idosos. Evitar."
    },
    "alprazolam": {
        "drug": "Alprazolam",
        "axis": "Critério de Beers - Tabela 2 (Evitar)",
        "recommendation": "Benzodiazepínico. Alto potencial de dependência física, tolerância, sedação e efeito rebote de ansiedade. Evitar."
    },
    "midazolam": {
        "drug": "Midazolam",
        "axis": "Critério de Beers - Tabela 2 (Evitar)",
        "recommendation": "Benzodiazepínico de curta ação. Restringir a procedimentos anestésicos/endoscópicos. Evitar como indutor do sono de enfermaria."
    },
    "zolpidem": {
        "drug": "Zolpidem",
        "axis": "Critério de Beers - Tabela 2 (Evitar)",
        "recommendation": "Agonista do receptor benzodiazepínico (Droga Z). Apresenta risco de sonambulismo, confusão mental, quedas e fraturas semelhante aos benzodiazepínicos. Evitar."
    },
    "zopiclona": {
        "drug": "Zopiclona",
        "axis": "Critério de Beers - Tabela 2 (Evitar)",
        "recommendation": "Droga Z sedativa. Risco elevado de sedação residual matinal, tontura e quedas. Evitar o uso crônico."
    },

    # --------------------------------------------------------------------------
    # ANTIDEPRESSIVOS TRICÍCLICOS E NEUROLÉPTICOS TÍPICOS / ATÍPICOS
    # --------------------------------------------------------------------------
    "amitriptilina": {
        "drug": "Amitriptilina",
        "axis": "Critério de Beers - Tabela 2 (Evitar)",
        "recommendation": "Antidepressivo tricíclico com potente efeito anticolinérgico e sedativo. Risco de hipotensão ortostática, arritmias e retenção urinária. Evitar."
    },
    "nortriptilina": {
        "drug": "Nortriptilina",
        "axis": "Critério de Beers - Tabela 2 (Evitar)",
        "recommendation": "Tricíclico com moderada atividade anticolinérgica. Risco de sedação e efeitos cardíacos. Evitar na primeira linha."
    },
    "clomipramina": {
        "drug": "Clomipramina",
        "axis": "Critério de Beers - Tabela 2 (Evitar)",
        "recommendation": "Tricíclico com alto bloqueio colinérgico e risco arritmogênico. Evitar em idosos."
    },
    "haloperidol": {
        "drug": "Haloperidol",
        "axis": "Critério de Beers - Tabela 2 (Evitar com ressalvas)",
        "recommendation": "Antipsicótico típico. Elevado risco de sintomas extrapiramidais, discinesia tardia e aumento da mortalidade em idosos com demência. Evitar como controle comportamental não psicótico."
    },
    "clorpromazina": {
        "drug": "Clorpromazina",
        "axis": "Critério de Beers - Tabela 2 (Evitar)",
        "recommendation": "Antipsicótico de baixa potência com forte efeito anticolinérgico, sedativo e hipotensor alfa-1 bloqueador. Evitar."
    },
    "levomepromazina": {
        "drug": "Levomepromazina",
        "axis": "Critério de Beers - Tabela 2 (Evitar)",
        "recommendation": "Alta sedação, hipotensão postural e bloqueio anticolinérgico intenso. Evitar em idosos."
    },
    "tioridazina": {
        "drug": "Tioridazina",
        "axis": "Critério de Beers - Tabela 2 (Evitar)",
        "recommendation": "Prolongamento do intervalo QT e efeito anticolinérgico severo. Evitar terminantemente."
    },
    "quetiapina": {
        "drug": "Quetiapina",
        "axis": "Critério de Beers - Tabela 2 (Evitar sem indicação precisa)",
        "recommendation": "Antipsicótico atípico. Evitar o uso como indutor simples de sono ou para agitação não psicótica em demência (aumento de risco cerebrovascular)."
    },
    "olanzapina": {
        "drug": "Olanzapina",
        "axis": "Critério de Beers - Tabela 2 (Evitar)",
        "recommendation": "Ação anticolinérgica intrínseca, ganho ponderal e risco de eventos vasculares encefálicos em idosos com demência."
    },
    "risperidona": {
        "drug": "Risperidona",
        "axis": "Critério de Beers - Tabela 2 (Evitar)",
        "recommendation": "Risco de sintomas extrapiramidais dose-dependentes e mortalidade aumentada em demência. Evitar exceto em psicoses graves."
    },

    # --------------------------------------------------------------------------
    # AGENTES GASTROINTESTINAIS E MOTILIDADE
    # --------------------------------------------------------------------------
    "metoclopramida": {
        "drug": "Metoclopramida",
        "axis": "Critério de Beers - Tabela 2 (Evitar)",
        "recommendation": "Antagonista dopaminérgico central. Alto risco de sintomas extrapiramidais e discinesia tardia irreversível em idosos. Evitar o uso profilático ou prolongado. Alternativa: ondansetrona ou domperidona com cautela."
    },
    "omeprazol": {
        "drug": "Omeprazol",
        "axis": "Critério de Beers - Tabela 2 (Evitar uso > 8 semanas)",
        "recommendation": "Inibidor da Bomba de Prótons (IBP). O uso contínuo desnecessário (> 8 semanas) está associado a infecção por Clostridioides difficile, fraturas ósseas, hipomagnesemia e deficiência de vitamina B12."
    },
    "pantoprazol": {
        "drug": "Pantoprazol",
        "axis": "Critério de Beers - Tabela 2 (Evitar uso > 8 semanas)",
        "recommendation": "IBP. Evitar uso além de 8 semanas sem indicação clínica formal (ex.: úlcera ativa ou uso crônico de antiagregante/anticoagulante com alto risco hemorrágico)."
    },
    "esomeprazol": {
        "drug": "Esomeprazol",
        "axis": "Critério de Beers - Tabela 2 (Evitar uso > 8 semanas)",
        "recommendation": "IBP. Monitorar necessidade real de manutenção prolongada pelo risco de infecções entéricas e desmineralização óssea."
    },
    "lansoprazol": {
        "drug": "Lansoprazol",
        "axis": "Critério de Beers - Tabela 2 (Evitar uso > 8 semanas)",
        "recommendation": "IBP. Reavaliar indicação após 8 semanas de tratamento em pacientes hospitalizados ou ambulatoriais idosos."
    },
    "oleo mineral": {
        "drug": "Óleo Mineral",
        "axis": "Critério de Beers - Tabela 2 (Evitar VO)",
        "recommendation": "Risco de pneumonia lipoídica por aspiração pulmonar em idosos acamados ou com disfagia. Evitar a via oral."
    },

    # --------------------------------------------------------------------------
    # ANTI-INFLAMATÓRIOS NÃO ESTEROIDAIS (AINES) E ANALGÉSICOS
    # --------------------------------------------------------------------------
    "diclofenaco": {
        "drug": "Diclofenaco",
        "axis": "Critério de Beers - Tabela 2 (Evitar uso crônico)",
        "recommendation": "AINE não seletivo. Alto risco de sangramento gastrointestinal, piora da função renal, retenção hídrica/descompensação de IC e elevação da pressão arterial."
    },
    "ibuprofeno": {
        "drug": "Ibuprofeno",
        "axis": "Critério de Beers - Tabela 2 (Evitar uso crônico)",
        "recommendation": "AINE. Risco de nefrotoxicidade aguda, hemorragia digestiva alta e antagonismo do efeito cardioprotetor da aspirina. Evitar uso prolongado."
    },
    "cetoprofeno": {
        "drug": "Cetoprofeno",
        "axis": "Critério de Beers - Tabela 2 (Evitar)",
        "recommendation": "AINE com pronunciada inibição de prostaglandinas renais e gástricas. Evitar o uso rotineiro em idosos internados."
    },
    "meloxicam": {
        "drug": "Meloxicam",
        "axis": "Critério de Beers - Tabela 2 (Evitar)",
        "recommendation": "AINE com preferência COX-2. Mantém risco de complicações cardiovasculares e desfechos renais adversos em idosos."
    },
    "piroxicam": {
        "drug": "Piroxicam",
        "axis": "Critério de Beers - Tabela 2 (Evitar)",
        "recommendation": "AINE de meia-vida extremamente longa. Toxicidade gastrointestinal e cutânea superior aos outros AINEs. Evitar terminantemente."
    },
    "indometacina": {
        "drug": "Indometacina",
        "axis": "Critério de Beers - Tabela 2 (Evitar)",
        "recommendation": "AINE com maior incidência de toxicidade no SNC (cefaleia, tontura, confusão mental) e eventos gástricos graves. Evitar."
    },
    "cetorolaco": {
        "drug": "Cetorolaco",
        "axis": "Critério de Beers - Tabela 2 (Evitar)",
        "recommendation": "AINE potente de uso parenteral/oral. Risco altíssimo de hemorragia gastrointestinal e falência renal aguda em idosos. Evitar."
    },
    "nimesulida": {
        "drug": "Nimesulida",
        "axis": "Critério de Beers - Tabela 2 (Evitar)",
        "recommendation": "AINE associado a casos severos de hepatotoxicidade fulminante e lesão renal aguda em pacientes geriátricos. Evitar."
    },

    # --------------------------------------------------------------------------
    # RELAXANTES MUSCULARES
    # --------------------------------------------------------------------------
    "ciclobenzaprina": {
        "drug": "Ciclobenzaprina",
        "axis": "Critério de Beers - Tabela 2 (Evitar)",
        "recommendation": "Estruturalmente similar aos antidepressivos tricíclicos. Intensa atividade anticolinérgica e sedativa. Elevado risco de sedação, arritmias e quedas em idosos. Evitar."
    },
    "carisoprodol": {
        "drug": "Carisoprodol",
        "axis": "Critério de Beers - Tabela 2 (Evitar)",
        "recommendation": "Metabolizado a meprobamato (sedativo com alto risco de dependência e depressão respiratória). Evitar."
    },
    "orfenadrina": {
        "drug": "Orfenadrina",
        "axis": "Critério de Beers - Tabela 2 (Evitar)",
        "recommendation": "Componente analgésico-relaxante com potente ação anticolinérgica e estimulante central. Risco de alucinações, boca seca e retenção urinária. Evitar."
    },
    "baclofeno": {
        "drug": "Baclofeno",
        "axis": "Critério de Beers - Tabela 2 (Cautela / Ajuste Renal)",
        "recommendation": "Risco de encefalopatia e sedação severa, especialmente se houver perda de função renal. Evitar suspensão abrupta."
    },

    # --------------------------------------------------------------------------
    # SISTEMA CARDIOVASCULAR E ANTI-HIPERTENSIVOS
    # --------------------------------------------------------------------------
    "digoxina": {
        "drug": "Digoxina",
        "axis": "Critério de Beers - Tabela 2 (Evitar na 1ª linha / Dose > 0.125mg)",
        "recommendation": "Glicosídeo cardíaco de estreita faixa terapêutica. Depuração renal diminuída no idoso leva a intoxicação digitálica (náuseas, arritmias, bloqueios e distúrbios visuais). Evitar doses superiores a 0,125 mg/dia."
    },
    "amiodarona": {
        "drug": "Amiodarona",
        "axis": "Critério de Beers - Tabela 2 (Evitar na 1ª linha para FA)",
        "recommendation": "Antiarrítmico com pronunciada toxicidade multissistêmica crônica (tireóide, pulmonar, hepática e prolongamento do intervalo QT). Evitar como terapia inicial de fibrilação atrial se houver alternativa de controle de frequência."
    },
    "espironolactona": {
        "drug": "Espironolactona",
        "axis": "Critério de Beers - Tabela 2 e 6 (Evitar se dose > 25mg ou CrCl < 30)",
        "recommendation": "Risco de hipercalemia fatal e acidose metabólica em idosos, especialmente em associação com IECA/BRA ou com insuficiência renal."
    },
    "clonidina": {
        "drug": "Clonidina",
        "axis": "Critério de Beers - Tabela 2 (Evitar na rotina de HAS)",
        "recommendation": "Agonista alfa-2 central. Alto risco de sedação, boca seca, bradicardia e hipotensão ortostática com quedas, além de hipertensão rebote severa na interrupção. Evitar como anti-hipertensivo rotineiro."
    },
    "metildopa": {
        "drug": "Metildopa",
        "axis": "Critério de Beers - Tabela 2 (Evitar)",
        "recommendation": "Ação central depressora, bradicardizante e risco de anemia hemolítica e hepatite medicamentosa. Evitar em geriatria."
    },
    "nifedipino": {
        "drug": "Nifedipino (Liberação Imediata)",
        "axis": "Critério de Beers - Tabela 2 (Evitar cápsula rápida)",
        "recommendation": "Risco de hipotensão precipitada com isquemia coronariana ou cerebral aguda secundária a taquicardia reflexa. Não utilizar via sublingual ou cápsula líquida rápida."
    },
    "doxazosina": {
        "drug": "Doxazosina",
        "axis": "Critério de Beers - Tabela 2 (Evitar para HAS)",
        "recommendation": "Bloqueador alfa-1 periférico. Causa hipotensão postural acentuada e síncope ao levantar. Evitar como terapia primária de hipertensão."
    },
    "prazosina": {
        "drug": "Prazosina",
        "axis": "Critério de Beers - Tabela 2 (Evitar)",
        "recommendation": "Hipotensão ortostática severa e risco de trauma mecânico por queda. Evitar."
    },

    # --------------------------------------------------------------------------
    # HIPOGLICEMIANTES / SULFONILUREIAS
    # --------------------------------------------------------------------------
    "glibenclamida": {
        "drug": "Glibenclamida",
        "axis": "Critério de Beers - Tabela 2 (Evitar)",
        "recommendation": "Sulfonilureia de meia-vida prolongada e metabólitos ativos acumulativos. Risco extremo de hipoglicemia grave e prolongada com dano neurológico permanente. Evitar. Alternativa: gliclazida, linagliptina ou metformina (ajustada à TFG)."
    },
    "glimepirida": {
        "drug": "Glimepirida",
        "axis": "Critério de Beers - Tabela 2 (Evitar)",
        "recommendation": "Risco elevado de hipoglicemia prolongada em pacientes idosos. Evitar."
    },
    "insulina": {
        "drug": "Insulina Escalonada (Sliding Scale)",
        "axis": "Critério de Beers - Tabela 2 (Evitar prescrição isolada de escala rápida)",
        "recommendation": "Evitar o uso exclusivo de esquema móvel/escalonado de insulina de ação rápida ou ultra-rápida (Sliding Scale) sem insulina basal em enfermarias, devido ao risco de hipoglicemia severa sem controle glicêmico adequado."
    },

    # --------------------------------------------------------------------------
    # ANALGÉSICOS OPIOIDES E DIVERSOS
    # --------------------------------------------------------------------------
    "tramadol": {
        "drug": "Tramadol",
        "axis": "Critério de Beers - Tabela 2 e 5 (Evitar / Risco de Síndrome Serotoninérgica e SIADH)",
        "recommendation": "Risco de hiponatremia por SIADH, confusão mental, náuseas e redução do limiar convulsivo. Em combinação com antidepressivos serotoninérgicos, pode desencadear Síndrome Serotoninérgica fatal."
    },
    "codeina": {
        "drug": "Codeína",
        "axis": "Critério de Beers - Tabela 2 (Cautela / Constipação grave)",
        "recommendation": "Metabolização dependente do CYP2D6. Risco elevado de constipação refratária, sedação e retenção urinária. Associar laxativos profiláticos."
    },
    "morfina": {
        "drug": "Morfina",
        "axis": "Critério de Beers - Tabela 6 (Ajuste Renal / Evitar no CrCl < 30)",
        "recommendation": "Acúmulo de metabólitos ativos (morfina-6-glicuronídeo e morfina-3-glicuronídeo) na disfunção renal, provocando narcose profunda, mioclonias e depressão respiratória."
    },
    "fentanila": {
        "drug": "Fentanila",
        "axis": "Critério de Beers - Tabela 2 (Evitar adesivo em paciente virgem de opioide)",
        "recommendation": "Risco de depressão respiratória fatal em pacientes geriátricos não tolerantes a opioides ou com caquexia (absorção errática)."
    },
    "meperidina": {
        "drug": "Meperidina",
        "axis": "Critério de Beers - Tabela 2 (Evitar terminantemente)",
        "recommendation": "Opioide com metabólito neurotóxico (normeperidina) que se acumula e provoca convulsões, mioclonias e alucinações. Evitar."
    }
}

# ==============================================================================
# DICIONÁRIO DE SINÔNIMOS E NOMES COMERCIAIS BRASILEIROS
# ==============================================================================
SYNONYM_MAP = {
    # Dexclorfeniramina
    "dexclorfeniramina": "dexclorfeniramina",
    "maleato de dexclorfeniramina": "dexclorfeniramina",
    "polaramine": "dexclorfeniramina",
    "polararen": "dexclorfeniramina",
    "polaren": "dexclorfeniramina",
    "clorfeniramina": "dexclorfeniramina",
    "coristina": "dexclorfeniramina",

    # Hidroxizina
    "hidroxizina": "hidroxizina",
    "cloridrato de hidroxizina": "hidroxizina",
    "hixizine": "hidroxizina",
    "prurizin": "hidroxizina",

    # Difenidramina
    "difenidramina": "difenidramina",
    "benadryl": "difenidramina",
    "difenidrin": "difenidramina",

    # Dimenidrinato
    "dimenidrinato": "dimenidrinato",
    "dramin": "dimenidrinato",
    "dramin b6": "dimenidrinato",

    # Prometazina
    "prometazina": "prometazina",
    "fenergan": "prometazina",
    "prometazol": "prometazina",

    # Biperideno
    "biperideno": "biperideno",
    "akineton": "biperideno",
    "cinetol": "biperideno",

    # Oxibutinina
    "oxibutinina": "oxibutinina",
    "retemic": "oxibutinina",

    # Escopolamina
    "escopolamina": "escopolamina",
    "hioscina": "escopolamina",
    "buscopan": "escopolamina",
    "butilbrometo de escopolamina": "escopolamina",

    # Benzodiazepínicos
    "diazepam": "diazepam",
    "valium": "diazepam",
    "dienpax": "diazepam",
    "clonazepam": "clonazepam",
    "rivotril": "clonazepam",
    "lorazepam": "lorazepam",
    "lorax": "lorazepam",
    "alprazolam": "alprazolam",
    "fronta": "alprazolam",
    "frontin": "alprazolam",
    "midazolam": "midazolam",
    "dormonid": "midazolam",
    "zolpidem": "zolpidem",
    "stilnox": "zolpidem",
    "patz": "zolpidem",
    "turnover": "zolpidem",
    "zopiclona": "zopiclona",
    "imovane": "zopiclona",

    # Antidepressivos Tricíclicos e Antipsicóticos
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
    "tioridazina": "tioridazina",
    "melleril": "tioridazina",
    "quetiapina": "quetiapina",
    "seroquel": "quetiapina",
    "olanzapina": "olanzapina",
    "zyprexa": "olanzapina",
    "risperidona": "risperidona",
    "risperdal": "risperidona",

    # Gastrointestinais
    "metoclopramida": "metoclopramida",
    "plasil": "metoclopramida",
    "omeprazol": "omeprazol",
    "losec": "omeprazol",
    "pantoprazol": "pantoprazol",
    "pantocal": "pantoprazol",
    "pantozol": "pantoprazol",
    "esomeprazol": "esomeprazol",
    "nexium": "esomeprazol",
    "lansoprazol": "lansoprazol",
    "prazol": "lansoprazol",
    "oleo mineral": "oleo mineral",
    "mineral": "oleo mineral",
    "nujol": "oleo mineral",

    # AINEs
    "diclofenaco": "diclofenaco",
    "voltaren": "diclofenaco",
    "cataflam": "diclofenaco",
    "ibuprofeno": "ibuprofeno",
    "advil": "ibuprofeno",
    "alivium": "ibuprofeno",
    "cetoprofeno": "cetoprofeno",
    "profenid": "cetoprofeno",
    "meloxicam": "meloxicam",
    "movatec": "meloxicam",
    "piroxicam": "piroxicam",
    "feldene": "piroxicam",
    "indometacina": "indometacina",
    "cetorolaco": "cetorolaco",
    "toradol": "cetorolaco",
    "deocil": "cetorolaco",
    "nimesulida": "nimesulida",
    "scutamil": "nimesulida",
    "nisulid": "nimesulida",

    # Relaxantes Musculares
    "ciclobenzaprina": "ciclobenzaprina",
    "miosan": "ciclobenzaprina",
    "musculare": "ciclobenzaprina",
    "carisoprodol": "carisoprodol",
    "tandrilax": "carisoprodol",
    "torsilax": "carisoprodol",
    "orfenadrina": "orfenadrina",
    "dorflex": "orfenadrina",
    "baclofeno": "baclofeno",
    "lioresal": "baclofeno",

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
    "prazosina": "prazosina",
    "minipress": "prazosina",

    # Hipoglicemiantes
    "glibenclamida": "glibenclamida",
    "daonil": "glibenclamida",
    "glimepirida": "glimepirida",
    "amaryl": "glimepirida",
    "insulina": "insulina",
    "insulina regular": "insulina",
    "insulina lispro": "insulina",
    "insulina asparte": "insulina",

    # Opioides
    "tramadol": "tramadol",
    "tramal": "tramadol",
    "dorless": "tramadol",
    "codeina": "codeina",
    "tylex": "codeina",
    "morfina": "morfina",
    "dimorf": "morfina",
    "fentanila": "fentanila",
    "durogesic": "fentanila",
    "meperidina": "meperidina",
    "petidina": "meperidina",
    "dolantina": "meperidina"
}

# ==============================================================================
# IDENTIFICADOR INTELIGENTE DE FÁRMACOS (ROBUSTO CONTRA DOSES E TEXTO EXTRA)
# ==============================================================================
def identify_drug_canonical(input_text: str) -> Optional[str]:
    """
    Identifica o fármaco canônico mesmo se o usuário digitar
    'Dexclorfeniramina 4mg vo 2x/dia', 'Polaramine comp', etc.
    """
    if not input_text:
        return None

    cleaned = normalize_text(input_text)

    # 1. Busca exata ou por chave direta de sinônimo
    if cleaned in SYNONYM_MAP:
        return SYNONYM_MAP[cleaned]

    # 2. Busca por palavras completas ou prefixos nos sinônimos (ex: dexclorfeniramina dentro de uma frase)
    # Ordena chaves das maiores para as menores para garantir casamento específico
    sorted_synonyms = sorted(SYNONYM_MAP.keys(), key=lambda x: len(x), reverse=True)
    for syn in sorted_synonyms:
        pattern = r"\b" + re.escape(syn) + r"\b"
        if re.search(pattern, cleaned):
            return SYNONYM_MAP[syn]

    # 3. Verificação de subcadeia de pelo menos 5 caracteres
    for syn, canonical in SYNONYM_MAP.items():
        if len(syn) >= 5 and syn in cleaned:
            return canonical

    return None

def lookup_hospital_drug(name: str) -> Optional[str]:
    """Mantém retrocompatibilidade de API"""
    return identify_drug_canonical(name)

# ==============================================================================
# MOTOR DE AVALIAÇÃO DE BEERS 2023
# ==============================================================================
def evaluate_patient_beers(
    medications: List[str],
    age: int,
    fall_risk: bool = False,
    conditions: Optional[List[str]] = None,
    crcl: Optional[float] = None
) -> List[Dict[str, Any]]:
    """
    Avalia a prescrição do paciente e retorna os alertas clínicos de Beers 2023.
    """
    alerts = []
    conditions = conditions or []

    # Critérios de Beers são estritamente desenhados para indivíduos idosos (>= 65 anos)
    if age < 65:
        return alerts

    processed_drugs = set()

    for raw_med in medications:
        canonical = identify_drug_canonical(raw_med)
        if not canonical:
            continue

        if canonical in processed_drugs:
            continue
        processed_drugs.add(canonical)

        # Regra Geral de Beers (Tabela 2)
        if canonical in BEERS_RULES:
            rule_info = BEERS_RULES[canonical]
            alert_payload = {
                "drug": rule_info["drug"],
                "axis": rule_info["axis"],
                "recommendation": rule_info["recommendation"]
            }

            # Acréscimo dinâmico se houver Risco de Quedas marcado
            if fall_risk and canonical in [
                "dexclorfeniramina", "hidroxizina", "difenidramina", "prometazina",
                "diazepam", "clonazepam", "lorazepam", "alprazolam", "midazolam",
                "zolpidem", "zopiclona", "amitriptilina", "quetiapina", "risperidona",
                "olanzapina", "haloperidol", "clonidina", "tramadol"
            ]:
                alert_payload["recommendation"] += " [ALERTA DE RISCO DE QUEDAS]: O paciente possui risco de quedas documentado; este fármaco aumenta exponencialmente a incidência de perda de equilíbrio, fraturas graves de fêmur e TCE."

            # Acréscimo dinâmico por Função Renal (Tabela 6)
            if crcl is not None:
                if canonical == "espironolactona" and crcl < 30:
                    alert_payload["recommendation"] += f" [AJUSTE RENAL CrCl={crcl} mL/min]: Espironolactona deve ser evitada com TFG < 30 mL/min pelo risco de hipercalemia fatal."
                elif canonical == "morfina" and crcl < 30:
                    alert_payload["recommendation"] += f" [AJUSTE RENAL CrCl={crcl} mL/min]: Morfina acumula metabólitos neurotóxicos e depressores respiratórios na insuficiência renal grave."

            alerts.append(alert_payload)

    return alerts
