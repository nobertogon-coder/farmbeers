# -*- coding: utf-8 -*-
"""
BASE FARMACOLÓGICA E REGRAS CLÍNICAS - CRITÉRIOS AGS BEERS 2023
Curadoria para o ambiente hospitalar brasileiro (UPI / UTI).
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
        "rat": "Meia-vida excessivamente longa (>48-100h); acúmulo sedativo, ataxia, lentidão psicomotora e alto risco de quedas e fraturas.",
        "tapering": "Desmame Gradual: Reduzir a dose em 25% a cada 1-2 semanas sob monitoramento de abstinência e insônia rebote."
    },
    {
        "drug": "Clonazepam",
        "aliases": ["rivotril", "navotrax", "clonotril"],
        "cat": "Benzodiazepínico",
        "rec": "Evitar no idoso.",
        "rat": "Lentificação psicomotora intensa, tolerância e elevado índice de fratura de colo de fêmur.",
        "tapering": "Desmame Gradual: Reduzir de 0,25 mg a 0,5 mg a cada 10 a 14 dias. Não interromper abruptamente."
    },
    {
        "drug": "Alprazolam",
        "aliases": ["frontal", "tranquinal", "apraz"],
        "cat": "Benzodiazepínico",
        "rec": "Evitar no idoso.",
        "rat": "Pico plasmático rápido com alto índice de dependência e ansiedade/agitação de rebote interdose.",
        "tapering": "Desmame: Redução gradual de 25% da dose a cada 1 ou 2 semanas."
    },
    {
        "drug": "Bromazepam",
        "aliases": ["lexotan", "somalium", "deptran"],
        "cat": "Benzodiazepínico",
        "rec": "Evitar no idoso.",
        "rat": "Sedação residual diurna, perda de coordenação motora e risco de broncoaspiração.",
        "tapering": "Desmame escalonado ao longo de 2 a 4 semanas."
    },
    {
        "drug": "Lorazepam",
        "aliases": ["lorax", "ansirax", "lorium"],
        "cat": "Benzodiazepínico",
        "rec": "Evitar no idoso.",
        "rat": "Apesar de metabolização por glicuronidação, induz alta sensibilidade central, delirium e quedas.",
        "tapering": "Desmame supervisionado com redução progressiva a cada 7-10 dias."
    },
    {
        "drug": "Midazolam",
        "aliases": ["dormonid"],
        "cat": "Benzodiazepínico",
        "rec": "Evitar uso oral ambulatorial/enfermaria como indutor de sono.",
        "rat": "Amnésia anterógrada rápida e sedação paradoxal aguda com risco respiratório no idoso.",
        "tapering": "Restringir estritamente a sedação para procedimentos e ambiente de UTI sob ventilação."
    },
    {
        "drug": "Clobazam",
        "aliases": ["frisium", "urbanil"],
        "cat": "Benzodiazepínico",
        "rec": "Evitar exceto em epilepsia refratária com acompanhamento neurológico.",
        "rat": "Sedação prolongada, perda de reflexos protetores e instabilidade na marcha.",
        "tapering": "Descontinuação progressiva lenta se em uso crônico."
    },
    {
        "drug": "Flurazepam",
        "aliases": ["dalmadorm"],
        "cat": "Benzodiazepínico",
        "rec": "Evitar estritamente.",
        "rat": "Metabólito ativo com meia-vida superior a 100 horas; risco cumulativo extremo de sonolência diurna contínua.",
        "tapering": "Descontinuação programada."
    },
    {
        "drug": "Nitrazepam",
        "aliases": ["mogadon", "nitrapan"],
        "cat": "Benzodiazepínico",
        "rec": "Evitar.",
        "rat": "Eliminação lenta com acúmulo sedativo, ataxia e confusão mental.",
        "tapering": "Desmame progressivo semanal."
    },
    {
        "drug": "Zolpidem",
        "aliases": ["stilnox", "patz", "noctaliv"],
        "cat": "Droga Z / Hipnótico",
        "rec": "Evitar no idoso.",
        "rat": "Gera comportamentos automáticos complexos do sono, perda de equilíbrio e traumatismos ósseos idênticos aos benzodiazepínicos.",
        "tapering": "Desmame: Reduzir para dose de 5 mg por 7 dias, depois uso em noites alternadas antes da suspensão total."
    },
    {
        "drug": "Zopiclona",
        "aliases": ["imovane"],
        "cat": "Droga Z / Hipnótico",
        "rec": "Evitar no idoso.",
        "rat": "Prejuízo motor matinal, disgeusia persistente e confusão mental noturna.",
        "tapering": "Redução progressiva ao longo de 7 a 10 dias."
    },

    # --- Relaxantes Musculares e Antiespasmódicos ---
    {
        "drug": "Carisoprodol",
        "aliases": ["torsilax", "dorflex", "miosan dc", "trilax"],
        "cat": "Relaxante Muscular",
        "rec": "Evitar estritamente.",
        "rat": "Biotransformado em meprobamato (ansiolítico de alta dependência química); sedação severa e quedas.",
        "tapering": "Desprescrição: Interrupção em 3 a 5 dias para prevenir sintomas de abstinência adrenérgica."
    },
    {
        "drug": "Ciclobenzaprina",
        "aliases": ["miosan", "musculare", "mirtax"],
        "cat": "Relaxante Muscular",
        "rec": "Evitar no idoso.",
        "rat": "Molécula tricíclica com alta carga anticolinérgica; causa retenção urinária, constipação, sonolência e arritmias.",
        "tapering": "Desprescrição: Interromper e indicar Dipirona ou Paracetamol, associados a calor local e fisioterapia."
    },
    {
        "drug": "Orfenadrina",
        "aliases": ["doricin", "sedilax"],
        "cat": "Relaxante Muscular / Anticolinérgico",
        "rec": "Evitar no idoso.",
        "rat": "Forte bloqueio muscarínico: taquicardia reflexa, retenção urinária aguda e precipitação de glaucoma agudo.",
        "tapering": "Substituição imediata por analgésico isolado."
    },
    {
        "drug": "Tizanidina",
        "aliases": ["sirdalud"],
        "cat": "Agonista Alfa-2 Central / Relaxante",
        "rec": "Evitar em idosos frágeis.",
        "rat": "Hipotensão postural acentuada, bradicardia e sedação profunda.",
        "tapering": "Desmame gradual para prevenir hipertensão de rebote."
    },

    # --- Anti-histamínicos de 1ª Geração e Anticolinérgicos ---
    {
        "drug": "Dexclorfeniramina",
        "aliases": ["polaramine", "histamin", "polaren", "coristina"],
        "cat": "Anti-histamínico 1ª Geração",
        "rec": "Evitar no idoso.",
        "rat": "Ação anticolinérgica acentuada: boca seca incapacitante, constipação severa, delírio e retenção de urina.",
        "tapering": "Substituição: Trocar por anti-histamínico de 2ª geração (Loratadina, Cetirizina ou Fexofenadina)."
    },
    {
        "drug": "Prometazina",
        "aliases": ["fenergan", "prometazol", "profergan"],
        "cat": "Anti-histamínico / Fenotiazina",
        "rec": "Evitar no idoso.",
        "rat": "Sedação profunda, hipotensão ortostática pronunciada e risco de sintomas extrapiramidais (acatisia).",
        "tapering": "Se utilizada para vômitos/náuseas, substituir por Ondansetrona."
    },
    {
        "drug": "Dimenidrinato",
        "aliases": ["dramin", "dramavit", "dimenidrin"],
        "cat": "Anti-histamínico / Antivertiginoso",
        "rec": "Evitar uso contínuo.",
        "rat": "Sedação profunda e bloqueio colinérgico que acelera declínio cognitivo e anula medicações anticolinesterásicas.",
        "tapering": "Restringir a crises vertiginosas agudas (máximo 48 a 72 horas)."
    },
    {
        "drug": "Hidroxizina",
        "aliases": ["hixizine", "prurizin"],
        "cat": "Anti-histamínico 1ª Geração",
        "rec": "Evitar no idoso.",
        "rat": "Sonolência residual diurna e risco de prolongamento do intervalo QTc no ECG.",
        "tapering": "Substituir por hidratantes de barreira e anti-histamínicos não sedativos."
    },
    {
        "drug": "Difenidramina",
        "aliases": ["benadryl", "difenidrin"],
        "cat": "Anti-histamínico 1ª Geração",
        "rec": "Evitar como hipnótico de rotina.",
        "rat": "Alta carga anticolinérgica e sedação diurna residual sem benefício no padrão do sono.",
        "tapering": "Suspensão direta; reforçar higiene do sono."
    },
    {
        "drug": "Ciproheptadina",
        "aliases": ["periactin", "apevitin", "cobavital"],
        "cat": "Anti-histamínico / Orexígeno",
        "rec": "Evitar estritamente para estímulo de apetite.",
        "rat": "Sedação acentuada, confusão mental e bloqueio colinérgico sem ganho de massa magra de qualidade.",
        "tapering": "Suspensão e abordagem por suplementos hipercalóricos/hiperproteicos orientados."
    },
    {
        "drug": "Meclizina",
        "aliases": ["meclin"],
        "cat": "Anti-histamínico / Antivertiginoso",
        "rec": "Evitar uso profilático contínuo.",
        "rat": "Sedação, tontura paradoxal e retenção urinária no paciente geriátrico.",
        "tapering": "Limitar a episódios agudos e priorizar fisioterapia vestibular."
    },
    {
        "drug": "Biperideno",
        "aliases": ["akineton", "cinetol"],
        "cat": "Anticolinérgico Central",
        "rec": "Evitar no idoso.",
        "rat": "Altíssimo potencial de desencadear alucinações visuais, delírio agudo e constipação obstrutiva grave.",
        "tapering": "Desmame lento e monitorado por neurologista."
    },
    {
        "drug": "Tri-hexifenidil",
        "aliases": ["artane"],
        "cat": "Anticolinérgico Central",
        "rec": "Evitar no idoso.",
        "rat": "Carga anticolinérgica extrema; deterioração cognitiva aguda e retenção vesical.",
        "tapering": "Desmame gradual para não desencadear crise de rebote motor."
    },
    {
        "drug": "Oxibutinina",
        "aliases": ["retomic", "incontinol"],
        "cat": "Antimuscarínico Urinário",
        "rec": "Evitar formulações de liberação imediata.",
        "rat": "Penetração substancial no SNC; precipita alucinações, perda de memória recente e confusão mental.",
        "tapering": "Avaliar beta-3 agonista (Mirabegrona) ou fisioterapia do assoalho pélvico."
    },
    {
        "drug": "Tolterodina",
        "aliases": ["detrusitol"],
        "cat": "Antimuscarínico Urinário",
        "rec": "Evitar se demência ou comprometimento cognitivo.",
        "rat": "Acentua o declínio cognitivo e induz boca seca incapacitante e xerostomia.",
        "tapering": "Titular para menor dose efetiva ou descontinuar."
    },

    # --- Antipsicóticos (Risco de AVC e Mortalidade em Idosos) ---
    {
        "drug": "Haloperidol",
        "aliases": ["haldol"],
        "cat": "Antipsicótico Típico",
        "rec": "Evitar para controle rotineiro de agitação em demência.",
        "rat": "Aumento comprovado de mortalidade e AVC em demência; elevado índice de parkinsonismo e discinesia tardia.",
        "tapering": "Desmame: Redução progressiva de 25% a 50% por semana após cessar a causa aguda do delirium."
    },
    {
        "drug": "Clorpromazina",
        "aliases": ["amplictil", "clorpromaz"],
        "cat": "Antipsicótico Típico",
        "rec": "Evitar.",
        "rat": "Hipotensão ortostática violenta, sedação profunda e efeitos anticolinérgicos marcados.",
        "tapering": "Desmame progressivo sob monitoramento pressórico."
    },
    {
        "drug": "Levomepromazina",
        "aliases": ["neozine", "levozine"],
        "cat": "Antipsicótico Típico",
        "rec": "Evitar como sedativo/hipnótico.",
        "rat": "Hipotensão postural com colapso hemodinâmico, alto risco de quedas e impregnação motora.",
        "tapering": "Retirada escalonada."
    },
    {
        "drug": "Tioridazina",
        "aliases": ["melleril"],
        "cat": "Antipsicótico Típico",
        "rec": "Evitar estritamente.",
        "rat": "Prolongamento perigoso do intervalo QTc com risco de arritmias ventriculares fatais (Torsades de Pointes).",
        "tapering": "Substituição imediata com controle por eletrocardiograma."
    },
    {
        "drug": "Olanzapina",
        "aliases": ["zyprexa", "neupride"],
        "cat": "Antipsicótico Atípico",
        "rec": "Evitar em demência ou insônia isolada.",
        "rat": "Ganho ponderal acentuado, descompensação glicêmica, sedação diurna e efeito anticolinérgico.",
        "tapering": "Desmame gradual ao longo de 2 a 4 semanas."
    },
    {
        "drug": "Quetiapina",
        "aliases": ["seroquel", "queropax", "quetros"],
        "cat": "Antipsicótico Atípico",
        "rec": "Evitar o uso rotineiro como indutor do sono.",
        "rat": "Hipotensão ortostática e tontura matinal com elevado índice de quedas sem melhoria na qualidade do sono.",
        "tapering": "Desmame: Titular dose até 12,5 mg antes da interrupção definitiva."
    },
    {
        "drug": "Risperidona",
        "aliases": ["risperdal", "riperidon", "zargus"],
        "cat": "Antipsicótico Atípico",
        "rec": "Evitar uso prolongado em demência.",
        "rat": "Sintomas extrapiramidais em doses > 1,5 mg/dia e aumento documentado de eventos isquêmicos cerebrais.",
        "tapering": "Limitar o tratamento agudo ao menor tempo possível (máximo 6 a 12 semanas)."
    },

    # --- Antidepressivos Tricíclicos ---
    {
        "drug": "Amitriptilina",
        "aliases": ["tryptanol", "amytril", "trisomatol"],
        "cat": "Antidepressivo Tricíclico",
        "rec": "Evitar no idoso.",
        "rat": "Efeito anticolinérgico potente: hipotensão postural, constipação grave, retenção vesical e arritmias cardíacas.",
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
        "tapering": "Desmame supervisionado."
    },
    {
        "drug": "Paroxetina",
        "aliases": ["aropax", "pondera", "benepax"],
        "cat": "ISRS com Ação Anticolinérgica",
        "rec": "Evitar no idoso.",
        "rat": "O mais anticolinérgico dos inibidores de recaptação de serotonina; causa sedação, disfunção cognitiva e boca seca.",
        "tapering": "Desmame muito lento (alto risco de sintomas de descontinuação); transicionar para Sertralina."
    },

    # --- AINEs Tradicionais (Toxicidade Renal, Hemorrágica e Cardiovascular) ---
    {
        "drug": "Cetorolaco",
        "aliases": ["toradol", "deocil", "cetolac"],
        "cat": "AINE Potente",
        "rec": "Evitar estritamente no idoso (inclusive via sublingual).",
        "rat": "Maior incidência relativa de hemorragia gastrointestinal alta e insuficiência renal aguda oligúrica da classe.",
        "tapering": "Contraindicado em geriatria; suspender e aplicar analgesia multimodal segura (Dipirona + opioide se necessário)."
    },
    {
        "drug": "Piroxicam",
        "aliases": ["feldene", "piroxibras", "inflamene"],
        "cat": "AINE",
        "rec": "Evitar no idoso.",
        "rat": "Meia-vida terminal muito prolongada (~50h); risco desproporcional de sangramento digestivo e úlcera perfurada.",
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
        "rat": "Lesão endotelial renal, retenção hidrossalina e neutralização do efeito antiplaquetário cardioprotetor do AAS.",
        "tapering": "Limitar o uso a casos agudos por no máximo 48h associado a proteção gástrica."
    },
    {
        "drug": "Meloxicam",
        "aliases": ["movatec", "meloxil", "inflatec"],
        "cat": "AINE",
        "rec": "Evitar uso contínuo.",
        "rat": "Perde seletividade COX-2 nas doses terapêuticas habituais; piora função renal e eleva pressão arterial.",
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
        "rat": "Provoca cefaleia, confusão mental, psicose tóxica além de severo dano renal agudo.",
        "tapering": "Suspensão imediata."
    },

    # --- Gastrointestinais e Procinéticos ---
    {
        "drug": "Metoclopramida",
        "aliases": ["plasil", "placton", "nausedron"],
        "cat": "Antagonista Dopaminérgico / Procinético",
        "rec": "Evitar exceto em gastroparesia documentada (máx 12 semanas).",
        "rat": "Bloqueio D2 no estriado: desencadeia discinesia tardia (frequentemente irreversível) e parkinsonismo agudo em idosos.",
        "tapering": "Substituição: Utilizar Ondansetrona ou Domperidona (com monitoramento do intervalo QTc)."
    },
    {
        "drug": "Omeprazol",
        "aliases": ["losec", "pepazol", "gasec"],
        "cat": "Inibidor da Bomba de Prótons",
        "rec": "Evitar uso contínuo > 8 semanas sem indicação documentada.",
        "rat": "Uso crônico associado a infecção entérica por Clostridioides difficile, hipomagnesemia e perda de densidade mineral óssea.",
        "tapering": "Desmame Gradual: Reduzir para dose padrão diária por 2 semanas, depois em dias alternados por 2 semanas para evitar hipersecreção ácida rebote."
    },
    {
        "drug": "Esomeprazol",
        "aliases": ["nexium", "esomex", "ezopen"],
        "cat": "Inibidor da Bomba de Prótons",
        "rec": "Evitar uso contínuo > 8 semanas sem indicação clínica formal.",
        "rat": "Redução da absorção de micronutrientes (Vitamina B12, ferro, magnésio) e nefrite intersticial.",
        "tapering": "Desmame escalonado em 4 semanas."
    },
    {
        "drug": "Pantoprazol",
        "aliases": ["pantozol", "pantocal", "adipept"],
        "cat": "Inibidor da Bomba de Prótons",
        "rec": "Evitar uso contínuo > 8 semanas sem indicação formal.",
        "rat": "Aumento do risco de fraturas de quadril e pneumonias microaspirativas comunitárias.",
        "tapering": "Desmame fracionado progressivo."
    },
    {
        "drug": "Lansoprazol",
        "aliases": ["ogastro", "prazol", "lanz"],
        "cat": "Inibidor da Bomba de Prótons",
        "rec": "Evitar uso contínuo desnecessário.",
        "rat": "Supercrescimento bacteriano no intestino delgado e hipomagnesemia.",
        "tapering": "Descontinuação progressiva."
    },
    {
        "drug": "Cimetidina",
        "aliases": ["tagamet", "cimecord"],
        "cat": "Antagonista H2",
        "rec": "Evitar no idoso.",
        "rat": "Inibidor potente de múltiplas isoenzimas do citocromo P450; causa delírio agudo, confusão e ginecomastia.",
        "tapering": "Substituir por Famotidina (com dose corrigida pela função renal)."
    },

    # --- Cardiovasculares e Hipoglicemiantes Críticos ---
    {
        "drug": "Clonidina",
        "aliases": ["atensina", "clonidin"],
        "cat": "Anti-hipertensivo Alfa-2 Central",
        "rec": "Evitar como monoterapia anti-hipertensiva.",
        "rat": "Risco acentuado de bradicardia sintomática, síncope, hipotensão ortostática e efeito rebote pressórico agudo se omitida dose.",
        "tapering": "Desmame Obrigatório: Retirada lenta e monitorada ao longo de 2 a 4 semanas. Nunca suspender abruptamente."
    },
    {
        "drug": "Doxazosina",
        "aliases": ["carduran", "duomo", "unoprost"],
        "cat": "Alfa-1 Bloqueador",
        "rec": "Evitar para tratamento exclusivo de hipertensão arterial.",
        "rat": "Hipotensão postural de primeira dose com colapso circulatório, vertigem e quedas graves.",
        "tapering": "Se utilizada para hiperplasia prostática benigna, administrar rigorosamente ao deitar."
    },
    {
        "drug": "Prazosina",
        "aliases": ["minipress"],
        "cat": "Alfa-1 Bloqueador",
        "rec": "Evitar para hipertensão arterial.",
        "rat": "Elevado índice de hipotensão ortostática severa e síncope.",
        "tapering": "Transicionar para anti-hipertensivo de primeira linha (IECA/BRA ou Anlodipino)."
    },
    {
        "drug": "Amiodarona",
        "aliases": ["ancoron", "atlansil", "miodaron"],
        "cat": "Antiarrítmico Classe III",
        "rec": "Evitar como primeira escolha para controle de frequência na fibrilação atrial.",
        "rat": "Toxicidade cumulativa multiorgânica: fibrose pulmonar, hipo/hipertireoidismo grave e prolongamento do intervalo QTc.",
        "tapering": "Reservar para controle de ritmo em IC com fração de ejeção reduzida ou se outras opções falharem."
    },
    {
        "drug": "Digoxina",
        "aliases": ["digoxina", "digopress"],
        "cat": "Glicosídeo Cardíaco",
        "rec": "Evitar doses > 0,125 mg/dia como primeira linha.",
        "rat": "Janela terapêutica estreita; o declínio fisiológico da filtração renal resulta em bloqueios AV e arritmias digitálicas fatais.",
        "tapering": "Ajuste Posológico: Titular para dose máxima de 0,125 mg/dia ou suspender; monitorar digoxinemia (alvo 0,5 a 0,9 ng/mL)."
    },
    {
        "drug": "Glibenclamida",
        "aliases": ["daonil", "gliconil", "glisulin"],
        "cat": "Sulfonilureia de Longa Ação",
        "rec": "Evitar estritamente no idoso.",
        "rat": "Metabólitos ativos de eliminação lenta; induz episódios graves e prolongados de hipoglicemia com dano encefálico irreversível.",
        "tapering": "Substituição Imediata: Transicionar para Gliclazida MR ou agentes incretínicos sob vigilância glicêmica."
    },
    {
        "drug": "Glimepirida",
        "aliases": ["amaryl", "bioglic", "glicimax"],
        "cat": "Sulfonilureia",
        "rec": "Evitar em idosos frágeis ou com disfunção renal.",
        "rat": "Risco substancial de hipoglicemias matinais e neuroglicopenia sustentada.",
        "tapering": "Transição para opções com menor risco de hipoglicemia (ex.: Gliclazida ou inibidores de SGLT2/DPP-4)."
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
# 2. TABELA 6: FÁRMACOS COM AJUSTE RENAL CRÍTICO (CONDICIONAL)
# Disparam alerta exclusivamente se ClCr < valor de corte
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
        "rat": "Filtração insuficiente para atingir concentração terapêutica na urina somada a risco aumentado de neuropatia periférica.",
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
# Dispara alerta se o medicamento e a comorbidade estiverem associados
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
        "rat": "Efeito inotrópico negativo direto precipita choque cardiogênico ou piora da classe funcional da IC."
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
        "rec": "Evitar no idoso demenciado.",
        "rat": "Bloqueio colinérgico central precipita agitação aguda, alucinações e acelera a perda cognitiva."
    },
    {
        "conditions": ["doença renal crônica", "doenca renal cronica", "drc", "insuficiência renal"],
        "drugs": ["diclofenaco", "ibuprofeno", "cetoprofeno", "meloxicam", "piroxicam", "cetorolaco", "naproxeno", "voltaren", "cataflam"],
        "title": "AINE na Doença Renal Crônica",
        "rec": "Evitar em DRC estágios III a V.",
        "rat": "Provoca vasoconstrição renal aguda sustentada, acelerando a necessidade de diálise."
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