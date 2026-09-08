"""
Script Name: db_connector.py
Author: Yurani Duque
Fecha: 2026-09-08
Fase ETL: Soporte (utilizado por Extraccion, Transformacion y Carga)
Descripcion: crea la conexion hacia la base de datos Postgres (Supabase) a partir
    de variables de entorno, sin exponer credenciales en el codigo fuente.
Entradas: variables de entorno DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
Salidas: engine de sqlalchemy listo para usar
Notas: requiere un archivo .env en la raiz del proyecto (ver .env.example)
"""

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()


def get_engine():
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    name = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")

    if not all([host, port, name, user, password]):
        raise RuntimeError("faltan variables de entorno de conexion, revisa el .env")

    url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}"
    return create_engine(url, pool_pre_ping=True)
