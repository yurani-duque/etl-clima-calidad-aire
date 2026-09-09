"""
Script Name: load.py
Author: Valentina Velasco
Fecha: 2026-09-09
Fase ETL: Carga
Descripcion: carga las tablas del modelo estrella en Supabase/Postgres, respetando
    el orden de integridad referencial (dimensiones primero, hechos despues).
Entradas: diccionario de dataframes producido por transform.py
Salidas: tablas pobladas en el esquema public de la base de datos
Notas: estrategia de carga = full load (trunca e inserta de nuevo), pensada para
    esta primera entrega donde el dataset se recarga completo cada vez
"""

import sys

import yaml
from sqlalchemy import text

sys.path.append(".")
from utils.db_connector import get_engine
from utils.logger import get_logger

logger = get_logger("load")

ORDEN_CARGA = ["dim_location", "dim_date", "dim_condition", "fact_weather_air_quality"]


def cargar_config(path="config/config.yaml") -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def truncar_tablas(engine, tablas: list[str]) -> None:
    with engine.begin() as conn:
        conn.execute(text(f"truncate table {', '.join(reversed(tablas))} restart identity cascade"))
    logger.info("tablas truncadas antes de la carga")


def cargar_tabla(engine, nombre: str, df, batch_size: int) -> None:
    try:
        df.to_sql(nombre, engine, if_exists="append", index=False,
                   method="multi", chunksize=batch_size)
        logger.info(f"tabla {nombre}: {len(df)} filas cargadas")
    except Exception as e:
        logger.error(f"error cargando {nombre}: {e}")
        raise


def cargar_todo(tablas: dict) -> None:
    cfg = cargar_config()
    engine = get_engine()
    batch_size = cfg["load"]["batch_size"]

    truncar_tablas(engine, ORDEN_CARGA)

    for nombre in ORDEN_CARGA:
        cargar_tabla(engine, nombre, tablas[nombre], batch_size)

    logger.info("carga completa")
