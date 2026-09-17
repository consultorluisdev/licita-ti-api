from pydantic import BaseModel
from typing import Optional, List

class Licitacao(BaseModel):
  id: str
  objeto: str
  orgao: str
  uf: Optional[str] = None
  municipio: Optional[float] = None
  valor_estimado: Optional[str] = None
  modalidade: Optional[str] = None
  data_publicacao: Optional[str] = None
  data_limite: Optional[str] = None
  link_pncp: str
  cnpj_orgao: Optional[str] = None

class BuscaResponse(BaseModel):
  total: int
  pagina: int
  resultados: List[Licitacao]
