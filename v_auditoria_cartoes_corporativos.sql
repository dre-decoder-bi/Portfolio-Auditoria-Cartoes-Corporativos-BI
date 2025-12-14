CREATE OR REPLACE VIEW v_auditoria_cartoes_corporativos AS

SELECT
    F.id_transacao,
    F.id_cartao,
    F.codigo_mcc,
    F.nome_estabelecimento,
    F.data_transacao::timestamp AS data_hora,
    F.data_transacao::date AS data_apenas,
    F.valor_transacao,
    D_Area.nome_departamento_responsavel AS area_dona_cartao,
    D_Area.nome_gerente_responsavel,
    D_Mcc.nome_mcc,
    D_Mcc.categoria_risco,
    D_Mcc.departamento_esperado AS area_esperada_gasto,

    CASE 
        WHEN D_Mcc.departamento_esperado = 'Geral' THEN 'OK'
        WHEN D_Mcc.departamento_esperado = D_Area.nome_departamento_responsavel THEN 'OK'
        ELSE 'ALERTA: Gasto Cruzado' 
    END AS flag_gasto_cruzado,

    CASE 
        WHEN D_Mcc.categoria_risco IN ('Alto', 'Bloqueado') THEN 'ALERTA: Categoria Proibida'
        WHEN D_Mcc.categoria_risco = 'Suspeito' THEN 'Atenção: Categoria Suspeita'
        ELSE 'OK' 
    END AS flag_categoria,

    CASE 
        WHEN EXTRACT(DOW FROM F.data_transacao::timestamp) IN (0, 6) THEN 'ALERTA: Fim de Semana'
        WHEN EXTRACT(HOUR FROM F.data_transacao::timestamp) < 6 OR EXTRACT(HOUR FROM F.data_transacao::timestamp) > 22 THEN 'ALERTA: Horário Incomum'
        ELSE 'OK'
    END AS flag_horario,

    CASE 
        WHEN F.valor_transacao > 100 AND (F.valor_transacao::numeric % 50) = 0 THEN 'Atenção: Valor Redondo'
        ELSE 'OK'
    END AS flag_valor_redondo,

    CASE 
        WHEN COUNT(*) OVER(PARTITION BY F.id_cartao, F.valor_transacao, F.nome_estabelecimento, F.data_transacao::date) > 1 THEN 'ALERTA: Duplicidade'
        ELSE 'OK'
    END AS flag_duplicidade

FROM
    fato_transacoes_cartao AS F
JOIN
    dim_cartoes_area AS D_Area ON F.id_cartao = D_Area.id_cartao
JOIN
    dim_mcc AS D_Mcc ON F.codigo_mcc = D_Mcc.codigo_mcc;