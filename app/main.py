from .pncp import buscar_propostas, mapear_licitacao
from .filters import is_ti_saas
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
from .schemas import BuscaResponse, Licitacao


app = FastAPI(
    title="Licita TI / SaaS API",
    description="Busca simples de Licitações de TI e SaaS no PNCP (foco Sc + Brasil)",
    version="1.0.0",
)

# Libera CORS pro seu React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # em producao coloque o frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "message": "Licita TI API rodando",
        "docs": "/docs",
        "endpoints": ["/licitacoes", "/health"],
    }


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/licitacoes", response_model=BuscaResponse)
async def buscar_licitacoes(
    uf: Optional[str] = Query("SC", description="UF da licitação (ex: SC, SP, RJ)"),
    pagina: int = Query(1, ge=1),
    tamanho: int = Query(50, ge=10, le=50),
    data_final: Optional[str] = Query(
        None, description="Data final para filtrar licitações"
    ),
    apenas_ti: bool = Query(True, description="Filtrar apenas licitações de TI e SaaS"),
):
    """
    busca licitações no PNCP com base nos parâmetros fornecidos.
    """
    try:
        itens_brutos = await buscar_propostas(
            uf=uf, pagina=pagina, tamanho_pagina=tamanho, data_final=data_final
        )
        resultados: List[Licitacao] = []
        for item in itens_brutos:
            licitacao = mapear_licitacao(item)

            if apenas_ti and not is_ti_saas(licitacao.objeto):
                continue

            resultados.append(licitacao)

        return BuscaResponse(
            total=len(resultados), pagina=pagina, resultados=resultados
        )

    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=502, detail=f"Erro na API do PNCP: : {e.response.status_code}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
