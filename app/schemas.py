from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ReservaCreate(BaseModel):
    titulo: str
    inicio: datetime
    fim: datetime
    usuario_id: int
    sala_id: int


class ReservaResponse(ReservaCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)