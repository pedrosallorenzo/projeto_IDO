from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.routes import reservas, salas, usuarios


BASE_DIR = Path(__file__).resolve().parent


app = FastAPI(
    title="Sistema de Reservas de Salas/Eventos"
)


app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)


app.include_router(usuarios.router)
app.include_router(salas.router)
app.include_router(reservas.router)


@app.get("/", include_in_schema=False)
def home():
    return FileResponse(
        BASE_DIR / "static" / "index.html"
    )