"""
Análise Exploratória de Dados - Desemprego no Brasil (2020-2024)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Configurar estilo
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Carregar dados
df = pd.read_csv('dados_desemprego_brasil.csv')
df['data'] = pd.to_datetime(df['data'])

print("=" * 80)
print("📊 ANÁLISE EXPLORATÓRIA DE DADOS - DESEMPREGO NO BRASIL (2020-2024)")
print("=" * 80)

# 1. Estatísticas Descritivas
print("\n1️⃣ ESTATÍSTICAS DESCRITIVAS")
print("-" * 80)
print(df[['taxa_desemprego', 'populacao_economicamente_ativa', 'total_desempregados']].describe())

# 2. Análise Temporal
print("\n2️⃣ ANÁLISE TEMPORAL")
print("-" * 80)

# Taxa média por ano
taxa_anual = df.groupby('ano')['taxa_desemprego'].agg(['mean', 'min', 'max', 'std'])
print("\n📅 Taxa de Desemprego por Ano:")
print(taxa_anual.round(2))

# Variação percentual entre anos
print("\n📉 Variação Percentual Anual:")
for i in range(2021, 2025):
    taxa_anterior = df[df['ano'] == i-1]['taxa_desemprego'].mean()
    taxa_atual = df[df['ano'] == i]['taxa_desemprego'].mean()
    variacao = ((taxa_atual - taxa_anterior) / taxa_anterior) * 100
    print(f"   {i-1} → {i}: {variacao:+.2f}%")

# 3. Análise Regional
print("\n3️⃣ ANÁLISE REGIONAL")
print("-" * 80)

taxa_regional = df.groupby('regiao')['taxa_desemprego'].agg(['mean', 'min', 'max'])
print("\n🌍 Taxa de Desemprego por Região:")
print(taxa_regional.round(2).sort_values('mean', ascending=False))

# 4. Análise Demográfica
print("\n4️⃣ ANÁLISE DEMOGRÁFICA")
print("-" * 80)

print("\n👥 Comparação de Taxas Médias:")
print(f"   Geral: {df['taxa_desemprego'].mean():.2f}%")
print(f"   Jovens (18-24): {df['taxa_desemprego_jovem'].mean():.2f}%")
print(f"   Mulheres: {df['taxa_desemprego_mulheres'].mean():.2f}%")
print(f"   Homens: {df['taxa_desemprego_homens'].mean():.2f}%")

# 5. Identificar Períodos Críticos
print("\n5️⃣ PERÍODOS CRÍTICOS")
print("-" * 80)

# Mês com maior desemprego
pior_mes = df.loc[df['taxa_desemprego'].idxmax()]
print(f"\n📍 Pior Mês:")
print(f"   Data: {pior_mes['data'].strftime('%B %Y')}")
print(f"   Região: {pior_mes['regiao']}")
print(f"   Taxa: {pior_mes['taxa_desemprego']:.2f}%")

# Mês com menor desemprego
melhor_mes = df.loc[df['taxa_desemprego'].idxmin()]
print(f"\n📍 Melhor Mês:")
print(f"   Data: {melhor_mes['data'].strftime('%B %Y')}")
print(f"   Região: {melhor_mes['regiao']}")
print(f"   Taxa: {melhor_mes['taxa_desemprego']:.2f}%")

# 6. Análise de Correlação
print("\n6️⃣ ANÁLISE DE CORRELAÇÃO")
print("-" * 80)

correlacao = df[['taxa_desemprego', 'taxa_desemprego_jovem', 
                  'taxa_desemprego_mulheres', 'taxa_desemprego_homens']].corr()
print("\n🔗 Matriz de Correlação:")
print(correlacao.round(3))

# 7. Insights e Conclusões
print("\n7️⃣ PRINCIPAIS INSIGHTS")
print("-" * 80)

# Comparação pré e pós pandemia
pre_pandemia = df[df['ano'] == 2020]['taxa_desemprego'].mean()
pos_pandemia = df[df['ano'] == 2024]['taxa_desemprego'].mean()
recuperacao = ((pre_pandemia - pos_pandemia) / pre_pandemia) * 100

print(f"""
✅ INSIGHTS PRINCIPAIS:

1. IMPACTO DA PANDEMIA:
   - Taxa média em 2020 (pico): {pre_pandemia:.2f}%
   - Taxa média em 2024 (atual): {pos_pandemia:.2f}%
   - Recuperação: {recuperacao:.1f}%

2. DISPARIDADES REGIONAIS:
   - Região mais afetada: {taxa_regional['mean'].idxmax()} ({taxa_regional['mean'].max():.2f}%)
   - Região menos afetada: {taxa_regional['mean'].idxmin()} ({taxa_regional['mean'].min():.2f}%)
   - Diferença: {taxa_regional['mean'].max() - taxa_regional['mean'].min():.2f} pontos percentuais

3. VULNERABILIDADE DEMOGRÁFICA:
   - Jovens enfrentam desemprego {(df['taxa_desemprego_jovem'].mean() / df['taxa_desemprego'].mean() - 1) * 100:.1f}% maior
   - Mulheres têm taxa {(df['taxa_desemprego_mulheres'].mean() / df['taxa_desemprego'].mean() - 1) * 100:.1f}% superior aos homens

4. TENDÊNCIA:
   - O mercado de trabalho mostra sinais de recuperação consistente
   - A variabilidade regional permanece um desafio
   - Políticas públicas devem focar em jovens e equidade de gênero
""")

print("=" * 80)
print("✅ Análise exploratória concluída!")
print("=" * 80)
