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
