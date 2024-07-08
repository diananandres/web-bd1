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
    Consulta1Response,
    Consulta2Response,
    Consulta3Response
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

@router.get("/etapa-mas-demorada-ultimo-mes",
            response_model=List[Consulta2Response]
            )

async def etapa_mas_demorada_ultimo_mes(
    session: AsyncSession = Depends(get_session)
):
    try:
        # Calcular fecha de inicio y fin del último mes
        fecha_fin_mes_actual = date.today().replace(day=1) - timedelta(days=1)
        fecha_inicio_mes_actual = fecha_fin_mes_actual.replace(day=1)

        query = text("""
            SELECT c.rin, c.nombre  AS cliente, 
                   e.estado  AS etapa, 
                   p.po AS pedido_po,
                   (e.fecha_finalizacion - e.fecha_inicio) AS tiempo_etapa_dias
            FROM cliente c
                JOIN pedido p ON c.rin = p.cliente_rin
                JOIN etapa e ON p.po = e.pedido_po
            WHERE e.fecha_finalizacion IS NOT NULL
                AND e.fecha_finalizacion > e.fecha_inicio
                AND e.fecha_finalizacion BETWEEN :fecha_inicio AND :fecha_fin;
        """)

        result = await session.execute(query, {
            "fecha_inicio": fecha_inicio_mes_actual,
            "fecha_fin": fecha_fin_mes_actual
        })

        # print(result.fetchall())
        rows = result.fetchall()
        response_objects = [
            Consulta2Response(rin=row[0], cliente=row[1], etapa=row[2], pedido_po=row[3] ,tiempo_etapa_dias=row[4])
            for row in rows
        ]

        return response_objects

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

 # consulta 3

@router.get("/categorias-mas-solicitadas",
            response_model=List[Consulta3Response])

async def categorias_mas_solicitadas(
    session: AsyncSession = Depends(get_session)
):
    try:
        query = text("""
            WITH categoria_frecuencia AS (
                SELECT c.rin,
                       c.nombre AS cliente_nombre,
                       pr.categoria,
                       COUNT(pr.categoria) AS frecuencia
                FROM cliente c
                    JOIN pedido p ON c.rin = p.cliente_rin
                    JOIN prenda pr ON p.po = pr.pedido_po
                GROUP BY c.rin, c.nombre, pr.categoria
            ),
            categoria_max_frecuencia AS (
                SELECT rin,
                       cliente_nombre,
                       categoria,
                       frecuencia,
                       RANK() OVER (PARTITION BY rin ORDER BY frecuencia DESC) AS rk
                FROM categoria_frecuencia
            )
            SELECT rin,
                   cliente_nombre,
                   categoria,
                   frecuencia
            FROM categoria_max_frecuencia
                WHERE rk = 1
            ORDER BY frecuencia DESC;
        """)

        result = await session.execute(query)
        rows = result.fetchall()
        
        # print(result.fetchall())
        response_objects = [
            Consulta3Response(rin=row[0], cliente_nombre=row[1], categoria=row[2], frecuencia=row[3])
            for row in rows
        ]

        return response_objects

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")
    

