import pandas as pd
import sqlite3

# --- Cleaning Sleep_health_and_lifestyle_dataset.csv ---
sleep_df = pd.read_csv("testeManus/Sleep_health_and_lifestyle_dataset.csv")

sleep_df["Sleep Disorder"] = sleep_df["Sleep Disorder"].fillna("None")

sleep_df[["Systolic Pressure", "Diastolic Pressure"]] = sleep_df["Blood Pressure"].str.split("/", expand=True)
sleep_df["Systolic Pressure"] = pd.to_numeric(sleep_df["Systolic Pressure"])
sleep_df["Diastolic Pressure"] = pd.to_numeric(sleep_df["Diastolic Pressure"])
sleep_df = sleep_df.drop(columns=["Blood Pressure"])

# --- Cleaning resumo_anual_2025.csv ---
anac_df = pd.read_csv("testeManus/resumo_anual_2025.csv", encoding="latin1", sep=";")

columns_to_fill_unknown = [
    "AEROPORTO DE ORIGEM (UF)", "AEROPORTO DE ORIGEM (REGIÃO)",
    "AEROPORTO DE DESTINO (UF)", "AEROPORTO DE DESTINO (REGIÃO)"
]
for col in columns_to_fill_unknown:
    anac_df[col] = anac_df[col].fillna("Desconhecido")

columns_to_fill_zero = [
    "PASSAGEIROS PAGOS", "PASSAGEIROS GRÁTIS", "CARGA PAGA (KG)",
    "CARGA GRÁTIS (KG)", "CORREIO (KG)", "ASK", "RPK", "ATK", "RTK",
    "COMBUSTÍVEL (LITROS)", "DISTÂNCIA VOADA (KM)", "DECOLAGENS",
    "CARGA PAGA KM", "CARGA GRATIS KM", "CORREIO KM", "ASSENTOS",
    "PAYLOAD", "BAGAGEM (KG)"
]
for col in columns_to_fill_zero:
    anac_df[col] = anac_df[col].fillna(0)

# Convert 'HORAS VOADAS' to numeric, handling potential errors
anac_df["HORAS VOADAS"] = pd.to_numeric(anac_df["HORAS VOADAS"], errors="coerce").fillna(0)

# Ensure 'ANO' and 'MÊS' are integers
anac_df["ANO"] = pd.to_numeric(anac_df["ANO"], errors="coerce").fillna(0).astype(int)
anac_df["MÊS"] = pd.to_numeric(anac_df["MÊS"], errors="coerce").fillna(0).astype(int)

print("ANAC DataFrame info after cleaning:")
anac_df.info()
print("ANAC DataFrame ANO and MÊS head after cleaning:")
print(anac_df[["ANO", "MÊS"]].head())

# --- Load to SQLite ---
conn = sqlite3.connect("testeManus/analytics_data.db")

sleep_df.to_sql("sleep_health", conn, if_exists="replace", index=False)
anac_df.to_sql("anac_flights", conn, if_exists="replace", index=False)

conn.close()

print("Data cleaning and loading to SQLite complete.")

