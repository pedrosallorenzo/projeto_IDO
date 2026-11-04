import json
from datetime import datetime

from app.cache import redis_client
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session


from app import models, schemas
from app.database import get_db


router = APIRouter(
    prefix="/salas",
    tags=["Salas"]
)


@router.post(
    "",
    response_model=schemas.SalaResponse,
    status_code=status.HTTP_201_CREATED
)
def criar_sala(
    sala: schemas.SalaCreate,
    db: Session = Depends(get_db)
):
    if sala.capacidade <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A capacidade da sala deve ser maior que zero."
        )

    nova_sala = models.Sala(
        nome=sala.nome,
        capacidade=sala.capacidade,
        localizacao=sala.localizacao
    )

    db.add(nova_sala)
    db.commit()
    db.refresh(nova_sala)

    return nova_sala


@router.get(
    "",
    response_model=list[schemas.SalaResponse]
)
def listar_salas(
    db: Session = Depends(get_db)
):
    salas = db.scalars(
        select(models.Sala).order_by(models.Sala.nome)
    ).all()

    return salas

@router.get("/{sala_id}/disponibilidade")
def verificar_disponibilidade(
    sala_id: int,
    inicio: datetime,
    fim: datetime,
    db: Session = Depends(get_db)
):
    if inicio >= fim:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O horário de início deve ser anterior ao horário de fim."
        )

    sala = db.get(models.Sala, sala_id)

    if sala is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sala não encontrada."
        )

    chave_cache = (
        f"disponibilidade:{sala_id}:"
        f"{inicio.isoformat()}:{fim.isoformat()}"
    )

    cache = redis_client.get(chave_cache)

    if cache is not None:
        return json.loads(cache)

    conflito = db.scalar(
        select(models.Reserva).where(
            models.Reserva.sala_id == sala_id,
            models.Reserva.inicio < fim,
            models.Reserva.fim > inicio
        )
    )

    resposta = {
        "sala_id": sala_id,
        "inicio": inicio.isoformat(),
        "fim": fim.isoformat(),
        "disponivel": conflito is None
    }

    redis_client.setex(
        chave_cache,
        60,
        json.dumps(resposta)
    )

    return resposta