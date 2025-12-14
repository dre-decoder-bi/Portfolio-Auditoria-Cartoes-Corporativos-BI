import pandas as pd
from faker import Faker
import random

print("--- Iniciando Geração das DIMENSÕES de Cartões ---")
fake = Faker('pt_BR')

# --- 1. Geração [dim_cartoes_area] ---
DEPARTAMENTOS = ['RH', 'TI', 'Marketing', 'Vendas', 'Operações', 'Financeiro']

dados_cartoes = []
for i, depto in enumerate(DEPARTAMENTOS):
    for n in range(1, 3):
        dados_cartoes.append({
            'id_cartao': (i + 1) * 1000 + n,
            'nome_departamento_responsavel': depto,
            'nome_gerente_responsavel': fake.name(),
            'limite_mensal': random.choice([20000, 50000, 80000]),
            'final_cartao': str(random.randint(1000, 9999))
        })

df_cartoes = pd.DataFrame(dados_cartoes)
df_cartoes.to_csv('dim_cartoes_area.csv', index=False, sep=';', encoding='utf-8-sig')
print("SUCESSO: 'dim_cartoes_area.csv' gerado.")

# --- 2. Geração [dim_mcc] ---
dados_mcc = [
    (5734, 'Software e Computadores', 'Baixo', 'TI'),
    (4816, 'Serviços de Nuvem (AWS/Azure)', 'Baixo', 'TI'),
    (8299, 'Escolas e Treinamentos', 'Baixo', 'RH'),
    (7361, 'Agências de Emprego', 'Baixo', 'RH'),
    (7311, 'Agências de Publicidade', 'Baixo', 'Marketing'),
    (5943, 'Brindes e Papelaria', 'Médio', 'Marketing'),
    (5812, 'Restaurantes e Bares', 'Médio', 'Geral'),
    (3000, 'Cia Aérea', 'Baixo', 'Geral'),
    (7995, 'Jogos de Azar e Cassinos', 'Alto', 'Bloqueado'),
    (5921, 'Bebidas Alcoólicas (Varejo)', 'Alto', 'Bloqueado'),
    (7298, 'Spas e Salões de Beleza', 'Alto', 'Bloqueado'),
    (5311, 'Lojas de Departamento', 'Médio', 'Geral')
]

df_mcc = pd.DataFrame(dados_mcc, columns=['codigo_mcc', 'nome_mcc', 'categoria_risco', 'departamento_esperado'])
df_mcc.to_csv('dim_mcc.csv', index=False, sep=';', encoding='utf-8-sig')
print("SUCESSO: 'dim_mcc.csv' gerado.")