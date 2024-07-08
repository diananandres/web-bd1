from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from server import puntozip

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todas las cabeceras
)
app.include_router(puntozip.router)

