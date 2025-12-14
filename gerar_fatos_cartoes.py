import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta

print("--- Iniciando Geração dos FATOS de Cartões (Com Anomalias) ---")
fake = Faker('pt_BR')

# Le dimensões
df_cartoes = pd.read_csv('dim_cartoes_area.csv', sep=';')
df_mcc = pd.read_csv('dim_mcc.csv', sep=';')

cartoes = df_cartoes.to_dict('records')
mccs = df_mcc.to_dict('records')

dados_transacoes = []
QTD_TRANSACOES = 5000

for i in range(1, QTD_TRANSACOES + 1):
    # 1. Escolhe um cartão
    cartao = random.choice(cartoes)
    depto_dono = cartao['nome_departamento_responsavel']
    
    # 2. Decide gerar uma anomalia
    gera_anomalia = random.random() < 0.20
    
    # 3. Escolhe o MCC
    if gera_anomalia:
        mcc_escolhido = random.choice(mccs)
    else:
        mccs_validos = [m for m in mccs if m['departamento_esperado'] in [depto_dono, 'Geral']]
        mcc_escolhido = random.choice(mccs_validos)
        
    # 4. Gera Data e Hora
    data_base = fake.date_between(start_date='-1y', end_date='today')
    
    # Injeta anomalia de Final de Semana
    if gera_anomalia and random.random() < 0.30:
        while data_base.weekday() < 5: 
            data_base += timedelta(days=1)
            
    # Injeta anomalia de horário
    if gera_anomalia and random.random() < 0.30:
        hora = f"{random.randint(0, 5):02d}:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}"
    else:
        hora = f"{random.randint(8, 20):02d}:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}"

    # Injeta anomalia de valor redondo
    if gera_anomalia and random.random() < 0.30:
        valor = float(random.randint(1, 20) * 100)
    else:
        valor = round(random.uniform(50, 5000), 2)

    # Nome do estabelecimento
    if mcc_escolhido['nome_mcc'] == 'Cia Aérea':
        estabelecimento = fake.company() + ' Airlines'
    elif 'Restaurante' in mcc_escolhido['nome_mcc']:
        estabelecimento = 'Restaurante ' + fake.first_name()
    else:
        estabelecimento = fake.company()

    dados_transacoes.append({
        'id_transacao': 100000 + i,
        'id_cartao': cartao['id_cartao'],
        'codigo_mcc': mcc_escolhido['codigo_mcc'],
        'nome_estabelecimento': estabelecimento,
        'data_transacao': f"{data_base} {hora}",
        'valor_transacao': valor
    })

    # Injeta anomalia de duplicidade
    if gera_anomalia and random.random() < 0.05:
        dados_transacoes.append({
            'id_transacao': 100000 + i + 900000,
            'id_cartao': cartao['id_cartao'],   
            'codigo_mcc': mcc_escolhido['codigo_mcc'],
            'nome_estabelecimento': estabelecimento,
            'data_transacao': f"{data_base} {hora}",
            'valor_transacao': valor
        })

df_fato = pd.DataFrame(dados_transacoes)
df_fato.to_csv('fato_transacoes_cartao.csv', index=False, sep=';', encoding='utf-8-sig')
print("SUCESSO: 'fato_transacoes_cartao.csv' gerado.")