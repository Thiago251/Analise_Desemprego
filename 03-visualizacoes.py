"""
Visualizações Avançadas - Desemprego no Brasil (2020-2024)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.gridspec import GridSpec
import warnings
warnings.filterwarnings('ignore')

# Configurar estilo
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_context("notebook", font_scale=1.1)
colors = sns.color_palette("husl", 5)

# Carregar dados
df = pd.read_csv('dados_desemprego_brasil.csv')
df['data'] = pd.to_datetime(df['data'])

print("🎨 Gerando visualizações...")

# ============================================================================
# GRÁFICO 1: Evolução Temporal da Taxa de Desemprego
# ============================================================================
fig1, ax1 = plt.subplots(figsize=(14, 6))

for i, regiao in enumerate(df['regiao'].unique()):
    df_regiao = df[df['regiao'] == regiao].groupby('data')['taxa_desemprego'].mean()
    ax1.plot(df_regiao.index, df_regiao.values, marker='o', markersize=3, 
             linewidth=2, label=regiao, color=colors[i])

# Destacar período da pandemia
ax1.axvspan(pd.Timestamp('2020-03-01'), pd.Timestamp('2021-12-31'), 
            alpha=0.2, color='red', label='Período Crítico da Pandemia')

ax1.set_title('Evolução da Taxa de Desemprego por Região (2020-2024)', 
              fontsize=16, fontweight='bold', pad=20)
ax1.set_xlabel('Período', fontsize=12, fontweight='bold')
ax1.set_ylabel('Taxa de Desemprego (%)', fontsize=12, fontweight='bold')
ax1.legend(loc='upper right', frameon=True, shadow=True)
ax1.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('grafico_01_evolucao_temporal.png', dpi=300, bbox_inches='tight')
print("✅ Gráfico 1 salvo: grafico_01_evolucao_temporal.png")

# ============================================================================
# GRÁFICO 2: Comparação Anual
# ============================================================================
fig2, (ax2a, ax2b) = plt.subplots(1, 2, figsize=(16, 6))

# Box plot por ano
df_box = df.groupby(['ano', 'regiao'])['taxa_desemprego'].mean().reset_index()
sns.boxplot(data=df_box, x='ano', y='taxa_desemprego', ax=ax2a, palette='Set2')
ax2a.set_title('Distribuição da Taxa de Desemprego por Ano', 
               fontsize=14, fontweight='bold')
ax2a.set_xlabel('Ano', fontsize=12, fontweight='bold')
ax2a.set_ylabel('Taxa de Desemprego (%)', fontsize=12, fontweight='bold')

# Bar plot comparativo
taxa_anual = df.groupby('ano')['taxa_desemprego'].mean()
bars = ax2b.bar(taxa_anual.index, taxa_anual.values, color=sns.color_palette("coolwarm", len(taxa_anual)))
ax2b.set_title('Taxa Média de Desemprego por Ano', fontsize=14, fontweight='bold')
ax2b.set_xlabel('Ano', fontsize=12, fontweight='bold')
ax2b.set_ylabel('Taxa Média (%)', fontsize=12, fontweight='bold')

# Adicionar valores nas barras
for bar in bars:
    height = bar.get_height()
    ax2b.text(bar.get_x() + bar.get_width()/2., height,
              f'{height:.1f}%', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig('grafico_02_comparacao_anual.png', dpi=300, bbox_inches='tight')
print("✅ Gráfico 2 salvo: grafico_02_comparacao_anual.png")

# ============================================================================
# GRÁFICO 3: Análise Regional
# ============================================================================
fig3 = plt.figure(figsize=(16, 10))
gs = GridSpec(2, 2, figure=fig3)

# Subplot 1: Heatmap regional por ano
ax3a = fig3.add_subplot(gs[0, :])
pivot_data = df.groupby(['ano', 'regiao'])['taxa_desemprego'].mean().unstack()
sns.heatmap(pivot_data.T, annot=True, fmt='.1f', cmap='YlOrRd', 
            cbar_kws={'label': 'Taxa de Desemprego (%)'}, ax=ax3a)
ax3a.set_title('Mapa de Calor: Taxa de Desemprego por Região e Ano', 
               fontsize=14, fontweight='bold')
ax3a.set_xlabel('Ano', fontsize=12, fontweight='bold')
ax3a.set_ylabel('Região', fontsize=12, fontweight='bold')

# Subplot 2: Ranking regional
ax3b = fig3.add_subplot(gs[1, 0])
taxa_regional = df.groupby('regiao')['taxa_desemprego'].mean().sort_values(ascending=True)
bars = ax3b.barh(taxa_regional.index, taxa_regional.values, color=colors)
ax3b.set_title('Ranking Regional - Taxa Média', fontsize=12, fontweight='bold')
ax3b.set_xlabel('Taxa Média de Desemprego (%)', fontsize=11, fontweight='bold')

for i, v in enumerate(taxa_regional.values):
    ax3b.text(v + 0.1, i, f'{v:.2f}%', va='center', fontweight='bold')

# Subplot 3: Variabilidade regional
ax3c = fig3.add_subplot(gs[1, 1])
df_regional = df.groupby('regiao')['taxa_desemprego'].agg(['mean', 'std']).reset_index()
ax3c.scatter(df_regional['mean'], df_regional['std'], s=300, alpha=0.6, c=colors)
for i, row in df_regional.iterrows():
    ax3c.annotate(row['regiao'], (row['mean'], row['std']), 
                  xytext=(5, 5), textcoords='offset points', fontweight='bold')
ax3c.set_title('Média vs Variabilidade por Região', fontsize=12, fontweight='bold')
ax3c.set_xlabel('Taxa Média (%)', fontsize=11, fontweight='bold')
ax3c.set_ylabel('Desvio Padrão', fontsize=11, fontweight='bold')
ax3c.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('grafico_03_analise_regional.png', dpi=300, bbox_inches='tight')
print("✅ Gráfico 3 salvo: grafico_03_analise_regional.png")

# ============================================================================
# GRÁFICO 4: Análise Demográfica
# ============================================================================
fig4, ((ax4a, ax4b), (ax4c, ax4d)) = plt.subplots(2, 2, figsize=(16, 12))

# Subplot 1: Comparação geral vs jovens
df_demografico = df.groupby('data')[['taxa_desemprego', 'taxa_desemprego_jovem']].mean()
ax4a.plot(df_demografico.index, df_demografico['taxa_desemprego'], 
          label='Geral', linewidth=2.5, color='steelblue')
ax4a.plot(df_demografico.index, df_demografico['taxa_desemprego_jovem'], 
          label='Jovens (18-24)', linewidth=2.5, color='coral')
ax4a.fill_between(df_demografico.index, 
                   df_demografico['taxa_desemprego'],
                   df_demografico['taxa_desemprego_jovem'],
                   alpha=0.3, color='orange')
ax4a.set_title('Desemprego: Geral vs Jovens', fontsize=13, fontweight='bold')
ax4a.set_ylabel('Taxa de Desemprego (%)', fontsize=11, fontweight='bold')
ax4a.legend(loc='upper right')
ax4a.grid(True, alpha=0.3)

# Subplot 2: Comparação por gênero
df_genero = df.groupby('data')[['taxa_desemprego_mulheres', 'taxa_desemprego_homens']].mean()
ax4b.plot(df_genero.index, df_genero['taxa_desemprego_mulheres'], 
          label='Mulheres', linewidth=2.5, color='mediumpurple')
ax4b.plot(df_genero.index, df_genero['taxa_desemprego_homens'], 
          label='Homens', linewidth=2.5, color='teal')
ax4b.set_title('Desemprego por Gênero', fontsize=13, fontweight='bold')
ax4b.set_ylabel('Taxa de Desemprego (%)', fontsize=11, fontweight='bold')
ax4b.legend(loc='upper right')
ax4b.grid(True, alpha=0.3)

# Subplot 3: Gap demográfico ao longo do tempo
df['gap_jovem'] = df['taxa_desemprego_jovem'] - df['taxa_desemprego']
df['gap_genero'] = df['taxa_desemprego_mulheres'] - df['taxa_desemprego_homens']

gap_temporal = df.groupby('data')[['gap_jovem', 'gap_genero']].mean()
ax4c.plot(gap_temporal.index, gap_temporal['gap_jovem'], 
          label='Gap Jovens', linewidth=2.5, color='orangered')
ax4c.plot(gap_temporal.index, gap_temporal['gap_genero'], 
          label='Gap Gênero', linewidth=2.5, color='darkviolet')
ax4c.axhline(y=0, color='black', linestyle='--', alpha=0.5)
ax4c.set_title('Gap de Desemprego ao Longo do Tempo', fontsize=13, fontweight='bold')
ax4c.set_ylabel('Diferença em Pontos Percentuais', fontsize=11, fontweight='bold')
ax4c.legend(loc='upper right')
ax4c.grid(True, alpha=0.3)

# Subplot 4: Resumo demográfico
categorias = ['Geral', 'Jovens', 'Mulheres', 'Homens']
valores = [
    df['taxa_desemprego'].mean(),
    df['taxa_desemprego_jovem'].mean(),
    df['taxa_desemprego_mulheres'].mean(),
    df['taxa_desemprego_homens'].mean()
]
bars = ax4d.bar(categorias, valores, color=['steelblue', 'coral', 'mediumpurple', 'teal'])
ax4d.set_title('Taxa Média por Grupo Demográfico (2020-2024)', 
               fontsize=13, fontweight='bold')
ax4d.set_ylabel('Taxa Média de Desemprego (%)', fontsize=11, fontweight='bold')

for bar in bars:
    height = bar.get_height()
    ax4d.text(bar.get_x() + bar.get_width()/2., height,
              f'{height:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=10)

plt.tight_layout()
plt.savefig('grafico_04_analise_demografica.png', dpi=300, bbox_inches='tight')
print("✅ Gráfico 4 salvo: grafico_04_analise_demografica.png")

# ============================================================================
# GRÁFICO 5: Dashboard Executivo
# ============================================================================
fig5 = plt.figure(figsize=(18, 10))
gs = GridSpec(3, 3, figure=fig5, hspace=0.3, wspace=0.3)

# Título principal
fig5.suptitle('DASHBOARD EXECUTIVO - DESEMPREGO NO BRASIL (2020-2024)', 
              fontsize=18, fontweight='bold', y=0.98)

# KPIs principais
ax5a = fig5.add_subplot(gs[0, 0])
ax5a.text(0.5, 0.7, f"{df['taxa_desemprego'].mean():.1f}%", 
          ha='center', va='center', fontsize=40, fontweight='bold', color='steelblue')
ax5a.text(0.5, 0.3, 'Taxa Média\n2020-2024', 
          ha='center', va='center', fontsize=12, fontweight='bold')
ax5a.axis('off')

ax5b = fig5.add_subplot(gs[0, 1])
variacao = ((df[df['ano']==2024]['taxa_desemprego'].mean() - 
             df[df['ano']==2020]['taxa_desemprego'].mean()) / 
            df[df['ano']==2020]['taxa_desemprego'].mean() * 100)
cor_variacao = 'green' if variacao < 0 else 'red'
ax5b.text(0.5, 0.7, f"{variacao:+.1f}%", 
          ha='center', va='center', fontsize=40, fontweight='bold', color=cor_variacao)
ax5b.text(0.5, 0.3, 'Variação\n2020→2024', 
          ha='center', va='center', fontsize=12, fontweight='bold')
ax5b.axis('off')

ax5c = fig5.add_subplot(gs[0, 2])
total_desemp = df['total_desempregados'].sum() / 1000000
ax5c.text(0.5, 0.7, f"{total_desemp:.1f}M", 
          ha='center', va='center', fontsize=40, fontweight='bold', color='orangered')
ax5c.text(0.5, 0.3, 'Total de\nDesempregados', 
          ha='center', va='center', fontsize=12, fontweight='bold')
ax5c.axis('off')

# Tendência geral
ax5d = fig5.add_subplot(gs[1, :])
df_mensal = df.groupby('data')['taxa_desemprego'].mean()
ax5d.plot(df_mensal.index, df_mensal.values, linewidth=3, color='steelblue')
ax5d.fill_between(df_mensal.index, df_mensal.values, alpha=0.3, color='steelblue')
z = np.polyfit(range(len(df_mensal)), df_mensal.values, 2)
p = np.poly1d(z)
ax5d.plot(df_mensal.index, p(range(len(df_mensal))), 
          "--", linewidth=2, color='red', label='Tendência')
ax5d.set_title('Tendência Geral da Taxa de Desemprego', fontsize=14, fontweight='bold')
ax5d.set_ylabel('Taxa (%)', fontsize=11, fontweight='bold')
ax5d.legend()
ax5d.grid(True, alpha=0.3)

# Top 3 regiões
ax5e = fig5.add_subplot(gs[2, 0])
top_regioes = df.groupby('regiao')['taxa_desemprego'].mean().nlargest(3)
ax5e.barh(range(len(top_regioes)), top_regioes.values, color='orangered')
ax5e.set_yticks(range(len(top_regioes)))
ax5e.set_yticklabels(top_regioes.index)
ax5e.set_title('TOP 3 Regiões\nMaior Desemprego', fontsize=11, fontweight='bold')
ax5e.set_xlabel('Taxa (%)', fontsize=10)
for i, v in enumerate(top_regioes.values):
    ax5e.text(v + 0.1, i, f'{v:.1f}%', va='center', fontsize=9)

# Sazonalidade
ax5f = fig5.add_subplot(gs[2, 1])
sazonalidade = df.groupby('mes')['taxa_desemprego'].mean()
meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 
         'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
ax5f.plot(range(1, 13), sazonalidade.values, marker='o', linewidth=2, 
          markersize=8, color='teal')
ax5f.set_xticks(range(1, 13))
ax5f.set_xticklabels(meses, rotation=45)
ax5f.set_title('Padrão Sazonal', fontsize=11, fontweight='bold')
ax5f.set_ylabel('Taxa (%)', fontsize=10)
ax5f.grid(True, alpha=0.3)

# Grupos vulneráveis
ax5g = fig5.add_subplot(gs[2, 2])
grupos = ['Jovens\n(18-24)', 'Mulheres', 'Homens']
valores_grupos = [
    df['taxa_desemprego_jovem'].mean(),
    df['taxa_desemprego_mulheres'].mean(),
    df['taxa_desemprego_homens'].mean()
]
cores_grupos = ['coral', 'mediumpurple', 'teal']
bars = ax5g.bar(grupos, valores_grupos, color=cores_grupos)
ax5g.set_title('Grupos Vulneráveis', fontsize=11, fontweight='bold')
ax5g.set_ylabel('Taxa (%)', fontsize=10)
ax5g.axhline(y=df['taxa_desemprego'].mean(), color='red', 
             linestyle='--', label='Média Geral', linewidth=2)
ax5g.legend(fontsize=8)
for bar in bars:
    height = bar.get_height()
    ax5g.text(bar.get_x() + bar.get_width()/2., height,
              f'{height:.1f}%', ha='center', va='bottom', fontsize=9, fontweight='bold')

plt.savefig('grafico_05_dashboard_executivo.png', dpi=300, bbox_inches='tight')
print("✅ Gráfico 5 salvo: grafico_05_dashboard_executivo.png")

print("\n🎉 Todas as visualizações foram geradas com sucesso!")
print("\n📁 Arquivos gerados:")
print("   - grafico_01_evolucao_temporal.png")
print("   - grafico_02_comparacao_anual.png")
print("   - grafico_03_analise_regional.png")
print("   - grafico_04_analise_demografica.png")
print("   - grafico_05_dashboard_executivo.png")
