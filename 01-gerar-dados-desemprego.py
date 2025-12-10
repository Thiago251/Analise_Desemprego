"""
Script para gerar dados realistas de desemprego (2020-2024)
Baseado em tendências reais do mercado de trabalho
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

# Configurar seed para reprodutibilidade
np.random.seed(42)

# Gerar datas mensais de 2020 a 2024
start_date = datetime(2020, 1, 1)
end_date = datetime(2024, 12, 31)
dates = pd.date_range(start=start_date, end=end_date, freq='MS')

# Regiões do Brasil
regioes = ['Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul']

# Criar dataset
data = []

for date in dates:
    mes = date.month
    ano = date.year
    
    for regiao in regioes:
        # Simular taxa de desemprego com padrões realistas
        # 2020: Pico da pandemia (alta)
        # 2021-2022: Recuperação gradual
        # 2023-2024: Estabilização
        
        base_rate = {
            'Norte': 12.5,
            'Nordeste': 14.2,
            'Centro-Oeste': 10.8,
            'Sudeste': 11.5,
            'Sul': 9.2
        }[regiao]
        
        # Efeito da pandemia
        if ano == 2020:
            pandemia_effect = 4.5 + np.random.normal(0, 1)
        elif ano == 2021:
            pandemia_effect = 3.0 + np.random.normal(0, 0.8)
        elif ano == 2022:
            pandemia_effect = 1.5 + np.random.normal(0, 0.6)
        elif ano == 2023:
            pandemia_effect = 0.5 + np.random.normal(0, 0.4)
        else:  # 2024
            pandemia_effect = 0.2 + np.random.normal(0, 0.3)
        
        # Sazonalidade (fim de ano tem menos desemprego)
        sazonalidade = -0.8 if mes == 12 else (0.5 if mes in [1, 2] else 0)
        
        taxa_desemprego = base_rate + pandemia_effect + sazonalidade + np.random.normal(0, 0.5)
        taxa_desemprego = max(5.0, min(20.0, taxa_desemprego))  # Limitar entre 5% e 20%
        
        # População economicamente ativa (em milhões)
        pea_base = {
            'Norte': 8.5,
            'Nordeste': 27.3,
            'Centro-Oeste': 8.2,
            'Sudeste': 45.6,
            'Sul': 15.4
        }[regiao]
        
        pea = pea_base * (1 + (ano - 2020) * 0.015) + np.random.normal(0, 0.2)
        
        # Calcular desempregados
        desempregados = (pea * taxa_desemprego / 100) * 1000000  # converter para pessoas
        
        # Dados demográficos
        faixa_etaria = {
            '18-24': np.random.uniform(18, 25),
            '25-39': np.random.uniform(35, 42),
            '40-59': np.random.uniform(30, 38),
            '60+': np.random.uniform(5, 10)
        }
        
        escolaridade = {
            'Sem instrução': np.random.uniform(8, 15),
            'Fundamental': np.random.uniform(20, 28),
            'Médio': np.random.uniform(35, 45),
            'Superior': np.random.uniform(15, 25)
        }
        
        data.append({
            'data': date,
            'ano': ano,
            'mes': mes,
            'regiao': regiao,
            'taxa_desemprego': round(taxa_desemprego, 2),
            'populacao_economicamente_ativa': round(pea, 2),
            'total_desempregados': int(desempregados),
            'taxa_desemprego_jovem': round(taxa_desemprego * 1.8, 2),
            'taxa_desemprego_mulheres': round(taxa_desemprego * 1.15, 2),
            'taxa_desemprego_homens': round(taxa_desemprego * 0.92, 2)
        })

# Criar DataFrame
df = pd.DataFrame(data)

# Salvar em CSV
df.to_csv('dados_desemprego_brasil.csv', index=False)

print("✅ Dados gerados com sucesso!")
print(f"\n📊 Resumo do Dataset:")
print(f"   - Período: {df['data'].min().strftime('%m/%Y')} a {df['data'].max().strftime('%m/%Y')}")
print(f"   - Total de registros: {len(df)}")
print(f"   - Regiões: {', '.join(regioes)}")
print(f"   - Taxa média de desemprego: {df['taxa_desemprego'].mean():.2f}%")
print(f"\n📈 Taxa de desemprego por ano:")
print(df.groupby('ano')['taxa_desemprego'].mean().round(2))
print(f"\n🌍 Taxa de desemprego por região:")
print(df.groupby('regiao')['taxa_desemprego'].mean().round(2))
