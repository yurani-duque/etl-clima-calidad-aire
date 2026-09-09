"""
Script Name: data_quality.py
Author: Valentina Velasco
Fecha: 2026-09-09
Fase ETL: Soporte (usado en Transformacion)
Descripcion: reglas de calidad del dato aplicadas al dataset de clima y calidad
    del aire antes de cargarlo al datawarehouse.
Entradas: dataframe crudo o parcialmente transformado
Salidas: dataframe filtrado + reporte de filas descartadas por regla
Notas: las reglas estan pensadas para este dataset en particular (rangos fisicos
    validos de humedad, indices de calidad del aire, coordenadas, etc.)
"""

import pandas as pd


def validar_rangos_fisicos(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    descartes = {}

    n0 = len(df)
    df = df[(df["humidity"] >= 0) & (df["humidity"] <= 100)]
    descartes["humidity_fuera_de_rango"] = n0 - len(df)

    n0 = len(df)
    df = df[(df["latitude"] >= -90) & (df["latitude"] <= 90)]
    df = df[(df["longitude"] >= -180) & (df["longitude"] <= 180)]
    descartes["coordenadas_invalidas"] = n0 - len(df)

    n0 = len(df)
    df = df[df["air_quality_us_epa_index"].between(1, 6)]
    descartes["epa_index_invalido"] = n0 - len(df)

    n0 = len(df)
    cols_no_negativas = [
        "air_quality_pm2_5", "air_quality_pm10", "air_quality_co",
        "air_quality_ozone", "air_quality_no2", "air_quality_so2",
        "precip_mm", "wind_kph", "pressure_mb",
    ]
    for col in cols_no_negativas:
        df = df[df[col] >= 0]
    descartes["mediciones_negativas"] = n0 - len(df)

    return df, descartes


def eliminar_duplicados(df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    n0 = len(df)
    df = df.drop_duplicates(subset=["country", "location_name", "last_updated_epoch"])
    return df, n0 - len(df)


def eliminar_nulos_criticos(df: pd.DataFrame, columnas_criticas: list[str]) -> tuple[pd.DataFrame, int]:
    n0 = len(df)
    df = df.dropna(subset=columnas_criticas)
    return df, n0 - len(df)
