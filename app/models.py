from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)

    reservas = relationship("Reserva", back_populates="usuario")


class Sala(Base):
    __tablename__ = "salas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    capacidade: Mapped[int] = mapped_column(Integer, nullable=False)
    localizacao: Mapped[str] = mapped_column(String(150), nullable=False)

    reservas = relationship("Reserva", back_populates="sala")


class Reserva(Base):
    __tablename__ = "reservas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    titulo: Mapped[str] = mapped_column(String(150), nullable=False)

    inicio: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    fim: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id"),
        nullable=False
    )

    sala_id: Mapped[int] = mapped_column(
        ForeignKey("salas.id"),
        nullable=False
    )

    usuario = relationship("Usuario", back_populates="reservas")
    sala = relationship("Sala", back_populates="reservas")