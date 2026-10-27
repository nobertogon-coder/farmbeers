import re
import unicodedata

# =====================================================================
# 1. DICIONÁRIO MESTRE DE DROGAS (Critérios de Beers AGS 2023 + ACB)
# Mapeia o Princípio Ativo (Genérico) para todos os seus sinônimos
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
    "enoxaparina": ["enoxaparina", "clexane", "versa", "heparina de baixo peso molecular"],
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

# =====================================================================
# 2. FUNÇÕES DE PROCESSAMENTO E DETECÇÃO
# =====================================================================

def normalize_text(text: str) -> str:
    """
    Remove acentos, caracteres especiais e converte tudo para minúsculas.
    Exemplo: "FENITOÍNA 100mg" -> "fenitoina 100mg"
    """
    if not text:
        return ""
    
    # Converte para string unicode normalizada e remove os acentos (diacríticos)
    nfkd_form = unicodedata.normalize('NFKD', text)
    text_without_accents = nfkd_form.encode('ASCII', 'ignore').decode('utf-8')
    
    return text_without_accents.lower()


def detect_drugs_in_prescription(prescription_text: str) -> list:
    """
    Varre o texto extraído do PDF da prescrição e retorna uma lista com os 
    nomes genéricos dos medicamentos de risco identificados.
    """
    detected_drugs = []
    
    # 1. Normaliza o texto total do PDF (sem acentos e minúsculo)
    normalized_text = normalize_text(prescription_text)
    
    # 2. Itera sobre o dicionário mestre
    for generic_name, synonyms in BEERS_DRUGS.items():
        for synonym in synonyms:
            # Normaliza também o sinônimo por segurança
            clean_synonym = normalize_text(synonym)
            
            # Utiliza Regex com \b (Word Boundary) para buscar a palavra exata.
            # Isso evita que a sílaba "dol" de um remédio acione "haloperidol", por exemplo.
            pattern = rf"\b{re.escape(clean_synonym)}\b"
            
            if re.search(pattern, normalized_text):
                detected_drugs.append(generic_name)
                # Se achou um sinônimo (ex: 'gardenal'), adiciona 'fenobarbital' na lista
                # e interrompe o loop dos sinônimos para não duplicar o mesmo remédio.
                break 
                
    return detected_drugs

# =====================================================================
# 3. TESTE DE VALIDAÇÃO (Pode apagar ou comentar em produção)
# =====================================================================
if __name__ == "__main__":
    texto_pdf_simulado = """
    HOSPITAL DE AERONÁUTICA DE RECIFE
    PRESCRIÇÃO MÉDICA - LEITO 05
    
    1. Cefazolina 1g IV 8/8h
    2. HIDANTAL 100mg IV 8/8h
    3. FENOCRIS 100mg VO 12/12h
    4. Rivotril 2mg VO SN
    5. FENERGAN 25mg IV SN
    """
    
    medicamentos_encontrados = detect_drugs_in_prescription(texto_pdf_simulado)
    print(f"Medicamentos de Risco Detectados: {medicamentos_encontrados}")
    # Resultado Esperado: ['fenobarbital', 'fenitoina', 'clonazepam', 'prometazina']
