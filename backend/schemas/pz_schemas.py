from pydantic import BaseModel, Field, field_validator
from datetime import date, time
from decimal import Decimal
from typing import Optional, List

class Consulta1(BaseModel):
    pedido_po: str = Field(..., max_length=20)
    cliente_rin: str = Field(..., max_length=7)
    costo_laboral: Decimal

class Consulta1Response(Consulta1):
    pass

class Consulta2(BaseModel):
    rin: str= Field(..., max_length=7)
    cliente: str
    etapa: str = Field(..., max_length=20)
    pedido_po: str = Field(..., max_length=20)
    tiempo_etapa_dias: int

class Consulta2Response(Consulta2):
    pass

class Consulta3(BaseModel):
    rin: str= Field(..., max_length=7)
    cliente_nombre: str
    categoria: str = Field(..., max_length=10)
    frecuencia: int

class Consulta3Response(Consulta3):
    pass