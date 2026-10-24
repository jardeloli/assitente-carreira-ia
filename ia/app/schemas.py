from pydantic import BaseModel, Field
from typing import Optional

class DocumentoRequest(BaseModel):
    informacoes: str = Field(min_length=10, description="Informações fornecidas pelo candidato em linguagem natural")
    cargo: str = Field(min_length=2)
    empresa: Optional[str] = None

class EntrevistaInicioRequest(BaseModel):
    cargo: str = Field(min_length=2)
    informacoes: str = ""

class EntrevistaRespostaRequest(BaseModel):
    chat_id: str
    resposta: str = Field(min_length=1)
