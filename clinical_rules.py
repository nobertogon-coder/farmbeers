# -*- coding: utf-8 -*-
"""
BASE FARMACOLÓGICA E REGRAS CLÍNICAS - CRITÉRIOS AGS BEERS 2023
Curadoria focada no ambiente hospitalar brasileiro (UPI / UTI).
"""

# =========================================================================
# 1. TABELA 2: MEDICAMENTOS POTENCIALMENTE INAPROPRIADOS (EVITAR SEMPRE)
# =========================================================================
TABLE_2_GENERAL = [
    # --- Benzodiazepínicos e Hipnóticos (Drogas Z) ---
    {
        "drug": "Diazepam",
        "aliases": ["valium", "dienpax", "calmociteno"],
        "cat": "Benzodiazepínico",
        "rec": "Evitar no idoso.",
        "rat": "Meia-vida longa (>48-100h); acúmulo sedativo, ataxia, lentificação psicomotora e elevado risco de quedas e fraturas.",
        "tapering": "Desmame Gradual: Reduzir a dose em 25% a cada 1-2 semanas monitorando ansiedade e insônia rebote."
    },
    {
        "drug": "Clonazepam",
        "aliases": ["rivotril", "navotrax", "clonotril"],
        "cat": "Benzodiazepínico",
        "rec": "Evitar no idoso.",
        "rat": "Lentificação psicomotora acentuada, tolerância e risco elevado de fratura de colo de fêmur.",
        "tapering": "Desmame Gradual: Reduzir 0,25 mg a 0,5 mg a cada 10-14 dias. Não suspender abruptamente."
    },
    {
        "drug": "Alprazolam",
        "aliases": ["frontal", "tranquinal", "apraz"],
        "cat": "Benzodiazepínico",
        "rec": "Evitar no idoso.",
        "rat": "Início de ação rápido com alto potencial de dependência física e episódios de abstinência/ansiedade interdose.",
        "tapering": "Desmame: Redução fracionada de 25% a cada 1-2 semanas."
    },
    {
        "drug": "Bromazepam",
        "aliases": ["lexotan", "somalium", "deptran"],
        "cat": "Benzodiazepínico",
        "rec": "Evitar no idoso.",
        "rat": "Sedação residual diurna, perda de coordenação motora e risco de broncoaspiração.",
        "tapering": "Desmame gradual ao longo de 2 a 4 semanas."
    },
    {
        "drug": "Lorazepam",
        "aliases": ["lorax", "ansirax", "lorium"],
        "cat": "Benzodiazepínico",
        "rec": "Evitar no idoso.",
        "rat": "Alta sensibilidade farmacodinâmica central no paciente geriátrico; risco aumentado de delirium e acidentes posturais.",
        "tapering": "Redução gradual fracionada sob supervisão clínica."
    },
    {
        "drug": "Midazolam",
        "aliases": ["dormonid"],
        "cat": "Benzodiazepínico",
        "rec": "Evitar uso oral em enfermaria como hipnótico de rotina.",
        "rat": "Amnésia anterógrada severa e sedação paradoxal aguda com risco de depressão ventilatória.",
        "tapering": "Restringir estritamente a sedação em procedimentos ou ambiente de UTI sob ventilação."
    },
    {
        "drug": "Clobazam",
        "aliases": ["frisium", "urbanil"],
        "cat": "Benzodiazepínico",
        "rec": "Evitar exceto em epilepsia refratária com acompanhamento neurológico.",
        "rat": "Sedação cumulativa, sonolência residual e instabilidade na marcha.",
        "tapering": "Descontinuação progressiva lenta se em uso contínuo."
    },
    {
        "drug": "Flurazepam",
        "aliases": ["dalmadorm"],
        "cat": "Benzodiazepínico",
        "rec": "Evitar estritamente.",
        "rat": "Metabólito ativo com meia-vida superior a 100 horas; risco cumulativo severo de sonolência contínua.",
        "tapering": "Descontinuação progressiva."
    },
    {
        "drug": "Nitrazepam",
        "aliases": ["mogadon", "nitrapan"],
        "cat": "Benzodiazepínico",
        "rec": "Evitar.",
        "rat": "Eliminação lenta com acúmulo sedativo, ataxia e confusão mental.",
        "tapering": "Desmame escalonado semanal."
    },
    {
        "drug": "Zolpidem",
        "aliases": ["stilnox", "patz", "noctaliv"],
        "cat": "Droga Z / Hipnótico",
        "rec": "Evitar no idoso.",
        "rat": "Gera comportamentos motores automáticos do sono, amnésia e traumatismos posturais idênticos aos benzodiazepínicos.",
        "tapering": "Desmame: Reduzir para dose de 5 mg por 7 dias, depois uso em dias alternados antes da suspensão total."
    },
    {
        "drug": "Zopiclona",
        "aliases": ["imovane"],
        "cat": "Droga Z / Hipnótico",
        "rec": "Evitar no idoso.",
        "rat": "Prejuízo motor matinal, disgeusia persistente e confusão mental noturna.",
        "tapering": "Redução progressiva ao longo de 7 a 10 dias."
    },

    # --- Relaxantes Musculares e Anticolinérgicos ---
    {
        "drug": "Carisoprodol",
        "aliases": ["torsilax", "dorflex", "miosan dc", "trilax"],
        "cat": "Relaxante Muscular",
        "rec": "Evitar estritamente.",
        "rat": "Biotransformado no metabólito meprobamato; forte dependência física, sedação profunda e perda de equilíbrio motor.",
        "tapering": "Desprescrição: Interrupção no prazo de 3 a 5 dias para prevenir abstinência adrenérgica."
    },
    {
        "drug": "Ciclobenzaprina",
        "aliases": ["miosan", "musculare", "mirtax"],
        "cat": "Relaxante Muscular",
        "rec": "Evitar no idoso.",
        "rat": "Estrutura análoga aos tricíclicos; alta carga anticolinérgica, retenção urinária, constipação e confusão mental.",
        "tapering": "Desprescrição: Interromper e instituir analgesia simples com Dipirona ou Paracetamol."
    },
    {
        "drug": "Orfenadrina",
        "aliases": ["doricin", "sedilax"],
        "cat": "Relaxante Muscular / Anticolinérgico",
        "rec": "Evitar no idoso.",
        "rat": "Bloqueio muscarínico acentuado: taquicardia sinusal reflexa, retenção urinária aguda e precipitação de glaucoma agudo.",
        "tapering": "Substituição imediata por analgésico isolado."
    },
    {
        "drug": "Tizanidina",
        "aliases": ["sirdalud"],
        "cat": "Agonista Alfa-2 Central / Relaxante",
        "rec": "Evitar em idosos frágeis.",
        "rat": "Hipotensão postural acentuada, bradicardia sinusal sintomática e sedação excessiva.",
        "tapering": "Desmame gradual para evitar hipertensão de rebote."
    },

    # --- Anti-histamínicos de 1ª Geração e Anticolinérgicos ---
    {
        "drug": "Dexclorfeniramina",
        "aliases": ["polaramine", "histamin", "polaren", "coristina"],
        "cat": "Anti-histamínico 1ª Geração",
        "rec": "Evitar no idoso.",
        "rat": "Ação anticolinérgica acentuada: boca seca, constipação grave, delírio e retenção urinária.",
        "tapering": "Substituição: Trocar por anti-histamínico de 2ª geração (Loratadina, Cetirizina ou Fexofenadina)."
    },
    {
        "drug": "Prometazina",
        "aliases": ["fenergan", "prometazol", "profergan"],
        "cat": "Anti-histamínico / Fenotiazina",
        "rec": "Evitar no idoso.",
        "rat": "Sedação profunda, hipotensão ortostática pronunciada e risco de sintomas extrapiramidais (acatisia).",
        "tapering": "Se utilizada para emese ou náusea, substituir por Ondansetrona."
    },
    {
        "drug": "Dimenidrinato",
        "aliases": ["dramin", "dramavit", "dimenidrin"],
        "cat": "Anti-histamínico / Antivertiginoso",
        "rec": "Evitar uso contínuo.",
        "rat": "Sedação e bloqueio colinérgico que acelera declínio cognitivo e anula medicações anticolinesterásicas.",
        "tapering": "Restringir a crises vertiginosas agudas (máximo 48 a 72 horas)."
    },
    {
        "drug": "Hidroxizina",
        "aliases": ["hixizine", "prurizin"],
        "cat": "Anti-histamínico 1ª Geração",
        "rec": "Evitar no idoso.",
        "rat": "Sonolência residual, xerostomia e potencial de prolongamento do intervalo QTc.",
        "tapering": "Substituir por medidas tópicas emolientes e anti-histamínico não sedativo."
    },
    {
        "drug": "Difenidramina",
        "aliases": ["benadryl", "difenidrin"],
        "cat": "Anti-histamínico 1ª Geração",
        "rec": "Evitar como sedativo/hipnótico.",
        "rat": "Alta carga anticolinérgica e sedação diurna residual sem ganho na arquitetura do sono.",
        "tapering": "Suspensão direta; reforçar medidas não farmacológicas de higiene do sono."
    },
    {
        "drug": "Ciproheptadina",
        "aliases": ["periactin", "apevitin", "cobavital"],
        "cat": "Anti-histamínico / Orexígeno",
        "rec": "Evitar estritamente para ganho de apetite.",
        "rat": "Sedação profunda, letargia e bloqueio anticolinérgico sem ganho de massa magra funcional.",
        "tapering": "Suspensão; avaliar suplementação nutricional orientada."
    },
    {
        "drug": "Meclizina",
        "aliases": ["meclin"],
        "cat": "Anti-histamínico / Antivertiginoso",
        "rec": "Evitar uso contínuo prolongado.",
        "rat": "Sedação, tontura paradoxal e retenção urinária no idoso.",
        "tapering": "Limitar a quadros agudos; priorizar manobras posturais e fisioterapia vestibular."
    },
    {
        "drug": "Biperideno",
        "aliases": ["akineton", "cinetol"],
        "cat": "Anticolinérgico Central",
        "rec": "Evitar no idoso.",
        "rat": "Altíssimo potencial de induzir alucinações visuais, delirium agudo e íleo paralítico.",
        "tapering": "Desmame lento com acompanhamento neurológico."
    },
    {
        "drug": "Tri-hexifenidil",
        "aliases": ["artane"],
        "cat": "Anticolinérgico Central",
        "rec": "Evitar no idoso.",
        "rat": "Carga anticolinérgica extrema; deterioração cognitiva aguda e retenção de urina.",
        "tapering": "Desmame gradual para prevenir piora motora abrupta."
    },
    {
        "drug": "Oxibutinina",
        "aliases": ["retomic", "incontinol"],
        "cat": "Antimuscarínico Urinário",
        "rec": "Evitar formulações de liberação imediata.",
        "rat": "Atravessa a barreira hematoencefálica causando alucinações, confusão mental e perda de memória.",
        "tapering": "Avaliar agonista beta-3 (Mirabegrona) ou fisioterapia pélvica."
    },
    {
        "drug": "Tolterodina",
        "aliases": ["detrusitol"],
        "cat": "Antimuscarínico Urinário",
        "rec": "Evitar em idosos com demência ou comprometimento cognitivo.",
        "rat": "Acelera declínio cognitivo e provoca xerostomia e obstipação severa.",
        "tapering": "Titular para a menor dose efetiva ou descontinuar."
    },

    # --- Antipsicóticos (Risco de AVC e Mortalidade em Demência) ---
    {
        "drug": "Haloperidol",
        "aliases": ["haldol"],
        "cat": "Antipsicótico Típico",
        "rec": "Evitar para controle de sintomas comportamentais em demência.",
        "rat": "Aumento documentado de mortalidade e AVC em demência; elevado índice de parkinsonismo e discinesia tardia.",
        "tapering": "Desmame: Redução progressiva de 25% a 50% por semana após cessar a causa aguda do delirium."
    },
    {
        "drug": "Clorpromazina",
        "aliases": ["amplictil", "clorpromaz"],
        "cat": "Antipsicótico Típico",
        "rec": "Evitar.",
        "rat": "Hipotensão ortostática acentuada, sedação profunda e efeitos anticolinérgicos marcados.",
        "tapering": "Desmame progressivo sob monitoramento pressórico."
    },
    {
        "drug": "Levomepromazina",
        "aliases": ["neozine", "levozine"],
        "cat": "Antipsicótico Típico",
        "rec": "Evitar como sedativo/hipnótico.",
        "rat": "Hipotensão postural com risco de síncope, colapso hemodinâmico e impregnação extrapiramidal.",
        "tapering": "Retirada escalonada supervisionada."
    },
    {
        "drug": "Tioridazina",
        "aliases": ["melleril"],
        "cat": "Antipsicótico Típico",
        "rec": "Evitar estritamente.",
        "rat": "Prolongamento acentuado do intervalo QTc no ECG com risco de arritmias ventriculares letais (Torsades de Pointes).",
        "tapering": "Substituição imediata com controle por eletrocardiograma."
    },
    {
        "drug": "Olanzapina",
        "aliases": ["zyprexa", "neupride"],
        "cat": "Antipsicótico Atípico",
        "rec": "Evitar em demência ou insônia isolada.",
        "rat": "Ganho ponderal acentuado, descompensação metabólica do diabetes, sedação diurna e efeito anticolinérgico.",
        "tapering": "Desmame gradual ao longo de 2 a 4 semanas."
    },
    {
        "drug": "Quetiapina",
        "aliases": ["seroquel", "queropax", "quetros"],
        "cat": "Antipsicótico Atípico",
        "rec": "Evitar o uso rotineiro como indutor do sono.",
        "rat": "Hipotensão ortostática e tontura com alto índice de quedas sem ganho comprovado na arquitetura do sono.",
        "tapering": "Desmame: Titular dose até 12,5 mg antes da interrupção definitiva."
    },
    {
        "drug": "Risperidona",
        "aliases": ["risperdal", "riperidon", "zargus"],
        "cat": "Antipsicótico Atípico",
        "rec": "Evitar uso prolongado em demência.",
        "rat": "Sintomas extrapiramidais dose-dependentes (> 1,5 mg/dia) e aumento documentado de eventos isquêmicos cerebrais.",
        "tapering": "Limitar o tratamento agudo ao menor tempo possível (máximo 6 a 12 semanas)."
    },

    # --- Antidepressivos Tricíclicos e ISRS Anticolinérgico ---
    {
        "drug": "Amitriptilina",
        "aliases": ["tryptanol", "amytril", "trisomatol"],
        "cat": "Antidepressivo Tricíclico",
        "rec": "Evitar no idoso.",
        "rat": "Potente efeito anticolinérgico: hipotensão ortostática severa, constipação, retenção vesical e arritmias cardíacas.",
        "tapering": "Desmame: Redução gradual de 25 mg a cada 1-2 semanas. Se indicada para dor neuropática, preferir Duloxetina."
    },
    {
        "drug": "Nortriptilina",
        "aliases": ["pamelor"],
        "cat": "Antidepressivo Tricíclico",
        "rec": "Evitar no idoso.",
        "rat": "Sedação considerável, risco de hipotensão ortostática e bloqueio colinérgico em idosos frágeis.",
        "tapering": "Desmame progressivo em 2 a 3 semanas."
    },
    {
        "drug": "Clomipramina",
        "aliases": ["anafranil"],
        "cat": "Antidepressivo Tricíclico",
        "rec": "Evitar no idoso.",
        "rat": "Sedação profunda e elevado potencial pró-arrítmico cardíaco.",
        "tapering": "Descontinuação progressiva fracionada."
    },
    {
        "drug": "Imipramina",
        "aliases": ["tofranil", "depramina"],
        "cat": "Antidepressivo Tricíclico",
        "rec": "Evitar no idoso.",
        "rat": "Hipotensão postural marcante e risco substancial de quedas noturnas.",
        "tapering": "Desmame supervisionado escalonado."
    },
    {
        "drug": "Paroxetina",
        "aliases": ["aropax", "pondera", "benepax"],
        "cat": "ISRS com Ação Anticolinérgica",
        "rec": "Evitar no idoso.",
        "rat": "O mais anticolinérgico dos ISRS; causa sedação, disfunção cognitiva, boca seca e síndrome de descontinuação intensa.",
        "tapering": "Desmame muito lento; transicionar para Sertralina."
    },

    # --- Anti-inflamatórios Não Esteroidais (AINEs) ---
    {
        "drug": "Cetorolaco",
        "aliases": ["toradol", "deocil", "cetolac"],
        "cat": "AINE Potente",
        "rec": "Evitar estritamente no idoso (inclusive via sublingual).",
        "rat": "Maior incidência relativa de hemorragia gastrointestinal alta e insuficiência renal aguda oligúrica da classe.",
        "tapering": "Contraindicado em geriatria; suspender e aplicar analgesia multimodal segura (Dipirona + opioide se dor intensa)."
    },
    {
        "drug": "Piroxicam",
        "aliases": ["feldene", "piroxibras", "inflamene"],
        "cat": "AINE",
        "rec": "Evitar no idoso.",
        "rat": "Meia-vida terminal muito longa (~50h); risco desproporcional de sangramento digestivo e úlcera perfurada.",
        "tapering": "Suspensão mandatória em pacientes idosos."
    },
    {
        "drug": "Diclofenaco",
        "aliases": ["voltaren", "cataflam", "biofenac", "artren"],
        "cat": "AINE",
        "rec": "Evitar uso contínuo ou repetido.",
        "rat": "Nefrotoxicidade hemodinâmica por supressão de prostaglandinas vasodilatadoras, descompensação de HAS e sangramento.",
        "tapering": "Desprescrição: Interromper e substituir por Dipirona/Paracetamol; se imprescindível, associar IBP protetor."
    },
    {
        "drug": "Cetoprofeno",
        "aliases": ["proflam", "artrosil"],
        "cat": "AINE",
        "rec": "Evitar uso contínuo.",
        "rat": "Dano renal agudo, retenção volêmica e toxicidade ulcerosa gastroduodenal.",
        "tapering": "Substituição imediata por analgesia escalonada."
    },
    {
        "drug": "Ibuprofeno",
        "aliases": ["advil", "alivium", "ibupril"],
        "cat": "AINE",
        "rec": "Evitar uso crônico ou frequente.",
        "rat": "Lesão endotelial renal, retenção hidrossalina e neutralização da cardioproteção antiplaquetária do AAS.",
        "tapering": "Limitar o uso a casos agudos por no máximo 48h associado a proteção gástrica."
    },
    {
        "drug": "Meloxicam",
        "aliases": ["movatec", "meloxil", "inflatec"],
        "cat": "AINE",
        "rec": "Evitar uso contínuo.",
        "rat": "Perde seletividade COX-2 nas doses usuais; piora da função renal e elevação da pressão arterial.",
        "tapering": "Interrupção do tratamento crônico."
    },
    {
        "drug": "Naproxeno",
        "aliases": ["flanax", "naprosyn", "naxotec"],
        "cat": "AINE",
        "rec": "Evitar uso crônico sem IBP.",
        "rat": "Toxicidade gástrica expressiva e redução da filtração glomerular em idosos desidratados.",
        "tapering": "Suspender o uso rotineiro diário."
    },
    {
        "drug": "Indometacina",
        "aliases": ["indocid"],
        "cat": "AINE",
        "rec": "Evitar estritamente.",
        "rat": "Provoca cefaleia, confusão mental, toxicidade central além de severo dano renal agudo hemodinâmico.",
        "tapering": "Suspensão imediata."
    },

    # --- Gastrointestinais e Procinéticos ---
    {
        "drug": "Metoclopramida",
        "aliases": ["plasil", "placton", "nausedron"],
        "cat": "Antagonista Dopaminérgico / Procinético",
        "rec": "Evitar exceto em gastroparesia documentada (máx 12 semanas).",
        "rat": "Bloqueio D2 no estriado: desencadeia discinesia tardia (frequentemente irreversível) e parkinsonismo medicamentoso.",
        "tapering": "Substituição: Utilizar Ondansetrona ou Domperidona (com vigilância do intervalo QTc)."
    },
    {
        "drug": "Omeprazol",
        "aliases": ["losec", "pepazol", "gasec"],
        "cat": "Inibidor da Bomba de Prótons",
        "rec": "Evitar uso contínuo > 8 semanas sem indicação clínica formal.",
        "rat": "Uso crônico correlacionado a infecção por Clostridioides difficile, hipomagnesemia e perda de densidade óssea.",
        "tapering": "Desmame Gradual: Reduzir para dose padrão por 2 semanas, depois dias alternados por 2 semanas para evitar hipersecreção rebote."
    },
    {
        "drug": "Esomeprazol",
        "aliases": ["nexium", "esomex", "ezopen"],
        "cat": "Inibidor da Bomba de Prótons",
        "rec": "Evitar uso contínuo > 8 semanas sem indicação documentada.",
        "rat": "Redução da absorção de micronutrientes (Vitamina B12, ferro, magnésio) e nefrite intersticial.",
        "tapering": "Desmame escalonado em 4 semanas."
    },
    {
        "drug": "Pantoprazol",
        "aliases": ["pantozol", "pantocal", "adipept"],
        "cat": "Inibidor da Bomba de Prótons",
        "rec": "Evitar uso contínuo > 8 semanas sem indicação formal.",
        "rat": "Aumento do risco de fraturas de quadril e pneumonias microaspirativas comunitárias.",
        "tapering": "Desmame progressivo fracionado."
    },
    {
        "drug": "Lansoprazol",
        "aliases": ["ogastro", "prazol", "lanz"],
        "cat": "Inibidor da Bomba de Prótons",
        "rec": "Evitar uso contínuo desnecessário.",
        "rat": "Supercrescimento bacteriano no intestino delgado e risco aumentado de hipomagnesemia.",
        "tapering": "Descontinuação progressiva."
    },
    {
        "drug": "Cimetidina",
        "aliases": ["tagamet", "cimecord"],
        "cat": "Antagonista H2",
        "rec": "Evitar no idoso.",
        "rat": "Inibidor potente de enzimas do citocromo P450; causa confusão mental, delirium agudo e ginecomastia.",
        "tapering": "Substituir por Famotidina (com dose corrigida pela função renal)."
    },

    # --- Cardiovasculares, Hipoglicemiantes e Opioides ---
    {
        "drug": "Clonidina",
        "aliases": ["atensina", "clonidin"],
        "cat": "Anti-hipertensivo Alfa-2 Central",
        "rec": "Evitar como monoterapia anti-hipertensiva.",
        "rat": "Risco de bradicardia sintomática, síncope, hipotensão ortostática e efeito rebote pressórico agudo se omitida dose.",
        "tapering": "Desmame Obrigatório: Retirada lenta ao longo de 2 a 4 semanas. Nunca suspender abruptamente."
    },
    {
        "drug": "Doxazosina",
        "aliases": ["carduran", "duomo", "unoprost"],
        "cat": "Alfa-1 Bloqueador",
        "rec": "Evitar para tratamento exclusivo de hipertensão arterial.",
        "rat": "Hipotensão postural intensa, síncope e quedas graves, principalmente após as primeiras doses.",
        "tapering": "Se indicada por HPB, administrar rigorosamente ao deitar."
    },
    {
        "drug": "Prazosina",
        "aliases": ["minipress"],
        "cat": "Alfa-1 Bloqueador",
        "rec": "Evitar para hipertensão arterial.",
        "rat": "Elevado índice de hipotensão ortostática severa e síncope motora.",
        "tapering": "Transicionar para anti-hipertensivo de primeira linha (IECA/BRA ou Anlodipino)."
    },
    {
        "drug": "Amiodarona",
        "aliases": ["ancoron", "atlansil", "miodaron"],
        "cat": "Antiarrítmico Classe III",
        "rec": "Evitar como primeira escolha para controle de frequência na FA.",
        "rat": "Toxicidade cumulativa multiorgânica: fibrose pulmonar, tireoidopatias e prolongamento do intervalo QTc.",
        "tapering": "Reservar para controle de ritmo em IC com FE reduzida ou refratariedade."
    },
    {
        "drug": "Digoxina",
        "aliases": ["digoxina", "digopress"],
        "cat": "Glicosídeo Cardíaco",
        "rec": "Evitar doses > 0,125 mg/dia como primeira linha.",
        "rat": "Janela terapêutica estreita; depuração renal reduzida induz bloqueios cardíacos e arritmias digitálicas letais.",
        "tapering": "Ajuste: Titular para dose máxima de 0,125 mg/dia ou suspender; monitorar digoxinemia (alvo 0,5 a 0,9 ng/mL)."
    },
    {
        "drug": "Glibenclamida",
        "aliases": ["daonil", "gliconil", "glisulin"],
        "cat": "Sulfonilureia de Longa Ação",
        "rec": "Evitar estritamente no idoso.",
        "rat": "Metabólitos ativos de eliminação lenta; induz hipoglicemias profundas, duradouras e com sequelas neurológicas graves.",
        "tapering": "Substituição Imediata: Transicionar para Gliclazida MR ou inibidores de SGLT2/DPP-4."
    },
    {
        "drug": "Glimepirida",
        "aliases": ["amaryl", "bioglic", "glicimax"],
        "cat": "Sulfonilureia",
        "rec": "Evitar em idosos frágeis ou com disfunção renal.",
        "rat": "Risco elevado de hipoglicemias matinais e neuroglicopenia sustentada.",
        "tapering": "Transição para opções com menor risco de hipoglicemia."
    },
    {
        "drug": "Meperidina",
        "aliases": ["dolantina", "dolosal"],
        "cat": "Opioide",
        "rec": "Evitar estritamente no idoso.",
        "rat": "Metabolizado em normeperidina, composto neurotóxico acumulativo que desencadeia tremores, mioclonias e convulsões.",
        "tapering": "Contraindicado em geriatria; substituir por Morfina ou Fentanil sob titulação analgésica."
    }
]

# =========================================================================
# 2. TABELA 6: FÁRMACOS COM AJUSTE RENAL CRÍTICO (CONDICIONAL AO ClCr)
# =========================================================================
TABLE_6_RENAL = [
    {
        "drug": "Pregabalina",
        "aliases": ["lyrica", "prebictal", "insit"],
        "cat": "Gabapentinoide",
        "cutoff_clcr": 60.0,
        "rec": "Ajustar dose rigorosamente conforme o ClCr.",
        "rat": "Excreção renal quase total; acúmulo causa sedação excessiva, edema periférico, ataxia e quedas.",
        "guideline": "ClCr 30-60: máx 150 mg/dia; ClCr 15-30: máx 75 mg/dia; ClCr < 15: máx 25-50 mg/dia."
    },
    {
        "drug": "Gabapentina",
        "aliases": ["neurontin", "progresse", "gamibetal"],
        "cat": "Gabapentinoide",
        "cutoff_clcr": 60.0,
        "rec": "Ajustar posologia para a função renal.",
        "rat": "Eliminação renal exclusiva; hiperdosagem relativa induz letargia profunda e encefalopatia.",
        "guideline": "ClCr 30-59: máx 700 mg/dia; ClCr 15-29: máx 300 mg/dia; ClCr < 15: máx 300 mg a cada 48h."
    },
    {
        "drug": "Espironolactona",
        "aliases": ["aldactone", "spiroctan", "diurisa"],
        "cat": "Antagonista da Aldosterona",
        "cutoff_clcr": 30.0,
        "rec": "Evitar se ClCr < 30 mL/min ou potássio sérico > 5,0 mEq/L.",
        "rat": "Risco crítico de hipercalemia refratária com arritmias graves e parada cardíaca.",
        "guideline": "Suspender se ClCr < 30 mL/min e dosar eletrólitos de urgência."
    },
    {
        "drug": "Nitrofurantoína",
        "aliases": ["macrodantina", "uro-furan"],
        "cat": "Antibacteriano Urinário",
        "cutoff_clcr": 30.0,
        "rec": "Evitar se ClCr < 30 mL/min.",
        "rat": "Filtração insuficiente para atingir concentração terapêutica na urina, somada a risco aumentado de neuropatia periférica.",
        "guideline": "Substituir por Fosfomicina ou Cefalosporina oral para infecção urinária."
    },
    {
        "drug": "Metformina",
        "aliases": ["glifage", "dimefor", "glicomet"],
        "cat": "Biguanida",
        "cutoff_clcr": 30.0,
        "rec": "Reduzir dose se ClCr 30-45; contraindicada se ClCr < 30 mL/min.",
        "rat": "Acúmulo corporal decorrente de filtração deficiente eleva risco de acidose láctica potencialmente fatal.",
        "guideline": "Suspender em vigência de instabilidade hemodinâmica, choque ou insuficiência renal aguda."
    },
    {
        "drug": "Sulfametoxazol + Trimetoprima",
        "aliases": ["bactrim", "infectrin", "bac-sulfitrin"],
        "cat": "Antibacteriano",
        "cutoff_clcr": 30.0,
        "rec": "Reduzir 50% da dose se ClCr 15-30; evitar se ClCr < 15 mL/min.",
        "rat": "Bloqueia a secreção tubular de creatinina gerando falsa elevação laboratorial e induz hipercalemia severa.",
        "guideline": "Monitorar potássio sérico durante todo o período de tratamento."
    }
]

# =========================================================================
# 3. TABELA 3: CRUZAMENTO FÁRMACO-DOENÇA / CONDIÇÃO CLÍNICA
# =========================================================================
TABLE_3_DISEASE_DRUG = [
    {
        "conditions": ["insuficiência cardíaca", "insuficiencia cardiaca", "ic"],
        "drugs": ["diclofenaco", "ibuprofeno", "cetoprofeno", "meloxicam", "piroxicam", "cetorolaco", "naproxeno", "voltaren", "cataflam"],
        "title": "AINE na Insuficiência Cardíaca",
        "rec": "Evitar estritamente.",
        "rat": "A inibição de prostaglandinas renais induz retenção hidrossalina severa e descompensação hemodinâmica aguda da IC."
    },
    {
        "conditions": ["insuficiência cardíaca", "insuficiencia cardiaca", "ic"],
        "drugs": ["diltiazem", "verapamil", "cardizem", "dilacoron"],
        "title": "Bloqueador de Canal de Cálcio Não-Di-hidropiridínico na IC",
        "rec": "Evitar em IC com Fração de Ejeção Reduzida.",
        "rat": "Efeito inotrópico negativo direto precipita choque cardiogênico ou piora funcional aguda."
    },
    {
        "conditions": ["doença de parkinson", "doenca de parkinson", "parkinson"],
        "drugs": ["metoclopramida", "plasil", "haloperidol", "haldol", "clorpromazina", "levomepromazina", "risperidona"],
        "title": "Antagonista Dopaminérgico na Doença de Parkinson",
        "rec": "Evitar estritamente.",
        "rat": "Bloqueio de receptores D2 estriatais agrava bradicinesia, tremores e rigidez muscular parkinsoniana."
    },
    {
        "conditions": ["demência", "demencia", "alzheimer", "déficit cognitivo"],
        "drugs": ["amitriptilina", "biperideno", "tri-hexifenidil", "dexclorfeniramina", "prometazina", "oxibutinina", "difenidramina", "polaramine", "artane", "akineton"],
        "title": "Anticolinérgico em Paciente com Demência",
        "rec": "Evitar no idoso com déficit cognitivo.",
        "rat": "Bloqueio colinérgico central precipita agitação aguda, alucinações e acelera a perda cognitiva."
    },
    {
        "conditions": ["doença renal crônica", "doenca renal cronica", "drc", "insuficiência renal"],
        "drugs": ["diclofenaco", "ibuprofeno", "cetoprofeno", "meloxicam", "piroxicam", "cetorolaco", "naproxeno", "voltaren", "cataflam"],
        "title": "AINE na Doença Renal Crônica",
        "rec": "Evitar em DRC estágios III a V.",
        "rat": "Provoca vasoconstrição renal aguda sustentada, acelerando perda funcional e necessidade de diálise."
    },
    {
        "conditions": ["queda", "quedas", "historico de quedas", "risco de queda"],
        "drugs": ["diazepam", "clonazepam", "alprazolam", "lorazepam", "zolpidem", "quetiapina", "haloperidol", "amitriptilina", "ciclobenzaprina", "carisoprodol", "rivotril", "stilnox", "torsilax"],
        "title": "Psicotrópico / Sedativo em Idoso com Risco Alto de Queda",
        "rec": "Evitar ou desprescrever com máxima urgência.",
        "rat": "Comprometimento dos reflexos vestibulares e proprioceptivos; alta correlação com traumatismo cranioencefálico e fratura de colo de fêmur."
    }
]

# =========================================================================
# 4. TABELA 5: INTERAÇÕES MEDICAMENTOSAS DUPLAS CRÍTICAS
# =========================================================================
TABLE_5_INTERACTIONS = [
    {
        "pair": (
            ["morfina", "tramadol", "oxicodona", "fentanil", "dimorf", "tramal", "codeina"],
            ["diazepam", "clonazepam", "alprazolam", "lorazepam", "midazolam", "rivotril", "valium", "frontal", "dormonid", "zolpidem", "stilnox"]
        ),
        "alert": "Associação Opioide + Benzodiazepínico / Hipnótico",
        "rec": "Evitar prescrição concomitante.",
        "rat": "Sinergismo depressor do SNC e do centro respiratório bulbar; risco acentuado de parada respiratória e óbito."
    },
    {
        "pair": (
            ["diclofenaco", "ibuprofeno", "cetoprofeno", "meloxicam", "piroxicam", "cetorolaco", "naproxeno", "voltaren", "cataflam"],
            ["varfarina", "marevan", "rivaroxabana", "xarelto", "apixabana", "eliquis", "enoxaparina", "clexane", "dabigatrana"]
        ),
        "alert": "Associação AINE + Anticoagulante",
        "rec": "Evitar estritamente.",
        "rat": "A inibição da agregação plaquetária somada à ulceração gastroduodenal do AINE na presença de anticoagulação sistêmica causa hemorragia digestiva maciça."
    }
]
