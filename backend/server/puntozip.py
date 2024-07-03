import fastapi

from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from db.db_setup import get_db

from sqlalchemy.future import select

from schemas.pz_schemas import (
    EmpleadoResponse
)

from db.models import (
    Empleado
)


router = fastapi.APIRouter()

@router.get("/")
def index():
    return '<html><body><h1>Hello, world!</h1></body></html>'

@router.get(
    "/empleado/{dni}",
    response_model=EmpleadoResponse,
    response_model_exclude_unset=True
)
async def get_empleado(
    dni: str,
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Empleado).filter(Empleado.dni == dni)
    result = await db.execute(stmt)
    empleado = result.scalars().first()
    return EmpleadoResponse.from_orm(empleado)
