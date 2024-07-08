import fastapi
from fastapi import HTTPException
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.db_setup import get_session
from sqlalchemy import text
# from sqlalchemy.orm import joinedload
# from sqlalchemy import func
from typing import List
from datetime import date, timedelta

from schemas.pz_schemas import (
    Consulta1Response
)

router = fastapi.APIRouter()

# consulta 1
@router.get(
    "/costos-laborales-ultimo-mes",
    response_model=List[Consulta1Response]
)
async def costos_laborales_ultimo_mes(
    session: AsyncSession = Depends(get_session)
):
    try:
        # Calcular fecha de inicio y fin del último mes
        fecha_fin_mes_actual = date.today().replace(day=1) - timedelta(days=1)
        fecha_inicio_mes_actual = fecha_fin_mes_actual.replace(day=1)

        query = text("""
            SELECT p.po AS pedido_po,
                   p.cliente_rin,
                   SUM(tt.tarifa * EXTRACT(EPOCH FROM (t.hora_salida - t.hora_entrada)) / 3600) AS costo_laboral
            FROM pedido p
                 JOIN etapa e ON p.po = e.pedido_po
                 JOIN trabaja tte ON e.pedido_po = tte.etapa_po AND e.estado = tte.etapa_estado
                 JOIN tiempo t ON tte.trabajador_dni = t.dni
                 JOIN trabajador_taller tt ON t.dni = tt.dni
            WHERE e.fecha_finalizacion IS NOT NULL
              AND e.fecha_finalizacion BETWEEN :fecha_inicio AND :fecha_fin
            GROUP BY p.po, p.cliente_rin
        """)

        result = await session.execute(query, {
            "fecha_inicio": fecha_inicio_mes_actual,
            "fecha_fin": fecha_fin_mes_actual
        })

        # print(result.fetchall())
        rows = result.fetchall()
        response_objects = [
            Consulta1Response(pedido_po=row[0], cliente_rin=row[1], costo_laboral=row[2])
            for row in rows
        ]

        return response_objects

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")


# consulta 2

# @router.get("/etapa-mas-demorada-ultimo-mes")
# async def etapa_mas_demorada_ultimo_mes(
#     db: AsyncSession = Depends(get_db)
# ):
#     # Calcular fecha de inicio y fin del último mes
#     fecha_fin_mes_actual = date.today().replace(day=1) - timedelta(days=1)
#     fecha_inicio_mes_actual = fecha_fin_mes_actual.replace(day=1)
#
#     stmt = select(
#         Cliente.rin,
#         Cliente.nombre.label('cliente'),
#         Etapa.estado.label('etapa'),
#         Pedido.po.label('pedido_po'),
#         (Etapa.fecha_finalizacion - Etapa.fecha_inicio).label('tiempo_etapa_dias')
#     ).join(Pedido).join(Etapa).filter(
#         Etapa.fecha_finalizacion.isnot(None),
#         Etapa.fecha_finalizacion > Etapa.fecha_inicio,
#         Etapa.fecha_finalizacion.between(fecha_inicio_mes_actual, fecha_fin_mes_actual)
#     )
#
#     result = await db.execute(stmt)
#     return await result.fetchall()
#
#
# # consulta 3
#
# @router.get("/categorias-mas-solicitadas")
# async def categorias_mas_solicitadas(
#     db: AsyncSession = Depends(get_db)
# ):
#     stmt = select(
#         Cliente.rin,
#         Cliente.nombre.label('cliente_nombre'),
#         Prenda.categoria,
#         func.count(Prenda.categoria).label('frecuencia')
#     ).join(Pedido).join(Prenda).group_by(
#         Cliente.rin, Cliente.nombre, Prenda.categoria
#     ).cte('categoria_frecuencia')
#
#     categoria_max_frecuencia = select(
#         stmt.c.rin,
#         stmt.c.cliente_nombre,
#         stmt.c.categoria,
#         stmt.c.frecuencia,
#         func.rank().over(partition_by=stmt.c.rin, order_by=stmt.c.frecuencia.desc()).label('rk')
#     ).select_from(stmt).where(stmt.c.rk == 1).order_by(stmt.c.frecuencia.desc())
#
#     result = await db.execute(categoria_max_frecuencia)
#     return await result.fetchall()
#
# #post
