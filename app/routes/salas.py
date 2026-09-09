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