import sqlite3
import pandas as pd
import streamlit as st

def get_connection():
    try:
        conn = sqlite3.connect("db/banco_sono.db")
        return conn
    except Exception as e:
        st.error(f"Erro ao conectar ao banco de dados: {str(e)}")
        return None

def execute_query(query, params=None, return_df=False):
    conn = get_connection()
    if not conn:
        return None
        
    try:
        cur = conn.cursor()
        if params == None:
            cur.execute(query)
        else:
            cur.execute(query, params)
        
        if query.strip().lower().startswith(('select', 'with')):
            if return_df:
                columns = [desc[0] for desc in cur.description]
                data = cur.fetchall()
                return pd.DataFrame(data, columns=columns)
            else:
                return cur.fetchall()
        else:
            conn.commit()
            return cur.rowcount
    except Exception as e:
        st.error(f"Erro na execução da query: {str(e)}")
        conn.rollback()
        return None
    finally:
        conn.close()

def create_db():
    conn = sqlite3.connect("db/banco_sono.db")
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pessoas (
        id_pessoas INTEGER PRIMARY KEY AUTOINCREMENT,
        genero TEXT NOT NULL,
        idade INTEGER NOT NULL,
        profissao TEXT NOT NULL,
        duracao_sono DECIMAL NOT NULL,
        qualidade_sono INTEGER NOT NULL,
        atividade_fisica INTEGER NOT NULL,
        nivel_estresse INTEGER NOT NULL,
        nivel_IMC TEXT NOT NULL,
        pressao_sanguinea DECIMAL(5, 2) NOT NULL,
        taxa_batimentos INT NOT NULL,
        passos_diarios INT NOT NULL,
        condicao_sono TEXT
    )
    ''')

    df = pd.read_csv("data/Sleep_health_and_lifestyle_dataset.csv")
    cursor.execute('SELECT COUNT(*) FROM pessoas')
    if cursor.fetchone()[0] == 0:
        for _, linha in df.iterrows():
            cursor.execute('''
                INSERT INTO pessoas 
                (id_pessoas, genero, idade, profissao, duracao_sono, qualidade_sono, atividade_fisica,
                nivel_estresse, nivel_IMC, pressao_sanguinea, taxa_batimentos, passos_diarios, condicao_sono) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (linha['Person ID'], linha['Gender'], linha['Age'], linha['Occupation'], linha['Sleep Duration'], linha['Quality of Sleep'], linha['Physical Activity Level'],
                linha['Stress Level'], linha['BMI Category'], linha['Blood Pressure'], linha['Heart Rate'], linha['Daily Steps'], linha['Sleep Disorder']))


    cursor.execute('''
    UPDATE pessoas
    SET nivel_IMC = 'Normal'
    WHERE nivel_IMC = 'Normal Weight';
    ''')

    cursor.execute('''
    UPDATE pessoas
    SET condicao_sono = 'Normal'
    WHERE condicao_sono IS NULL;
    ''')

    conn.commit()
    conn.close()

