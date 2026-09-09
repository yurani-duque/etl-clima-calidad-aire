"""
Script Name: transform.py
Author: Valentina Velasco
Fecha: 2026-09-09
Fase ETL: Transformacion
Descripcion: limpia el dataset crudo, estandariza nombres y tipos, aplica reglas
    de calidad de datos y arma las tablas del modelo estrella (dimensiones + hechos)
    listas para cargar en el datawarehouse.
Entradas: dataframe crudo entregado por extract.py
Salidas: diccionario con los dataframes dim_location, dim_date, dim_condition,
    fact_weather_air_quality
Notas: los nombres de columnas de salida son los que espera el DDL en
    dwh_version/001_create_star_schema.sql
"""

import sys

import pandas as pd

sys.path.append(".")
from utils.data_quality import (
    eliminar_duplicados,
    eliminar_nulos_criticos,
    validar_rangos_fisicos,
)
from utils.logger import get_logger

logger = get_logger("transform")

RENOMBRAR_COLUMNAS = {
    "air_quality_Carbon_Monoxide": "air_quality_co",
    "air_quality_Ozone": "air_quality_ozone",
    "air_quality_Nitrogen_dioxide": "air_quality_no2",
    "air_quality_Sulphur_dioxide": "air_quality_so2",
    "air_quality_PM2.5": "air_quality_pm2_5",
    "air_quality_PM10": "air_quality_pm10",
    "air_quality_us-epa-index": "air_quality_us_epa_index",
    "air_quality_gb-defra-index": "air_quality_gb_defra_index",
}

COLUMNAS_CRITICAS = [
    "country", "location_name", "latitude", "longitude", "timezone",
    "last_updated", "last_updated_epoch", "condition_text",
]


def limpiar(df: pd.DataFrame) -> pd.DataFrame:
    df = df.rename(columns=RENOMBRAR_COLUMNAS)
    df.columns = [c.strip() for c in df.columns]

    df["country"] = df["country"].str.strip()
    df["location_name"] = df["location_name"].str.strip()
    df["condition_text"] = df["condition_text"].str.strip()

    df["last_updated"] = pd.to_datetime(df["last_updated"], errors="coerce")

    df, n_dup = eliminar_duplicados(df)
    logger.info(f"duplicados eliminados: {n_dup}")

    df, n_nulos = eliminar_nulos_criticos(df, COLUMNAS_CRITICAS)
    logger.info(f"filas con nulos criticos eliminadas: {n_nulos}")

    df, descartes = validar_rangos_fisicos(df)
    for regla, cantidad in descartes.items():
        logger.info(f"regla '{regla}': {cantidad} filas descartadas")

    return df


def construir_dim_location(df: pd.DataFrame) -> pd.DataFrame:
    dim = (
        df[["country", "location_name", "latitude", "longitude", "timezone"]]
        .drop_duplicates(subset=["country", "location_name"])
        .reset_index(drop=True)
    )
    return dim


def construir_dim_date(df: pd.DataFrame) -> pd.DataFrame:
    fechas = pd.DataFrame({"full_date": df["last_updated"].dt.date.unique()})
    fechas["full_date"] = pd.to_datetime(fechas["full_date"])
    fechas["year"] = fechas["full_date"].dt.year
    fechas["month"] = fechas["full_date"].dt.month
    fechas["day"] = fechas["full_date"].dt.day
    fechas["month_name"] = fechas["full_date"].dt.month_name()
    fechas["day_of_week"] = fechas["full_date"].dt.day_name()
    return fechas.sort_values("full_date").reset_index(drop=True)


def construir_dim_condition(df: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame({"condition_text": df["condition_text"].unique()})


def construir_fact(df: pd.DataFrame, dim_location: pd.DataFrame,
                    dim_date: pd.DataFrame, dim_condition: pd.DataFrame) -> pd.DataFrame:
    dim_location = dim_location.reset_index().rename(columns={"index": "location_id"})
    dim_location["location_id"] += 1

    dim_date = dim_date.reset_index().rename(columns={"index": "date_id"})
    dim_date["date_id"] += 1

    dim_condition = dim_condition.reset_index().rename(columns={"index": "condition_id"})
    dim_condition["condition_id"] += 1

    df = df.copy()
    df["full_date"] = pd.to_datetime(df["last_updated"].dt.date)

    df = df.merge(dim_location[["location_id", "country", "location_name"]],
                   on=["country", "location_name"], how="left")
    df = df.merge(dim_date[["date_id", "full_date"]], on="full_date", how="left")
    df = df.merge(dim_condition[["condition_id", "condition_text"]], on="condition_text", how="left")

    columnas_fact = [
        "location_id", "date_id", "condition_id", "last_updated_epoch",
        "temperature_celsius", "wind_kph", "wind_degree", "wind_direction",
        "pressure_mb", "precip_mm", "humidity", "cloud", "feels_like_celsius",
        "visibility_km", "uv_index", "gust_kph", "air_quality_co", "air_quality_ozone",
        "air_quality_no2", "air_quality_so2", "air_quality_pm2_5", "air_quality_pm10",
        "air_quality_us_epa_index", "air_quality_gb_defra_index", "moon_illumination",
    ]
    fact = df[columnas_fact].drop_duplicates(
        subset=["location_id", "date_id", "last_updated_epoch"]
    )
    return fact.reset_index(drop=True)


def transformar(df_crudo: pd.DataFrame) -> dict:
    df = limpiar(df_crudo)

    dim_location = construir_dim_location(df)
    dim_date = construir_dim_date(df)
    dim_condition = construir_dim_condition(df)
    fact = construir_fact(df, dim_location, dim_date, dim_condition)

    logger.info(f"dim_location: {len(dim_location)} filas")
    logger.info(f"dim_date: {len(dim_date)} filas")
    logger.info(f"dim_condition: {len(dim_condition)} filas")
    logger.info(f"fact_weather_air_quality: {len(fact)} filas")

    return {
        "dim_location": dim_location,
        "dim_date": dim_date,
        "dim_condition": dim_condition,
        "fact_weather_air_quality": fact,
    }
