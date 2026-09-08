"""
Script Name: extract.py
Author: Yurani Duque
Fecha: 2026-09-08
Fase ETL: Extraccion
Descripcion: lee el CSV crudo del World Weather Repository (Kaggle) y hace una
    validacion basica de estructura antes de pasarlo a la fase de transformacion.
Entradas: data/raw/GlobalWeatherRepository.csv
Salidas: dataframe de pandas en memoria
Notas: el csv viene en UTF-8, separado por comas
"""

import sys

import pandas as pd
import yaml

sys.path.append(".")
from utils.logger import get_logger

logger = get_logger("extract")


def cargar_config(path="config/config.yaml") -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def extraer_csv(path: str, encoding: str = "utf-8") -> pd.DataFrame:
    logger.info(f"leyendo archivo fuente: {path}")
    try:
        df = pd.read_csv(path, encoding=encoding)
    except FileNotFoundError:
        logger.error(f"no se encontro el archivo {path}")
        raise
    except UnicodeDecodeError:
        logger.error("problema de encoding leyendo el csv")
        raise

    logger.info(f"filas leídas: {len(df)}, columnas: {len(df.columns)}")

    if len(df) == 0:
        raise ValueError("el archivo fuente esta vacio")

    return df


if __name__ == "__main__":
    cfg = cargar_config()
    datos = extraer_csv(cfg["source"]["file"], cfg["source"]["encoding"])
    print(datos.head())
