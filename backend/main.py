from fastapi import FastAPI
from server import puntozip

app = FastAPI()

app.include_router(puntozip.router)

