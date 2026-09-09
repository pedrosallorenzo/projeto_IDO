from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db


router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)


@router.post(
    "",
    response_model=schemas.UsuarioResponse,
    status_code=status.HTTP_201_CREATED
)
def criar_usuario(
    usuario: schemas.UsuarioCreate,
    db: Session = Depends(get_db)
):
    usuario_existente = db.scalar(
        select(models.Usuario).where(
            models.Usuario.email == usuario.email
        )
    )

    if usuario_existente is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Já existe um usuário cadastrado com este e-mail."
        )

    novo_usuario = models.Usuario(
        nome=usuario.nome,
        email=usuario.email
    )

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    return novo_usuario


@router.get(
    "",
    response_model=list[schemas.UsuarioResponse]
)
def listar_usuarios(
    db: Session = Depends(get_db)
):
    usuarios = db.scalars(
        select(models.Usuario).order_by(models.Usuario.nome)
    ).all()

    return usuarios