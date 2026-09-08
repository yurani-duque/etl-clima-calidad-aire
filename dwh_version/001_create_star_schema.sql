-- star schema para el datawarehouse de clima y calidad del aire
-- fuente: world weather repository (kaggle), alineado a ODS 13 (accion por el clima) y ODS 11
-- orden de creacion: dimensiones primero, despues la tabla de hechos (por las FK)

drop table if exists fact_weather_air_quality cascade;
drop table if exists dim_location cascade;
drop table if exists dim_date cascade;
drop table if exists dim_condition cascade;

create table dim_location (
    location_id serial primary key,
    country varchar(100) not null,
    location_name varchar(100) not null,
    latitude numeric(8,4) not null,
    longitude numeric(8,4) not null,
    timezone varchar(60) not null,
    unique (country, location_name)
);

create table dim_date (
    date_id serial primary key,
    full_date date not null unique,
    year smallint not null,
    month smallint not null,
    day smallint not null,
    month_name varchar(15) not null,
    day_of_week varchar(15) not null
);

create table dim_condition (
    condition_id serial primary key,
    condition_text varchar(80) not null unique
);

create table fact_weather_air_quality (
    fact_id bigserial primary key,
    location_id integer not null references dim_location (location_id),
    date_id integer not null references dim_date (date_id),
    condition_id integer not null references dim_condition (condition_id),
    last_updated_epoch bigint not null,
    temperature_celsius numeric(5,2),
    wind_kph numeric(6,2),
    wind_degree smallint,
    wind_direction varchar(5),
    pressure_mb numeric(7,2),
    precip_mm numeric(6,2),
    humidity smallint,
    cloud smallint,
    feels_like_celsius numeric(5,2),
    visibility_km numeric(5,2),
    uv_index numeric(4,2),
    gust_kph numeric(6,2),
    air_quality_co numeric(10,3),
    air_quality_ozone numeric(10,3),
    air_quality_no2 numeric(10,3),
    air_quality_so2 numeric(10,3),
    air_quality_pm2_5 numeric(10,3),
    air_quality_pm10 numeric(10,3),
    air_quality_us_epa_index smallint,
    air_quality_gb_defra_index smallint,
    moon_illumination smallint,
    unique (location_id, date_id, last_updated_epoch)
);

create index idx_fact_location on fact_weather_air_quality (location_id);
create index idx_fact_date on fact_weather_air_quality (date_id);
create index idx_fact_condition on fact_weather_air_quality (condition_id);
