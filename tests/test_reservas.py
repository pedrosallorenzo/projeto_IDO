from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app


engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def limpar_banco():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def criar_usuario():
    response = client.post(
        "/usuarios",
        json={
            "nome": "Victor",
            "email": "victor@test.com"
        }
    )

    return response.json()["id"]


def criar_sala(nome="Sala 1"):
    response = client.post(
        "/salas",
        json={
            "nome": nome,
            "capacidade": 30,
            "localizacao": "Bloco A"
        }
    )

    return response.json()["id"]


def test_criar_reserva_valida():
    limpar_banco()

    usuario_id = criar_usuario()
    sala_id = criar_sala()

    response = client.post(
        "/reservas",
        json={
            "titulo": "Reuniao",
            "inicio": "2026-11-10T10:00:00",
            "fim": "2026-11-10T11:00:00",
            "usuario_id": usuario_id,
            "sala_id": sala_id
        }
    )

    assert response.status_code == 201
    assert response.json()["titulo"] == "Reuniao"


def test_conflito_de_horario():
    limpar_banco()

    usuario_id = criar_usuario()
    sala_id = criar_sala()

    client.post(
        "/reservas",
        json={
            "titulo": "Reserva 1",
            "inicio": "2026-11-10T10:00:00",
            "fim": "2026-11-10T11:00:00",
            "usuario_id": usuario_id,
            "sala_id": sala_id
        }
    )

    response = client.post(
        "/reservas",
        json={
            "titulo": "Reserva 2",
            "inicio": "2026-11-10T10:30:00",
            "fim": "2026-11-10T11:30:00",
            "usuario_id": usuario_id,
            "sala_id": sala_id
        }
    )

    assert response.status_code == 409


def test_mesmo_horario_em_salas_diferentes():
    limpar_banco()

    usuario_id = criar_usuario()

    sala_1 = criar_sala("Sala 1")
    sala_2 = criar_sala("Sala 2")

    primeira = client.post(
        "/reservas",
        json={
            "titulo": "Reserva Sala 1",
            "inicio": "2026-11-10T10:00:00",
            "fim": "2026-11-10T11:00:00",
            "usuario_id": usuario_id,
            "sala_id": sala_1
        }
    )

    segunda = client.post(
        "/reservas",
        json={
            "titulo": "Reserva Sala 2",
            "inicio": "2026-11-10T10:00:00",
            "fim": "2026-11-10T11:00:00",
            "usuario_id": usuario_id,
            "sala_id": sala_2
        }
    )

    assert primeira.status_code == 201
    assert segunda.status_code == 201


def test_horario_invalido():
    limpar_banco()

    usuario_id = criar_usuario()
    sala_id = criar_sala()

    response = client.post(
        "/reservas",
        json={
            "titulo": "Horario invalido",
            "inicio": "2026-11-10T12:00:00",
            "fim": "2026-11-10T11:00:00",
            "usuario_id": usuario_id,
            "sala_id": sala_id
        }
    )

    assert response.status_code == 400


def test_listar_reservas():
    limpar_banco()

    usuario_id = criar_usuario()
    sala_id = criar_sala()

    client.post(
        "/reservas",
        json={
            "titulo": "Reserva teste",
            "inicio": "2026-11-10T10:00:00",
            "fim": "2026-11-10T11:00:00",
            "usuario_id": usuario_id,
            "sala_id": sala_id
        }
    )

    response = client.get("/reservas")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_cancelar_reserva():
    limpar_banco()

    usuario_id = criar_usuario()
    sala_id = criar_sala()

    reserva = client.post(
        "/reservas",
        json={
            "titulo": "Reserva para cancelar",
            "inicio": "2026-11-10T10:00:00",
            "fim": "2026-11-10T11:00:00",
            "usuario_id": usuario_id,
            "sala_id": sala_id
        }
    )

    reserva_id = reserva.json()["id"]

    response = client.delete(
        f"/reservas/{reserva_id}"
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Reserva cancelada com sucesso."


def test_cancelar_reserva_inexistente():
    limpar_banco()

    response = client.delete("/reservas/999")

    assert response.status_code == 404