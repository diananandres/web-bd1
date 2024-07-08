import fastapi
from fastapi import  HTTPException
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.db_setup import get_db
from sqlalchemy.future import select
from sqlalchemy import func
from typing import List
from datetime import date, timedelta

from schemas.pz_schemas import (
PedidoResponse, 
ClienteResponse, 
TrabajaResponse, 
TiempoResponse, 
TrabajadorTallerResponse,
EtapaResponse,
PrendaResponse
)

from db.models import (
Pedido,
Cliente, 
Trabaja, 
Tiempo, 
TrabajadorTaller,
Etapa,
Prenda
)


router = fastapi.APIRouter()

##consulta 1
@router.get("/costos-laborales-ultimo-mes")
async def costos_laborales_ultimo_mes(
    db: AsyncSession = Depends(get_db)
):
    # Calcular fecha de inicio y fin del último mes
    fecha_fin_mes_actual = date.today().replace(day=1) - timedelta(days=1)
    fecha_inicio_mes_actual = fecha_fin_mes_actual.replace(day=1)
    
    stmt = select(
        Pedido.po.label('pedido_po'),
        Pedido.cliente_rin,
        func.sum(TrabajadorTaller.tarifa * func.extract('epoch', Tiempo.hora_salida - Tiempo.hora_entrada) / 3600).label('costo_laboral')
    ).join(Etapa).join(Trabaja).join(Tiempo).join(TrabajadorTaller).filter(
        Etapa.fecha_finalizacion.isnot(None),
        Etapa.fecha_finalizacion.between(fecha_inicio_mes_actual, fecha_fin_mes_actual)
    ).group_by(Pedido.po, Pedido.cliente_rin)

    result = await db.execute(stmt)
    return await result.fetchall()


##consulta 2

@router.get("/etapa-mas-demorada-ultimo-mes")
async def etapa_mas_demorada_ultimo_mes(
    db: AsyncSession = Depends(get_db)
):
    # Calcular fecha de inicio y fin del último mes
    fecha_fin_mes_actual = date.today().replace(day=1) - timedelta(days=1)
    fecha_inicio_mes_actual = fecha_fin_mes_actual.replace(day=1)
    
    stmt = select(
        Cliente.rin,
        Cliente.nombre.label('cliente'),
        Etapa.estado.label('etapa'),
        Pedido.po.label('pedido_po'),
        (Etapa.fecha_finalizacion - Etapa.fecha_inicio).label('tiempo_etapa_dias')
    ).join(Pedido).join(Etapa).filter(
        Etapa.fecha_finalizacion.isnot(None),
        Etapa.fecha_finalizacion > Etapa.fecha_inicio,
        Etapa.fecha_finalizacion.between(fecha_inicio_mes_actual, fecha_fin_mes_actual)
    )

    result = await db.execute(stmt)
    return await result.fetchall()


##consulta 3

@router.get("/categorias-mas-solicitadas")
async def categorias_mas_solicitadas(
    db: AsyncSession = Depends(get_db)
):
    stmt = select(
        Cliente.rin,
        Cliente.nombre.label('cliente_nombre'),
        Prenda.categoria,
        func.count(Prenda.categoria).label('frecuencia')
    ).join(Pedido).join(Prenda).group_by(
        Cliente.rin, Cliente.nombre, Prenda.categoria
    ).cte('categoria_frecuencia')

    categoria_max_frecuencia = select(
        stmt.c.rin,
        stmt.c.cliente_nombre,
        stmt.c.categoria,
        stmt.c.frecuencia,
        func.rank().over(partition_by=stmt.c.rin, order_by=stmt.c.frecuencia.desc()).label('rk')
    ).select_from(stmt).where(stmt.c.rk == 1).order_by(stmt.c.frecuencia.desc())

    result = await db.execute(categoria_max_frecuencia)
    return await result.fetchall()

#post
