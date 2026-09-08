"""
Script Name: logger.py
Author: Yurani Duque
Fecha: 2026-09-08
Fase ETL: Soporte (utilizado por todas las fases)
Descripcion: configura un logger comun para las tres fases del pipeline, con
    salida a consola y a archivo con marca de tiempo.
Entradas: nombre del modulo que solicita el logger
Salidas: objeto logging.Logger configurado
Notas: los logs quedan en logs/etl.log (carpeta se crea si no existe)
"""

import logging
import os

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "etl.log")


def get_logger(name):
    os.makedirs(LOG_DIR, exist_ok=True)

    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")

    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(fmt)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(fmt)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger
