from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from .schemas import Licitacao
from .filters import is_ti_saas



BASE_URL = "https://pncp.gov.br/api/consulta/v1/"


async def buscar_propostas(
    uf: Optional[str] = None,
    pagina: int = 1,
    tamanho_pagina: int = 50,
    data_final: Optional[str] = None,
) -> List[Dict]:
    """
    Busca propostas no PNCP com base nos parâmetros fornecidos.
    """
    if not data_final:
        data_final = (datetime.now() + timedelta(days=60)).strftime("%Y-%m-%d")

    params = {
        "pagina": pagina,
        "data_final": data_final,
        "tamanhoPagina": min(tamanho_pagina, 50),
    }
    if uf:
        params["uf"] = uf.upper()

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(f"{BASE_URL}/contratacoes/propostas", params=params)

        if response.status_code == 204:
            return []
        response.raise_for_status()
        data = response.json()
        return data.get("data", [])


def mapear_licitacao(item: Dict[str, Any]) -> Licitacao:
    """
    Mapeia um item bruto do PNCP para o modelo Licitacao.
    """
    orgao = item.get("orgao", {}) or {}
    unidade = item.get("unidadeOrgao", {}) or {}

    cnpj = orgao.get("cnpj", "")
    ano = item.get("anoCompra")
    sequencial = item.get("sequencial")

    link = ""
    if cnpj and ano and sequencial:
        link = f"https://pncp.gov.br/licitacoes/{cnpj}/{ano}/{sequencial}"

    return Licitacao(
        id=f"{cnpj}-{ano}-{sequencial}",
        objeto=item.get("objetoCompra") or item.get("objeto") or "Sem objeto",
        orgao=orgao.get("razaoSocial")
        or unidade.get("nomeUnidade")
        or "Órgão não informado",
        uf=unidade.get("ufSigla") or orgao.get("uf") or None,
        municipio=unidade.get("municipioNome") or None,
        valor_estimado=item.get("valorTotalEstimado"),
        modalidade=item.get("modalidadeNome") or str(item.get("modalidadeId", "")),
        data_publicacao=item.get("dataPublicacaoPncp"),
        data_limite=item.get("dataEncerramentoProposta")
        or item.get("dataAberturaProposta"),
        link_pncp=link,
        cnpj_orgao=cnpj,
    )
