from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Sistema de Reservas de Salas/Eventos"}