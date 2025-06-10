import sqlite3
import pandas as pd

def create_db_anac():
    conn = sqlite3.connect("db/anac/banco_anac.db")
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS viagens(
        id_viagens INTEGER PRIMARY KEY AUTOINCREMENT,
        sigla_empresa TEXT NOT NULL,
        ano INTEGER NOT NULL,
        mes INTEGER NOT NULL,
        aeroporto_origem_sigla TEXT NOT NULL,
        aeroporto_origem_pais TEXT NOT NULL,
        aeroporto_destino_sigla TEXT NOT NULL,
        aeroporto_destino_pais TEXT NOT NULL,
        natureza TEXT NOT NULL,
        passageiros_pagos INTEGER NOT NULL,
        carga_paga INTEGER NOT NULL,
        ask INTEGER NOT NULL,
        rpk INTEGER NOT NULL,
        atk INTEGER NOT NULL,
        rtk INTEGER NOT NULL,
        litros_combustivel INTEGER NOT NULL,
        distancia_voada_km INTEGER NOT NULL,
        decolagens INTEGER NOT NULL,
        horas_voadas INTEGER NOT NULL,
        assentos INTEGER NOT NULL,
        payload INTEGER NOT NULL
    )   
    ''')

    df = pd.read_csv("data/resumo_anual_2025.csv", sep=';',encoding='latin1')
    cursor.execute('SELECT COUNT(*) FROM viagens')
    if cursor.fetchone()[0] == 0:
        for _, linha in df.iterrows():
            cursor.execute('''
                INSERT INTO viagens
                (sigla_empresa, ano, mes, aeroporto_origem_sigla, aeroporto_origem_pais, aeroporto_destino_sigla, aeroporto_destino_pais, natureza, passageiros_pagos,
                carga_paga, ask, rpk, atk, rtk, litros_combustivel, distancia_voada_km, decolagens, horas_voadas, assentos, payload) 
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            ''', (linha['EMPRESA (SIGLA)'], linha['ANO'], linha['MÊS'], linha['AEROPORTO DE ORIGEM (SIGLA)'], linha['AEROPORTO DE ORIGEM (PAÍS)'], linha['AEROPORTO DE DESTINO (SIGLA)'],
                linha['AEROPORTO DE DESTINO (PAÍS)'], linha['NATUREZA'], linha['PASSAGEIROS PAGOS'], linha['CARGA PAGA (KG)'], linha['ASK'], linha['RPK'], linha['ATK'], linha['RTK'],
                linha['COMBUSTÍVEL (LITROS)'], linha['DISTÂNCIA VOADA (KM)'], linha['DECOLAGENS'], linha['HORAS VOADAS'], linha['ASSENTOS'], linha['PAYLOAD']))
            
    conn.commit()
    conn.close()