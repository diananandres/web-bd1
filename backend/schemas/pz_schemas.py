from pydantic import BaseModel, Field
from datetime import date
from typing import Optional, List

class Empleado(BaseModel):
    dni: str = Field(..., max_length=8)
    nombres: str
    apellidos: str
    fecha_contratacion: date
    fecha_nacimiento: date

    class Config:
        from_attributes = True

class EmpleadoResponse(Empleado):
    pass

