from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db


router = APIRouter(
    prefix="/reservas",
    tags=["Reservas"]
)


@router.post(
    "",
    response_model=schemas.ReservaResponse,
    status_code=status.HTTP_201_CREATED
)
def criar_reserva(
    reserva: schemas.ReservaCreate,
    db: Session = Depends(get_db)
):
    if reserva.inicio >= reserva.fim:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O horário de início deve ser anterior ao horário de fim."
        )

    usuario = db.get(models.Usuario, reserva.usuario_id)

    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado."
        )

    sala = db.get(models.Sala, reserva.sala_id)

    if sala is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sala não encontrada."
        )

    conflito = db.scalar(
        select(models.Reserva).where(
            models.Reserva.sala_id == reserva.sala_id,
            models.Reserva.inicio < reserva.fim,
            models.Reserva.fim > reserva.inicio
        )
    )

    if conflito is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Já existe uma reserva para esta sala neste horário."
        )

    nova_reserva = models.Reserva(
        titulo=reserva.titulo,
        inicio=reserva.inicio,
        fim=reserva.fim,
        usuario_id=reserva.usuario_id,
        sala_id=reserva.sala_id
    )

    db.add(nova_reserva)
    db.commit()
    db.refresh(nova_reserva)

    return nova_reserva


@router.get(
    "",
    response_model=list[schemas.ReservaResponse]
)
def listar_reservas(
    db: Session = Depends(get_db)
):
    reservas = db.scalars(
        select(models.Reserva).order_by(models.Reserva.inicio)
    ).all()

    return reservas


@router.delete("/{reserva_id}")
def cancelar_reserva(
    reserva_id: int,
    db: Session = Depends(get_db)
):
    reserva = db.get(models.Reserva, reserva_id)

    if reserva is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reserva não encontrada."
        )

    db.delete(reserva)
    db.commit()

    return {"message": "Reserva cancelada com sucesso."}