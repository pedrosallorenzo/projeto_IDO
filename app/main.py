from fastapi import FastAPI

from app.routes import reservas


app = FastAPI(
    title="Sistema de Reservas de Salas/Eventos"
)

app.include_router(reservas.router)


@app.get("/")
def home():
    return {"message": "Sistema de Reservas de Salas/Eventos"}