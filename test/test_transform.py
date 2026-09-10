"""
Script Name: test_transform.py
Author: Valentina Velasco
Fecha: 2026-09-10
Fase ETL: Pruebas
Descripcion: valida las funciones de transformacion y las reglas de calidad de
    datos con un dataframe de ejemplo pequeno.
Entradas: ninguna (datos simulados dentro del propio test)
Salidas: resultado de la suite de pruebas (pytest)
Notas: correr con "uv run pytest test/"
"""

import sys

import pandas as pd

sys.path.append(".")
from src.transform import construir_dim_condition, construir_dim_location, limpiar
from utils.data_quality import eliminar_duplicados, validar_rangos_fisicos


def _df_ejemplo():
    return pd.DataFrame({
        "country": ["Colombia", "Colombia", "Peru"],
        "location_name": ["Cali", "Cali", "Lima"],
        "latitude": [3.43, 3.43, -12.05],
        "longitude": [-76.52, -76.52, -77.04],
        "timezone": ["America/Bogota", "America/Bogota", "America/Lima"],
        "last_updated": ["2026-09-01 10:00", "2026-09-01 10:00", "2026-09-01 11:00"],
        "last_updated_epoch": [1, 1, 2],
        "condition_text": ["Sunny", "Sunny", "Cloudy"],
        "humidity": [55, 55, 120],
        "air_quality_us_epa_index": [2, 2, 9],
        "air_quality_pm2_5": [5.0, 5.0, 3.0],
        "air_quality_pm10": [10.0, 10.0, 6.0],
        "air_quality_co": [200.0, 200.0, 150.0],
        "air_quality_ozone": [30.0, 30.0, 25.0],
        "air_quality_no2": [1.0, 1.0, 0.5],
        "air_quality_so2": [0.5, 0.5, 0.2],
        "air_quality_gb_defra_index": [1, 1, 1],
        "precip_mm": [0.0, 0.0, 0.0],
        "wind_kph": [10.0, 10.0, 5.0],
        "pressure_mb": [1012.0, 1012.0, 1010.0],
    })


def test_eliminar_duplicados_quita_filas_repetidas():
    df = _df_ejemplo()
    resultado, n_quitados = eliminar_duplicados(df)
    assert n_quitados == 1
    assert len(resultado) == 2


def test_validar_rangos_fisicos_descarta_humedad_invalida():
    df = _df_ejemplo()
    resultado, descartes = validar_rangos_fisicos(df)
    assert (resultado["humidity"] <= 100).all()
    assert descartes["humidity_fuera_de_rango"] >= 1


def test_construir_dim_location_no_duplica_ciudades():
    df = _df_ejemplo()
    df, _ = eliminar_duplicados(df)
    dim = construir_dim_location(df)
    assert len(dim) == len(dim.drop_duplicates(subset=["country", "location_name"]))


def test_construir_dim_condition_es_unica():
    df = _df_ejemplo()
    dim = construir_dim_condition(df)
    assert dim["condition_text"].is_unique
