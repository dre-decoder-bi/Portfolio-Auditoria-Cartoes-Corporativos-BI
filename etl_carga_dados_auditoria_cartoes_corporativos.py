import pandas as pd
from sqlalchemy import create_engine
import os

print("--- Iniciando Carga (Projeto Cartões Corporativos) ---")

DATABASE_URL = "postgresql://postgres:[SUA_SENHA_AQUI]@[SEU_HOST_AQUI]/postgres"

ARQUIVOS = ['dim_cartoes_area.csv', 'dim_mcc.csv', 'fato_transacoes_cartao.csv']

if "COLE_SUA" in DATABASE_URL:
    print("ERRO: Configure sua connection string!")
else:
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            print("Conectado ao Supabase!")

        for arquivo in ARQUIVOS:
            tabela = arquivo.replace('.csv', '')
            if os.path.exists(arquivo):
                print(f"Carregando {tabela}...")
                df = pd.read_csv(arquivo, sep=';')
                df.to_sql(tabela, engine, if_exists='replace', index=False, schema='public')
                print(f"-> {tabela} OK.")
            else:
                print(f"ERRO: {arquivo} não encontrado.")
        print("\n--- SUCESSO ---")
    except Exception as e:
        print(f"ERRO: {e}")