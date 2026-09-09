from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UsuarioCreate(BaseModel):
    nome: str
    email: str


class UsuarioResponse(UsuarioCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


class SalaCreate(BaseModel):
    nome: str
    capacidade: int
    localizacao: str


class SalaResponse(SalaCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ReservaCreate(BaseModel):
    titulo: str
    inicio: datetime
    fim: datetime
    usuario_id: int
    sala_id: int


class ReservaResponse(ReservaCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)