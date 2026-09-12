# ETL - Clima y Calidad del Aire Global (ODS 11 y ODS 13)

Pipeline ETL que consolida datos diarios de clima y calidad del aire de más de 280
ciudades capitales del mundo (World Weather Repository, Kaggle) en un datawarehouse
relacional con esquema estrella, alojado en Supabase/PostgreSQL. Proyecto alineado con
el ODS 13 (Acción por el clima) y la meta 11.6 del ODS 11 (calidad del aire urbano).

Entrega 1 - curso ETL (G51), Universidad Autónoma de Occidente.

## Stack tecnológico

- **Python 3.14**, gestionado con **uv**
- **pandas** para extracción y transformación
- **PostgreSQL 17** (Supabase) como datawarehouse
- **SQLAlchemy + psycopg2** para la conexión a base de datos
- **Jupyter Notebook** para el EDA (consultas directas a la BD vía SQL)
- **Graphviz**, matplotlib y seaborn para diagramas y visualizaciones
- **pytest** para pruebas unitarias
- **python-docx** para el documento técnico

## Estructura del repositorio

```
config/          configuración del proyecto (config.yaml, sin credenciales)
src/             extract.py, transform.py, load.py
utils/           conexión a BD, logging, reglas de calidad de datos
test/            pruebas unitarias (pytest)
dwh_version/     DDL del esquema estrella (.sql)
docs/            documento técnico APA, diagramas y scripts que los generan
notebooks/       EDA y visualizaciones (consultas SQL contra Supabase)
run.py           orquestador del pipeline completo (CLI)
```

## Modelo de datos

Esquema estrella: `dim_location`, `dim_date`, `dim_condition` y la tabla de hechos
`fact_weather_air_quality`. Ver diagrama completo en
`docs/img/star_schema.png` y el DDL en `dwh_version/001_create_star_schema.sql`.

## Instalación

Requiere [uv](https://docs.astral.sh/uv/) instalado.

```bash
uv venv --python 3.14
uv sync
```

Copiar `.env.example` a `.env` y completar las credenciales de la base de datos
(nunca se suben credenciales reales al repositorio, ver `.gitignore`):

```bash
cp .env.example .env
```

## Ejecución del pipeline

```bash
uv run run.py
```

Esto ejecuta en orden: extracción del CSV fuente, limpieza y control de calidad,
construcción del modelo estrella, y carga (full load) en Supabase. Los logs quedan en
`logs/etl.log`.

## Pruebas

```bash
uv run pytest test/
```

## Análisis exploratorio

El notebook `notebooks/eda_clima_calidad_aire.ipynb` consulta directamente la base de
datos vía SQL (no el CSV original) y genera las visualizaciones que respaldan el
documento técnico.

## Documento técnico

El informe completo (formato APA 7, 10 componentes del proceso ETL, diagramas,
mapeo de datos y evidencias) está en `docs/Documento_Tecnico_ETL_G_.docx`.

## Autores

- Yurani Duque
- Valentina Velasco
