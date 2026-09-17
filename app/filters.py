# Palavras-chave focadas em TI / SaaS
KEYWORDS_TI = [
    "software", "saas", "sistema", "sistemas", "licença", "licenca",
    "cloud", "infraestrutura de ti", "tecnologia da informação",
    "tecnologia da informacao", "desenvolvimento de software",
    "solução de ti", "solucao de ti", "manutenção de sistemas",
    "manutencao de sistemas", "aplicativo", "plataforma digital",
    "erp", "crm", "hospedagem", "datacenter", "segurança da informação",
    "seguranca da informacao", "backup", "suporte técnico", "suporte tecnico"
]

def is_ti_saas(objeto: str) -> bool:
    if not objeto:
        return False
    texto = objeto.lower()
    return any(kw in texto for kw in KEYWORDS_TI)
