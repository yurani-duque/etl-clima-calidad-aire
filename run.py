"""
Script Name: run.py
Author: Yurani Duque
Fecha: 2026-09-10
Fase ETL: Orquestacion (Extraccion + Transformacion + Carga)
Descripcion: orquesta el pipeline completo desde linea de comandos, llamando en
    orden a extract, transform y load.
Entradas: config/config.yaml, data/raw/GlobalWeatherRepository.csv, .env
Salidas: datawarehouse poblado en Supabase
Notas: ejecutar con "uv run run.py" desde la raiz del proyecto
"""

import sys
import time

from src.extract import cargar_config, extraer_csv
from src.load import cargar_todo
from src.transform import transformar
from utils.logger import get_logger

logger = get_logger("run")


def main():
    inicio = time.time()
    logger.info("=== inicio del pipeline ETL ===")

    try:
        cfg = cargar_config()
        df_crudo = extraer_csv(cfg["source"]["file"], cfg["source"]["encoding"])
        tablas = transformar(df_crudo)
        cargar_todo(tablas)
    except Exception as e:
        logger.error(f"pipeline detenido por error: {e}")
        sys.exit(1)

    duracion = round(time.time() - inicio, 2)
    logger.info(f"=== pipeline finalizado en {duracion}s ===")


if __name__ == "__main__":
    main()
