import sqlite3

conn = sqlite3.connect("testeManus/analytics_data.db")
cursor = conn.cursor()

# View for Sleep Health Data
cursor.execute("""
CREATE VIEW IF NOT EXISTS sleep_health_summary AS
SELECT
    Gender,
    Age,
    Occupation,
    `Sleep Duration` AS sleep_duration,
    `Quality of Sleep` AS quality_of_sleep,
    `Physical Activity Level` AS physical_activity_level,
    `Stress Level` AS stress_level,
    `BMI Category` AS bmi_category,
    `Systolic Pressure` AS systolic_pressure,
    `Diastolic Pressure` AS diastolic_pressure,
    `Heart Rate` AS heart_rate,
    `Daily Steps` AS daily_steps,
    `Sleep Disorder` AS sleep_disorder
FROM
    sleep_health;
""")

# View for ANAC Flights Data
cursor.execute("""
CREATE VIEW IF NOT EXISTS anac_flights_summary AS
SELECT
    `EMPRESA (SIGLA)` AS empresa_sigla,
    `EMPRESA (NOME)` AS empresa_nome,
    `EMPRESA (NACIONALIDADE)` AS empresa_nacionalidade,
    ANO AS ano,
    MÊS AS mes,
    `AEROPORTO DE ORIGEM (SIGLA)` AS origem_sigla,
    `AEROPORTO DE ORIGEM (NOME)` AS origem_nome,
    `AEROPORTO DE ORIGEM (UF)` AS origem_uf,
    `AEROPORTO DE ORIGEM (REGIÃO)` AS origem_regiao,
    `AEROPORTO DE ORIGEM (PAÍS)` AS origem_pais,
    `AEROPORTO DE ORIGEM (CONTINENTE)` AS origem_continente,
    `AEROPORTO DE DESTINO (SIGLA)` AS destino_sigla,
    `AEROPORTO DE DESTINO (NOME)` AS destino_nome,
    `AEROPORTO DE DESTINO (UF)` AS destino_uf,
    `AEROPORTO DE DESTINO (REGIÃO)` AS destino_regiao,
    `AEROPORTO DE DESTINO (PAÍS)` AS destino_pais,
    `AEROPORTO DE DESTINO (CONTINENTE)` AS destino_continente,
    NATUREZA AS natureza,
    `GRUPO DE VOO` AS grupo_voo,
    `PASSAGEIROS PAGOS` AS passageiros_pagos,
    `PASSAGEIROS GRÁTIS` AS passageiros_gratis,
    `CARGA PAGA (KG)` AS carga_paga_kg,
    `CARGA GRÁTIS (KG)` AS carga_gratis_kg,
    `CORREIO (KG)` AS correio_kg,
    ASK,
    RPK,
    ATK,
    RTK,
    `COMBUSTÍVEL (LITROS)` AS combustivel_litros,
    `DISTÂNCIA VOADA (KM)` AS distancia_voada_km,
    DECOLAGENS AS decolagens,
    `CARGA PAGA KM` AS carga_paga_km,
    `CARGA GRATIS KM` AS carga_gratis_km,
    `CORREIO KM` AS correio_km,
    ASSENTOS AS assentos,
    PAYLOAD AS payload,
    `HORAS VOADAS` AS horas_voadas,
    `BAGAGEM (KG)` AS bagagem_kg
FROM
    anac_flights;
""")

conn.commit()
conn.close()

print("SQL views created successfully.")

